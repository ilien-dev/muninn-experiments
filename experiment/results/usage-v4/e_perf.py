#!/usr/bin/env python3
"""Section E, latency and cost. Nothing else should run on the machine while this runs.

  python -I e_perf.py --bin <base muninn.exe> --against <candidate muninn.exe>
                      --bench-base <muninn-bench of the base> --bench <muninn-bench of the candidate>
                      [--runs 7] [--stop-runs 20] [--parts perf,stop] [--commit <candidate commit>]
  (or --bench-base-src / --bench-src <tree> to build each bench into the work directory)

Harness revision 2 (`harness_rev` in the counts). Revision 1 timed both builds with one bench
built from the candidate's tree; once the schema moved past the base's, the base binary refused
that store and every base figure timed an error path. `verdict.py` reads E only from rev-2 counts.

perf. Each build is timed by a `muninn-bench` built from its own source, so each runs on a store
its own code created. `--bench-base-src` builds the base's bench from a *copy* of the base tree
in the work directory, with one change: the 8,336-row `fire_ledger` seed the candidate's bench
adds (`--ledger-seed`, on by default), so both benches seed the same workload; the `workload`
key of the counts says what was done. `muninn-bench perf --strict --json --muninn <bin>`, `--runs`
times a build, alternating base and candidate run by run. Read from the JSON (the exit code is
not used: the 1 ms gated contract fails on this machine in every build): p50/p95/p99 of each hook.
Every run is checked: the bench's JSON must hold all four hooks and the run count asked for, and
the store the bench left (under a private TEMP) is opened by the measured binary through its own
hooks: every hook invocation of the run (the bench's 4 x 300 and two of the harness's) must be
logged in the store's heartbeat as finished ok with no error, and the harness's two must leave
nothing on stderr. Any miss is a failure and no counts are written.
stop. Each build gets its own fresh copy of W02 (database, log directory, init.json). Its first
`maintain` is the write open that migrates the copy to the build's schema; it is timed and
reported apart (`first_write_open_ms`), then a second `maintain`, then one synthetic turn
appended and `hook Stop` run after each, `--stop-runs` + 1 times, builds alternating; the first
Stop is the catch-up and is dropped. Wall-clock ms; the rule reads the median.
"""
import glob, json, os, re, shutil, sqlite3, statistics as stt, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

HARNESS_REV = 2
ap = parser(__doc__)
ap.add_argument('--against')
ap.add_argument('--bench', help='muninn-bench built from the candidate (--against) tree')
ap.add_argument('--bench-src')
ap.add_argument('--bench-base', help='muninn-bench built from the base (--bin) tree')
ap.add_argument('--bench-base-src')
ap.add_argument('--no-ledger-seed', action='store_true', help='build the base bench from its tree unchanged')
ap.add_argument('--runs', type=int, default=7)
ap.add_argument('--stop-runs', type=int, default=20)
ap.add_argument('--parts', default='perf,stop')
args = ap.parse_args()
F = fixtures()
parts = set(args.parts.split(','))
base_bin = os.path.abspath(args.bin)
cand_bin = os.path.abspath(args.against) if args.against else None
bins = [base_bin] + ([cand_bin] if cand_bin else [])
ENV = {k: v for k, v in os.environ.items() if not k.startswith('MUNINN_')}
res = {b: {} for b in bins}
workload = {}

SEED = '''    // usage-v4 harness: the fire_ledger seed of the candidate's bench, so both benches seed the
    // same workload (8 336 rows under the session the hooks run with).
    {
        let tx = db.write_tx()?;
        {
            let mut st = tx.prepare(
                "INSERT INTO fire_ledger(session_id, compaction_epoch, record_id, fired_at, tokens, reason) \\
                 VALUES('b', 0, ?1, ?2, 0, ?3)",
            )?;
            for i in 0..8_336usize {
                let reason = match i % 10 {
                    0..=7 => "literal:gated:budget:54",
                    8 => "literal:cue:event:post_compact",
                    _ => "literal:literal",
                };
                let id = (rng.next() as usize % records) as i64 + 1;
                st.execute(rusqlite::params![
                    id,
                    1_700_000_000_000i64 + i as i64,
                    reason
                ])?;
            }
        }
        tx.commit()?;
    }
'''


