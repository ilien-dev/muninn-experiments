#!/usr/bin/env python3
"""Score judge-v2 by the rule registered in PREREGISTRATION.md.

Per call the model's pick is the most probable letter. It retires the picked record when the
pick is not "none" and its probability is at least theta, fitted on dev only: the smallest value
on the 0.01 grid at which no dev call retires a record it should not.

Against A0 (the rules, adjacent order, from judge-v1 and judge-v1b's rows), per language on test:
  rescued      calls whose target A0 did not retire and the model did
  added_false  calls where the model retires a record that is not the target and A0 did not retire
  combined     calls whose target is retired by A0 or by the model
and, beside them, A0 in the separated order, which is the order the candidates are listed in.

Usage: choice_score.py [--arms B1,B3]
"""
import argparse, json, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parent / "results"
sys.path.insert(0, str(HERE))
import choice  # noqa: E402
import sets  # noqa: E402

GRID = [round(x / 100, 2) for x in range(0, 102)]
LANGS = ["en", "es", "pt", "fr", "ja", "de"]


def a0_retired(order):
    """call id -> set of candidate indices the rules retired."""
    items = {x["id"]: x for x in sets.items() + sets.probe_items()}
    rows = [json.loads(l) for l in open(R / f"judge-v1/{'A0' if order == 'adjacent' else 'A0-separated'}.jsonl")]
    if order == "adjacent":
        rows += [json.loads(l) for l in open(R / "judge-v1b/A0.jsonl")]
    cand = {c["id"]: c["cands"] for c in choice.calls()}
    out = defaultdict(set)
    for r in rows:
        it = items[r["id"]]
        cid = r["id"].split("|", 1)[1] if it["kind"] != "neg_shared" else r["id"]
        if r["p"] == 1.0 and cid in cand:
            out[cid].add(cand[cid].index(it["a"]))
    return out


def decide(row, theta):
    p = row["p"]
    k = max(range(len(p)), key=lambda i: p[i])
    return (k - 1) if k > 0 and p[k] >= theta else None  # candidate index, or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default="B1,B3")
    ap.add_argument("--dir", default=str(R / "judge-v2"))
    a = ap.parse_args()
    d = Path(a.dir)
    a0 = a0_retired("adjacent")
    a0s = a0_retired("separated")
    report = []
    for arm in a.arms.split(","):
        rows = [json.loads(l) for l in open(d / f"{arm}.jsonl")]
        dev = [r for r in rows if r["split"] == "dev"]
        theta = next((g for g in GRID if all(decide(r, g) in (None, r["target"]) for r in dev)), None)
        res = {"arm": arm, "theta": theta, "langs": {}, "probes": {}}
        for key in ("lang", "probe"):
            acc = defaultdict(lambda: defaultdict(int))
            for r in rows:
                if r["split"] != "test" or (key == "probe" and not r["probe"]):
                    continue
                s = acc[r[key]]
                pick = decide(r, theta) if theta is not None else None
                rule = a0.get(r["id"], set())
                t = r["target"]
                s["calls"] += 1
                if t is not None:
                    s["targets"] += 1
                    s["a0_hit"] += t in rule
                    s["a0_sep_hit"] += t in a0s.get(r["id"], set())
                    s["rescued"] += (t not in rule) and pick == t
                    s["combined"] += (t in rule) or pick == t
                    s["model_hit"] += pick == t
                s["a0_false"] += len(rule - {t})
                s["added_false"] += pick is not None and pick != t and pick not in rule
                s["model_false"] += pick is not None and pick != t
            res["langs" if key == "lang" else "probes"] = {k: dict(v) for k, v in acc.items()}
        meta = json.load(open(d / f"{arm}.meta.json"))
        full = sorted(x["ms"] for x in meta["full_prompt"])
        res["ms_full_p50"] = full[len(full) // 2]
        res["ms_full_p95"] = full[min(len(full) - 1, int(0.95 * len(full)))]
        rr = d / f"{arm}-rerun.jsonl"
        if rr.exists():
            main_p = {r["id"]: r["p"] for r in rows}
            re = [json.loads(l) for l in open(rr)]
            res["rerun_same"] = f"{sum(main_p[r['id']] == r['p'] for r in re)}/{len(re)}"
        rv = d / f"{arm}-reverse.jsonl"
        if rv.exists():
            main_pick = {r["id"]: decide(r, theta) for r in rows}
            rv_rows = [json.loads(l) for l in open(rv)]
            res["reverse_same_decision"] = f"{sum(main_pick[r['id']] == decide(r, theta) for r in rv_rows)}/{len(rv_rows)}"
        report.append(res)
        print(f"\n{arm}  theta={theta}  full p50/p95 {res['ms_full_p50']:.0f}/{res['ms_full_p95']:.0f} ms  "
              f"rerun {res.get('rerun_same')}  reversed order same decision {res.get('reverse_same_decision')}")
        for lang in LANGS:
            s = res["langs"].get(lang)
            if s:
                print(f"  {lang}: model {s.get('model_hit', 0)}/{s.get('targets', 0)}  "
                      f"rescued {s.get('rescued', 0)}/{s.get('targets', 0) - s.get('a0_hit', 0)}  "
                      f"added_false {s.get('added_false', 0)}  model_false {s.get('model_false', 0)}/{s['calls']}  "
                      f"combined {s.get('combined', 0)}/{s.get('targets', 0)}  "
                      f"A0 adj {s.get('a0_hit', 0)} (false {s.get('a0_false', 0)})  A0 sep {s.get('a0_sep_hit', 0)}")
        for pr, s in sorted(res["probes"].items()):
            print(f"  probe {pr:28} model {s.get('model_hit', 0)}/{s.get('targets', 0)}  model_false {s.get('model_false', 0)}/{s['calls']}")
    json.dump(report, open(d / "score.json", "w"), indent=1)


if __name__ == "__main__":
    main()
