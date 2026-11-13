#!/usr/bin/env python3
"""Section B, retirement. Three parts, each selectable with --parts (default b1,b2,b3).

  python -I b_retire.py --bin <muninn.exe> [--parts b1,b2,b3] [--jobs 6]

B1. usage-v1's replay (`../usage-v1/replay.py`, run unchanged from a private copy of its
    directory layout) on two corpora:
    - the usage-v1 store snapshots of the four projects that hold its 95 labelled retirements;
    - today's store copies of W02 and L01, for the 13 typed retirements by a user decision since
      1.2.0 (WP-06), labelled in this review with usage-v1's codes. L01's transcripts are read
      through the WSL share and its project is replayed without git (its 13 are conversational).
    Each labelled item is found in the replayed store as usage-v1's `score.py` finds it (a key
    of its text and its kind) and read as active, retired or absent. The rule reads retired items
    labelled `loss`, and whether both `valid` items are retired.
B2. Three synthetic repositories, written before any fix:
    - reword: one commit rewords a README line so a word that three recorded statements contain
      leaves that line (it stays in two other tracked files); counted: typed records retired,
      `said:` records created.
    - aba: "We go with Postgres for the job queue." / "Actually, switch the job queue to Redis
      instead of Postgres." / the first sentence again, ingested per turn; then a fresh
      UserPromptSubmit asks about the job queue. Counted from the hook's output: whether a block
      states A, whether one states B (any kind, and typed records only), and the active decisions.
    - revert: a commit that introduces a value, then `git revert` of it, then one `maintain`
      (and, as a second reading, maintain between the two); counted: whether the reverted
      commit's record is retired.
B3. The loop-8 held-out set through both evaluators, arms both and noise, orders adjacent and
    blocks: `../../loop8/eval_all.py` as registered, and `../usage-v1/eval_dated.py`, the dated
    copy usage-v1's amendment adopted because the undated one dates commits before their messages.

The B items are not split (B1 is a design set by construction, B3 is held-out by construction);
the counts are written under `all` whatever --split says.
"""
import collections, concurrent.futures as cf, json, os, shutil, sqlite3, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from inputs import staged, staged_git

ap = parser(__doc__)
ap.add_argument('--parts', default='b1,b2,b3')
ap.add_argument('--jobs', type=int, default=6)
ap.add_argument('--score-only', action='store_true', help='b1: score the replayed stores already in the work directory')
args = ap.parse_args()
F = fixtures()
L = local()
build = build_name(args)
BIN = os.path.abspath(args.bin).replace('\\', '/')
EXP = os.path.dirname(os.path.dirname(HERE))
parts = set(args.parts.split(','))
out = {}


