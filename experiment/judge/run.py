#!/usr/bin/env python3
"""The judge tournament: every arm answers the same question on the same pairs (sets.py).

  A0  the shipped rules: a fresh store per pair, `muninn ingest` the earlier message, then the
      later one, and read whether the earlier is still served (loop 10's method)
  A1  Qwen3.5-4B Q4_K_M, letter logits (SemIf's method), stock llama.cpp
  A2  Qwen3.5-2B Q4_K_M, the same prompt
  A3  Gemma 4 E4B-it Q4_K_M, the same prompt
  A4  mDeBERTa-v3-base-xnli-multilingual-nli-2mil7, ONNX: P(contradiction), premise = earlier
  A5  laya-multilingual, one `noul` question over {earlier, later}

Every arm writes one row per pair: p (rounded to 2 decimals, the value thresholds are fitted
on), the raw value, and the milliseconds that pair took. No arm sees a label.

Usage: run.py --arm A1 [--out DIR] [--limit N] [--threads 16] [--full-prompt-sample 100]
"""
import argparse, hashlib, json, os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sets  # noqa: E402

MODELS = Path(os.environ.get("MUNINN_JUDGE_MODELS", Path.home() / ".cache/muninn-judge/models"))
REPO = HERE.parent.parent.parent.parent

GGUF = {"A1": "qwen35-4b-q4km.gguf", "A2": "qwen35-2b-q4km.gguf", "A3": "gemma4-e4b-q4km.gguf"}

# The prompt is part of the registration: changing a word of it is a new arm.
QUESTION = (
    "You keep the memory of a software project. Each record states something the project "
    "decided or holds. Records can be in any language.\n\n"
    "Question: does the new message replace, reverse or withdraw what the earlier record "
    "states, so that the earlier record is no longer current?\n"
    "A) Yes: the earlier record is no longer current.\n"
    "B) No: the new message is about something else, adds detail, or leaves the earlier "
    "record true.\n\n"
    "Earlier record:\n<<<{a}>>>\n\n")
SUFFIX = "New message, written later in the same project:\n<<<{b}>>>\n\nAnswer with the letter only."
SENTINEL = "\x00SPLIT\x00"

LAYA_Q = {"replaces": {"type": "noul", "instructions":
          "Does `later` replace, reverse or withdraw what `earlier` states, so that `earlier` "
          "is no longer current?"}}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- A0: the shipped rules

def transcript(path: Path, sid: str, ts: datetime, user: str) -> None:
    base = {"isSidechain": False, "userType": "external", "cwd": "/work/project", "sessionId": sid}
    rows = [
        {**base, "parentUuid": None, "type": "user", "uuid": f"{sid}-u",
         "timestamp": ts.isoformat().replace("+00:00", "Z"),
         "message": {"role": "user", "content": user}},
        {**base, "parentUuid": f"{sid}-u", "type": "assistant", "uuid": f"{sid}-a",
         "timestamp": (ts + timedelta(seconds=2)).isoformat().replace("+00:00", "Z"),
         "message": {"role": "assistant", "type": "message", "model": "synthetic",
                     "content": [{"type": "text", "text": "Noted."}], "stop_reason": "end_turn"}},
    ]
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


T0 = datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc)


