#!/usr/bin/env python3
"""Head-to-head v4: the same grid with and without the decisions in the code.

Reads the two result directories, labels each cell `<arm>|code` or `<arm>|nocode`, and runs
the contrasts the pre-registration names, in its words:

  B - D   muninn with code  vs  claude-mem with code   (the claim; Holm over {B-D, B-A})
  B - A   muninn with code  vs  muninn without code    (did the code condition help Muninn)
  D - C   claude-mem with code vs without              (the control: if the commits help the
                                                        competitor too, the grid measured the
                                                        fixture and no claim is made)

Pass is the Gate 3 oracle, unchanged: the current value written and the retired one absent.
Only replacement scenarios are counted, as in every other head-to-head.

  analyze_v4.py <code-dir> <nocode-dir>
"""
import argparse
import json
import os
from math import comb


def fisher_two_sided(a, n1, b, n2):
    K, N = a + b, n1 + n2
    if N == 0 or K == 0 or K == N:
        return 1.0

    def p(x):
        return comb(K, x) * comb(N - K, n1 - x) / comb(N, n1)

    p0 = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, K - n2), min(K, n1) + 1)
                        if p(x) <= p0 * (1 + 1e-9)))


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    out, running = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        out[i] = running
    return out


def load(d, cond):
    cfg = json.load(open(os.path.join(d, "config.json")))
    sc = {t["id"]: t["scenario"] for t in cfg["tasks"]}
    rows = [json.loads(l) for l in open(os.path.join(d, "results.jsonl"))]
    for r in rows:
        s = sc[r["task"]]
        r["replacement"] = s["new"] is not None
        r["cell"] = f"{r['arm']}|{cond}"
        p = os.path.join(d, "diffs", f"r{r['run']}-{r['task']}-{r['arm']}.patch")
        added = ""
        if os.path.exists(p):
            added = "\n".join(l[1:] for l in open(p, errors="replace").read().splitlines()
                              if l.startswith("+") and not l.startswith("+++")).lower()
        r["unsafe"] = int(s["old"].lower() in added)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("nocode")
    a = ap.parse_args()
    rows = load(a.code, "code") + load(a.nocode, "nocode")
    ok = [r for r in rows if r["status"] != "error" and r["replacement"]]
    cells = sorted({r["cell"] for r in ok})
    tally = {}
    print("| arm | condition | replacement pass | retired value written | errors |")
    print("|---|---|---|---|---|")
    for c in cells:
        sub = [r for r in ok if r["cell"] == c]
        err = sum(1 for r in rows if r["cell"] == c and r["status"] == "error"
                  and r["replacement"])
        tally[c] = (sum(r["status"] == "pass" for r in sub), len(sub))
        arm, cond = c.split("|")
        print(f"| {arm} | {cond} | {tally[c][0]}/{len(sub)} | "
              f"{sum(r['unsafe'] for r in sub)}/{len(sub)} | {err} |")

    def contrast(x, y):
        (ax, nx), (ay, ny) = tally.get(x, (0, 0)), tally.get(y, (0, 0))
        return fisher_two_sided(ax, nx, ay, ny), (ax, nx, ay, ny)

    muninns = sorted({c.split("|")[0] for c in cells if c.startswith("muninn")})
    other = next((c.split("|")[0] for c in cells if not c.startswith("muninn")), "claude-mem")
    muninn = muninns[0] if muninns else "muninn-loop8"
    B, A = f"{muninn}|code", f"{muninn}|nocode"
    D, C = f"{other}|code", f"{other}|nocode"
    registered = [("B-D  claim", B, D), ("B-A  code helped Muninn", B, A)]
    # any further Muninn arm is reported against the registered one and against the
    # competitor, outside the registered family and labelled as such
    extra = [(f"{m} vs {muninn}", f"{m}|code", B) for m in muninns[1:]] + \
            [(f"{m} vs {other}", f"{m}|code", D) for m in muninns[1:]]
    ps = [contrast(x, y)[0] for _, x, y in registered]
    adj = holm(ps)
    print()
    for (label, x, y), p, q in zip(registered, ps, adj):
        ax, nx, ay, ny = contrast(x, y)[1]
        print(f"{label:28s} {ax}/{nx} vs {ay}/{ny}   Fisher p = {p:.4g}   Holm p = {q:.4g}")
    for label, x, y in extra:
        p, (ax, nx, ay, ny) = contrast(x, y)
        print(f"{label:28s} {ax}/{nx} vs {ay}/{ny}   Fisher p = {p:.4g}   (not in the "
              f"registered family)")
    p_ctrl, (ax, nx, ay, ny) = contrast(D, C)
    print(f"{'D-C  control (must be ns)':28s} {ax}/{nx} vs {ay}/{ny}   Fisher p = {p_ctrl:.4g}")
    print()
    claim = adj[0] < 0.05 and tally.get(B, (0, 0))[0] * tally.get(D, (0, 1))[1] > \
        tally.get(D, (0, 0))[0] * tally.get(B, (0, 1))[1]
    print("claim:", "made" if (claim and p_ctrl >= 0.05) else "not made",
          "(control significant — the fixture, not the memory)" if p_ctrl < 0.05 else "")


if __name__ == "__main__":
    main()