# ---------------------------------------------------------------------------------------------- B1
def b1():
    lab = L['project_labels']
    rundir = work('b_retire', 'runner')
    input_counts = {}
    shutil.copyfile(os.path.join(EXP, 'results', 'usage-v1', 'replay.py'), os.path.join(rundir, 'replay.py'))
    projects = work('b_retire', 'projects_staged')
    corpora = []
    # tenth amendment: replay.py reads only staged copies of the transcripts (inputs.py stage); each
    # corpus gets a store that holds only the staged paths, the one thing replay.py reads from it
    names = [(proj, proj) for proj in sorted(os.listdir(F + '/fixtures/usage-v1/stores'))] + [(st + 'now', L['label_projects'].get(st)) for st in ('W02', 'L01')]
    for name, proj in names:
        paths, c = staged('b1:' + name)
        input_counts[(lab.get(name) or name).replace('now', '-now')] = c
        d = os.path.join(rundir, 'stores', name)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, 'muninn.db')
        if os.path.exists(p):
            os.remove(p)
        dst = sqlite3.connect(p)
        dst.execute('create table record (transcript_ref text)')
        dst.executemany('insert into record values (?)', [(sp + ':0',) for sp in sorted(paths.values())])
        dst.commit()
        dst.close()
        corpora.append((name, proj))
    if any(c['status'] != 'ok' for c in input_counts.values()):
        return {'status': 'missing input', 'inputs': input_counts}
    for name, proj in corpora:
        link = os.path.join(projects, name)
        target = staged_git(proj) if proj else None  # the staged clone, never the live checkout
        if target and os.path.isdir(os.path.join(target, '.git')) and not os.path.exists(link):
            subprocess.run(['cmd', '/c', 'mklink', '/J', link.replace('/', '\\'), target.replace('/', '\\')], capture_output=True)
    rp = work('b_retire', 'rp')
    env = dict(os.environ, PROJECTS_DIR=projects)
    t0 = time.time()

    def marker(name):
        return os.path.join(rp, build, name + '.done.json')

    def one(name):
        if os.path.exists(marker(name)):
            os.remove(marker(name))
        r = run([sys.executable, '-I', os.path.join(rundir, 'replay.py'), BIN, build, name, rp], 'b1:replay', timeout=7200, env=env, text=True)
        try:
            v = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            fail('b1:replay:no_output')
            v = {'error': 'no output'}
        if 'error' in v:
            fail('b1:replay:error')
        elif r is not None and r.returncode == 0:  # a marker only for a replay that exited 0
            json.dump({k: v[k] for k in ('sessions', 'batches', 'git', 's') if k in v}, open(marker(name), 'w'))
        v.pop('p', None)
        return name, v

    stats = {}
    prev = os.path.join(COUNTS, 'b_retire_%s.json' % build)
    if args.score_only and os.path.isfile(prev):
        old = json.load(open(prev))['splits']['all'].get('b1', {})
        stats, t0 = old.get('replay', {}), time.time() - old.get('wall_s', 0)
    with cf.ThreadPoolExecutor(args.jobs) as ex:
        for name, v in ex.map(one, [] if args.score_only else [c[0] for c in sorted(corpora, key=lambda c: c[0] != 'W02now')]):
            key = (lab.get(name) or name).replace('now', '-now')
            stats[key] = {k: v[k] for k in ('sessions', 'batches', 'git', 's', 'error') if k in v}
    # score only replays that finished in this run, or, with --score-only, in an earlier one
    for name, _ in corpora:
        if not os.path.exists(marker(name)):
            fail('b1:replay_not_finished')

    def state(db, key, kind):
        if not os.path.exists(db):
            fail('b1:no_replayed_store')
            return 'noproj', 'noproj'
        c = sqlite3.connect('file:%s?mode=ro' % db, uri=True)
        k = key.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        rows = c.execute("select invalid from record where body like ? escape '\\' and kind=? order by created_at, id", ('%' + k + '%', kind)).fetchall()
        c.close()
        if not rows:
            return 'absent', 'absent'
        # score.py's reading: active if any row with the key is active. The earliest row is the
        # statement itself; a later row with the same opening (a restatement) can make score.py
        # read a retired item as active, so both are kept.
        anyrow = 'active' if any(r[0] == 0 for r in rows) else 'retired'
        first = 'active' if rows[0][0] == 0 else 'retired'
        return anyrow, first

    def state_free(db, key):
        """Twelfth amendment: the same reading among every typed kind but `episode`."""
        if not os.path.exists(db):
            return 'noproj', 'noproj'
        c = sqlite3.connect('file:%s?mode=ro' % db, uri=True)
        k = key.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        rows = c.execute("select invalid from record where body like ? escape '\\' and kind <> 'episode' order by created_at, id", ('%' + k + '%',)).fetchall()
        c.close()
        if not rows:
            return 'absent', 'absent'
        return ('active' if any(r[0] == 0 for r in rows) else 'retired'), ('active' if rows[0][0] == 0 else 'retired')

    def free_key(text):
        """The first line of the old body without a leading `user: ` label, its first 70 characters."""
        line = text.split('\n')[0]
        if line.startswith('user: '):
            line = line[len('user: '):]
        return line[:70]

    S1 = json.load(open(F + '/fixtures/usage-v1/label/sup.json', encoding='utf8'))
    O1 = {(x['p'], int(x['id'])): x for x in json.load(open(F + '/fixtures/usage-v1/label/sup.out.json', encoding='utf8'))}
    v1 = collections.Counter()
    items = {}
    for s in S1:
        db = os.path.join(rp, build, s['p'], '.muninn', 'muninn.db')
        st, st1 = state(db, s['old'].split('\n')[0][:70], s['kind'])
        fr, fr1 = state_free(db, free_key(s['old']))
        o = O1[(s['p'], int(s['id']))]
        iid = 'v1:%s:%s' % (lab.get(s['p'], '?'), s['id'])
        items[iid] = {'label': o['label'], 'loss': bool(o['loss']), 'state': st, 'earliest': st1, 'free': fr, 'free_earliest': fr1}
        v1['%s:%s' % (o['label'], st)] += 1
        v1['%s:%s' % ('loss' if o['loss'] else 'noloss', st)] += 1
    S2 = [json.loads(l) for l in open(F + '/out/usage-v4/labels/b_since120.jsonl', encoding='utf-8')]
    v2 = collections.Counter()
    for s in S2:
        db = os.path.join(rp, build, s['store'] + 'now', '.muninn', 'muninn.db')
        st, st1 = state(db, s['key'], s['kind'])
        fr, fr1 = state_free(db, free_key(s['key']))
        iid = 'now:%s:%d' % (s['store'], s['id'])
        items[iid] = {'label': s['label'], 'loss': bool(s['loss']), 'state': st, 'earliest': st1, 'free': fr, 'free_earliest': fr1}
        v2['%s:%s' % (s['label'], st)] += 1
        v2['%s:%s' % ('loss' if s['loss'] else 'noloss', st)] += 1
    totals = {}
    for name in sorted(os.listdir(os.path.join(rp, build))):
        db = os.path.join(rp, build, name, '.muninn', 'muninn.db')
        if not os.path.exists(db):
            continue
        c = sqlite3.connect('file:%s?mode=ro' % db, uri=True)
        t = collections.Counter()
        for k, i, n in c.execute('select kind, invalid, count(*) from record group by 1, 2'):
            t['%s%d' % (k, i)] += n
        t['typed_superseded_heir'] = c.execute("select count(*) from record where invalid=1 and invalid_reason='superseded' and invalidated_by is not null and kind!='episode'").fetchone()[0]
        t['typed_superseded_noheir'] = c.execute("select count(*) from record where invalid=1 and invalid_reason='superseded' and invalidated_by is null and kind!='episode'").fetchone()[0]
        t['older_heir'] = c.execute("select count(*) from record r join record h on h.id=r.invalidated_by where r.invalid=1 and h.created_at<r.created_at").fetchone()[0]
        c.close()
        totals[(lab.get(name) or name).replace('now', '-now')] = dict(t)
    loss_ret = sum(1 for v in items.values() if v['loss'] and v['state'] == 'retired')
    # twelfth amendment: where the kind-bound reading is absent, the kind-free one binds
    for v in items.values():
        v['bind'] = v['free'] if v['state'] == 'absent' else v['state']
        v['bind_earliest'] = v['free_earliest'] if v['earliest'] == 'absent' else v['earliest']
    return {
        'status': 'ok', 'inputs': input_counts,
        'usage_v1_95': dict(v1), 'since_1_2_0_13': dict(v2),
        'loss_retired_total': loss_ret,
        'loss_retired_v1': sum(1 for k, v in items.items() if k.startswith('v1:') and v['loss'] and v['state'] == 'retired'),
        'loss_retired_since120': sum(1 for k, v in items.items() if k.startswith('now:') and v['loss'] and v['state'] == 'retired'),
        'valid_states': {k: v['state'] for k, v in items.items() if v['label'] == 'valid'},
        'valid_states_earliest_row': {k: v['earliest'] for k, v in items.items() if v['label'] == 'valid'},
        'loss_retired_total_earliest_row': sum(1 for v in items.values() if v['loss'] and v['earliest'] == 'retired'),
        'item_states_earliest_row': {k: v['earliest'] for k, v in sorted(items.items())},
        'item_states': {k: v['state'] for k, v in sorted(items.items())},
        'kind_free': {
            'item_states': {k: v['free'] for k, v in sorted(items.items())},
            'item_states_earliest_row': {k: v['free_earliest'] for k, v in sorted(items.items())},
            'split': dict(collections.Counter(v['free'] for v in items.values())),
            'split_earliest_row': dict(collections.Counter(v['free_earliest'] for v in items.values())),
            'binding_item_states': {k: v['bind'] for k, v in sorted(items.items())},
            'binding_split': dict(collections.Counter(v['bind'] for v in items.values())),
            'binding_split_earliest_row': dict(collections.Counter(v['bind_earliest'] for v in items.values())),
            'loss_retired_total': sum(1 for v in items.values() if v['loss'] and v['bind'] == 'retired'),
            'loss_retired_total_earliest_row': sum(1 for v in items.values() if v['loss'] and v['bind_earliest'] == 'retired'),
            'valid_states_earliest_row': {k: v['bind_earliest'] for k, v in items.items() if v['label'] == 'valid'},
            'valid_states': {k: v['bind'] for k, v in items.items() if v['label'] == 'valid'},
        },
        'store_totals': totals, 'replay': stats, 'wall_s': round(time.time() - t0),
    }


