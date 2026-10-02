#!/usr/bin/env python3
"""Two stores, the same conversation, different session ids: is the memory the same?

The head-to-head's snapshots answer this for a live grid, and are the reason the property
was checked at all (PREREGISTRATION.md, "is the memory reproducible?"). This is the same
question in one command and no model: the same messages are ingested into N fresh stores,
each with its own randomly generated session ids, and the stored records are compared after
normalising the two identifiers that vary by construction — the session id and any hash.

Anything that differs after that is Muninn varying on its own input, and is a defect.

Measured on three phrasing files (20, 30 and 90 messages, three stores each): identical, and
identical on the binary that carried the one defect this property has actually caught — that
one needed topic inheritance to land on an *episode*, which these files do not produce, and is
pinned instead by `ingest::tests::an_episodes_subject_does_not_sort_its_session_id_among_the_topic`.
So this script is the sweep, not the regression test: it says nothing else varies.

  same_input_same_store.py --muninn <binary> [--stores 3] [--phrasings ...]
"""
import argparse, json, os, re, sqlite3, subprocess, tempfile, uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
UUIDRE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
HASHRE = re.compile(r"\b[0-9a-f]{7,40}\b")


def normalise(t: str) -> str:
    return HASHRE.sub("<hash>", UUIDRE.sub("<session>", t))


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


def build(muninn: str, messages: list) -> set:
    root = Path(tempfile.mkdtemp(prefix="same-"))
    tdir = Path(tempfile.mkdtemp(prefix="same-t-"))
    (root / ".git").mkdir()
    env = {**os.environ, "MUNINN_ROOT": str(root), "MUNINN_NO_PROJECT": "1"}
    subprocess.run([muninn, "--cwd", str(root), "init", "--keep-native"],
                   env=env, capture_output=True)
    t0 = datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc)
    for k, m in enumerate(messages):
        p = tdir / f"{k:03d}.jsonl"
        transcript(p, str(uuid.uuid4()), t0 + timedelta(minutes=30 * k), m)
        subprocess.run([muninn, "--cwd", str(root), "ingest", str(p)],
                       env=env, capture_output=True)
    con = sqlite3.connect(root / ".muninn" / "muninn.db")
    rows = con.execute("SELECT kind, subject, object FROM record WHERE invalid = 0").fetchall()
    con.close()
    subprocess.run(["rm", "-rf", str(root), str(tdir)])
    return {normalise(" | ".join(str(c) for c in r)) for r in rows}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--muninn", required=True)
    ap.add_argument("--stores", type=int, default=3)
    ap.add_argument("--phrasings", default=str(EXP / "loop9" / "heldout_phrasings.json"))
    a = ap.parse_args()
    rows = json.load(open(a.phrasings))
    # every phrasing file the loops use: {key,a,b[,c]}, with or without a style suffix
    messages = [r[k] for r in rows for k in ("a", "b", "c") if r.get(k)]
    sets = [build(a.muninn, messages) for _ in range(a.stores)]
    union, inter = set.union(*sets), set.intersection(*sets)
    print(f"{len(messages)} messages, {a.stores} stores, {[len(s) for s in sets]} records")
    print(f"identical: {union == inter}   items in some store but not all: {len(union - inter)}")
    for d in sorted(union - inter)[:10]:
        print(f"  {d[:120]}")


if __name__ == "__main__":
    main()
