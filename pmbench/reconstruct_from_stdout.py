#!/usr/bin/env python3
"""Rebuild a PM-Bench action log from a runner's console output.

Round 4 launched the three baseline runs of each arm in the same second, and PM-Bench's runner
names the log by that second, so the three trajectories of an arm overwrote one file. The
console output of each run (one file per run) prints every action:

    === Monday ===
    Model action: query_state clock
    Model action: choose B + action(s) asthma_1100

This script turns that back into the JSONL the scorer reads (day, step_id, choice, task_ids,
check_time, state_queries) using the scenario's step order, then scores it. Validation: on the
run whose original log survived, the rebuilt entries are identical (`--check <jsonl>`).

Usage: reconstruct_from_stdout.py --scenario week.json --stdout run.log --out run.jsonl [--check orig.jsonl]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DAY_RE = re.compile(r"^=== (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) ===$")
QUERY_RE = re.compile(r"^Model action: query_state (\S+)$")
CHOOSE_RE = re.compile(r"^Model action: choose ([ABC])(?: \+ (?:action|task)\(s\) (.*))?$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--stdout", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", default="reconstructed-from-stdout")
    ap.add_argument("--check", default=None)
    a = ap.parse_args()
    scenario = json.load(open(a.scenario, encoding="utf-8"))
    steps_by_day = {d["name"]: [s["id"] for s in d["steps"]] for d in scenario["days"]}

    entries = []
    day = None
    step_idx = 0
    queries = {}
    for raw in open(a.stdout, encoding="utf-8", errors="replace"):
        line = raw.rstrip("\n")
        m = DAY_RE.match(line)
        if m:
            day = m.group(1)
            step_idx = 0
            queries = {}
            continue
        m = QUERY_RE.match(line)
        if m and day:
            queries[m.group(1)] = queries.get(m.group(1), 0) + 1
            continue
        m = CHOOSE_RE.match(line)
        if m and day:
            ids = [t.strip() for t in (m.group(2) or "").split(",") if t.strip()]
            entries.append({
                "day": day,
                "step_id": steps_by_day[day][step_idx],
                "choice": m.group(1),
                "task_ids": ids,
                "check_time": queries.get("clock", 0),
                "state_queries": dict(queries),
            })
            step_idx += 1
            queries = {}
    total = sum(len(v) for v in steps_by_day.values())
    if len(entries) != total:
        sys.exit(f"reconstructed {len(entries)} steps, scenario has {total}")

    if a.check:
        orig = [json.loads(l) for l in open(a.check, encoding="utf-8")]
        orig = [o for o in orig if "step_id" in o]
        keys = ("day", "step_id", "choice", "task_ids", "check_time", "state_queries")
        diffs = [(o["step_id"], {k: (o.get(k), e.get(k)) for k in keys if o.get(k) != e.get(k)}) for o, e in zip(orig, entries) if any(o.get(k) != e.get(k) for k in keys)]
        print(f"check against {Path(a.check).name}: {len(orig)} entries, {len(diffs)} differing steps")
        for d in diffs[:10]:
            print("  ", d)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"record_type": "run_metadata", "mode": a.mode, "source_stdout": Path(a.stdout).name, "entry_count": len(entries)}) + "\n")
        for e in entries:
            fh.write(json.dumps(e) + "\n")
    print(f"wrote {a.out}")
    pm = Path(a.scenario).resolve().parents[1] / "sim" / "pm_bench.py"
    subprocess.run([sys.executable, str(pm), "score", "--scenario", a.scenario, "--log", a.out], stdout=subprocess.DEVNULL, check=True)


if __name__ == "__main__":
    main()