# ---------------------------------------------------------------------------------------------- B2
def git(root, *a, date=None):
    e = dict(os.environ, GIT_AUTHOR_NAME='a', GIT_AUTHOR_EMAIL='a@b', GIT_COMMITTER_NAME='a', GIT_COMMITTER_EMAIL='a@b')
    if date:
        e['GIT_AUTHOR_DATE'] = e['GIT_COMMITTER_DATE'] = date
    r = run(['git', '-C', root] + list(a), 'b2:git:' + a[0], env=e, text=True)
    return r if r is not None else subprocess.CompletedProcess(a, 1, '', '')


def mun(root, *a):
    """A muninn write command on a synthetic store; a non-zero exit or an error on stderr counts."""
    r = run([BIN, '--cwd', root] + list(a), 'b2:' + a[0], env=ENV)
    if r is not None and b'error' in r.stderr.lower():
        fail('b2:%s:stderr' % a[0])
    return r


def fresh(name):
    root = work('b_retire', 'b2', build, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, '.muninn', 'log'))
    open(os.path.join(root, '.muninn', 'muninn.db'), 'w').close()
    return root


ENV = {k: v for k, v in os.environ.items() if not k.startswith('MUNINN_')}


def msg(sid, root, i, text, reply='Understood.', minute=0, day='2026-11-02'):
    u = {'type': 'user', 'sessionId': sid, 'cwd': root, 'timestamp': '%sT10:%02d:00.000Z' % (day, minute + i), 'message': {'role': 'user', 'content': text}}
    a = {'type': 'assistant', 'sessionId': sid, 'timestamp': '%sT10:%02d:30.000Z' % (day, minute + i), 'message': {'role': 'assistant', 'content': [{'type': 'text', 'text': reply}]}}
    return json.dumps(u) + '\n' + json.dumps(a) + '\n'


