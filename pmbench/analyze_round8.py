#!/usr/bin/env python3
"""Analyse PM-Bench round 8 results (held-out weeks, store ablation, second model family).

Input: one or more result roots written by run_round8.py, each optionally tagged ``label=path``
(the label defaults to the directory name; one root per model). Layout
``<root>/<week>/<arm>/**/*.score.md``. The week named ``v9`` is the development week: it is
reported but excluded from every pooled statistic and from the decision rules.

Statistics (set-F1 in percentage points, read from each run's ``Rates:`` line exactly as
aggregate_round4.py does):
  * per (model, week, arm): the per-run values in directory order, mean, sample sd (n-1), min,
    max, n; and the mean of the secondary metrics (set precision, set recall, cross-day miss,
    update miss, time-modality hit, proactive-monitoring hit, false alarms per step).
  * per (model, week) contrasts A-B for the pre-registered pairs muninn_store-single_baseline,
    muninn_store-todo_ledger, muninn_store-plain_store, plain_store-single_baseline: the
    difference of means and the worst-case gap min(A runs) - max(B runs) (positive means every
    A run beat every B run).
  * pooled over the held-out weeks, per contrast:
      - point estimate: mean over weeks of the per-week difference of means;
      - exact stratified permutation test: within each week every C(nA+nB, nA) relabeling of
        that week's runs, weeks combined as a cartesian product; statistic = mean over weeks of
        the difference of means; one-sided p = share of relabelings whose statistic is >= the
        observed one (A > B), two-sided p = share whose |statistic| >= |observed|. The observed
        labeling is one of the relabelings, so the smallest attainable one-sided p is 1/N and N
        is printed. Above 2e6 relabelings the test switches to 200000 Monte-Carlo relabelings
        (seed 20260913, p = (count+1)/(reps+1)) and the output says so;
      - cluster bootstrap by week: 10000 resamples, seed 20260913, weeks drawn with
        replacement, runs drawn with replacement within each drawn week; 95 % percentile
        interval of the same statistic. With three clusters the interval is coarse; the
        permutation test is the primary inference;
      - sign pattern: the number of held-out weeks whose worst-case gap is positive.
  * decision rules, evaluated from the CLI and printed MET / NOT MET:
      --line L           mean set-F1 of muninn_store over all held-out runs >= L;
      --spread-rule      on EVERY held-out week muninn_store's mean exceeds single_baseline's
                         and todo_ledger's by more than the largest within-arm range (max-min)
                         observed among the arms on that week;
      --ablation-band B  |pooled muninn_store - plain_store| <= B and no held-out week whose
                         worst-case gap exceeds B in either direction -> "store implementation
                         not distinguishable".
Output: Markdown on stdout; every number also in ``--json <file>``.
"""
import argparse
import glob
import itertools
import json
import math
import os
import random
import re
import statistics
import sys
from statistics import fmean

ARMS = ["muninn_store", "plain_store", "single_baseline", "todo_ledger"]
BASELINES = ["single_baseline", "todo_ledger"]
CONTRASTS = [("muninn_store", "single_baseline"), ("muninn_store", "todo_ledger"),
             ("muninn_store", "plain_store"), ("plain_store", "single_baseline")]
SECONDARY = [("set_precision", "set P"), ("set_recall", "set R"), ("cross-day miss", "x-day miss"),
             ("update miss", "update miss"), ("mod_time", "time hit"), ("monitoring_hit", "proactive hit"),
             ("false alarm/step", "FA/step")]
EXACT_CAP, MC_REPS, BOOT_REPS, SEED, EPS = 2_000_000, 200_000, 10_000, 20260913, 1e-9


def parse_rates(path):
    """Same regexes as aggregate_round4.py."""
    text = open(path, encoding="utf-8").read()
    rates = {}
    m = re.search(r"^Rates: (.*)$", text, flags=re.M)
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
    return rates


def pct(v):
    return float(v.rstrip("%"))


