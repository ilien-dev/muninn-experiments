#!/usr/bin/env python3
"""How much of the turn's context each memory spends.

A memory's price to the agent is not only what it costs to run: it is the room it takes in
the window before the agent has read a line of code. Claude Code records what every hook put
into a session as `attachment` rows in the transcript, so the two arms can be compared on the
same tasks with no instrumentation of either tool.

Counted per cell, in characters of the attachment payload, **`hook_additional_context`
only** — the one payload that is certainly the model's context. The others are reported
beside it and deliberately not added in:

  hook_success        the hook result record, whose `stdout` *repeats* the context for a tool
                      that returns it on stdout (Muninn) and not for one that does not
                      (claude-mem). Adding it counts one arm's injection twice; the first
                      version of this script did exactly that, and it flattered Muninn.
  hook_system_message a terminal message, ANSI-coloured, which claude-mem uses and Muninn does
                      not. Whether the model sees it is not established here, so it is not
                      counted for or against.
  everything else     harness scaffolding, reported as a check

Paired by (run, task) so every arm answers the same question in the same checkout, and
reported as a median ratio with a bootstrap interval over the pairs.

**Exploratory.** The grid was registered to answer whether a replacement is noticed. This
reads something else off it afterwards. A claim would need a grid with context size as its
registered outcome — which is cheap to run, and is the honest next step if the number matters.

  context_cost.py <results dir> [--baseline claude-mem]
"""
import argparse
import json
import pathlib
import random
import statistics as st

MEMORY_KEY = "hook_additional_context"
SIDE_KEYS = ("hook_system_message", "hook_success")


def cell_bytes(path: pathlib.Path) -> dict:
    out = {k: 0 for k in (MEMORY_KEY, *SIDE_KEYS)}
    out["other"] = 0
    if not path.exists():
        return out
    for line in path.open(errors="replace"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("type") != "attachment":
            continue
        k = (r.get("attachment") or {}).get("type", "?")
        n = len(json.dumps(r))
        out[k if k in (MEMORY_KEY, *SIDE_KEYS) else "other"] += n
    return out


def collect(d: pathlib.Path):
    rows = [json.loads(l) for l in (d / "results.jsonl").read_text().splitlines() if l.strip()]
    logs = d / "logs"
    for r in rows:
        b = cell_bytes(logs / f"r{r['run']}-{r['task']}-{r['arm']}.transcript.jsonl")
        r["memory_chars"] = b[MEMORY_KEY]
        r["side_chars"] = sum(b[k] for k in SIDE_KEYS)
        r["other_chars"] = b["other"]
        r["detail"] = b
    return [r for r in rows if r.get("error") is None and r["memory_chars"] > 0]


def ratio_ci(pairs, reps=10000, seed=7):
    rng = random.Random(seed)
    base = st.median(a / b for a, b in pairs if b)
    boots = []
    for _ in range(reps):
        s = [pairs[rng.randrange(len(pairs))] for _ in pairs]
        vals = [a / b for a, b in s if b]
        if vals:
            boots.append(st.median(vals))
    boots.sort()
    return base, boots[int(0.025 * len(boots))], boots[int(0.975 * len(boots))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--baseline", default="claude-mem")
    a = ap.parse_args()
    d = pathlib.Path(a.out)
    rows = collect(d)
    arms = sorted({r["arm"] for r in rows})
    print(f"# {d.name} — context characters a memory adds to a cell")
    print("| arm | cells | median context chars | median hook/terminal chars | median harness chars |")
    print("|---|---|---|---|---|")
    for arm in arms:
        sub = [r for r in rows if r["arm"] == arm]
        print(f"| {arm} | {len(sub)} | {st.median(r['memory_chars'] for r in sub):.0f} | "
              f"{st.median(r['side_chars'] for r in sub):.0f} | "
              f"{st.median(r['other_chars'] for r in sub):.0f} |")
    idx = {(r["run"], r["task"], r["arm"]): r for r in rows}
    for arm in arms:
        if arm == a.baseline:
            continue
        keys = {(r, t) for (r, t, m) in idx if m == arm} & \
               {(r, t) for (r, t, m) in idx if m == a.baseline}
        pairs = [(idx[(r, t, arm)]["memory_chars"], idx[(r, t, a.baseline)]["memory_chars"])
                 for r, t in sorted(keys)]
        if not pairs:
            continue
        m, lo, hi = ratio_ci(pairs)
        verdict = "smaller" if hi < 1 else ("larger" if lo > 1 else "not distinguishable")
        print(f"\n{arm} / {a.baseline} = {m:.3f} [{lo:.3f}, {hi:.3f}]  {verdict}"
              f"   ({len(pairs)} paired cells)")
    print("\nExploratory, post-hoc, on a grid registered for a different question.")


if __name__ == "__main__":
    main()
