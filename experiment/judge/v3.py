#!/usr/bin/env python3
"""judge-v3: pick, then confirm — with the assistant's reply beside every record and message.

Step 1 (pick): every candidate record at once, one letter back (A = none), as judge-v2.
Step 2 (confirm): judge-v1's yes/no on the picked record and the new message only.
Since v41 Muninn stores the reply with every decision, so both steps see it here.

Calls:
  fresh   judge/fresh_v3.json: seven projects with replies; dev = en-A, es-A, pt; test = en-B,
          es-B, fr, de
  old     judge-v2's calls whose later message is a change (b_i), loop 10's and the
          third-language pairs, and the 60 probe pairs — no replies; dev only. The loop sets'
          c messages are left out: judge-v2 found some presuppose the change they follow.

Arms: C1 Qwen3.5-4B, C2 Qwen3.5-9B, C1n Qwen3.5-4B with the replies withheld (ablation).
Usage: v3.py --arm C1 [--limit N] [--tag T]    |    v3.py --a0
"""
import argparse, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import choice  # noqa: E402
from run import MODELS, REPO, sha256, transcript, T0  # noqa: E402

GGUF = {"C1": "qwen35-4b-q4km.gguf", "C1n": "qwen35-4b-q4km.gguf", "C2": "qwen35-9b-q4km.gguf"}
LETTERS = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
OUT = HERE.parent / "results/judge-v3"

# The prompts are part of the registration.
PICK_HEAD = ("You keep the memory of a software project. Below are records the project holds, "
             "oldest first, each with the assistant's reply when there was one. Records can be in "
             "any language.\n\nRecords:\n")
PICK_TAIL = ("\nA new message was written later in the same project:\n{b}\n\n"
             "Question: which record does the new message replace, reverse or withdraw, so that it "
             "is no longer current? A message that asks something, adds detail, is about something "
             "else, or leaves every record true replaces none of them.\n\n"
             "Answer with the letter only.")
CONFIRM = ("You keep the memory of a software project. Each record states something the project "
           "decided or holds. Records can be in any language.\n\n"
           "Question: does the new message replace, reverse or withdraw what the earlier record "
           "states, so that the earlier record is no longer current?\n"
           "A) Yes: the earlier record is no longer current.\n"
           "B) No: the new message is about something else, adds detail, asks something, is "
           "hypothetical, or leaves the earlier record true.\n\n"
           "Earlier record:\n{a}\n\nNew message, written later in the same project:\n{b}\n\n"
           "Answer with the letter only.")


def show(text, reply):
    return f"<<<{text}>>>" + (f"\n   (assistant replied: <<<{reply}>>>)" if reply else "")


def calls():
    out = []
    for g in json.load(open(HERE / "fresh_v3.json"))["groups"]:
        ids = [r["id"] for r in g["records"]]
        for m in g["later"]:
            out.append({"id": m["id"], "src": "fresh", "group": g["name"], "split": g["split"],
                        "lang": g["lang"], "probe": m["probe"],
                        "cands": [(r["text"], r["reply"]) for r in g["records"]],
                        "b": (m["text"], m["reply"]),
                        "target": ids.index(m["target"]) if m["target"] else None})
    for c in choice.calls():
        if c["set"] != "v1b" and c["kind"] == "none":
            continue  # loop and third-language c messages: see the docstring
        out.append({"id": c["id"], "src": "old", "group": c["group"], "split": "dev", "lang": c["lang"],
                    "probe": c["probe"], "cands": [(a, "") for a in c["cands"]], "b": (c["b"], ""),
                    "target": c["target"]})
    return out


class Judge:
    def __init__(self, path, threads):
        import numpy as np, llama_cpp
        from jinja2 import Environment
        self.np, self.lc = np, llama_cpp
        self.llm = llama_cpp.Llama(model_path=str(path), n_ctx=4096, n_threads=threads,
                                   n_threads_batch=threads, n_gpu_layers=0, seed=0,
                                   logits_all=False, verbose=False)
        env = Environment()
        env.globals["raise_exception"] = lambda m: (_ for _ in ()).throw(ValueError(m))
        self.tpl = env.from_string(self.llm.metadata["tokenizer.chat_template"])
        self.tok_of = {}
        for L in LETTERS:
            t = self.llm.tokenize(L.encode(), add_bos=False, special=False)
            assert len(t) == 1
            self.tok_of[L] = t[0]
        self.n_vocab = self.llm.n_vocab()
        self.cached, self.state = None, None

    def render(self, content):
        return self.tpl.render(messages=[{"role": "user", "content": content}], add_generation_prompt=True,
                               enable_thinking=False, bos_token="", eos_token="")

    def letters(self, prefix, full, letters):
        tok = lambda s: self.llm.tokenize(s.encode(), add_bos=True, special=True)
        pt, ft = tok(prefix), tok(full)
        if prefix and ft[:len(pt)] == pt:
            if self.cached != prefix:
                self.llm.reset(); self.llm.eval(pt)
                self.state, self.cached = self.llm.save_state(), prefix
            else:
                self.llm.load_state(self.state)
            self.llm.eval(ft[len(pt):])
        else:
            self.llm.reset(); self.llm.eval(ft); self.cached = None
        lg = self.np.ctypeslib.as_array(self.lc.llama_get_logits_ith(self.llm._ctx.ctx, -1), shape=(self.n_vocab,))
        v = self.np.array([lg[self.tok_of[L]] for L in letters], dtype=float)
        p = self.np.exp(v - v.max()); p /= p.sum()
        return [float(x) for x in p]

    def pick(self, cands, b, cached=True):
        letters = LETTERS[: len(cands) + 1]
        recs = "A) none of them\n" + "".join(f"{L}) {show(*c)}\n" for L, c in zip(letters[1:], cands))
        full = self.render(PICK_HEAD + recs + PICK_TAIL.replace("{b}", show(*b)))
        split = full.index("\nA new message was written later")
        return self.letters(full[:split] if cached else "", full, letters)

    def confirm(self, a, b):
        full = self.render(CONFIRM.replace("{a}", show(*a)).replace("{b}", show(*b)))
        return self.letters("", full, ["A", "B"])[0]