def load(root):
    """{week: {arm: [(run file name, rates)]}} in directory order; runs without a set_f1 are skipped."""
    data = {}
    for week in sorted(os.listdir(root)):
        wdir = os.path.join(root, week)
        if not os.path.isdir(wdir) or week == "weeks":
            continue
        for arm in sorted(os.listdir(wdir)):
            adir = os.path.join(wdir, arm)
            if not os.path.isdir(adir):
                continue
            for s in sorted(p for p in glob.glob(os.path.join(adir, "**", "*.score.md"), recursive=True) if "excess-runs" not in p):  # runs beyond the pre-registered count are never used
                r = parse_rates(s)
                if "set_f1" in r:
                    data.setdefault(week, {}).setdefault(arm, []).append((os.path.basename(s), r))
    return data


def summary(xs):
    return {"runs": xs, "n": len(xs), "mean": fmean(xs) if xs else None,
            "sd": statistics.stdev(xs) if len(xs) > 1 else None,
            "min": min(xs) if xs else None, "max": max(xs) if xs else None}


def contrast(a, b):
    return {"diff_means": fmean(a) - fmean(b), "worst_gap": min(a) - max(b)} if a and b else None


def week_diffs(a, b):
    """mean(A) - mean(B) for every C(n, nA) relabeling of one week's runs; the observed one comes first."""
    pool, n, na = a + b, len(a) + len(b), len(a)
    out = []
    for idx in itertools.combinations(range(n), na):
        chosen = set(idx)
        out.append(fmean(pool[i] for i in idx) - fmean(pool[i] for i in range(n) if i not in chosen))
    return out


def permutation(pairs):
    per = [week_diffs(a, b) for a, b in pairs]
    k = len(per)
    obs = fmean(d[0] for d in per)
    total = math.prod(len(d) for d in per)
    exact = total <= EXACT_CAP
    if exact:
        stats, n = (sum(c) / k for c in itertools.product(*per)), total
    else:
        rng = random.Random(SEED)
        stats, n = (sum(rng.choice(d) for d in per) / k for _ in range(MC_REPS)), MC_REPS
    ge = ge2 = 0
    for t in stats:
        ge += t >= obs - EPS
        ge2 += abs(t) >= abs(obs) - EPS
    if not exact:
        ge, ge2, n = ge + 1, ge2 + 1, n + 1
    return {"observed": obs, "p_one_sided": ge / n, "p_two_sided": ge2 / n, "count_one_sided": ge,
            "count_two_sided": ge2, "relabelings": n, "exact": exact}


def bootstrap(pairs):
    rng, k, out = random.Random(SEED), len(pairs), []
    for _ in range(BOOT_REPS):
        acc = 0.0
        for _ in range(k):
            a, b = pairs[rng.randrange(k)]
            acc += fmean(rng.choices(a, k=len(a))) - fmean(rng.choices(b, k=len(b)))
        out.append(acc / k)
    out.sort()
    return [out[math.floor(0.025 * (BOOT_REPS - 1))], out[math.ceil(0.975 * (BOOT_REPS - 1))]]


