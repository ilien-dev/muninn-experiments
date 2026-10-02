#!/usr/bin/env python3
"""Does the same input give the same memory? (PREREGISTRATION.md, "is the memory reproducible?")

The head-to-head seeds every arm three times with the same twenty messages, so its snapshots
are three samples of the same input. This reads each snapshot with the tool's own store and
reduces it to a set of stored memory texts, then reports the Jaccard similarity of the three
run pairs, within an arm. Never between arms: the two tools store different kinds of thing.

Exact-string Jaccard is harsh on a tool that writes prose titles, so a second, wording-free
figure is reported beside it and disclosed as an addition to the registered analysis: of the
values the grid actually seeded, how many appear anywhere in each run's store. That one does
not care how the text is phrased — only whether the decision was kept at all.

  reproducible.py <work-dir> [--arms muninn-loop8,claude-mem] [--runs 3] [--tasks <file>]

<work-dir> is the harness's working directory, e.g. /tmp/muninn-h2h/h2h-v4-code.
"""
import argparse
import pathlib
import re
import sqlite3
import subprocess
import tempfile


# Two identifiers vary by construction and say nothing about what was stored: the harness
# gives every run its own checkout, so the same commit has a different hash in each, and the
# harness gives every seeding message its own session, so the same message has a different
# session id. Both are normalised away, in both tools, before anything is compared. What is
# left is the text. Disclosed rather than silent, because it is the one place this analysis
# touches the data — the raw figure without it is in the report.
UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
HASHISH = re.compile(r"\b[0-9a-f]{7,40}\b")


def normalise(text: str) -> str:
    return HASHISH.sub("<hash>", UUID.sub("<session>", text))


def muninn_items(snap: pathlib.Path) -> set:
    db = snap / ".muninn" / "muninn.db"
    if not db.exists():
        return set()
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / "m.db"
        copy.write_bytes(db.read_bytes())
        con = sqlite3.connect(copy)
        rows = con.execute(
            "SELECT kind, subject, object FROM record WHERE invalid = 0"
        ).fetchall()
        con.close()
    return {normalise(" | ".join(str(c) for c in r)) for r in rows}


def claude_mem_items(snap: pathlib.Path) -> set:
    db = snap / "claude-mem.db"
    if not db.exists():
        hits = list(snap.rglob("claude-mem.db"))
        if not hits:
            return set()
        db = hits[0]
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / "c.db"
        copy.write_bytes(db.read_bytes())
        con = sqlite3.connect(copy)
        con.row_factory = sqlite3.Row
        tables = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        items = set()
        for t in tables:
            cols = [r[1] for r in con.execute(f"PRAGMA table_info('{t}')").fetchall()]
            textish = [c for c in cols
                       if c.lower() in ("text", "content", "body", "summary", "memory",
                                        "title", "description")]
            if not textish:
                continue
            for row in con.execute(f"SELECT {', '.join(textish)} FROM '{t}'"):
                v = " | ".join(str(x) for x in row if x is not None).strip()
                if v:
                    items.add(normalise(f"{t}: {v}"))
        con.close()
    return items


READERS = {"claude-mem": claude_mem_items}


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def seeded_values(tasks: pathlib.Path) -> list:
    import json
    out = []
    for t in json.loads(tasks.read_text())["tasks"]:
        for v in (t["scenario"]["old"], t["scenario"]["new"]):
            if v:
                out.append(v.split(" with ")[0].split(",")[0])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("work")
    ap.add_argument("--arms", default="muninn-loop8,claude-mem")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--tasks", default=str(pathlib.Path(__file__).resolve().parent.parent
                                           / "revocation" / "tasks-revocation-public.json"))
    a = ap.parse_args()
    values = seeded_values(pathlib.Path(a.tasks)) if pathlib.Path(a.tasks).exists() else []
    work = pathlib.Path(a.work)
    print(f"# {work.name}")
    print("| arm | runs | items per run | pairwise Jaccard | items in one run only | seeded values present |")
    print("|---|---|---|---|---|---|")
    for arm in a.arms.split(","):
        read = READERS.get(arm, muninn_items)
        sets, sizes = [], []
        for r in range(a.runs):
            snap = work / f"snap-r{r}-{arm}"
            if not snap.exists():
                continue
            s = read(snap)
            sets.append(s)
            sizes.append(len(s))
        if len(sets) < 2:
            print(f"| {arm} | {len(sets)} | — | not enough snapshots | — |")
            continue
        pairs = [(i, j) for i in range(len(sets)) for j in range(i + 1, len(sets))]
        js = [jaccard(sets[i], sets[j]) for i, j in pairs]
        only = len(set.union(*sets) - set.intersection(*sets))
        cover = [sum(1 for v in values if v.lower() in " ".join(st).lower()) for st in sets]
        print(f"| {arm} | {len(sets)} | {sizes} | "
              f"{', '.join(f'{x:.3f}' for x in js)} | {only} | "
              f"{cover if values else '—'} of {len(values)} |")
        if min(js) < 1.0:
            diff = sorted(set.union(*sets) - set.intersection(*sets))[:5]
            for d in diff:
                print(f"|  | | | | `{d[:110]}` |")


if __name__ == "__main__":
    main()
