#!/usr/bin/env python3
"""Dry check of the E gates, no timing: the gate functions on fixed inputs, the seed fingerprint on a
doctored store in the work directory, and verdict.py's E rows on the committed counts and on
doctored copies of them (written to the work directory, never to counts/).

  python -I check_e_gates.py <base sha16> <candidate sha16>
"""
import json, os, shutil, sqlite3, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fixtures, work
from e_gates import seed_fingerprint, gate_workload, gate_deliver

HERE = os.path.dirname(os.path.abspath(__file__))
B, C = sys.argv[1], sys.argv[2]
ok = True


def expect(name, got, want):
    global ok
    good = got == want
    ok &= good
    print('%-4s %-62s got %s' % ('ok' if good else 'FAIL', name, got))


# gate functions
expect('workload: same count and fingerprint', gate_workload({'b': [(8336, 'aa')] * 2, 'c': [(8336, 'aa')] * 2})[0], True)
expect('workload: counts differ', gate_workload({'b': [(8336, 'aa')], 'c': [(8335, 'aa')]})[0], False)
expect('workload: fingerprints differ', gate_workload({'b': [(8336, 'aa')], 'c': [(8336, 'ab')]})[0], False)
expect('workload: one run of one build differs', gate_workload({'b': [(8336, 'aa'), (8336, 'aa')], 'c': [(8336, 'aa'), (8336, 'zz')]})[0], False)
expect('workload: a build with no checked run', gate_workload({'b': [(8336, 'aa')], 'c': []})[0], False)
expect('workload: both empty seeds', gate_workload({'b': [(0, 'e3')], 'c': [(0, 'e3')]})[0], False)
expect('deliver: both', gate_deliver({'b': 3, 'c': 2}), 'both')
expect('deliver: one', gate_deliver({'b': 3, 'c': 0}), 'one')
expect('deliver: neither', gate_deliver({'b': 0, 'c': 0}), 'neither')
expect('deliver: missing', gate_deliver({'b': 3, 'c': None}), 'missing')

# seed fingerprint on a doctored copy of a store (fire_ledger rows in the seed's time range)
d = work('e_perf', 'gate-check')
db = os.path.join(d, 'muninn.db')
shutil.copyfile(fixtures() + '/stores/W05/muninn.db', db)
con = sqlite3.connect(db)
con.executemany("insert into fire_ledger(session_id, compaction_epoch, record_id, fired_at, tokens, reason) values('b', 0, ?, ?, 0, 'literal:literal')",
                [(i + 1, 1700000000000 + i) for i in range(5)])
con.commit()
f1 = seed_fingerprint(con)
con.execute("update fire_ledger set record_id = record_id + 1 where fired_at = 1700000000003")
con.commit()
f2 = seed_fingerprint(con)
con.close()
expect('fingerprint: 5 seed rows counted', f1[0], 5)
expect('fingerprint: one record_id changed -> differs', f1[1] != f2[1], True)


# verdict.py E rows
def e_rows(counts_dir=None):
    a = [sys.executable, '-I', os.path.join(HERE, 'verdict.py'), B, C, '--json'] + (['--counts-dir', counts_dir] if counts_dir else [])
    rows = json.loads(subprocess.run(a, capture_output=True, text=True).stdout)
    return {r['rule'].split(' p95')[0].split(' with')[0]: r['verdict'] for r in rows if r['rule'].startswith('E')}


expect('committed counts (revision 2) read missing', set(e_rows().values()), {'missing'})
cd = work('e_perf', 'gate-check', 'counts')
for f in os.listdir(os.path.join(HERE, 'counts')):
    shutil.copyfile(os.path.join(HERE, 'counts', f), os.path.join(cd, f))


def doctor(fn):
    for b in (B, C):
        p = os.path.join(cd, 'e_perf_%s.json' % b)
        j = json.load(open(os.path.join(HERE, 'counts', 'e_perf_%s.json' % b)))
        j['harness_rev'] = 3
        j['workload'] = dict(j.get('workload') or {}, equal=True, must_deliver={'verdict': 'both'})
        st = j['splits']['all']['stop_ingest_W02']
        st['schema_expected'] = st['schema_after']
        st['stop_hooks_ok'] = True
        fn(j, b)
        json.dump(j, open(p, 'w'))
    return e_rows(cd)


r = doctor(lambda j, b: None)
expect('doctored rev 3, all gates met: no E row missing', 'missing' in r.values(), False)
perf = lambda r: {k: v for k, v in r.items() if k != 'E Stop'}
r = doctor(lambda j, b: j['workload'].update(equal=False, caveat='seed fingerprints differ'))
expect('doctored: workloads not equal -> perf rows missing', set(perf(r).values()), {'missing'})
expect('doctored: workloads not equal -> Stop (own W02 copies) still read', r.get('E Stop') != 'missing', True)
r = doctor(lambda j, b: j['workload'].update(must_deliver={'verdict': 'one'}))
expect('doctored: must-deliver on one build only -> missing', set(r.values()), {'missing'})
r = doctor(lambda j, b: j['workload'].update(must_deliver={'verdict': 'neither'}))
expect('doctored: must-deliver on neither -> missing', set(r.values()), {'missing'})
r = doctor(lambda j, b: j['splits']['all']['stop_ingest_W02'].update(schema_expected='99') if b == C else None)
expect('doctored: candidate schema not as expected -> Stop missing', r.get('E Stop'), 'missing')
r = doctor(lambda j, b: j['splits']['all']['perf']['store_checks'].update(all_hooks_ok=False) if b == B else None)
expect('doctored: a base hook error in the bench heartbeat -> perf rows missing', set(perf(r).values()), {'missing'})
r = doctor(lambda j, b: j['splits']['all']['stop_ingest_W02'].update(stop_hooks_ok=False) if b == B else None)
expect('doctored: a base Stop error in its heartbeat -> Stop missing', r.get('E Stop'), 'missing')
print('ALL GATES BEHAVE' if ok else 'SOME GATE MISBEHAVES')
sys.exit(0 if ok else 1)
