#!/usr/bin/env python3
"""Runs usage-v1's replay.py, unchanged, with one step added (eighteenth amendment).

  python -I b1_replay.py <replay.py> <arm-binary> <arm> <project> <workdir>

A record whose anchor resolves outside the replay directory is not validated against the live
file: before every `maintain` the replay runs, and once more when it ends, the stored hash of
each such record is cleared, so the validator, which reads only records that hold a hash,
leaves it alone. Anchors inside the replay directory are not touched. How many records were
skipped is written beside the replayed store as `<project>.anchors.json` (a count, no path).
"""
import json, os, runpy, sqlite3, subprocess, sys

REPLAY = sys.argv[1]
sys.argv = [REPLAY] + sys.argv[2:]
BIN, ARM, PROJ, WORK = sys.argv[1:5]
ROOT = os.path.normcase(os.path.normpath('%s/%s/%s' % (WORK, ARM, PROJ)))
DB = os.path.join(ROOT, '.muninn', 'muninn.db')
SIDE = os.path.join(os.path.dirname(ROOT), PROJ + '.anchors.json')
skipped = set()


def outside(anchor):
    """Resolved as the engine resolves it: an absolute path as it is, anything else under the root."""
    p = os.path.normcase(os.path.normpath(os.path.join(ROOT, anchor)))
    return not (p == ROOT or p.startswith(ROOT + os.sep))


def skip():
    if not os.path.isfile(DB):
        return
    c = sqlite3.connect(DB, timeout=30)
    try:
        ids = [i for i, a in c.execute('select id, anchor_path from record where anchor_path is not null and anchor_hash is not null') if outside(a)]
        c.executemany('update record set anchor_hash = null where id = ?', [(i,) for i in ids])
        c.commit()
        skipped.update(ids)
    finally:
        c.close()


_run = subprocess.run


def run(args, *a, **k):
    if isinstance(args, (list, tuple)) and len(args) >= 2 and args[0] == BIN and args[1] == 'maintain':
        skip()
    return _run(args, *a, **k)


subprocess.run = run
if os.path.exists(SIDE):
    os.remove(SIDE)
try:
    runpy.run_path(REPLAY, run_name='__main__')
finally:
    skip()
    os.makedirs(os.path.dirname(SIDE), exist_ok=True)
    json.dump({'anchors_outside_skipped': len(skipped)}, open(SIDE, 'w'))