def build_bench(src, name, seed=False):
    tree = os.path.abspath(src)
    if seed:
        # a copy of the tree in the work directory; the source tree itself is never written
        copy = work('e_perf', 'bench-src-' + name)
        shutil.rmtree(copy, ignore_errors=True)
        shutil.copytree(tree, copy, ignore=shutil.ignore_patterns('target', '.git', '.muninn', 'node_modules', 'corpora', 'research', 'site'))
        mp = os.path.join(copy, 'crates', 'muninn-bench', 'src', 'main.rs')
        s = open(mp, encoding='utf-8').read()
        if 'INSERT INTO fire_ledger(session_id, compaction_epoch' in s:
            workload['base_bench'] = 'tree already seeds the ledger; built unchanged'
        else:
            anchor = '    tx.commit()?;\n    // The index a store actually has'
            if anchor not in s:
                m = re.search(r'\n    tx\.commit\(\)\?;\n', s[s.index('fn populate'):])
                if not m:
                    sys.exit('cannot place the ledger seed in the base bench')
                at = s.index('fn populate') + m.end()
                s = s[:at] + SEED + s[at:]
            else:
                s = s.replace(anchor, '    tx.commit()?;\n' + SEED + '    // The index a store actually has', 1)
            open(mp, 'w', encoding='utf-8', newline='\n').write(s)
            workload['base_bench'] = 'copy of the base tree with the candidate bench\'s 8,336-row fire_ledger seed added after the cue load'
            workload['base_bench_main_rs_sha256'] = sha16(mp)
        tree = copy
    tgt = work('target', 'bench-' + name)
    r = run(['cargo', 'build', '--release', '--locked', '-p', 'muninn-bench', '--target-dir', tgt], 'bench:build:' + name, timeout=3600, cwd=tree, text=True)
    if r is None or r.returncode:
        sys.exit('muninn-bench (%s) did not build:\n%s' % (name, (r.stderr if r else '')[-2000:]))
    return os.path.join(tgt, 'release', 'muninn-bench.exe' if os.name == 'nt' else 'muninn-bench')


ENV_ERR = re.compile(r'error|panic|schema|newer|unable', re.I)


def check_store(b, tmp):
    """The store the bench left behind, opened by the binary it timed, through its own hooks."""
    dirs = glob.glob(os.path.join(tmp, 'muninn-bench-*'))
    if len(dirs) != 1 or not os.path.isfile(os.path.join(dirs[0], '.muninn', 'muninn.db')):
        fail('perf:no_bench_store')
        return None
    root = dirs[0].replace('\\', '/')
    con = sqlite3.connect('file:%s/.muninn/muninn.db?mode=ro' % root, uri=True)
    ver = con.execute("select value from meta where key='schema_version'").fetchone()
    ledger = con.execute('select count(*) from fire_ledger').fetchone()[0]
    con.close()
    ok = True
    delivered = {}
    for event, payload in (('SessionStart', {'session_id': 'check'}),
                           ('UserPromptSubmit', {'session_id': 'check', 'prompt': 'implement retry backoff for the webhook handler with idempotent tokens'})):
        inp = json.dumps(dict(payload, hook_event_name=event, cwd=root))
        r = run([b, 'hook', event], 'perf:check:' + event, timeout=120, cwd=root, input=inp.encode(), env=ENV)
        if r is None:
            ok = False
            continue
        if ENV_ERR.search(r.stderr.decode('utf-8', 'replace')):
            fail('perf:check:%s:stderr' % event)
            ok = False
        try:
            text = json.loads(r.stdout.decode('utf-8'))['hookSpecificOutput']['additionalContext']
        except Exception:
            text = ''
        delivered[event] = bool(block_ids(text))
    # every hook invocation of the run, the bench's and these two, as the binary logged it
    fin = bad = 0
    hb = os.path.join(root, '.muninn', 'log', 'heartbeat.jsonl')
    for l in (open(hb, encoding='utf-8', errors='replace') if os.path.isfile(hb) else []):
        try:
            v = json.loads(l)
        except ValueError:
            continue
        if v.get('ev') == 'finish':
            fin += 1
            bad += not v.get('ok') or v.get('err') is not None
    if bad or fin < 4 * 300 + 2:
        fail('perf:check:heartbeat')
        ok = False
    shutil.rmtree(dirs[0], ignore_errors=True)
    return {'schema_version': ver[0] if ver else None, 'fire_ledger_rows': ledger, 'hooks_ok': ok, 'hook_finishes': fin, 'hook_errors': bad, 'delivered': delivered}


