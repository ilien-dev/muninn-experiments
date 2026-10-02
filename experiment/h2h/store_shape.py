#!/usr/bin/env python3
"""The shape of the store each fixture's seeding actually builds, offline and without a model.

A grid compares two builds by their cells. It cannot tell you whether the code under test ever
ran. This can: it rebuilds each fixture's store from the committed seeding snapshot the same way
`offline_injection.py` does, and reports the counts a read path branches on.

It exists because v32 was reverted by an adverse rule that fired on `v4`, `v5` and `v7` — three
fixtures whose stores hold seven to twelve typed records, where the change under test branches
only under five and therefore never executed. The rule fired on drift between grids.

  store_shape.py [--binary target/release/muninn] [--grids h2h-v32-v3 h2h-v32-v4 ...]
"""
import argparse, datetime as dt, json, os, shutil, sqlite3, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
DEFAULT_GRIDS = ["h2h-v32-v3", "h2h-v32-v4", "h2h-v32-v5", "h2h-v32-v6", "h2h-v32-v7"]


def as_transcript(seed_file: Path, out: Path) -> None:
    """The seeding snapshot is the harness's own log — `{i, prompt, reply, …}` — not a
    transcript. Each row is one seeding session: a user turn and its reply."""
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


def shape(binary: Path, seed_file: Path) -> dict:
    root = Path(tempfile.mkdtemp(prefix="shape-"))
    try:
        # `MUNINN_ROOT` is the project root, not the store directory: the store lands one
        # level further down. Reading it from the wrong path returns an empty database that
        # SQLite creates on connect, which looks like a store with no schema in it.
        env = {**os.environ, "MUNINN_ROOT": str(root / ".muninn"), "MUNINN_NO_PROJECT": "1"}
        subprocess.run(["git", "init", "-q", str(root)], capture_output=True)
        run = lambda *a: subprocess.run([str(binary), "--cwd", str(root), *a], env=env,
                                        capture_output=True, text=True)
        run("init", "--keep-native")
        t = root / "seed.jsonl"
        as_transcript(seed_file, t)
        run("ingest", str(t))
        run("maintain")
        db = sqlite3.connect(root / ".muninn" / ".muninn" / "muninn.db")
        q = lambda s: db.execute(s).fetchone()[0]
        out = {
            "typed": q("SELECT count(*) FROM served_record WHERE kind IN "
                       "('decision','invariant','deadend','correction')"),
            "episodes": q("SELECT count(*) FROM served_record WHERE kind = 'episode'"),
            "short_episodes": q("SELECT count(*) FROM served_record WHERE kind = 'episode' "
                                "AND length(object) <= 120"),
            "retired": q("SELECT count(*) FROM record WHERE invalid = 1"),
        }
        db.close()
        return out
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary", default=str(EXP.parents[2] / "target/release/muninn"))
    ap.add_argument("--grids", nargs="*", default=DEFAULT_GRIDS)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    # Which binary this is, printed before any number it produced. `cargo test` does not
    # rebuild `target/release/muninn`, so a gate that ends green can leave this reading an
    # older binary than the tree — it did, and a published figure was two cells low because
    # of it.
    sha = subprocess.run(["sha256sum", str(a.binary)], capture_output=True, text=True).stdout[:16]
    mtime = Path(a.binary).stat().st_mtime if Path(a.binary).exists() else 0
    import datetime as _dt
    print(f"binary {sha} built {_dt.datetime.fromtimestamp(mtime):%Y-%m-%d %H:%M}")
    rows = []
    for g in a.grids:
        d = EXP / "results" / g / "seeding"
        if not d.exists():
            print(f"{g}: no seeding snapshot")
            continue
        for f in sorted(d.glob("r*.jsonl")):
            rows.append({"grid": g, "seed": f.name, **shape(Path(a.binary), f)})
    if a.json:
        print(json.dumps(rows, indent=2))
        return
    print(f"{'grid':16} {'seed':28} {'typed':>5} {'episodes':>8} {'short':>5} {'retired':>7}")
    for r in rows:
        print(f"{r['grid']:16} {r['seed']:28} {r['typed']:>5} {r['episodes']:>8} "
              f"{r['short_episodes']:>5} {r['retired']:>7}")


if __name__ == "__main__":
    main()
