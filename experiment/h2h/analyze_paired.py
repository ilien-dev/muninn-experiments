#!/usr/bin/env python3
"""Two arms of one grid, compared cell by cell instead of count against count.

Every analyzer in this directory tallies each arm and tests the two totals. That throws away
the pairing the grid already has: both arms answered the same task in the same run, and a task
the whole grid finds hard contributes to both totals without telling you anything about the
difference. Testing the totals with Fisher treats the two arms as independent samples, which
they are not.

The paired test is McNemar's, exact: among cells where the two arms disagree, is the split
between "A passed, B failed" and "B passed, A failed" further from even than chance allows? The
concordant cells — both passed, both failed — carry no information about the difference and are
counted but not tested. On a grid where most cells agree, this resolves differences that a
test on the totals cannot.

It reports both, because they answer different questions and the registered tests in this
project are written against the totals.

  analyze_paired.py <grid dir> <arm A> <arm B> [--all-tasks]
"""
import argparse, json, pathlib
from math import comb


def fisher_two_sided(a, n1, b, n2):
    K, N = a + b, n1 + n2
    def p(x):
        return comb(K, x) * comb(N - K, n1 - x) / comb(N, n1)
    p0 = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, K - n2), min(K, n1) + 1) if p(x) <= p0 * (1 + 1e-9)))


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar: b and c are the discordant counts. Under the null each
    discordant cell is a fair coin, so the test is a two-sided binomial on b of b + c."""
    n = b + c
    if n == 0:
        return 1.0
    pk = comb(n, b) / 2 ** n
    return min(1.0, sum(comb(n, x) / 2 ** n for x in range(n + 1)
                        if comb(n, x) / 2 ** n <= pk * (1 + 1e-9)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("grid")
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--all-tasks", action="store_true",
                    help="every task, not only the replacement ones the registered tests use")
    args = ap.parse_args()
    d = pathlib.Path(args.grid)
    cfg = json.load((d / "config.json").open())
    keep = {t["id"] for t in cfg["tasks"]
            if args.all_tasks or t["scenario"].get("new") is not None}
    cells: dict = {}
    for line in (d / "results.jsonl").open():
        if not line.strip():
            continue
        r = json.loads(line)
        if r["task"] in keep and r["arm"] in (args.a, args.b):
            cells.setdefault((r["run"], r["task"]), {})[r["arm"]] = r.get("oracle_exit") == 0

    pairs = [(v[args.a], v[args.b]) for v in cells.values() if args.a in v and args.b in v]
    if not pairs:
        raise SystemExit(f"no cell has both {args.a} and {args.b} in {d}")
    both = sum(1 for x, y in pairs if x and y)
    neither = sum(1 for x, y in pairs if not x and not y)
    only_a = sum(1 for x, y in pairs if x and not y)
    only_b = sum(1 for x, y in pairs if y and not x)
    ka, kb = both + only_a, both + only_b
    n = len(pairs)

    print(f"{d.name}: {n} paired cells")
    print(f"  {args.a:24s} {ka:3d} / {n}")
    print(f"  {args.b:24s} {kb:3d} / {n}")
    print(f"  agree: {both} both pass, {neither} both fail  ({both + neither} of {n})")
    print(f"  disagree: {only_a} only {args.a}, {only_b} only {args.b}")
    print(f"  paired (exact McNemar)   p = {mcnemar_exact(only_a, only_b):.4f}")
    print(f"  unpaired (exact Fisher)  p = {fisher_two_sided(ka, n, kb, n):.4f}")
    if len(pairs) < len(cells):
        print(f"  note: {len(cells) - len(pairs)} cell(s) had only one of the two arms and were dropped")


if __name__ == "__main__":
    main()
