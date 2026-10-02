#!/usr/bin/env python3
"""v42 step 1: the judge's pairs in each seeded store, read against the fixture's phrasings.
true = decision k paired with change k; false = any other pair (including a record whose text
matches no phrasing, printed as None). Usage: judged_pairs.py <fixture> <work dir>"""
import json, sqlite3, sys
fx, work = sys.argv[1], sys.argv[2]
ph = json.load(open(f"h2h/{fx}/seed_phrasings.json"))
def which(body, side):
    for k, p in enumerate(ph):
        if p[side][:40].lower() in body.lower():
            return k
    return None
def label(body, first, other):
    k = which(body, first)
    return f"{first}{k}" if k is not None else f"{other}{which(body, other)}"
out, tt, tf = [], 0, 0
for r in range(6):
    c = sqlite3.connect(f"{work}/snap-r{r}-muninn-judge/.muninn/muninn.db")
    rows = c.execute("SELECT o.body, n.body FROM judged_conflict j JOIN record o ON o.id = j.old_id "
                     "JOIN record n ON n.id = j.new_id").fetchall()
    pairs = sorted({(label(o, "a", "b"), label(n, "b", "a")) for o, n in rows})
    t = sum(1 for o, n in pairs if o[0] == "a" and n[0] == "b" and o[1:] == n[1:] and o[1:] != "None")
    retired = c.execute("SELECT COUNT(*) FROM record WHERE invalid = 1").fetchone()[0]
    out.append({"run": r, "pairs": pairs, "true": t, "false": len(pairs) - t, "rules_retired_records": retired})
    tt += t; tf += len(pairs) - t
print(json.dumps({"fixture": fx, "runs": out, "avg_true": tt / 6, "total_true": tt, "total_false": tf,
                  "cells_run": tt / 6 >= 3 and tf < tt}, indent=1))
