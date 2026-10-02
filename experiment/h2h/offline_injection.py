#!/usr/bin/env python3
"""v16-offline (PREREGISTRATION.md, same title): Muninn's own injected characters, two builds.

No model. For each run × task of the v13 fixture: a fresh store outside any checkout, the
committed seeding snapshot ingested, then `hook SessionStart` and one `hook UserPromptSubmit`
with the frozen task prompt. What is counted is the `additionalContext` of both, in
characters. The competitor's half of the published ratio is held fixed by its pinned version
and is not touched here.

  offline_injection.py --base <binary> --head <binary> [--out results.json]
"""
import argparse, json, os, random, statistics as st, subprocess, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
SEED = EXP / "results/h2h-v13-final/seeding"
TASKS = EXP / "revocation/tasks-revocation-public.json"


def as_transcript(seed_file: Path, out: Path) -> None:
    """The committed seeding snapshot is the harness's own log — `{i, prompt, reply, …}` —
    not a transcript. Each row is one seeding session: a user turn and its reply."""
    import datetime as dt

    lines = []
    for n, raw in enumerate(seed_file.read_text().splitlines()):
        if not raw.strip():
            continue
        r = json.loads(raw)
        ts = dt.datetime.fromtimestamp(r["created_at"] / 1000, dt.timezone.utc)
        sid = f"seed{n:03d}"
        base = {"isSidechain": False, "userType": "external", "cwd": "/work", "sessionId": sid}
        lines.append({**base, "parentUuid": None, "type": "user", "uuid": f"{sid}-u",
                      "timestamp": ts.isoformat().replace("+00:00", "Z"),
                      "message": {"role": "user", "content": r["prompt"]}})
        lines.append({**base, "parentUuid": f"{sid}-u", "type": "assistant", "uuid": f"{sid}-a",
                      "timestamp": (ts + dt.timedelta(seconds=2)).isoformat().replace("+00:00", "Z"),
                      "message": {"role": "assistant", "type": "message", "model": "synthetic",
                                  "content": [{"type": "text", "text": r.get("reply", "")}],
                                  "stop_reason": "end_turn"}})
    out.write_text("".join(json.dumps(l) + "\n" for l in lines))


def injected(binary: Path, seed_file: Path, prompt: str) -> int:
    root = Path(tempfile.mkdtemp(prefix="v16-"))
    try:
        env = {**os.environ, "MUNINN_ROOT": str(root / ".muninn"), "MUNINN_NO_PROJECT": "1"}
        subprocess.run(["git", "init", "-q", str(root)], capture_output=True)
        run = lambda *a, **k: subprocess.run([str(binary), "--cwd", str(root), *a],
                                             env=env, capture_output=True, text=True, **k)
        run("init", "--keep-native")
        t = root / "seed.jsonl"
        as_transcript(seed_file, t)
        run("ingest", str(t))
        run("maintain")
        total = 0
        for event, payload in (
            ("SessionStart", {"session_id": "cell", "cwd": str(root),
                              "hook_event_name": "SessionStart", "source": "startup"}),
            ("UserPromptSubmit", {"session_id": "cell", "cwd": str(root), "prompt": prompt,
                                  "hook_event_name": "UserPromptSubmit"}),
        ):
            p = subprocess.run([str(binary), "--cwd", str(root), "hook", event],
                               input=json.dumps(payload), env=env, capture_output=True, text=True)
            if p.stdout.strip():
                try:
                    total += len(json.loads(p.stdout)["hookSpecificOutput"]["additionalContext"])
                except (json.JSONDecodeError, KeyError):
                    pass
        return total
    finally:
        shutil.rmtree(root, ignore_errors=True)


def boot_ci(pairs, reps=10000, seed=7):
    rng = random.Random(seed)
    meds = []
    for _ in range(reps):
        s = [pairs[rng.randrange(len(pairs))] for _ in pairs]
        meds.append(st.median(h / b for h, b in s if b))
    meds.sort()
    return meds[int(0.025 * reps)], meds[int(0.975 * reps)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("--out", default=str(EXP / "results/v16-offline.json"))
    a = ap.parse_args()
    raw = json.load(open(TASKS))
    tasks = raw if isinstance(raw, list) else raw.get("tasks", raw)
    seeds = sorted(SEED.glob("r*-muninn-ship.jsonl"))
    rows = []
    for s in seeds:
        run = s.name.split("-")[0]
        for t in tasks:
            b = injected(Path(a.base), s, t["prompt"])
            h = injected(Path(a.head), s, t["prompt"])
            rows.append({"run": run, "task": t["id"], "base": b, "head": h})
            print(f"  {run} {t['id']:26s} base {b:6d}  head {h:6d}  {h/b if b else float('nan'):.3f}")
    pairs = [(r["head"], r["base"]) for r in rows if r["base"]]
    ratio = st.median(h / b for h, b in pairs)
    lo, hi = boot_ci(pairs)
    out = {"cells": len(rows), "median_ratio_head_over_base": ratio, "ci95": [lo, hi],
           "median_base_chars": st.median(r["base"] for r in rows),
           "median_head_chars": st.median(r["head"] for r in rows), "rows": rows}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"\n{len(rows)} cells · median HEAD/BASE {ratio:.3f} [{lo:.3f}, {hi:.3f}]"
          f" · base {out['median_base_chars']:.0f} chars, head {out['median_head_chars']:.0f}")


if __name__ == "__main__":
    main()