def analyse(data, args):
    weeks = list(data)
    held = [w for w in weeks if w != "v9"]
    f1 = {w: {arm: [pct(r["set_f1"]) for _, r in runs] for arm, runs in data[w].items()} for w in weeks}
    res = {"weeks": weeks, "heldout_weeks": held, "cells": {}, "contrasts": {}, "pooled": {}, "rules": {}}
    for w in weeks:
        for arm, runs in data[w].items():
            c = summary(f1[w][arm])
            c["run_files"] = [name for name, _ in runs]
            c["secondary"] = {k: fmean(pct(r[k]) for _, r in runs if k in r) for k, _ in SECONDARY
                              if any(k in r for _, r in runs)}
            res["cells"][f"{w}/{arm}"] = c
        for a, b in CONTRASTS:
            c = contrast(f1[w].get(a), f1[w].get(b))
            if c:
                res["contrasts"][f"{w}/{a}-{b}"] = c
    for a, b in CONTRASTS:
        pairs = [(f1[w][a], f1[w][b]) for w in held if f1[w].get(a) and f1[w].get(b)]
        if pairs:
            p = permutation(pairs)
            p.update(weeks=len(pairs), ci95=bootstrap(pairs), weeks_all_a_above_b=sum(min(x) - max(y) > 0 for x, y in pairs))
            res["pooled"][f"{a}-{b}"] = p
    ms = [x for w in held for x in f1[w].get("muninn_store", [])]
    res["rules"]["line"] = {"line": args.line, "mean": fmean(ms) if ms else None, "met": bool(ms) and fmean(ms) >= args.line}
    per_week = {}
    for w in held:
        arms = f1[w]
        if "muninn_store" in arms and all(b in arms for b in BASELINES):
            spread = max(max(v) - min(v) for v in arms.values() if v)
            per_week[w] = {"largest_range": spread,
                           **{b: {"diff": fmean(arms["muninn_store"]) - fmean(arms[b]),
                                  "ok": fmean(arms["muninn_store"]) - fmean(arms[b]) > spread} for b in BASELINES}}
    res["rules"]["spread"] = {"weeks": per_week, "met": bool(per_week) and len(per_week) == len(held)
                              and all(pw[b]["ok"] for pw in per_week.values() for b in BASELINES)}
    band, pooled = args.ablation_band, res["pooled"].get("muninn_store-plain_store")
    beyond = {w: max(min(f1[w]["muninn_store"]) - max(f1[w]["plain_store"]), min(f1[w]["plain_store"]) - max(f1[w]["muninn_store"]))
              for w in held if f1[w].get("muninn_store") and f1[w].get("plain_store")}
    res["rules"]["ablation"] = {"band": band, "pooled_diff": pooled["observed"] if pooled else None,
                                "worst_gap_beyond_band_per_week": beyond,
                                "met": bool(pooled) and len(beyond) == len(held) and abs(pooled["observed"]) <= band
                                and all(g <= band for g in beyond.values())}
    return res


def f(x, d=1):
    return "" if x is None else f"{x:.{d}f}"