def a0_store(muninn: str, earlier: list, later: str) -> dict:
    """A store that holds every earlier message of a group, one session each in order, then the
    later one. Returns, per earlier message, whether it was recorded and nothing of it is still
    served. A group store and not a two-message one: with a single earlier record, the anaphora
    rule (ingest.rs, "the latest short episode") has only that record to take, which would
    charge the rules with a false retirement no real store would show."""
    t = time.perf_counter()
    root = Path(tempfile.mkdtemp(prefix="judge-a0-"))
    try:
        (root / ".git").mkdir()
        env = {**os.environ, "MUNINN_ROOT": str(root), "MUNINN_NO_PROJECT": "1"}
        subprocess.run([muninn, "--cwd", str(root), "init", "--keep-native"], env=env, capture_output=True)
        for k, text in enumerate(earlier + [later]):
            f = root / f"t{k}.jsonl"
            transcript(f, f"s{k:03d}", T0 + timedelta(minutes=30 * k), text)
            subprocess.run([muninn, "--cwd", str(root), "ingest", str(f)], env=env, capture_output=True)
        subprocess.run([muninn, "--cwd", str(root), "--json", "export", "--all", "--out",
                        str(root / "x.jsonl")], env=env, capture_output=True)
        recs = [json.loads(l) for l in open(root / "x.jsonl")]
        out = {}
        for a in earlier:
            key = a.strip().rstrip(".!;")[:40].lower()
            held = [r for r in recs if key in (r.get("body") or "").lower()]
            kept = [r for r in held if not r.get("invalid")]
            out[a] = {"p": 1.0 if held and not kept else 0.0,
                      "raw": {"held": len(held), "kept": len(kept), "store": len(earlier)}}
        ms = (time.perf_counter() - t) * 1000
        for v in out.values():
            v["ms"] = ms
        return out
    finally:
        subprocess.run(["rm", "-rf", str(root)])


def run_a0(items, args):
    muninn = str(REPO / "target/release/muninn")
    meta = {"binary": muninn, "sha256": sha256(Path(muninn)),
            "method": "one store per (group, later message): every earlier message of the group, then the later one",
            "order": args.order}
    earlier, laters, a_of = {}, {}, {}
    for it in items:
        earlier.setdefault(it["group"], [])
        if it["a"] not in earlier[it["group"]]:
            earlier[it["group"]].append(it["a"])
        a_key, later_key = it["id"].split("|")[:2]
        a_of[(it["group"], a_key)] = it["a"]
        laters.setdefault((it["group"], it["b"]), later_key)
    # loop 10, third-language and user pairs are pairs, not groups: their store is the pair
    pairwise = {it["group"] for it in items if it["kind"] in ("neg_shared", "neg_user")
                or it["set"] == "user"}
    jobs = []
    for (g, later), later_key in laters.items():
        if g in pairwise:
            for it in items:
                if it["group"] == g and it["b"] == later:
                    jobs.append(((g, later, it["a"]), [it["a"]], later))
        elif args.order == "adjacent":
            # the decision this message belongs to is the last one before it, as in a
            # conversation that changes its mind right away: the order most favourable to the
            # rules, whose anaphora path takes the latest episode
            own = a_of[(g, later_key)]
            jobs.append(((g, later, None), [a for a in earlier[g] if a != own] + [own], later))
        else:
            jobs.append(((g, later, None), earlier[g], later))
    with ThreadPoolExecutor(args.jobs) as ex:
        done = dict(zip([j[0] for j in jobs], ex.map(lambda j: a0_store(muninn, j[1], j[2]), jobs)))
    rows = []
    for it in items:
        key = (it["group"], it["b"], it["a"] if it["group"] in pairwise else None)
        rows.append(done[key][it["a"]])
    return meta, rows


# ---------------------------------------------------------------- A1-A3: letter logits

