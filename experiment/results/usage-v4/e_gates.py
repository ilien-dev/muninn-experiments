"""The E harness's gates, apart from e_perf.py so they can be checked without a measurement
(`check_e_gates.py`)."""
import json


SEED_SQL = ("select session_id, compaction_epoch, record_id, fired_at, tokens, reason from fire_ledger "
            "where fired_at between 1700000000000 and 1700000008335 order by fired_at, id")


def seed_fingerprint(con):
    """Count and sha256 of the rows the ledger seed writes, read-only, in seed order."""
    import hashlib
    h = hashlib.sha256()
    n = 0
    for row in con.execute(SEED_SQL):
        n += 1
        h.update(json.dumps(row).encode() + b'\n')
    return n, h.hexdigest()[:16]


def gate_workload(seeds):
    """seeds: {build: [(rows, fingerprint) per run]}. Equal only when every run of every build
    holds the same non-empty seed, by count and by fingerprint."""
    allv = {v for runs in seeds.values() for v in runs}
    per = {b: sorted(set(r)) for b, r in seeds.items()}
    equal = len(allv) == 1 and all(per.values()) and next(iter(allv))[0] > 0
    return equal, per


def gate_deliver(blocks):
    """blocks: {build: number of blocks the must-deliver case returned}. Both must deliver."""
    vals = list(blocks.values())
    if not vals or any(v is None for v in vals):
        return 'missing'
    if all(v > 0 for v in vals):
        return 'both'
    return 'neither' if not any(v > 0 for v in vals) else 'one'
