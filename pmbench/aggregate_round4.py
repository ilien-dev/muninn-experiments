#!/usr/bin/env python3
"""Aggregate PM-Bench score reports (`*.score.md`) per arm: per-run set-F1 and the secondary
metrics pre-registered for round 4. Usage: aggregate_round4.py <out dir> [<out dir> ...]"""
import glob
import json
import os
import re
import statistics
import sys


def parse_rates(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^Rates: (.*)$", text, flags=re.M)
    rates = {}
    if m:
        for part in m.group(1).split("|"):
            k, _, v = part.strip().rpartition(" ")
            rates[k.strip()] = v.strip()
    mod = re.search(r"^Hit rates \(by modality\): (.*)$", text, flags=re.M)
    if mod:
        for part in mod.group(1).split("|"):
            k, _, v = part.strip().rpartition(" ")
            rates["mod_" + k.strip()] = v.strip()
    mon = re.search(r"proactive_monitoring_required \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| ([0-9.]+%)", text)
    if mon:
        rates["monitoring_hit"] = mon.group(5)
    sq = re.search(r"state query calls: (\d+)", text)
    if sq:
        rates["state_queries"] = sq.group(1)
    return rates


def pct(v):
    return float(v.rstrip("%"))


def main():
    rows = {}
    for out in sys.argv[1:]:
        for arm in sorted(os.listdir(out)):
            d = os.path.join(out, arm)
            if not os.path.isdir(d):
                continue
            for score in sorted(glob.glob(os.path.join(d, "**", "*.score.md"), recursive=True)):
                r = parse_rates(score)
                meta = {}
                log = score.replace(".score.md", ".jsonl")
                if os.path.exists(log):
                    try:
                        meta = json.loads(open(log, encoding="utf-8").readline())
                    except Exception:  # noqa: BLE001
                        meta = {}
                r["_dur_min"] = round(float(meta.get("duration_seconds", 0)) / 60, 1)
                r["_guards"] = meta.get("guard_events")
                r["_est_tokens"] = meta.get("est_input_tokens")
                rows.setdefault(arm, []).append((os.path.basename(score), r))
    keys = ["set_f1", "set_precision", "set_recall", "cross-day miss", "update miss", "mod_time", "mod_event", "monitoring_hit", "false alarm/step", "state_queries"]
    for arm, runs in rows.items():
        print(f"\n## {arm} ({len(runs)} runs)")
        print("| run | " + " | ".join(keys) + " | min | guards | est tok |")
        print("|---|" + "---|" * (len(keys) + 3))
        for name, r in runs:
            print(f"| {name[:38]} | " + " | ".join(str(r.get(k, "")) for k in keys) + f" | {r['_dur_min']} | {r['_guards']} | {r['_est_tokens']} |")
        f1 = [pct(r["set_f1"]) for _, r in runs if "set_f1" in r]
        if f1:
            print(f"mean set-F1 {statistics.mean(f1):.1f} %" + (f" (sd {statistics.stdev(f1):.1f})" if len(f1) > 1 else "") + f" · per run {' · '.join(f'{x:.1f}' for x in f1)}")
            for k in ("cross-day miss", "update miss", "mod_time", "monitoring_hit"):
                vals = [pct(r[k]) for _, r in runs if k in r]
                if vals:
                    print(f"mean {k} {statistics.mean(vals):.1f} %")


if __name__ == "__main__":
    main()
