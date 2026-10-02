#!/usr/bin/env python3
"""Score judge-v3 by the rule registered in PREREGISTRATION.md.

A call retires its picked record when the pick is not "none", the pick's probability is >= tc
and the confirm step's P(yes) is >= tp. Both thresholds are fitted on dev only, on the 0.01 grid:
  retire tier  the pair with the most dev hits among those with 0 dev false retirements
               (ties: the larger tc + tp)
  ask tier     the pair with the most dev hits among those with dev precision >= 0.9: what the
               model would mark `conflict` for the agent to ask about, instead of retiring
On the fresh test groups, per language, against A0 (fresh set, adjacent order):
  rescued      targets A0 left active that the tier retires (or flags)
  added_false  records the tier retires (or flags) that are not the target and A0 left active
Usage: v3_score.py [--arms C1,C2,C1n]
"""
import argparse, json
from collections import defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "results/judge-v3"
GRID = [x / 100 for x in range(0, 101)]


def fit(dev, precision=None):
    best = None
    pts = [(r["p"][r["pick"] + 1], r["confirm"], r["pick"] == r["target"]) for r in dev if r["pick"] is not None]
    for tc in GRID:
        for tp in GRID:
            hits = sum(1 for pc, pp, ok in pts if pc >= tc and pp >= tp and ok)
            flags = sum(1 for pc, pp, ok in pts if pc >= tc and pp >= tp)
            false = flags - hits
            if precision is None and false:
                continue
            if precision is not None and flags and hits / flags < precision:
                continue
            key = (hits, tc + tp)
            if best is None or key > best[0]:
                best = (key, tc, tp)
    return best[1], best[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default="C1,C2,C1n")
    a = ap.parse_args()
    a0 = {r["id"]: r for r in map(json.loads, open(D / "A0.jsonl"))}
    report = []
    for arm in a.arms.split(","):
        f = D / f"{arm}.jsonl"
        if not f.exists():
            continue
        rows = [json.loads(l) for l in open(f)]
        dev = [r for r in rows if r["split"] == "dev"]
        test = [r for r in rows if r["split"] == "test"]
        res = {"arm": arm, "tiers": {}}
        for tier, prec in (("retire", None), ("ask", 0.9)):
            tc, tp = fit(dev, prec)
            by = defaultdict(lambda: defaultdict(int))
            for r in test:
                s = by[r["lang"]]
                rule = set(a0[r["id"]]["retired"])
                t = r["target"]
                acted = r["pick"] is not None and r["p"][r["pick"] + 1] >= tc and r["confirm"] >= tp
                s["calls"] += 1
                if t is not None:
                    s["targets"] += 1
                    s["a0_hit"] += t in rule
                    s["rescued"] += t not in rule and acted and r["pick"] == t
                s["a0_false"] += len(rule - {t})
                s["acted"] += acted
                s["acted_ok"] += acted and r["pick"] == t
                s["added_false"] += acted and r["pick"] != t and r["pick"] not in rule
            res["tiers"][tier] = {"tc": tc, "tp": tp, "langs": {k: dict(v) for k, v in by.items()}}
        full = D / f"{arm}-full.jsonl"
        if full.exists():
            ms = sorted(json.loads(l)["ms_total"] for l in open(full))
            res["ms_p50"], res["ms_p95"] = ms[len(ms) // 2], ms[min(len(ms) - 1, int(0.95 * len(ms)))]
        rr = D / f"{arm}-rerun.jsonl"
        if rr.exists():
            main_rows = {r["id"]: (r["p"], r["confirm"]) for r in rows}
            re = [json.loads(l) for l in open(rr)]
            res["rerun_same"] = f"{sum(main_rows[r['id']] == (r['p'], r['confirm']) for r in re)}/{len(re)}"
        report.append(res)
        print(f"\n{arm}  full-prompt pick+confirm p50/p95 {res.get('ms_p50')}/{res.get('ms_p95')} ms  rerun {res.get('rerun_same')}")
        for tier, t in res["tiers"].items():
            print(f"  {tier}: tc={t['tc']} tp={t['tp']}")
            for lang in ["en", "es", "fr", "de"]:
                s = t["langs"].get(lang)
                if s:
                    print(f"    {lang}: rescued {s.get('rescued', 0)}/{s.get('targets', 0) - s.get('a0_hit', 0)}  "
                          f"added_false {s.get('added_false', 0)}  acted {s.get('acted', 0)} (correct {s.get('acted_ok', 0)})  "
                          f"A0 {s.get('a0_hit', 0)}/{s.get('targets', 0)} false {s.get('a0_false', 0)}")
    json.dump(report, open(D / "score.json", "w"), indent=1)


if __name__ == "__main__":
    main()