def run_arm(args):
    cs = calls()
    if args.limit:
        cs = cs[:: max(1, len(cs) // args.limit)][: args.limit]
    if args.arm == "C1n":
        cs = [{**c, "cands": [(a, "") for a, _ in c["cands"]], "b": (c["b"][0], "")} for c in cs]
    path = MODELS / GGUF[args.arm]
    j = Judge(path, args.threads)
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    name = f"{args.arm}{args.tag}"
    with open(OUT / f"{name}.jsonl", "w") as f:
        for n, c in enumerate(cs):
            t = time.perf_counter()
            p = j.pick(c["cands"], c["b"], cached=not args.full)
            t_pick = time.perf_counter() - t
            k = max(range(len(p)), key=lambda i: p[i])
            conf = j.confirm(c["cands"][k - 1], c["b"]) if k > 0 else None
            f.write(json.dumps({"id": c["id"], "src": c["src"], "group": c["group"], "split": c["split"],
                                "lang": c["lang"], "probe": c["probe"], "target": c["target"],
                                "n_cands": len(c["cands"]), "p": [round(x, 4) for x in p], "pick": k - 1 if k else None,
                                "confirm": None if conf is None else round(conf, 4),
                                "ms_pick": round(t_pick * 1000, 1),
                                "ms_total": round((time.perf_counter() - t) * 1000, 1)}, ensure_ascii=False) + "\n")
            if n % 100 == 0:
                print(f"{name} {n}/{len(cs)}", file=sys.stderr, flush=True)
    json.dump({"arm": args.arm, "model": path.name, "sha256": sha256(path), "threads": args.threads,
               "calls": len(cs), "full_prompt": args.full, "wall_s": round(time.time() - t0, 1),
               "started": datetime.fromtimestamp(t0, timezone.utc).isoformat(),
               "cpu": "AMD Ryzen 9 7950X3D, 16 cores"}, open(OUT / f"{name}.meta.json", "w"), indent=1)


def run_a0():
    """The rules on the fresh set: one store per later message, holding the group's records with
    their replies in order, the target moved last when there is one (the adjacent order), then
    the message with its reply. Which records end up retired."""
    import os, subprocess, tempfile
    muninn = str(REPO / "target/release/muninn")
    rows = []
    for c in [c for c in calls() if c["src"] == "fresh"]:
        order = list(range(len(c["cands"])))
        if c["target"] is not None:
            order.remove(c["target"]); order.append(c["target"])
        root = Path(tempfile.mkdtemp(prefix="judge-v3-a0-"))
        (root / ".git").mkdir()
        env = {**os.environ, "MUNINN_ROOT": str(root), "MUNINN_NO_PROJECT": "1"}
        subprocess.run([muninn, "--cwd", str(root), "init", "--keep-native"], env=env, capture_output=True)
        seq = [c["cands"][i] for i in order] + [c["b"]]
        for k, (text, reply) in enumerate(seq):
            f = root / f"t{k}.jsonl"
            transcript(f, f"s{k:03d}", T0 + __import__("datetime").timedelta(minutes=30 * k), text)
            rows_ = [json.loads(l) for l in open(f)]
            rows_[1]["message"]["content"][0]["text"] = reply or "Noted."
            f.write_text("".join(json.dumps(r) + "\n" for r in rows_))
            subprocess.run([muninn, "--cwd", str(root), "ingest", str(f)], env=env, capture_output=True)
        subprocess.run([muninn, "--cwd", str(root), "--json", "export", "--all", "--out", str(root / "x.jsonl")],
                       env=env, capture_output=True)
        recs = [json.loads(l) for l in open(root / "x.jsonl")]
        retired = []
        for i, (text, _) in enumerate(c["cands"]):
            key = text.strip().rstrip(".!;")[:40].lower()
            held = [r for r in recs if key in (r.get("body") or "").lower()]
            if held and not [r for r in held if not r.get("invalid")]:
                retired.append(i)
        subprocess.run(["rm", "-rf", str(root)])
        rows.append({"id": c["id"], "split": c["split"], "lang": c["lang"], "target": c["target"], "retired": retired})
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "A0.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    json.dump({"binary": muninn, "sha256": sha256(Path(muninn)), "order": "adjacent"},
              open(OUT / "A0.meta.json", "w"), indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=list(GGUF))
    ap.add_argument("--a0", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--threads", type=int, default=16)
    ap.add_argument("--full", action="store_true", help="no cached prefix: the latency maintain pays")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    run_a0() if args.a0 else run_arm(args)


if __name__ == "__main__":
    main()
