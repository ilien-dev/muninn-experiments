#!/usr/bin/env python3
"""What each memory costs the turn it helps — an exploratory read of an existing grid.

**This is post-hoc.** The head-to-head was pre-registered to answer one question: does the tool
notice, without labels, that a decision was replaced. It was not registered to compare cost, and
this analysis was written after its data existed. It is reported as exploratory, it is not a
claim, and it does not become one by having a pleasant result. What would make it a claim is a
pre-registered grid with cost as its outcome.

What is compared, per replacement cell, paired by (run, task) so every arm answers the same
question in the same checkout:

  cost_usd     what the agent's own session cost. Memory changes this by changing how much
               context arrives and how much searching the agent does instead.
  duration_ms  wall clock for the cell.
  num_turns    how many turns the agent took.

What this is **not**: the overhead of the memory engine. A cell where memory delivered the fact
is cheaper because the agent stopped looking, not because the hook was fast. Cost here is
downstream of whether the memory worked, and the two cannot be separated in this grid. The hook's
own cost is `perf --strict`, measured separately and without a model.

  python3 cost_analysis.py <results dir> [--baseline claude-mem]
"""
import argparse
import json
import pathlib
import random
import statistics as st

def load(d: pathlib.Path):
    """The replacement cells only — the same split `analyze_h2h.py` reports on.

    A scenario is a replacement when its `new` value exists; the two withdrawal scenarios are
    a different question and are left out here as they are there.
    """
    cfg = json.loads((d / "config.json").read_text())
    replacement = {t["id"] for t in cfg["tasks"] if t["scenario"]["new"] is not None}
    rows = [json.loads(l) for l in (d / "results.jsonl").read_text().splitlines() if l.strip()]
    return [r for r in rows
            if r.get("error") is None
            and r.get("cost_usd") is not None
            and r["task"] in replacement]


def paired(rows, a, b, field):
    """(a, b) values for the cells both arms ran."""
    idx = {(r["run"], r["task"], r["arm"]): r for r in rows}
    keys = {(r["run"], r["task"]) for r in rows if r["arm"] == a} & \
           {(r["run"], r["task"]) for r in rows if r["arm"] == b}
    return [(idx[(k[0], k[1], a)][field], idx[(k[0], k[1], b)][field])
            for k in sorted(keys)
            if idx.get((k[0], k[1], a)) and idx.get((k[0], k[1], b))]


def boot_ratio(pairs, iters=10000, seed=11):
    """Median of a / median of b, resampled over pairs."""
    rnd = random.Random(seed)
    def ratio(sample):
        return st.median(x for x, _ in sample) / st.median(y for _, y in sample)
    point = ratio(pairs)
    draws = sorted(ratio([rnd.choice(pairs) for _ in pairs]) for _ in range(iters))
    return point, draws[int(0.025 * iters)], draws[int(0.975 * iters) - 1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("results", type=pathlib.Path)
    ap.add_argument("--arm", default="muninn-latest")
    ap.add_argument("--baseline", default="claude-mem")
    a = ap.parse_args()

    rows = load(a.results)
    arms = sorted({r["arm"] for r in rows})
    print(f"{a.results} — {len(rows)} replacement cells, arms: {', '.join(arms)}\n")
    print(f"{'arm':22} {'n':>4} {'pass':>5} {'cost/cell':>10} {'seconds':>9} {'turns':>7}")
    for arm in arms:
        v = [r for r in rows if r["arm"] == arm]
        print(f"{arm:22} {len(v):>4} {sum(r['status'] == 'pass' for r in v):>5} "
              f"{st.median(r['cost_usd'] for r in v):>10.4f} "
              f"{st.median(r['duration_ms'] for r in v) / 1000:>9.1f} "
              f"{st.median(r['num_turns'] for r in v if r.get('num_turns')):>7.1f}")

    print(f"\npaired against {a.baseline}, median ratio [95 % bootstrap over paired cells]:")
    for field, unit in (("cost_usd", "cost"), ("duration_ms", "wall clock"), ("num_turns", "turns")):
        pairs = [(x, y) for x, y in paired(rows, a.arm, a.baseline, field) if y]
        if not pairs:
            continue
        p, lo, hi = boot_ratio(pairs)
        verdict = "cheaper" if hi < 1 else ("dearer" if lo > 1 else "not distinguishable")
        print(f"  {unit:<12} {a.arm} / {a.baseline} = {p:.3f} [{lo:.3f}, {hi:.3f}]  {verdict}")

    # The obvious objection: an arm that solves more cells finishes sooner, so the difference
    # could be the outcome rather than the memory. Split by outcome and look again — if the arm
    # is faster inside both strata, that explanation does not cover it.
    print(f"\nsplit by outcome (the same comparison inside each stratum):")
    print(f"  {'arm':22} {'outcome':8} {'n':>3} {'seconds':>8} {'cost':>9} {'turns':>7}")
    for arm in (a.arm, a.baseline):
        for outcome in ("pass", "fail"):
            v = [r for r in rows if r["arm"] == arm and r["status"] == outcome]
            if not v:
                continue
            print(f"  {arm:22} {outcome:8} {len(v):>3} "
                  f"{st.median(r['duration_ms'] for r in v) / 1000:>8.1f} "
                  f"{st.median(r['cost_usd'] for r in v):>9.4f} "
                  f"{st.median(r['num_turns'] for r in v):>7.1f}")

    print("\nExploratory, post-hoc, on a grid registered for a different question. Cost here is\n"
          "downstream of whether the memory worked and is not the engine's overhead; the hook's\n"
          "own cost is `perf --strict`.")


if __name__ == "__main__":
    main()
