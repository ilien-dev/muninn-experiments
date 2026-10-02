#!/usr/bin/env python3
"""Score the judge tournament by the rule registered in PREREGISTRATION.md ("judge-v1").

Thresholds are fitted on the dev split only, on the 0.01 grid the rows are rounded to:
  theta_hi  the smallest grid value above every dev negative: the model retires alone at p >= theta_hi
  theta_lo  the largest grid value at or below every dev positive A0 retired: a rule retirement
            with p < theta_lo is vetoed
Then, on the test split, per language:
  added_false   negatives the model retires that A0 did not             (gate: 0 everywhere)
  vetoed_false  A0's false retirements the veto removes
  vetoed_true   A0's true retirements the veto removes                   (a cost)
  rescued       positives A0 missed that the model retires, of how many A0 missed
  combined      recall of A0-or-model
  auc           threshold-free separation of positives from negatives
and latency: the full-prompt p50/p95 (no cached prefix), which is what `maintain` would pay.

Usage: score.py [--dir results/judge-v1] [--arms A1,A2,...]
"""
import argparse, json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRID = [round(x / 100, 2) for x in range(0, 102)]
LANGS = ["en", "es", "pt", "fr", "ja"]


def load(path):
    return {r["id"]: r for r in map(json.loads, open(path))}


def auc(pos, neg):
    if not pos or not neg:
        return None
    wins = 0.0
    neg_sorted = sorted(neg)
    import bisect
    for p in pos:
        lo = bisect.bisect_left(neg_sorted, p)
        hi = bisect.bisect_right(neg_sorted, p)
        wins += lo + 0.5 * (hi - lo)
    return wins / (len(pos) * len(neg))


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else None


def score_arm(arm, rows, a0):
    dev = [r for r in rows.values() if r["split"] == "dev"]
    dev_neg = [r["p"] for r in dev if r["label"] == 0]
    theta_hi = next((g for g in GRID if g > max(dev_neg)), None)
    dev_pos_ruled = [r["p"] for r in dev if r["label"] == 1 and a0[r["id"]]["p"] == 1.0]
    theta_lo = max((g for g in GRID if g <= min(dev_pos_ruled)), default=0.0) if dev_pos_ruled else 0.0
    out = {"arm": arm, "theta_hi": theta_hi, "theta_lo": theta_lo, "langs": {}}
    for lang in LANGS:
        t = [r for r in rows.values() if r["split"] == "test" and r["lang"] == lang]
        if not t:
            continue
        s = defaultdict(int)
        pos, neg = [], []
        for r in t:
            rule = a0[r["id"]]["p"] == 1.0
            model = theta_hi is not None and r["p"] >= theta_hi
            veto = rule and r["p"] < theta_lo
            (pos if r["label"] else neg).append(r["p_raw"])
            if r["label"]:
                s["positives"] += 1
                s["a0_hit"] += rule
                s["a0_miss"] += not rule
                s["rescued"] += (not rule) and model
                s["vetoed_true"] += veto
                s["combined"] += rule or model
            else:
                s["negatives"] += 1
                s["a0_false"] += rule
                s["added_false"] += (not rule) and model
                s["vetoed_false"] += veto
        s["auc"] = auc(pos, neg)
        out["langs"][lang] = dict(s)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(HERE.parent / "results/judge-v1"))
    ap.add_argument("--arms", default="A1,A2,A3,A4,A5")
    a = ap.parse_args()
    d = Path(a.dir)
    a0 = load(d / "A0.jsonl")
    report = []
    for arm in a.arms.split(","):
        f = d / f"{arm}.jsonl"
        if not f.exists():
            continue
        rows = load(f)
        res = score_arm(arm, rows, a0)
        meta = json.load(open(d / f"{arm}.meta.json"))
        full = [x["ms"] for x in meta.get("full_prompt", [])] or [r["ms"] for r in rows.values()]
        res["ms_full_p50"], res["ms_full_p95"] = pct(full, 0.5), pct(full, 0.95)
        res["ms_cached_p50"] = pct([r["ms"] for r in rows.values()], 0.5)
        res["same_p_full_vs_cached"] = (sum(x["same_p"] for x in meta["full_prompt"]) / len(meta["full_prompt"])
                                        if meta.get("full_prompt") else None)
        report.append(res)
    base = {lang: {} for lang in LANGS}
    for r in a0.values():
        if r["split"] != "test":
            continue
        b = base[r["lang"]]
        k = "pos" if r["label"] else "neg"
        b[k] = b.get(k, 0) + 1
        b[k + "_retired"] = b.get(k + "_retired", 0) + (r["p"] == 1.0)
    print("A0 test:", json.dumps(base))
    for res in report:
        print(f"\n{res['arm']}  theta_hi={res['theta_hi']}  theta_lo={res['theta_lo']}  "
              f"full p50/p95 {res['ms_full_p50']:.0f}/{res['ms_full_p95']:.0f} ms  "
              f"cached p50 {res['ms_cached_p50']:.0f} ms  same_p {res['same_p_full_vs_cached']}")
        for lang, s in res["langs"].items():
            print(f"  {lang}: rescued {s.get('rescued', 0)}/{s.get('a0_miss', 0)}  "
                  f"added_false {s.get('added_false', 0)}/{s.get('negatives', 0)}  "
                  f"combined {s.get('combined', 0)}/{s.get('positives', 0)}  "
                  f"veto false {s.get('vetoed_false', 0)}/{s.get('a0_false', 0)} "
                  f"true {s.get('vetoed_true', 0)}/{s.get('a0_hit', 0)}  "
                  f"auc {s['auc']:.3f}" if s["auc"] is not None else "")
    json.dump(report, open(d / "score.json", "w"), indent=1)


if __name__ == "__main__":
    main()