if 'perf' in parts:
    if not cand_bin:
        sys.exit('E compares two builds: give --against <candidate muninn.exe>')
    bench_base = args.bench_base or (build_bench(args.bench_base_src, 'base', seed=not args.no_ledger_seed) if args.bench_base_src else None)
    bench_cand = args.bench or (build_bench(args.bench_src, 'cand') if args.bench_src else None)
    if not bench_base or not bench_cand:
        sys.exit('--bench-base/--bench-base-src and --bench/--bench-src are both required for perf')
    if args.bench_base and 'base_bench' not in workload:
        workload['base_bench'] = 'given by --bench-base (%s)' % sha16(bench_base)
    benches = {base_bin: bench_base, cand_bin: bench_cand}
    rows = {b: [] for b in bins}
    checks = {b: [] for b in bins}
    for i in range(args.runs):
        for b in bins:
            tmp = work('e_perf', 'tmp', 'run-%d-%d' % (i, bins.index(b)))
            shutil.rmtree(tmp, ignore_errors=True)
            os.makedirs(tmp)
            env = dict(ENV, TEMP=tmp.replace('/', '\\'), TMP=tmp.replace('/', '\\'), TMPDIR=tmp)
            p = run([benches[b], 'perf', '--strict', '--json', '--muninn', b], 'perf', timeout=3600, ok_codes=(0, 1), text=True, env=env)
            line = next((l for l in p.stdout.splitlines() if l.startswith('{')), None) if p else None
            if not line:
                fail('perf:no_json')
                continue
            j = json.loads(line)
            if j.get('runs') != 300 or any(h not in j.get('hook', {}) for h in ('SessionStart', 'SubagentStart', 'UserPromptSubmit_gated', 'UserPromptSubmit_full')):
                fail('perf:incomplete_json')
            if p.stderr and ENV_ERR.search(re.sub(r'Error: \d+ contract\(s\) exceeded', '', p.stderr)):
                fail('perf:bench_stderr')
            rows[b].append(j)
            checks[b].append(check_store(b, tmp))
    led = {b: sorted({c['fire_ledger_rows'] for c in checks[b] if c}) for b in bins}
    workload['fire_ledger_rows_per_bench_store'] = {sha16(b): led[b] for b in bins}
    workload['equal'] = all(v and min(v) >= 8336 for v in led.values())  # both stores hold the 8,336-row seed
    if not workload['equal']:
        workload['caveat'] = 'the two benches seeded different workloads: the comparison is each build\'s own contract run'
    for b in bins:
        rs = rows[b]
        hooks = {}
        for h in ('SessionStart', 'SubagentStart', 'UserPromptSubmit_gated', 'UserPromptSubmit_full'):
            p95 = [r['hook'][h][1] for r in rs]
            hooks[h] = {'p95_runs': [round(x, 3) for x in p95], 'p95_median': round(stt.median(p95), 3) if p95 else None,
                        'p50_median': round(stt.median([r['hook'][h][0] for r in rs]), 3) if rs else None}
        res[b]['perf'] = {'runs': len(rs), 'bench_sha256': sha16(benches[b]), 'hooks': hooks,
                          'store_checks': {'schema_versions': sorted({str(c['schema_version']) for c in checks[b] if c}),
                                           'all_hooks_ok': all(c and c['hooks_ok'] for c in checks[b]),
                                           'hook_finishes': sum(c['hook_finishes'] for c in checks[b] if c),
                                           'hook_errors': sum(c['hook_errors'] for c in checks[b] if c),
                                           'check_prompts_delivered': [c['delivered'] for c in checks[b] if c][:1]},
                          'process_start_p50_median': round(stt.median([r['process_start'][0] for r in rs]), 3) if rs else None,
                          'ingest_200_ms_median': round(stt.median([r['ingest_200_ms'] for r in rs]), 1) if rs else None,
                          'contracts_failed_per_run': [[c['name'] for c in r['contracts'] if not c['ok']] for r in rs],
                          'interleaved_with': [sha16(x) for x in bins if x != b]}