class LetterJudge:
    def __init__(self, path: Path, threads: int):
        import numpy as np
        import llama_cpp
        from jinja2 import Environment
        self.np, self.lc = np, llama_cpp
        self.llm = llama_cpp.Llama(model_path=str(path), n_ctx=1024, n_threads=threads,
                                   n_threads_batch=threads, n_gpu_layers=0, seed=0,
                                   logits_all=False, verbose=False)
        tpl = self.llm.metadata["tokenizer.chat_template"]
        env = Environment()
        env.globals["raise_exception"] = lambda m: (_ for _ in ()).throw(ValueError(m))
        msg = [{"role": "user", "content": QUESTION.replace("{a}", "{a}") + SENTINEL + SUFFIX}]
        rendered = env.from_string(tpl).render(messages=msg, add_generation_prompt=True,
                                               enable_thinking=False, bos_token="", eos_token="")
        self.pre_tpl, self.suf_tpl = rendered.split(SENTINEL)
        self.letters = [self._single(c) for c in ("A", "B")]
        self.cached_a, self.state = None, None
        self.n_vocab = self.llm.n_vocab()

    def _single(self, s):
        toks = self.llm.tokenize(s.encode(), add_bos=False, special=False)
        assert len(toks) == 1, (s, toks)
        return toks[0]

    def _tok(self, s):
        return self.llm.tokenize(s.encode(), add_bos=True, special=True)

    def _logits(self):
        ptr = self.lc.llama_get_logits_ith(self.llm._ctx.ctx, -1)
        return self.np.ctypeslib.as_array(ptr, shape=(self.n_vocab,))

    def score(self, a: str, b: str, cached: bool = True):
        pre = self.pre_tpl.replace("{a}", a)
        full = pre + self.suf_tpl.replace("{b}", b)
        pt, ft = self._tok(pre), self._tok(full)
        if not cached or ft[:len(pt)] != pt:
            self.llm.reset()
            self.llm.eval(ft)
            self.cached_a = None
        else:
            if self.cached_a != pre:
                self.llm.reset()
                self.llm.eval(pt)
                self.state, self.cached_a = self.llm.save_state(), pre
            else:
                self.llm.load_state(self.state)
            self.llm.eval(ft[len(pt):])
        lg = self._logits()
        la, lb = float(lg[self.letters[0]]), float(lg[self.letters[1]])
        m = max(la, lb)
        pa = self.np.exp(la - m) / (self.np.exp(la - m) + self.np.exp(lb - m))
        top = int(lg.argmax())
        return float(pa), {"la": la, "lb": lb, "top_is_letter": top in self.letters}


