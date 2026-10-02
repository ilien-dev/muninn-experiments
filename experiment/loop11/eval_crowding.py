#!/usr/bin/env python3
"""Loop 11 — what does the `--code` condition put in the block? (no model)

Head-to-head v4 ran the same engine twice: without commits in the grid it scores 18/27, with
them 6/27, and four registered fixes moved it to 4, 7, 9 and 5. Every one of those arms
delivered the current decision in 27 cells of 27, so none of them was a retrieval failure in
the usual sense. Reading the blocks the cells were actually given says what changed:

    condition   blocks/cell   commit records/cell   of those, about the cell's own topic
    nocode          4.0              0.2                        0 of 6
    code            7.3-8.0          4.0-5.7                   12 of 108-155

The `--code` condition roughly doubles the block, and about nine in ten of what it adds are
commit-confirmation records for *other* decisions. This harness reproduces that store offline
so a candidate fix can be measured in seconds instead of a five-hour grid.

It is a replica, not the grid. The seeding messages are the frozen phrasings the grid used
and the commits are the same swaps with the same uninformative subject, but the assistant's
acknowledgements here are a fixed synthetic line rather than a model's: absolute counts will
not match the grid. What it measures is one build against another on an identical store.

Per replacement task, from `muninn --json recall <the cell's own prompt>`:

    answered     the current value appears in the delivered block   (must stay 9/9)
    retired      the retired value appears in it                    (must stay 0/9)
    rank         1-based position of the first record stating the current value
    offtopic     delivered commit records that do not state this task's current value
    blocks       records delivered

Usage: eval_crowding.py --muninn <binary> [--tag base] [--out results.json]
"""
import argparse
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRID = HERE.parent / "results" / "h2h-v4-code" / "config.json"
PHRASINGS = HERE.parent / "h2h" / "v2" / "seed_phrasings.json"
DECISIONS_DIR = "config/decisions"
COMMIT_MSG = "update dependencies"          # the grid's subject, which never names the value
ACK = "Noted."                              # synthetic: no model runs in this harness


def transcript(path: Path, sid: str, ts: datetime, user: str) -> None:
    base = {"isSidechain": False, "userType": "external", "cwd": "/work/project", "sessionId": sid}
    rows = [
        {**base, "parentUuid": None, "type": "user", "uuid": f"{sid}-u",
         "timestamp": ts.isoformat().replace("+00:00", "Z"),
         "message": {"role": "user", "content": user}},
        {**base, "parentUuid": f"{sid}-u", "type": "assistant", "uuid": f"{sid}-a",
         "timestamp": (ts + timedelta(seconds=2)).isoformat().replace("+00:00", "Z"),
         "message": {"role": "assistant", "type": "message", "model": "synthetic",
                     "content": [{"type": "text", "text": ACK}], "stop_reason": "end_turn"}},
    ]
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), "-c", "user.email=cell@h2h", "-c", "user.name=cell",
                    *args], check=True, capture_output=True)


def seed(muninn: str, root: Path, tdir: Path, tasks: list, pairs: list,
         commits: bool = True) -> dict:
    """The v4 `--code` store: the phrasings as sessions, the values in tracked files, and one
    commit per change whose subject never names the new value."""
    env = {**os.environ, "MUNINN_ROOT": str(root), "MUNINN_NO_PROJECT": "1"}
    (root / DECISIONS_DIR).mkdir(parents=True, exist_ok=True)
    for t in tasks:
        if commits:
            (root / DECISIONS_DIR / f"{t['id']}.json").write_text(
                json.dumps({"value": t["scenario"]["old"]}, indent=1) + "\n")
    (root / "README.md").write_text("base\n")
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    subprocess.run([muninn, "--cwd", str(root), "init", "--keep-native"], env=env,
                   capture_output=True)
    t0 = datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc)
    for i, (t, p) in enumerate(zip(tasks, pairs)):
        for k, text in enumerate((p["a"], p["b"])):
            f = tdir / f"{i:02d}{k}.jsonl"
            transcript(f, f"s{i:02d}{k}", t0 + timedelta(minutes=30 * (2 * i + k)), text)
            subprocess.run([muninn, "--cwd", str(root), "ingest", str(f)], env=env,
                           capture_output=True)
        if commits and t["scenario"]["new"]:
            (root / DECISIONS_DIR / f"{t['id']}.json").write_text(
                json.dumps({"value": t["scenario"]["new"]}, indent=1) + "\n")
            git(root, "add", "-A")
            git(root, "commit", "-qm", COMMIT_MSG)
        subprocess.run([muninn, "--cwd", str(root), "maintain"], env=env, capture_output=True)
    return env


