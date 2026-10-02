#!/usr/bin/env python3
"""Gate 4 §2 — compaction survival ("decay probe"), reproducible in one command, no model.

Seeds a fresh store with N invariants (default 10), then forces R compactions (default
100). A forced compaction is what Claude Code does around a real one: the `PreCompact` hook,
then the `PostCompact` hook, each fed the harness's JSON on stdin. After every compaction
the probe reads the `PostCompact` hook's `additionalContext` and counts how many of the N
invariants it carries (each invariant holds a token that exists nowhere else). Per-hook wall
time is measured around the whole process (spawn included), which is what the harness pays.

Writes `<out>/log.jsonl` (one line per compaction: delivered ids, ms per hook) and
`<out>/summary.json`, and prints the summary. Exit code 1 if any compaction lost an
invariant, so CI can run it.

  python3 crates/muninn-bench/experiment/decay_probe.py --reps 100
"""
import argparse
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def hook(muninn: str, env: dict, event: str, payload: dict) -> tuple[str, float]:
    t0 = time.perf_counter()
    p = subprocess.run([muninn, "hook", event], input=json.dumps(payload), capture_output=True, text=True, env=env)
    ms = (time.perf_counter() - t0) * 1000
    if p.returncode != 0:
        sys.exit(f"{event} exited {p.returncode}: {p.stderr[-300:]}")   # read hooks must always exit 0
    text = ""
    if p.stdout.strip():
        try:
            text = json.loads(p.stdout).get("hookSpecificOutput", {}).get("additionalContext", "")
        except json.JSONDecodeError:
            text = ""
    return text, ms


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reps", type=int, default=100)
    ap.add_argument("--invariants", type=int, default=10)
    ap.add_argument("--muninn", default=str(ROOT / "target" / "release" / "muninn"))
    ap.add_argument("--out", default=str(HERE / "results" / "decay-probe"))
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="muninn-decay-"))
    (work / ".git").mkdir()
    env = {**os.environ, "MUNINN_ROOT": str(work), "MUNINN_NO_PROJECT": "1", "MUNINN_ARM": "literal"}
    env.pop("MUNINN_NO_CUES", None)
    subprocess.run([a.muninn, "--cwd", str(work), "init", "--keep-native", "--no-boot-block"], check=True, env=env, capture_output=True)

    # N invariants, each with a token that exists nowhere else
    tokens = [f"zq{i:02d}kx{(i * 7919) % 10007:04d}" for i in range(a.invariants)]
    rows = []
    for i, tok in enumerate(tokens):
        rows.append({"kind": "invariant", "subject": f"probe.rule{i}", "relation": "must",
                     "object": f"always keep marker {tok}", "body": f"Invariant {i}: the marker {tok} must survive compaction.\n",
                     "origin": "user_said", "session_id": "decay-seed", "created_at": 1_800_000_000_000 + i})
    seed = work / "seed.jsonl"
    seed.write_text("".join(json.dumps(r) + "\n" for r in rows))
    subprocess.run([a.muninn, "--cwd", str(work), "import", str(seed)], check=True, env=env, capture_output=True)

    session = "decay-session"
    base = {"session_id": session, "cwd": str(work), "transcript_path": str(work / "transcript.jsonl")}
    (work / "transcript.jsonl").write_text("")
    # a session start first, as in a real session (gated delivery; the probe does not count it)
    hook(a.muninn, env, "SessionStart", {**base, "hook_event_name": "SessionStart", "source": "startup"})

    log = open(out / "log.jsonl", "w")
    pre_ms, post_ms, complete, lost = [], [], 0, []
    for r in range(a.reps):
        _, ms1 = hook(a.muninn, env, "PreCompact", {**base, "hook_event_name": "PreCompact", "trigger": "auto"})
        text, ms2 = hook(a.muninn, env, "PostCompact", {**base, "hook_event_name": "PostCompact", "compact_summary": "Context compacted."})
        pre_ms.append(ms1)
        post_ms.append(ms2)
        got = [t for t in tokens if t in text]
        if len(got) == len(tokens):
            complete += 1
        else:
            lost.append(r)
        log.write(json.dumps({"rep": r, "delivered": len(got), "pre_ms": round(ms1, 2), "post_ms": round(ms2, 2),
                              "context_chars": len(text)}) + "\n")
    log.close()
    (out / "last_context.txt").write_text(text)   # what the agent saw after the last compaction

    ver = subprocess.run([a.muninn, "--version"], capture_output=True, text=True, env=env).stdout.strip()
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    summary = {
        "muninn": ver, "commit": commit, "reps": a.reps, "invariants": a.invariants,
        "compactions_with_all_invariants": complete,
        "facts_delivered": a.reps * a.invariants - sum(a.invariants - int(json.loads(l)["delivered"]) for l in open(out / "log.jsonl")),
        "facts_expected": a.reps * a.invariants, "lost_at_reps": lost,
        "post_compact_ms": {"median": round(statistics.median(post_ms), 2), "p95": round(sorted(post_ms)[int(0.95 * len(post_ms)) - 1], 2), "max": round(max(post_ms), 2)},
        "pre_compact_ms": {"median": round(statistics.median(pre_ms), 2), "max": round(max(pre_ms), 2)},
        "measured_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))
    sys.exit(0 if complete == a.reps else 1)


if __name__ == "__main__":
    main()