if 'stop' in parts:
    def schema(root):
        con = sqlite3.connect('file:%s/.muninn/muninn.db?mode=ro' % root, uri=True)
        v = con.execute("select value from meta where key='schema_version'").fetchone()
        con.close()
        return v[0] if v else None

    def prepare(b, k):
        root = work('e_perf', 'stop', str(k))
        shutil.rmtree(root, ignore_errors=True)
        shutil.copytree(F + '/stores/W02', root + '/.muninn', ignore=shutil.ignore_patterns('muninn.db-shm', 'muninn.db-wal'))
        before = schema(root)
        t0 = time.perf_counter()
        r = run([b, '--cwd', root, 'maintain'], 'stop:maintain', env=ENV)  # the write open that migrates the copy
        first = (time.perf_counter() - t0) * 1000
        if r is not None and ENV_ERR.search(r.stderr.decode('utf-8', 'replace')):
            fail('stop:maintain:stderr')
        run([b, '--cwd', root, 'maintain'], 'stop:maintain', env=ENV)
        open(root + '/synthetic-session.jsonl', 'w').close()
        return root, {'schema_before': before, 'schema_after': schema(root), 'first_write_open_ms': round(first, 1)}

    sid = '00000000-aaaa-bbbb-cccc-000000000001'

    def turn(root, i):
        u = {'type': 'user', 'sessionId': sid, 'cwd': root, 'timestamp': '2026-11-11T10:%02d:00.000Z' % i,
             'message': {'role': 'user', 'content': 'Synthetic audit turn number %d about the zebra pipeline widget, please look at it' % i}}
        a = {'type': 'assistant', 'sessionId': sid, 'timestamp': '2026-11-11T10:%02d:30.000Z' % i,
             'message': {'role': 'assistant', 'content': [{'type': 'text', 'text': 'Looked at the zebra pipeline widget, iteration %d. Nothing to change.' % i}]}}
        with open(root + '/synthetic-session.jsonl', 'a', newline='') as f:
            f.write(json.dumps(u) + '\n' + json.dumps(a) + '\n')

    prep = {b: prepare(b, k) for k, b in enumerate(bins)}
    ms = {b: [] for b in bins}
    for i in range(args.stop_runs + 1):
        for b in bins:
            root = prep[b][0]
            turn(root, i)
            inp = json.dumps({'session_id': sid, 'transcript_path': root + '/synthetic-session.jsonl', 'cwd': root, 'hook_event_name': 'Stop'})
            t0 = time.perf_counter()
            r = run([b, '--cwd', root, 'hook', 'Stop'], 'stop:hook', timeout=120, input=inp.encode(), env=ENV)
            ms[b].append((time.perf_counter() - t0) * 1000)
            if r is not None and ENV_ERR.search(r.stderr.decode('utf-8', 'replace')):
                fail('stop:hook:stderr')
    for b in bins:
        root, info = prep[b]
        xs = ms[b][1:]
        con = sqlite3.connect('file:%s/.muninn/muninn.db?mode=ro' % root, uri=True)
        ingested = con.execute("select count(*) from record where session_id=?", (sid,)).fetchone()[0]
        con.close()
        if ingested < args.stop_runs:
            fail('stop:not_ingested')
        res[b]['stop_ingest_W02'] = dict(info, runs=len(xs), median_ms=round(stt.median(xs), 1), p90_ms=round(sorted(xs)[int(0.9 * (len(xs) - 1))], 1),
                                         min_ms=round(min(xs), 1), max_ms=round(max(xs), 1), records_from_synthetic_session=ingested,
                                         interleaved_with=[sha16(x) for x in bins if x != b])

for b in bins:
    a = type('A', (), {})()
    a.bin, a.labels, a.split = b, args.labels, 'all'
    a.build = args.build if b == bins[0] else None
    a.commit = args.commit if b == cand_bin else None
    write_counts('e_perf', a.build or sha16(b), a, {'all': res[b]}, {'harness_rev': HARNESS_REV, 'workload': workload})
