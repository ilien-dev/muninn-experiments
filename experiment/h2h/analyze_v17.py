#!/usr/bin/env python3
"""v17 (PREREGISTRATION.md, "the build after a day of defect fixes").

The arm was run into a directory of its own, so its competitor is not in the same
`results.jsonl`. This reads the new arm's cells from one grid and the competitor's from
v13's, pairs nothing, and applies the registered test:

  confirmatory   pass(muninn-day2) - pass(claude-mem), exact two-sided Fisher, alpha = 0.05
  reported       pass(muninn-day2) - pass(muninn-ship)

The competitor cells are **not re-run**: they are v13's, on the same fixture, the same tasks
and the same seed phrasings, with claude-mem pinned to the same version. That substitution is
what the registration says this arm is measured against, and it is the whole of what makes
this cheaper than a full grid.

  analyze_v17.py <new grid dir> <v13 dir>
"""
import argparse, collections, json, pathlib
from math import comb


def fisher_two_sided(a, n1, b, n2):
    K, N = a + b, n1 + n2
    def p(x):
        return comb(K, x) * comb(N - K, n1 - x) / comb(N, n1)
    p0 = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, K - n2), min(K, n1) + 1) if p(x) <= p0 * (1 + 1e-9)))


def cells(d: pathlib.Path):
    """The replacement cells, split exactly as `analyze_h2h.py` splits them: a task is a
    replacement when its scenario has a `new` value. Nine of the fixture's ten do, which is
    where the published 54 comes from. (`inferable` is a different field and is false for
    every row; reading it as the split gave 60 cells here before the config was consulted.)"""
    cfg = json.load((d / "config.json").open())
    replacement = {t["id"] for t in cfg["tasks"] if t["scenario"].get("new") is not None}
    rows = [json.loads(l) for l in (d / "results.jsonl").open() if l.strip()]
    return [r for r in rows if r["task"] in replacement]


def tally(rows, arm):
    sub = [r for r in rows if r["arm"] == arm]
    return sum(1 for r in sub if r.get("oracle_exit") == 0), len(sub)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("new")
    ap.add_argument("old")
    a = ap.parse_args()
    new, old = cells(pathlib.Path(a.new)), cells(pathlib.Path(a.old))
    print("arm                    pass / cells   source")
    got = {}
    for arm, rows, src in (("muninn-day2", new, a.new), ("claude-mem", old, a.old),
                           ("muninn-ship", old, a.old), ("off", old, a.old)):
        k, n = tally(rows, arm)
        got[arm] = (k, n)
        print(f"  {arm:20s} {k:3d} / {n:3d}     {pathlib.Path(src).name}")
    (kd, nd), (kc, nc) = got["muninn-day2"], got["claude-mem"]
    if nd and nc:
        print(f"\nconfirmatory  muninn-day2 vs claude-mem: "
              f"{kd}/{nd} vs {kc}/{nc}, exact Fisher p = {fisher_two_sided(kd, nd, kc, nc):.3g}")
    (ks, ns) = got["muninn-ship"]
    if nd and ns:
        print(f"reported      muninn-day2 vs muninn-ship: "
              f"{kd}/{nd} vs {ks}/{ns}, exact Fisher p = {fisher_two_sided(kd, nd, ks, ns):.3g}")
    err = collections.Counter(r.get("error") for r in new if r.get("error"))
    if err:
        print("\nerrors in the new grid:", dict(err))


if __name__ == "__main__":
    main()
