#!/usr/bin/env python3
"""The registered secondary of v17: how much each arm put in the model's window.

Per replacement cell, the characters of the `hook_additional_context` attachments in that
cell's own transcript. The published 2.591 excludes `hook_system_message` — the payload
claude-mem leans on and Muninn does not — and so does this by default; `--with-system` reads
both, which is the figure that answers "what did the window actually hold".

This instrument does **not** reproduce the published number exactly: it reads `muninn-ship`,
the arm the 2.591 was measured on, at 2.824 [2.606, 3.010] over the same 54 cells. The
intervals overlap and the two are measuring the same thing in different ways; what is
trustworthy here is the ratio *between arms read by one instrument*, not the absolute value
against a figure produced by another.

  injected_context.py <new dir> <v13 dir> [--with-system]
"""
import argparse, json, pathlib, random, statistics as st

BOTH = ("hook_additional_context", "hook_system_message")


def chars(path: pathlib.Path, keys) -> int:
    if not path.exists():
        return 0
    n = 0
    for line in path.open(errors="replace"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        at = r.get("attachment") or {}
        if r.get("type") == "attachment" and at.get("type") in keys:
            c = at.get("content")
            n += len(" ".join(c) if isinstance(c, list) else str(c))
    return n


def ci(pairs, f, reps=10000, seed=7):
    rng = random.Random(seed)
    m = []
    for _ in range(reps):
        s = [pairs[rng.randrange(len(pairs))] for _ in pairs]
        m.append(st.median(f(x) for x in s))
    m.sort()
    return m[int(0.025 * reps)], m[int(0.975 * reps)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("new")
    ap.add_argument("old")
    ap.add_argument("--new-arm", default="muninn-day2")
    ap.add_argument("--base-arm", default="muninn-ship",
                    help="the arm in the old grid to read as the baseline")
    ap.add_argument("--with-system", action="store_true")
    a = ap.parse_args()
    keys = BOTH if a.with_system else BOTH[:1]
    new, old = pathlib.Path(a.new), pathlib.Path(a.old)
    cfg = json.load((old / "config.json").open())
    rep = [t["id"] for t in cfg["tasks"] if t["scenario"].get("new") is not None]
    runs = 1 + max(json.loads(l)["run"] for l in (new / "results.jsonl").open() if l.strip())
    pairs = []
    for r in range(runs):
        for t in rep:
            row = (chars(new / "logs" / f"r{r}-{t}-{a.new_arm}.transcript.jsonl", keys),
                   chars(old / "logs" / f"r{r}-{t}-claude-mem.transcript.jsonl", keys),
                   chars(old / "logs" / f"r{r}-{t}-{a.base_arm}.transcript.jsonl", keys))
            if all(row):
                pairs.append(row)
    print(f"{len(pairs)} replacement cells · {'additionalContext + systemMessage' if a.with_system else 'additionalContext only'}")
    for name, f in ((f"{a.new_arm} / claude-mem", lambda x: x[0] / x[1]),
                    (f"{a.base_arm} / claude-mem", lambda x: x[2] / x[1]),
                    (f"{a.new_arm} / {a.base_arm}", lambda x: x[0] / x[2])):
        lo, hi = ci(pairs, f)
        print(f"  {name:28s} {st.median(f(x) for x in pairs):.3f} [{lo:.3f}, {hi:.3f}]")
    for i, name in ((0, a.new_arm), (2, a.base_arm), (1, "claude-mem")):
        print(f"  median chars {name:22s} {st.median(x[i] for x in pairs):.0f}")


if __name__ == "__main__":
    main()
