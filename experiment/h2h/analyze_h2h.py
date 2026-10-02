#!/usr/bin/env python3
"""Analysis of the label-free head-to-head (PREREGISTRATION.md, "Head-to-head without labels").

Per arm, on the eight replacement scenarios (24 cells per arm with three runs): pass (Gate 3 oracle:
current value written, retired value absent), unsafe (retired value written), and a secondary figure
that the pre-registration's oracle does not reward: current value written, whatever else the file
says. On the two revocation scenarios: pass. Exact two-sided Fisher tests: every memory arm against
`off`, and each Muninn arm against each competitor arm (Holm-adjusted within each Muninn arm's family).
Usage: analyze_h2h.py <out-dir> [--muninn-arms muninn,muninn-fixed,muninn-loop3]
"""
import argparse, json, os
from math import comb


def fisher_two_sided(a, n1, b, n2):
    K, N = a + b, n1 + n2
    def p(x):
        return comb(K, x) * comb(N - K, n1 - x) / comb(N, n1)
    p0 = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, K - n2), min(K, n1) + 1) if p(x) <= p0 * (1 + 1e-9)))


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    out, running = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        out[i] = running
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--muninn-arms", default="muninn,muninn-fixed,muninn-loop3")
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(a.out, "config.json")))
    sc = {t["id"]: t["scenario"] for t in cfg["tasks"]}
    rows = [json.loads(l) for l in open(os.path.join(a.out, "results.jsonl"))]
    for r in rows:
        p = os.path.join(a.out, "diffs", f"r{r['run']}-{r['task']}-{r['arm']}.patch")
        added = ""
        if os.path.exists(p):
            added = "\n".join(l[1:] for l in open(p, errors="replace").read().splitlines()
                              if l.startswith("+") and not l.startswith("+++")).lower()
        s = sc[r["task"]]
        r["replacement"] = s["new"] is not None
        r["unsafe"] = int(s["old"].lower() in added)
        r["current"] = int(bool(s["new"]) and s["new"].lower().split(" with ")[0] in added)
    arms = sorted({r["arm"] for r in rows}, key=lambda x: (x != "off", x))
    ok = [r for r in rows if r["status"] != "error"]
    print("| arm | replacement pass | unsafe | current value written | revocation pass | errors |")
    print("|---|---|---|---|---|---|")
    tally = {}
    for arm in arms:
        rep = [r for r in ok if r["arm"] == arm and r["replacement"]]
        rev = [r for r in ok if r["arm"] == arm and not r["replacement"]]
        err = sum(1 for r in rows if r["arm"] == arm and r["status"] == "error")
        tally[arm] = (sum(r["status"] == "pass" for r in rep), len(rep))
        print(f"| {arm} | {tally[arm][0]}/{len(rep)} | {sum(r['unsafe'] for r in rep)}/{len(rep)} | "
              f"{sum(r['current'] for r in rep)}/{len(rep)} | {sum(r['status'] == 'pass' for r in rev)}/{len(rev)} | {err} |")
    print("\nEvery arm against off (replacement pass, Fisher two-sided):")
    for arm in arms:
        if arm == "off" or "off" not in tally:
            continue
        print(f"  {arm}: p = {fisher_two_sided(*tally[arm], *tally['off']):.3g}")
    competitors = [x for x in arms if x != "off" and x not in a.muninn_arms.split(",")]
    for m in a.muninn_arms.split(","):
        if m not in tally or not competitors:
            continue
        ps = [fisher_two_sided(*tally[m], *tally[c]) for c in competitors]
        print(f"\n{m} against each competitor (Holm within this family):")
        for c, p, h in zip(competitors, ps, holm(ps)):
            d = tally[m][0] / max(1, tally[m][1]) - tally[c][0] / max(1, tally[c][1])
            print(f"  vs {c}: {tally[m][0]}/{tally[m][1]} vs {tally[c][0]}/{tally[c][1]}  Δ {d:+.3f}  p = {p:.3g}  Holm = {h:.3g}")


if __name__ == "__main__":
    main()
