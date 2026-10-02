#!/usr/bin/env python3
"""Loop 10 — does the conversational rule retire things that are still true? (no model)

Every loop so far measured *recall*: given a decision and the message that replaces it, is
the first one retired. `kept_b` checks that the replacement survives, and the `noise` arm
checks that an unrelated **commit** retires nothing. Nothing measured what happens when a
later message is about something else and happens to share words with an earlier one, which
is what most of a real conversation looks like.

It was worth measuring because a real store said so: six of this project's own transcripts,
395 records, and of four sampled conversational retirements three looked wrong — a note about
`gzip`/`zstd` retired by a message about *running a test* on gzip and zstd.

Each pair here is two messages about different things that share two or more content words,
where both stay true. The outcomes, per pair:

  kept_a    the first message is still served after the second arrives  (this is the gate)
  kept_b    the second is there too, which it always should be

Usage: eval_precision.py --muninn <binary> [--pairs pairs.json] [--out results.json]
"""
import argparse, json, os, subprocess, tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent


def transcript(path: Path, sid: str, ts: datetime, user: str) -> None:
    base = {"isSidechain": False, "userType": "external", "cwd": "/work/project", "sessionId": sid}
    rows = [
        {**base, "parentUuid": None, "type": "user", "uuid": f"{sid}-u",
         "timestamp": ts.isoformat().replace("+00:00", "Z"),
         "message": {"role": "user", "content": user}},
        {**base, "parentUuid": f"{sid}-u", "type": "assistant", "uuid": f"{sid}-a",
         "timestamp": (ts + timedelta(seconds=2)).isoformat().replace("+00:00", "Z"),
         "message": {"role": "assistant", "type": "message", "model": "synthetic",
                     "content": [{"type": "text", "text": "Noted."}], "stop_reason": "end_turn"}},
    ]
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--muninn", required=True)
    ap.add_argument("--pairs", default=str(HERE / "pairs.json"))
    ap.add_argument("--out", default=str(HERE / "results.json"))
    a = ap.parse_args()
    pairs = json.load(open(a.pairs))
    results = []
    for i, p in enumerate(pairs):
        # one store per pair: the question is what the second message does to the first,
        # not what fifteen unrelated decisions do to each other
        root = Path(tempfile.mkdtemp(prefix="loop10-"))
        tdir = Path(tempfile.mkdtemp(prefix="loop10-t-"))
        (root / ".git").mkdir()
        env = {**os.environ, "MUNINN_ROOT": str(root), "MUNINN_NO_PROJECT": "1"}
        subprocess.run([a.muninn, "--cwd", str(root), "init", "--keep-native"],
                       env=env, capture_output=True)
        t0 = datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc)
        for k, text in enumerate((p["a"], p["b"])):
            f = tdir / f"{k}.jsonl"
            transcript(f, f"s{i:02d}{k}", t0 + timedelta(minutes=30 * k), text)
            subprocess.run([a.muninn, "--cwd", str(root), "ingest", str(f)],
                           env=env, capture_output=True)
        subprocess.run([a.muninn, "--cwd", str(root), "--json", "export", "--all",
                        "--out", str(root / "x.jsonl")], env=env, capture_output=True)
        recs = [json.loads(l) for l in open(root / "x.jsonl")]

        def active_with(text):
            key = text.strip().rstrip(".!;")[:40].lower()
            return [r for r in recs if not r.get("invalid")
                    and key in (r.get("body") or "").lower()]

        results.append({
            "key": p["key"],
            "shared": p.get("shared"),
            "kept_a": bool(active_with(p["a"])),
            "kept_b": bool(active_with(p["b"])),
            "a": p["a"], "b": p["b"],
        })
        subprocess.run(["rm", "-rf", str(root), str(tdir)])

    json.dump(results, open(a.out, "w"), indent=1)
    ka = sum(r["kept_a"] for r in results)
    kb = sum(r["kept_b"] for r in results)
    print(f"kept_a {ka}/{len(results)}   kept_b {kb}/{len(results)}")
    for r in results:
        if not r["kept_a"]:
            print(f"  LOST  {r['key']}")
            print(f"    a: {r['a']}")
            print(f"    b: {r['b']}")


if __name__ == "__main__":
    main()
