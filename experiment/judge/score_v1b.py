#!/usr/bin/env python3
"""judge-v1b: every arm on the 60 probe pairs, under the thresholds it fitted on judge-v1's dev
split (results/judge-v1/score.json), with no refit. Per language and per probe."""
import json, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent / "results/judge-v1b"
sys.path.insert(0, str(HERE))
import sets  # noqa: E402

probe = {x["id"]: x for x in sets.probe_items()}
theta = {r["arm"]: r for r in json.load(open(HERE.parent / "results/judge-v1/score.json"))}
a0 = {r["id"]: r for r in map(json.loads, open(D / "A0.jsonl"))}
print("A0 retires:", sorted(k.split("|")[0] for k, r in a0.items() if r["p"] == 1.0))
for arm in ["A1", "A2", "A3", "A4", "A5"]:
    rows = {r["id"]: r for r in map(json.loads, open(D / f"{arm}.jsonl"))}
    hi, lo = theta[arm]["theta_hi"], theta[arm]["theta_lo"]
    by = defaultdict(lambda: defaultdict(int))
    wrong = []
    for i, r in rows.items():
        rule, model = a0[i]["p"] == 1.0, r["p"] >= hi
        for k in (r["lang"], "probe:" + probe[i]["probe"]):
            s = by[k]
            if r["label"]:
                s["pos"] += 1; s["a0_miss"] += not rule; s["rescued"] += (not rule) and model
            else:
                s["neg"] += 1; s["a0_false"] += rule; s["added_false"] += (not rule) and model
        if (r["label"] == 0 and model and not rule) or (r["label"] and not rule and not model):
            wrong.append((i.split("|")[0], r["label"], r["p_raw"]))
    print(f"\n{arm} theta_hi={hi} theta_lo={lo}")
    for k, s in sorted(by.items()):
        print(f"  {k:32} rescued {s['rescued']}/{s['a0_miss']}  added_false {s['added_false']}/{s['neg'] - s['a0_false']}")
    # threshold-free: how each probe's pairs rank, to read what the model understood
    pos = sorted(r["p_raw"] for r in rows.values() if r["label"])
    neg = sorted(r["p_raw"] for r in rows.values() if not r["label"])
    auc = sum((sum(n < p for n in neg) + 0.5 * sum(n == p for n in neg)) for p in pos) / (len(pos) * len(neg))
    print(f"  auc {auc:.3f}")
    print("  p per pair:", " ".join(f"{k}{'+' if l else '-'}{p:.2f}" for k, l, p in
                                    sorted((i.split('|')[0], r['label'], r['p_raw']) for i, r in rows.items())))