def typed(root):
    c = sqlite3.connect(os.path.join(root, '.muninn', 'muninn.db'))
    r = c.execute("select id, kind, origin, invalid, subject, object, body from record order by id").fetchall()
    c.close()
    return r


def b2():
    res = {}
    # reword ----------------------------------------------------------------------------------
    root = fresh('reword')
    git(root, 'init', '-q')
    open(os.path.join(root, 'README.md'), 'w', newline='\n').write('# Demo\n\nThe heron mascot is on the cover page.\n\nSee docs/birds.md for the heron notes.\n')
    os.makedirs(os.path.join(root, 'docs'))
    open(os.path.join(root, 'docs', 'birds.md'), 'w', newline='\n').write('The heron scheduler runs the nightly batch jobs.\n')
    open(os.path.join(root, '.gitignore'), 'w').write('.muninn/\n*.jsonl\n')
    git(root, 'add', '-A')
    git(root, 'commit', '-q', '-m', 'initial', date='2026-11-01T09:00:00Z')
    tp = os.path.join(root, 'session.jsonl')
    sid = '00000000-aaaa-bbbb-cccc-000000000002'
    with open(tp, 'w', newline='') as f:
        for i, m in enumerate(['We go with the heron scheduler for the nightly batch jobs.',
                               'Never deploy on Fridays without running the heron checklist first.',
                               'No, the heron scheduler must keep its retry budget in the config file.']):
            f.write(msg(sid, root, i, m))
    mun(root, 'ingest', tp)
    before = {r[0] for r in typed(root) if r[3] == 0}
    open(os.path.join(root, 'README.md'), 'w', newline='\n').write('# Demo\n\nThe mascot is on the cover page.\n\nSee docs/birds.md for the heron notes.\n')
    git(root, 'add', '-A')
    git(root, 'commit', '-q', '-m', 'docs: reword the cover sentence', date='2026-11-03T09:00:00Z')
    mun(root, 'maintain')
    after = typed(root)
    res['reword'] = {'records_before': len(before),
                     'retired': sum(1 for r in after if r[0] in before and r[3] == 1),
                     'retired_typed': sum(1 for r in after if r[0] in before and r[3] == 1 and r[1] != 'episode'),
                     'said_records_created': sum(1 for r in after if r[2] == 'commit_linked' and r[4].startswith('said:'))}
    # aba ---------------------------------------------------------------------------------------
    root = fresh('aba')
    tp = os.path.join(root, 't.jsonl')
    sid = '00000000-aaaa-bbbb-cccc-000000000042'
    A = 'We go with Postgres for the job queue.'
    B = 'Actually, switch the job queue to Redis instead of Postgres.'
    open(tp, 'w').close()
    for i, (m, rep) in enumerate([(A, 'Understood.'), (B, 'Understood, switching the job queue from Postgres to Redis.'), (A, 'Understood.')]):
        with open(tp, 'a', newline='') as f:
            f.write(msg(sid, root, i, m, rep, day='2026-11-05'))
        mun(root, 'ingest', tp)
    text = hook(BIN, 'UserPromptSubmit', root, {'session_id': 'b2-aba-ask', 'prompt': 'Which store do we use for the job queue now?'}, env=ENV)
    blocks = [b for b in text.split('\n[muninn:') if b.strip()]
    tb = [b for b in blocks if not b.startswith('episode') and not b.startswith('[muninn:episode')]
    a_in = lambda bs: any('go with postgres for the job queue' in b.lower() for b in bs)
    b_in = lambda bs: any('switch the job queue to redis' in b.lower() for b in bs)
    rows = typed(root)
    res['aba'] = {'served_A_any_block': a_in(blocks), 'served_B_any_block': b_in(blocks),
                  'served_A_typed': a_in(tb), 'served_B_typed': b_in(tb), 'blocks': len(block_ids(text)),
                  'active_decisions_A': sum(1 for r in rows if r[1] == 'decision' and r[3] == 0 and 'go with postgres' in r[6].lower()),
                  'active_decisions_B': sum(1 for r in rows if r[1] == 'decision' and r[3] == 0 and 'redis' in r[6].lower())}
    # revert ------------------------------------------------------------------------------------
    for variant in ('one_maintain', 'maintain_between'):
        root = fresh('revert_' + variant)
        git(root, 'init', '-q')
        open(os.path.join(root, '.gitignore'), 'w').write('.muninn/\n*.jsonl\n')
        open(os.path.join(root, 'package.json'), 'w', newline='\n').write('{\n  "name": "demo",\n  "devDependencies": {\n    "jest": "29.7.0"\n  }\n}\n')
        git(root, 'add', '-A')
        git(root, 'commit', '-q', '-m', 'initial', date='2026-11-01T09:00:00Z')
        tp = os.path.join(root, 'session.jsonl')
        with open(tp, 'w', newline='') as f:
            f.write(msg('00000000-aaaa-bbbb-cccc-000000000077', root, 0, 'We test with jest for the unit tests.'))
        mun(root, 'ingest', tp)
        open(os.path.join(root, 'package.json'), 'w', newline='\n').write('{\n  "name": "demo",\n  "devDependencies": {\n    "vitest": "2.1.0"\n  }\n}\n')
        git(root, 'add', '-A')
        git(root, 'commit', '-q', '-m', 'use vitest instead of jest for the unit tests', date='2026-11-03T09:00:00Z')
        head = git(root, 'rev-parse', 'HEAD').stdout.strip()
        if variant == 'maintain_between':
            mun(root, 'maintain')
        git(root, 'revert', '--no-edit', head, date='2026-11-03T10:00:00Z')
        if variant == 'maintain_between':
            # the first maintain moved both git watermarks to now, past the pinned commit dates;
            # set them back to 09:30, after the reverted commit and before its revert, as usage-v1's replay does
            con = sqlite3.connect(os.path.join(root, '.muninn', 'muninn.db'))
            for k in ('git_watermark_ms', 'values_watermark_ms'):
                con.execute('insert or replace into meta(key, value) values(?, ?)', (k, '1793698200000'))
            con.commit()
            con.close()
        mun(root, 'maintain')
        rows = typed(root)
        tgt = [r for r in rows if r[2] == 'commit_linked' and head[:7] in (r[4] + r[6]) and 'revert' not in r[5].lower()]
        res['revert_' + variant] = {'reverted_commit_records': len(tgt), 'reverted_commit_retired': sum(1 for r in tgt if r[3] == 1),
                                    'revert_deadends': sum(1 for r in rows if r[1] == 'deadend'),
                                    'jest_decision_active': sum(1 for r in rows if r[1] == 'decision' and r[2] == 'user_said' and r[3] == 0 and 'jest' in r[5].lower())}
    return res


