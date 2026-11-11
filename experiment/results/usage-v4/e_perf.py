#!/usr/bin/env python3
"""Section E, latency and cost. Nothing else may run on the machine while this runs.

  python -I e_perf.py --bin <muninn.exe> [--against <other muninn.exe>] --bench <muninn-bench.exe>
                      [--runs 7] [--stop-runs 20] [--parts perf,stop]
  (or --bench-src <tree> to build muninn-bench from that tree into the work directory)

perf. `muninn-bench perf --strict --json --muninn <bin>`, `--runs` times a build; with --against
the two builds alternate run by run, with the same bench binary. Read from the JSON (the exit
code is not used: on this machine the 1 ms gated contract fails in every build): p50/p95/p99 of
each hook and process start, and each contract's value. The rule reads the median over runs of
each read hook's p95.
stop. A copy of W02 (database, log directory, init.json), `maintain` twice so the copy is
materialised as a live store is, then one synthetic turn appended to a synthetic transcript and
`hook Stop` run after each, `--stop-runs` + 1 times; the first is the catch-up and is dropped.
With --against the two builds alternate on two copies. Wall-clock ms; the rule reads the median.
"""
import json, os, shutil, statistics as stt, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

ap = parser(__doc__)
ap.add_argument('--against')
ap.add_argument('--bench')
ap.add_argument('--bench-src')
ap.add_argument('--runs', type=int, default=7)
ap.add_argument('--stop-runs', type=int, default=20)
ap.add_argument('--parts', default='perf,stop')
args = ap.parse_args()
F = fixtures()
parts = set(args.parts.split(','))
bins = [os.path.abspath(args.bin)] + ([os.path.abspath(args.against)] if args.against else [])
ENV = {k: v for k, v in os.environ.items() if not k.startswith('MUNINN_')}
res = {b: {} for b in bins}

if 'perf' in parts:
    bench = args.bench
    if not bench:
        if not args.bench_src:
            sys.exit('--bench or --bench-src is required for perf')
        tgt = work('target', 'bench')
        r = subprocess.run(['cargo', 'build', '--release', '-p', 'muninn-bench', '--target-dir', tgt], cwd=args.bench_src, capture_output=True, text=True)
        if r.returncode:
            sys.exit('muninn-bench did not build:\n' + r.stderr[-2000:])
        bench = os.path.join(tgt, 'release', 'muninn-bench.exe' if os.name == 'nt' else 'muninn-bench')
    rows = {b: [] for b in bins}
    for i in range(args.runs):
        for b in bins:
            p = run([bench, 'perf', '--strict', '--json', '--muninn', b], 'perf', timeout=3600, ok_codes=(0, 1), text=True, env=ENV)
            line = next((l for l in p.stdout.splitlines() if l.startswith('{')), None) if p else None
            if line:
                rows[b].append(json.loads(line))
            else:
                fail('perf:no_json')
    for b in bins:
        rs = rows[b]
        hooks = {}
        for h in ('SessionStart', 'SubagentStart', 'UserPromptSubmit_gated', 'UserPromptSubmit_full'):
            p95 = [r['hook'][h][1] for r in rs]
            hooks[h] = {'p95_runs': [round(x, 3) for x in p95], 'p95_median': round(stt.median(p95), 3) if p95 else None,
                        'p50_median': round(stt.median([r['hook'][h][0] for r in rs]), 3) if rs else None}
        res[b]['perf'] = {'runs': len(rs), 'bench_sha256': sha16(bench), 'hooks': hooks,
                          'process_start_p50_median': round(stt.median([r['process_start'][0] for r in rs]), 3) if rs else None,
                          'ingest_200_ms_median': round(stt.median([r['ingest_200_ms'] for r in rs]), 1) if rs else None,
                          'contracts_failed_per_run': [[c['name'] for c in r['contracts'] if not c['ok']] for r in rs],
                          'interleaved_with': [sha16(x) for x in bins if x != b]}

if 'stop' in parts:
    def prepare(b, k):
        root = work('e_perf', 'stop', str(k))
        shutil.rmtree(root, ignore_errors=True)
        shutil.copytree(F + '/stores/W02', root + '/.muninn', ignore=shutil.ignore_patterns('muninn.db-shm', 'muninn.db-wal'))
        for _ in range(2):
            run([b, '--cwd', root, 'maintain'], 'stop:maintain', env=ENV)
        open(root + '/synthetic-session.jsonl', 'w').close()
        return root

    sid = '00000000-aaaa-bbbb-cccc-000000000001'

    def turn(root, i):
        u = {'type': 'user', 'sessionId': sid, 'cwd': root, 'timestamp': '2026-11-11T10:%02d:00.000Z' % i,
             'message': {'role': 'user', 'content': 'Synthetic audit turn number %d about the zebra pipeline widget, please look at it' % i}}
        a = {'type': 'assistant', 'sessionId': sid, 'timestamp': '2026-11-11T10:%02d:30.000Z' % i,
             'message': {'role': 'assistant', 'content': [{'type': 'text', 'text': 'Looked at the zebra pipeline widget, iteration %d. Nothing to change.' % i}]}}
        with open(root + '/synthetic-session.jsonl', 'a', newline='') as f:
            f.write(json.dumps(u) + '\n' + json.dumps(a) + '\n')

    roots = {b: prepare(b, k) for k, b in enumerate(bins)}
    ms = {b: [] for b in bins}
    for i in range(args.stop_runs + 1):
        for b in bins:
            root = roots[b]
            turn(root, i)
            inp = json.dumps({'session_id': sid, 'transcript_path': root + '/synthetic-session.jsonl', 'cwd': root, 'hook_event_name': 'Stop'})
            t0 = time.perf_counter()
            run([b, '--cwd', root, 'hook', 'Stop'], 'stop:hook', timeout=120, input=inp.encode(), env=ENV)
            ms[b].append((time.perf_counter() - t0) * 1000)
    for b in bins:
        xs = ms[b][1:]
        con = __import__('sqlite3').connect('file:%s/.muninn/muninn.db?mode=ro' % roots[b], uri=True)
        ingested = con.execute("select count(*) from record where session_id=?", (sid,)).fetchone()[0]
        con.close()
        if ingested < args.stop_runs:
            fail('stop:not_ingested')
        res[b]['stop_ingest_W02'] = {'runs': len(xs), 'median_ms': round(stt.median(xs), 1), 'p90_ms': round(sorted(xs)[int(0.9 * (len(xs) - 1))], 1),
                                     'min_ms': round(min(xs), 1), 'max_ms': round(max(xs), 1), 'records_from_synthetic_session': ingested}

for b in bins:
    a = type('A', (), {})()
    a.bin, a.labels, a.build, a.split = b, args.labels, (args.build if b == bins[0] else None), 'all'
    a.commit = args.commit if b == bins[0] else None
    write_counts('e_perf', a.build or sha16(b), a, {'all': res[b]})