def run_letters(items, args):
    path = MODELS / GGUF[args.arm]
    j = LetterJudge(path, args.threads)
    meta = {"model": path.name, "sha256": sha256(path), "threads": args.threads,
            "prefix_tokens_sample": len(j._tok(j.pre_tpl.replace("{a}", items[0]["a"])))}
    # earlier record outermost, so the cached prefix is reused across every later message
    order = sorted(range(len(items)), key=lambda i: (items[i]["a"], items[i]["b"]))
    rows = [None] * len(items)
    for n, i in enumerate(order):
        t = time.perf_counter()
        p, raw = j.score(items[i]["a"], items[i]["b"])
        rows[i] = {"p": p, "raw": raw, "ms": (time.perf_counter() - t) * 1000}
        if n % 500 == 0:
            print(f"{args.arm} {n}/{len(items)}", file=sys.stderr, flush=True)
    full = []
    for i in range(0, len(items), max(1, len(items) // args.full_prompt_sample)):
        t = time.perf_counter()
        p, _ = j.score(items[i]["a"], items[i]["b"], cached=False)
        full.append({"id": items[i]["id"], "ms": (time.perf_counter() - t) * 1000,
                     "same_p": round(p, 2) == round(rows[i]["p"], 2)})
    meta["full_prompt"] = full
    return meta, rows


# ---------------------------------------------------------------- A4: NLI encoder

def run_nli(items, args):
    import numpy as np
    import onnxruntime as ort
    from tokenizers import Tokenizer
    d = MODELS / "mdeberta"
    cfg = json.load(open(d / "config.json"))
    contra = [int(k) for k, v in cfg["id2label"].items() if v.lower() == "contradiction"][0]
    tok = Tokenizer.from_file(str(d / "tokenizer.json"))
    so = ort.SessionOptions()
    so.intra_op_num_threads = args.threads
    sess = ort.InferenceSession(str(d / "onnx/model.onnx"), so, providers=["CPUExecutionProvider"])
    names = [x.name for x in sess.get_inputs()]
    meta = {"model": "mdeberta/onnx/model.onnx", "sha256": sha256(d / "onnx/model.onnx"),
            "labels": cfg["id2label"], "threads": args.threads}
    rows = []
    for n, it in enumerate(items):
        t = time.perf_counter()
        e = tok.encode(it["a"], it["b"])
        feed = {"input_ids": np.array([e.ids], dtype=np.int64),
                "attention_mask": np.array([e.attention_mask], dtype=np.int64)}
        if "token_type_ids" in names:
            feed["token_type_ids"] = np.array([e.type_ids], dtype=np.int64)
        lg = sess.run(None, feed)[0][0]
        pr = np.exp(lg - lg.max()); pr /= pr.sum()
        rows.append({"p": float(pr[contra]), "raw": [round(float(x), 4) for x in pr],
                     "ms": (time.perf_counter() - t) * 1000})
        if n % 1000 == 0:
            print(f"A4 {n}/{len(items)}", file=sys.stderr, flush=True)
    return meta, rows


# ---------------------------------------------------------------- A5: laya-multilingual

def run_laya(items, args):
    os.environ.setdefault("USE_TF", "0")
    import torch
    torch.set_num_threads(args.threads)
    import laya
    agent = laya.load("convaiinnovations/laya-multilingual", device="cpu")
    meta = {"model": "convaiinnovations/laya-multilingual", "threads": args.threads,
            "question": LAYA_Q, "temperatures": "as shipped (uncalibrated)"}
    rows = []
    for n, it in enumerate(items):
        t = time.perf_counter()
        r = agent.predict({"earlier": it["a"], "later": it["b"]}, LAYA_Q)
        p = float(r["answers"]["replaces"]["noul"])
        rows.append({"p": p, "raw": None, "ms": (time.perf_counter() - t) * 1000})
        if n % 1000 == 0:
            print(f"A5 {n}/{len(items)}", file=sys.stderr, flush=True)
    return meta, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["A0", "A1", "A2", "A3", "A4", "A5"])
    ap.add_argument("--out", default=str(HERE.parent / "results/judge-v1"))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--threads", type=int, default=16)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--full-prompt-sample", type=int, default=100)
    ap.add_argument("--tag", default="")
    ap.add_argument("--set", default="v1", choices=["v1", "v1b"])
    ap.add_argument("--order", default="adjacent", choices=["adjacent", "separated"],
                    help="A0 only: where the scenario's own decision sits among the group's")
    args = ap.parse_args()
    items = sets.probe_items() if args.set == "v1b" else sets.items()
    if args.limit:
        items = items[:: max(1, len(items) // args.limit)][: args.limit]
    run = {"A0": run_a0, "A1": run_letters, "A2": run_letters, "A3": run_letters,
           "A4": run_nli, "A5": run_laya}[args.arm]
    t = time.time()
    meta, rows = run(items, args)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    name = f"{args.arm}{args.tag}"
    with open(out / f"{name}.jsonl", "w") as f:
        for it, r in zip(items, rows):
            f.write(json.dumps({"id": it["id"], "split": it["split"], "lang": it["lang"],
                                "kind": it["kind"], "label": it["label"], "set": it["set"],
                                "p": round(r["p"], 2), "p_raw": r["p"], "ms": round(r["ms"], 2),
                                "raw": r["raw"]}, ensure_ascii=False) + "\n")
    meta.update({"arm": args.arm, "items": len(items), "wall_s": round(time.time() - t, 1),
                 "started": datetime.fromtimestamp(t, timezone.utc).isoformat(),
                 "cpu": "AMD Ryzen 9 7950X3D, 16 cores"})
    json.dump(meta, open(out / f"{name}.meta.json", "w"), indent=1, ensure_ascii=False)
    print(f"{name}: {len(items)} pairs in {meta['wall_s']} s", file=sys.stderr)


if __name__ == "__main__":
    main()