# ---------------------------------------------------------------------------------------------- B3
def b3():
    res = {}
    ph = os.path.join(EXP, 'loop8', 'heldout_phrasings.json')
    sc = os.path.join(EXP, 'loop8', 'scenarios.json')
    o = work('b_retire', 'b3', build)
    for ev, path in (('dated', os.path.join(EXP, 'results', 'usage-v1', 'eval_dated.py')), ('registered', os.path.join(EXP, 'loop8', 'eval_all.py'))):
        for arm in ('both', 'noise'):
            for order in ('adjacent', 'blocks'):
                f = os.path.join(o, '%s_%s_%s.json' % (ev, arm, order))
                if os.path.exists(f):
                    os.remove(f)
                run([sys.executable, '-I', path, '--muninn', BIN, '--arm', arm, '--order', order,
                     '--phrasings', ph, '--scenarios', sc, '--out', f], 'b3:' + ev, timeout=1800, env=ENV)
                if not os.path.isfile(f):
                    fail('b3:no_output')
                    continue
                rows = json.load(open(f))
                if len(rows) != 30:
                    fail('b3:cells')
                res['%s/%s/%s' % (ev, arm, order)] = {k: '%d/%d' % (sum(1 for r in rows if r.get(k)), len(rows)) for k in ('retired_a', 'kept_b', 'served_ok', 'old_served')}
    return res


if 'b1' in parts:
    out['b1'] = b1()
if 'b2' in parts:
    out['b2'] = b2()
if 'b3' in parts:
    out['b3'] = b3()
BINDING = {'b1_loss': 'loss_retired_total (score.py rule); loss_retired_total_earliest_row is secondary',
           'b1_valid': 'valid_states_earliest_row; valid_states (score.py rule) is secondary',
           'b2_reword': 'reword.retired (any kind) == 0; retired_typed is secondary',
           'b2_aba': 'served_A_typed and not served_B_typed', 'b2_revert': 'revert_one_maintain.reverted_commit_retired',
           'b3': 'registered/* (loop8/eval_all.py); noise retired_a <= base; dated/* is secondary'}
write_counts('b_retire', build, args, {'all': out}, {'note': 'B is not split; see the docstring', 'binding': BINDING})
