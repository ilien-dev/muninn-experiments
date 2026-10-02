#!/usr/bin/env python3
"""judge-v2: one question per later message — which of the store's records does it replace?

judge-v1 asked yes/no per (earlier, later) pair and failed on a shape it cannot answer: "let's
use Unleash instead" scores ~1 against every record, because the pair alone does not say what
"instead" refers to. Here the model sees every candidate record of the group at once and picks
one letter: A = none of them, B.. = a record. Candidates are listed in set order (the scenario's
own record is not moved next to its change), which is the order where the rules fall to 16/180.

A call is one later message:
  target   the record it replaces (b_i -> a_i; probe pairs labelled 1 -> their own a) or none
           (c_i, loop 10's pairs, third-language negatives, probe traps)
Rows: the letter distribution (softmax over the valid letters only), the pick, and the ms.

Usage: choice.py --arm B1|B3 [--out DIR] [--limit N] [--reverse] [--tag T]
"""
import argparse, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sets  # noqa: E402
from run import MODELS, sha256  # noqa: E402

GGUF = {"B1": "qwen35-4b-q4km.gguf", "B3": "gemma4-e4b-q4km.gguf"}
LETTERS = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
NONE = "A"

# The prompt is part of the registration: changing a word of it is a new arm.
HEAD = ("You keep the memory of a software project. Below are records the project holds, "
        "oldest first. Records can be in any language.\n\nRecords:\n")
TAIL = ("\nA new message was written later in the same project:\n<<<{b}>>>\n\n"
        "Question: which record does the new message replace, reverse or withdraw, so that it "
        "is no longer current? A message that asks something, adds detail, is about something "
        "else, or leaves every record true replaces none of them.\n\n"
        "Answer with the letter only.")
SENTINEL = "\x00SPLIT\x00"


def calls():
    """Every later message with its candidate records and its target (index into candidates,
    or None)."""
    out, items = [], sets.items() + sets.probe_items()
    groups = {}
    for it in items:
        g = groups.setdefault(it["group"], {"earlier": [], "later": {}})
        if it["a"] not in g["earlier"] and it["kind"] != "neg_shared":
            g["earlier"].append(it["a"])
    for it in items:
        g = groups[it["group"]]
        if it["kind"] == "neg_shared":
            # loop 10 and the third-language negatives are pairs: the store is the pair
            out.append({"id": it["id"], "group": it["group"], "split": it["split"], "lang": it["lang"],
                        "set": it["set"], "probe": it.get("probe"), "cands": [it["a"]],
                        "b": it["b"], "target": None, "kind": "shared"})
            continue
        c = g["later"].setdefault(it["b"], {"id": it["id"].split("|", 1)[1], "group": it["group"],
                                            "split": it["split"], "lang": it["lang"], "set": it["set"],
                                            "probe": it.get("probe"), "cands": g["earlier"],
                                            "b": it["b"], "target": None, "kind": "none"})
        if it["label"] == 1:
            c["target"], c["kind"] = g["earlier"].index(it["a"]), "replaces"
    for g in groups.values():
        out += list(g["later"].values())
    assert all(len(c["cands"]) <= 25 for c in out)
    return out