def report(label, res, data, args):
    out = [f"# PM-Bench round 8 · {label}", ""]
    counts, flags = [], []
    for w in res["weeks"]:
        counts.append(f"{w}: " + ", ".join(f"{arm} {len(data[w].get(arm, []))}" for arm in ARMS))
        flags += [f"{w}/{arm}" for arm in ARMS if len(data[w].get(arm, [])) < args.runs]
    out.append("Runs found: " + " · ".join(counts) + (f". FEWER THAN {args.runs}: {', '.join(flags)}" if flags else "."))
    out += ["", "## Set-F1 per (week, arm)", "", "| week | arm | runs | mean | sd | min | max | n |", "|---|---|---|---|---|---|---|---|"]
    for key, c in res["cells"].items():
        w, arm = key.split("/")
        out.append(f"| {w} | {arm} | {' · '.join(f(x) for x in c['runs'])} | {f(c['mean'])} | {f(c['sd'])} | {f(c['min'])} | {f(c['max'])} | {c['n']} |")
    out += ["", "## Secondary metrics (mean per cell, %)", "", "| week | arm | " + " | ".join(n for _, n in SECONDARY) + " |", "|---|---|" + "---|" * len(SECONDARY)]
    for key, c in res["cells"].items():
        out.append(f"| {key.replace('/', ' | ')} | " + " | ".join(f(c["secondary"].get(k)) for k, _ in SECONDARY) + " |")
    out += ["", "## Per-week contrasts (A − B, set-F1 points)", "", "| week | contrast | Δ mean | worst-case gap min(A) − max(B) |", "|---|---|---|---|"]
    for key, c in res["contrasts"].items():
        w, pair = key.split("/")
        out.append(f"| {w} | {pair} | {c['diff_means']:+.1f} | {c['worst_gap']:+.1f} |")
    out += ["", f"## Pooled over held-out weeks {res['heldout_weeks']} (v9 excluded)", "",
            "| contrast | weeks | Δ mean | perm p (A > B) | perm p (two-sided) | relabelings | bootstrap 95 % CI | weeks with all A > all B |",
            "|---|---|---|---|---|---|---|---|"]
    for pair, p in res["pooled"].items():
        out.append(f"| {pair} | {p['weeks']} | {p['observed']:+.2f} | {p['p_one_sided']:.6f} ({p['count_one_sided']}/{p['relabelings']}) | "
                   f"{p['p_two_sided']:.6f} ({p['count_two_sided']}/{p['relabelings']}) | {p['relabelings']}{'' if p['exact'] else ' (Monte-Carlo)'} | "
                   f"[{p['ci95'][0]:+.2f}, {p['ci95'][1]:+.2f}] | {p['weeks_all_a_above_b']}/{p['weeks']} |")
    mc = [k for k, p in res["pooled"].items() if not p["exact"]]
    out += ["", "Permutation test: exact stratified enumeration; the smallest attainable one-sided p is 1/relabelings."
            + (f" Monte-Carlo fallback ({MC_REPS} relabelings, seed {SEED}) used for: {', '.join(mc)}." if mc else ""),
            f"Bootstrap: {BOOT_REPS} cluster resamples by week, seed {SEED}. With {len(res['heldout_weeks'])} clusters the CI is coarse; the permutation test is primary.",
            "", "## Decision rules (held-out weeks only)", ""]
    r = res["rules"]
    out.append(f"- Line: mean muninn_store set-F1 {f(r['line']['mean'])} % vs line {args.line} % → {'MET' if r['line']['met'] else 'NOT MET'}")
    if args.spread_rule:
        detail = "; ".join(f"{w}: range {pw['largest_range']:.1f}, " + ", ".join(f"vs {b} {pw[b]['diff']:+.1f} {'ok' if pw[b]['ok'] else 'FAIL'}" for b in BASELINES)
                           for w, pw in r["spread"]["weeks"].items()) or "no complete week"
        out.append(f"- Spread rule: muninn_store mean above each baseline by more than the largest within-arm range, every held-out week → {'MET' if r['spread']['met'] else 'NOT MET'} ({detail})")
    ab = r["ablation"]
    detail = ", ".join(f"{w} {g:+.1f}" for w, g in ab["worst_gap_beyond_band_per_week"].items()) or "no complete week"
    out.append(f"- Ablation band ±{args.ablation_band}: pooled muninn_store − plain_store {f(ab['pooled_diff'], 2)}; per-week largest one-sided worst-case gap {detail} → "
               f"store implementation not distinguishable: {'MET' if ab['met'] else 'NOT MET'}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("roots", nargs="+", help="result root, optionally label=path")
    ap.add_argument("--json", help="write every number to this file")
    ap.add_argument("--runs", type=int, default=3, help="expected runs per (week, arm)")
    ap.add_argument("--line", type=float, default=82.9, help="mean set-F1 line on held-out weeks")
    ap.add_argument("--spread-rule", action="store_true", help="evaluate the within-arm-range spread rule")
    ap.add_argument("--ablation-band", type=float, default=2.0, help="band (points) for the store ablation")
    args = ap.parse_args()
    everything = {}
    for spec in args.roots:
        label, _, path = spec.rpartition("=")
        label = label or os.path.basename(os.path.normpath(path))
        data = load(path)
        if not data:
            print(f"# {label}: no *.score.md under {path}", file=sys.stderr)
            continue
        res = analyse(data, args)
        everything[label] = res
        print(report(label, res, data, args) + "\n")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"args": vars(args), "models": everything}, fh, indent=1)


if __name__ == "__main__":
    main()
