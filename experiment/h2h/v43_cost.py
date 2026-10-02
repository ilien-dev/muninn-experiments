#!/usr/bin/env python3
"""v43, exploratory and post hoc: what each task cost each arm, from the cells' own records.

Not registered before the run and not a claim. Every non-error cell of v43's five grids, both
arms: `cost_usd`, `num_turns` and `duration_ms` as the agent's own result reports them. The
competitor's background observer model is not in these figures.
Usage: v43_cost.py > ../results/h2h-v43-cost.json
"""
import json, statistics as st
from pathlib import Path

R = Path(__file__).resolve().parent.parent / "results"
out = {}
for fx in ["v3", "v4", "v5", "v6", "v7"]:
    for line in open(R / f"h2h-v43-{fx}" / "results.jsonl"):
        r = json.loads(line)
        if r["status"] == "error" or r.get("cost_usd") is None:
            continue
        a = out.setdefault(r["arm"], {"cost": [], "turns": [], "ms": []})
        a["cost"].append(r["cost_usd"]); a["turns"].append(r.get("num_turns") or 0); a["ms"].append(r.get("duration_ms") or 0)
print(json.dumps({arm: {"cells": len(a["cost"]), "total_cost_usd": round(sum(a["cost"]), 2),
                        "mean_cost_usd": round(st.mean(a["cost"]), 3), "mean_turns": round(st.mean(a["turns"]), 1),
                        "mean_seconds": round(st.mean(a["ms"]) / 1000, 1)} for arm, a in out.items()}, indent=1))