class ChoiceJudge:
    def __init__(self, path: Path, threads: int):
        import numpy as np
        import llama_cpp
        from jinja2 import Environment
        self.np, self.lc = np, llama_cpp
        self.llm = llama_cpp.Llama(model_path=str(path), n_ctx=4096, n_threads=threads,
                                   n_threads_batch=threads, n_gpu_layers=0, seed=0,
                                   logits_all=False, verbose=False)
        env = Environment()
        env.globals["raise_exception"] = lambda m: (_ for _ in ()).throw(ValueError(m))
        msg = [{"role": "user", "content": "{records}" + SENTINEL + TAIL}]
        r = env.from_string(self.llm.metadata["tokenizer.chat_template"]).render(
            messages=msg, add_generation_prompt=True, enable_thinking=False, bos_token="", eos_token="")
        self.pre_tpl, self.suf_tpl = r.split(SENTINEL)
        self.tok_of = {}
        for L in LETTERS:
            t = self.llm.tokenize(L.encode(), add_bos=False, special=False)
            assert len(t) == 1, (L, t)
            self.tok_of[L] = t[0]
        self.cached, self.state = None, None
        self.n_vocab = self.llm.n_vocab()

    def _tok(self, s):
        return self.llm.tokenize(s.encode(), add_bos=True, special=True)

    def score(self, cands, b, cached=True):
        letters = [NONE] + LETTERS[1:len(cands) + 1]
        records = "A) none of them\n" + "".join(f"{L}) <<<{a}>>>\n" for L, a in zip(letters[1:], cands))
        pre = self.pre_tpl.replace("{records}", HEAD + records)
        full = pre + self.suf_tpl.replace("{b}", b)
        pt, ft = self._tok(pre), self._tok(full)
        if not cached or ft[:len(pt)] != pt:
            self.llm.reset(); self.llm.eval(ft); self.cached = None
        else:
            if self.cached != pre:
                self.llm.reset(); self.llm.eval(pt)
                self.state, self.cached = self.llm.save_state(), pre
            else:
                self.llm.load_state(self.state)
            self.llm.eval(ft[len(pt):])
        lg = self.np.ctypeslib.as_array(self.lc.llama_get_logits_ith(self.llm._ctx.ctx, -1),
                                        shape=(self.n_vocab,))
        v = self.np.array([lg[self.tok_of[L]] for L in letters], dtype=float)
        p = self.np.exp(v - v.max()); p /= p.sum()
        top = int(lg.argmax())
        return [float(x) for x in p], {"top_is_letter": top in self.tok_of.values(), "prefix_tokens": len(pt)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=list(GGUF))
    ap.add_argument("--out", default=str(HERE.parent / "results/judge-v2"))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--threads", type=int, default=16)
    ap.add_argument("--full-prompt-sample", type=int, default=50)
    ap.add_argument("--reverse", action="store_true", help="candidates newest first (position-bias check)")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    cs = calls()
    if args.limit:
        cs = cs[:: max(1, len(cs) // args.limit)][: args.limit]
    path = MODELS / GGUF[args.arm]
    j = ChoiceJudge(path, args.threads)
    t0 = time.time()
    rows = []
    for n, c in enumerate(cs):
        cands = c["cands"][::-1] if args.reverse else c["cands"]
        t = time.perf_counter()
        p, raw = j.score(cands, c["b"])
        if args.reverse:  # back to set order, so rows compare index for index
            p = [p[0]] + p[1:][::-1]
        rows.append({"p": p, "raw": raw, "ms": (time.perf_counter() - t) * 1000})
        if n % 100 == 0:
            print(f"{args.arm} {n}/{len(cs)}", file=sys.stderr, flush=True)
    full = []
    for i in range(0, len(cs), max(1, len(cs) // args.full_prompt_sample)):
        t = time.perf_counter()
        p, _ = j.score(cs[i]["cands"][::-1] if args.reverse else cs[i]["cands"], cs[i]["b"], cached=False)
        full.append({"id": cs[i]["id"], "ms": (time.perf_counter() - t) * 1000})
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    name = f"{args.arm}{args.tag}"
    with open(out / f"{name}.jsonl", "w") as f:
        for c, r in zip(cs, rows):
            f.write(json.dumps({"id": c["id"], "group": c["group"], "split": c["split"], "lang": c["lang"],
                                "set": c["set"], "probe": c["probe"], "kind": c["kind"], "target": c["target"],
                                "n_cands": len(c["cands"]), "p": [round(x, 4) for x in r["p"]],
                                "ms": round(r["ms"], 2), "raw": r["raw"]}, ensure_ascii=False) + "\n")
    json.dump({"arm": args.arm, "model": path.name, "sha256": sha256(path), "threads": args.threads,
               "calls": len(cs), "reverse": args.reverse, "full_prompt": full,
               "wall_s": round(time.time() - t0, 1),
               "started": datetime.fromtimestamp(t0, timezone.utc).isoformat(),
               "cpu": "AMD Ryzen 9 7950X3D, 16 cores"}, open(out / f"{name}.meta.json", "w"), indent=1)
    print(f"{name}: {len(cs)} calls in {round(time.time() - t0, 1)} s", file=sys.stderr)


if __name__ == "__main__":
    main()