# a commit-confirmation record, either writer: `commit <hash>: <file> now reads …` or
# `commit <hash>: <subject>` with a `files:` line
COMMITISH = re.compile(r"commit [0-9a-f]{7,}", re.I)


def records(text: str) -> list:
    return [r for r in re.split(r"(?=\[muninn:)", text) if r.startswith("[muninn:")]


def measure(muninn: str, root: Path, env: dict, tasks: list) -> list:
    out = []
    for t in tasks:
        if not t["scenario"]["new"]:
            continue
        new = t["scenario"]["new"].lower().split(" with ")[0]
        old = t["scenario"]["old"].lower()
        # the hook, not `muninn recall`: the hooks fuse the lexical list with the cues in
        # `hook::deliver_fused` and never call the CLI's `deliver`. A first version of this
        # harness probed `recall` and scored a change that reached no cell.
        hook = json.dumps({"session_id": f"probe-{t['id']}", "cwd": str(root),
                           "prompt": t["prompt"], "hook_event_name": "UserPromptSubmit"})
        p = subprocess.run([muninn, "--cwd", str(root), "hook", "UserPromptSubmit"],
                           env=env, input=hook, capture_output=True, text=True)
        try:
            d = json.loads(p.stdout or "{}")
        except json.JSONDecodeError:
            d = {}
        ctx = (d.get("hookSpecificOutput") or {}).get("additionalContext")
        text = ctx if isinstance(ctx, str) else (d.get("additionalContext") or "")
        recs = records(text)
        rank = next((i + 1 for i, r in enumerate(recs) if new in r.lower()), 0)
        out.append({
            "task": t["id"],
            "answered": int(new in text.lower()),
            "retired": int(old in text.lower()),
            "rank": rank,
            "blocks": len(recs),
            "commits": sum(bool(COMMITISH.search(r)) for r in recs),
            "offtopic": sum(bool(COMMITISH.search(r)) and new not in r.lower() for r in recs),
            "tokens": len(text) // 3,
        })
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--muninn", required=True)
    ap.add_argument("--tag", default="base")
    ap.add_argument("--out", default=None)
    ap.add_argument("--keep", action="store_true", help="leave the store for inspection")
    ap.add_argument("--no-commits", action="store_true",
                    help="the plain condition: the decisions never reach a file, so the store "
                         "holds only what the sessions said — the grid arm that scores 18/27")
    a = ap.parse_args()
    tasks = json.load(open(GRID))["tasks"]
    pairs = json.load(open(PHRASINGS))
    root = Path(tempfile.mkdtemp(prefix=f"loop11-{a.tag}-"))
    tdir = Path(tempfile.mkdtemp(prefix="loop11-t-"))
    env = seed(a.muninn, root, tdir, tasks, pairs, commits=not a.no_commits)
    rows = measure(a.muninn, root, env, tasks)
    n = len(rows)
    summary = {
        "tag": a.tag, "tasks": n,
        "answered": sum(r["answered"] for r in rows),
        "retired": sum(r["retired"] for r in rows),
        "blocks": sum(r["blocks"] for r in rows) / n,
        "commits": sum(r["commits"] for r in rows) / n,
        "offtopic": sum(r["offtopic"] for r in rows) / n,
        "rank1": sum(r["rank"] == 1 for r in rows),
        "tokens": sum(r["tokens"] for r in rows) / n,
    }
    json.dump({"summary": summary, "rows": rows}, open(
        a.out or HERE / f"results-{a.tag}.json", "w"), indent=1)
    print(f"{a.tag:14s} answered {summary['answered']}/{n}  retired {summary['retired']}/{n}  "
          f"rank1 {summary['rank1']}/{n}  blocks/task {summary['blocks']:.1f}  "
          f"commits/task {summary['commits']:.1f}  offtopic/task {summary['offtopic']:.1f}  "
          f"tokens/task {summary['tokens']:.0f}")
    for r in rows:
        print(f"  {r['task']:24s} answered {r['answered']} retired {r['retired']} "
              f"rank {r['rank']} blocks {r['blocks']} offtopic {r['offtopic']}")
    if a.keep:
        print("store:", root)
    else:
        subprocess.run(["rm", "-rf", str(root), str(tdir)])


if __name__ == "__main__":
    main()
