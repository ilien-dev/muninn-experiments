#!/usr/bin/env python3
"""Section A, extraction. Runs the `extract_dump` example of a source tree over the sessions that
hold the labelled items, and scores what it emits. No model runs.

  python -I a_extract.py --bin <muninn.exe> --src <source tree> [--split design|heldout|all] [--labels final|first]

`--src` is the build's own tree (the base is an export of 00d691630; the candidate is the
worktree). The example is built with `cargo build --release -p muninn-capture --example
extract_dump` into a target directory of its own per tree. `--bin` only names the build.

Items. Precision set: the 109 typed records (`STORE:id`); a record of the set is *emitted* when
the dump of its session holds a candidate of the same kind whose body is the record's body
(whitespace and case folded), or contains its object. The two `deadend` records are
`tool_observed` and the example prints `user_said` candidates only, so they are reported as not
measurable. Recall set: the 300 sampled messages (`STORE:session8:offset`); a candidate belongs
to a message when it has the message's session and turn index. A durable message is *emitted*
when one of its candidates contains one of the anchor phrases its label carries.

Candidate classes on the recall set: `durable` (carries an anchor), `a_other` (from a durable
message, another sentence), `b` (message holds no durable statement), `c` (message not typed by
a person), `opt` (a bare option pick; counted on neither side). Message-level precision is
durable / (durable + a_other + b + c).
"""
import collections, hashlib, json, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

ap = parser(__doc__)
ap.add_argument('--src', required=True, help='source tree whose extract_dump is measured')
args = ap.parse_args()
F = fixtures()
build = build_name(args)


def extract_dump(src):
    src = os.path.abspath(src)
    tgt = work('target', hashlib.sha1(src.encode()).hexdigest()[:10])
    r = subprocess.run(['cargo', 'build', '--release', '-p', 'muninn-capture', '--example', 'extract_dump', '--target-dir', tgt],
                       cwd=src, capture_output=True, text=True)
    if r.returncode:
        sys.exit('extract_dump did not build:\n' + r.stderr[-2000:])
    exe = os.path.join(tgt, 'release', 'examples', 'extract_dump.exe' if os.name == 'nt' else 'extract_dump')
    return exe


P = [json.loads(l) for l in open(F + '/out/extract/precision_items.jsonl', encoding='utf-8')]
R = [json.loads(l) for l in open(F + '/out/extract/recall_items.jsonl', encoding='utf-8')]
T = json.load(open(F + '/out/extract/transcripts.json', encoding='utf-8'))
by_sid = {os.path.basename(t['path']).rsplit('.', 1)[0]: t['path'] for t in T}
for r in R:
    by_sid.setdefault(r['session'], r['path'])

# stage the transcripts the items live in (copied once; re-copied when the size changes)
need = collections.defaultdict(set)
for p in P:
    need[p['store']].add(p['session'])
for r in R:
    need[r['store']].add(r['session'])
tx = work('a_extract', 'tx')
missing = set()
for st, sids in need.items():
    d = os.path.join(tx, st)
    os.makedirs(d, exist_ok=True)
    for sid in sids:
        src = by_sid.get(sid)
        dst = os.path.join(d, sid + '.jsonl')
        if not src or not os.path.isfile(src):
            missing.add(sid)
            continue
        if not os.path.isfile(dst) or os.path.getsize(dst) != os.path.getsize(src):
            shutil.copyfile(src, dst)


def dump(exe):
    out = []
    for st in sorted(need):
        r = run([exe, 'transcripts', '%s=%s' % (st, os.path.join(tx, st))], 'extract_dump:' + st)
        if r is None:
            continue
        if r.stderr.strip():
            fail('extract_dump:%s:stderr' % st)
        for l in r.stdout.decode('utf-8', 'replace').splitlines():
            if not l.strip():
                continue
            try:
                out.append(json.loads(l))
            except ValueError:
                fail('extract_dump:%s:bad_line' % st)
    if not out:
        fail('extract_dump:no_candidates')
    return out


cands = dump(extract_dump(args.src))
by_sess = collections.defaultdict(list)
for c in cands:
    by_sess[(c['project'], c['session'])].append(c)

# --- precision set -----------------------------------------------------------------------------
plab = {x['id']: x['label'] for x in labels('precision', args.labels)}


def matches(p, c):
    if c['kind'] != p['kind']:
        return False
    nb, nc = norm(p['body']), norm(c['body'])
    return nb == nc or (norm(p['object']) and norm(p['object']) in nc)


prec_rows = []
turn_of = {}
for p in P:
    k = '%s:%d' % (p['store'], p['id'])
    row = {'id': k, 'label': plab[k], 'kind': p['kind']}
    if p['kind'] == 'deadend' or p['origin'] != 'user_said':
        row['state'] = 'not_measurable'
    elif p['session'] in missing:
        row['state'] = 'transcript_missing'
    else:
        hit = [c for c in by_sess[(p['store'], p['session'])] if matches(p, c)]
        row['state'] = 'emitted' if hit else 'not_emitted'
        if hit:
            turn_of[k] = (p['store'], p['session'], hit[0]['turn'])
    prec_rows.append(row)

# --- recall set --------------------------------------------------------------------------------
rlab = {x['id']: x for x in labels('recall', args.labels)}
anchors = {}
if args.labels == 'final':
    anchors = {a['id']: [norm(x) for x in a['anchors']] for a in (json.loads(l) for l in open(F + '/out/usage-v4/labels/recall_anchors.jsonl', encoding='utf-8'))}
rec_rows = []
rturn = set()
align = collections.Counter()
for r in R:
    lab = rlab[r['uid']]
    cs = [c for c in by_sess[(r['store'], r['session'])] if c['turn'] == r['turn']]
    rturn.add((r['store'], r['session'], r['turn']))
    msg = norm(r['text_shown'])
    for c in cs:
        body = norm(c['body'][6:] if c['body'].startswith('user: ') else c['body'])
        align['candidates'] += 1
        align['text_in_message'] += body[:60] in msg
    row = {'id': r['uid'], 'label': lab['label'], 'kind': lab.get('kind'), 'missing': r['session'] in missing, 'classes': []}
    for c in cs:
        if lab['label'] == 'a':
            body = norm(c['body'])
            cl = 'durable' if any(a and a in body for a in anchors.get(r['uid'], [])) else 'a_other'
        elif lab['label'] == 'nh':
            cl = 'c'
        else:
            cl = lab['label']
        row['classes'].append(cl)
    row['carried'] = 'durable' in row['classes']
    row['store_hit'] = bool(lab.get('hit'))  # first labels only: the store held a carrying record
    rec_rows.append(row)

# candidates from precision source turns that are not one of the 109 and not in the recall set
unl = collections.Counter()
for k, (st, sid, t) in turn_of.items():
    if (st, sid, t) in rturn:
        continue
    for c in by_sess[(st, sid)]:
        if c['turn'] == t and not any(matches(p, c) for p in P if p['session'] == sid):
            unl[split_of(k)] += 1


def ratio(a, b):
    return round(a / b, 4) if b else None


per = {}
for sp in splits_for(args.split):
    pr = [x for x in prec_rows if in_split(x['id'], sp)]
    em = collections.Counter(x['label'] for x in pr if x['state'] == 'emitted')
    ne = collections.Counter(x['label'] for x in pr if x['state'] == 'not_emitted')
    by_kind = collections.Counter('%s:%s' % (x['kind'], x['label']) for x in pr if x['state'] == 'emitted')
    rr = [x for x in rec_rows if in_split(x['id'], sp)]
    pos = [x for x in rr if x['label'] == 'a']
    cl = collections.Counter(c for x in rr for c in x['classes'])
    msgs = collections.Counter(x['label'] for x in rr if x['classes'])
    scored = cl['durable'] + cl['a_other'] + cl['b'] + cl['c']
    per[sp] = {
        'precision_set': {
            'items': len(pr), 'measurable': sum(x['state'] in ('emitted', 'not_emitted') for x in pr),
            'not_measurable_deadend': sum(x['state'] == 'not_measurable' for x in pr),
            'transcript_missing': sum(x['state'] == 'transcript_missing' for x in pr),
            'labels': dict(collections.Counter(x['label'] for x in pr)),
            'emitted_by_label': dict(em), 'not_emitted_by_label': dict(ne), 'emitted_by_kind_label': dict(by_kind),
            'emitted': sum(em.values()), 'noise_emitted': em['b'] + em['c'] + em['d'], 'durable_emitted': em['a'],
            'record_precision': ratio(em['a'], sum(em.values())),
            'unlabelled_candidates_in_source_turns': unl[sp] if sp != 'all' else sum(unl.values()),
        },
        'recall_set': {
            'messages': len(rr), 'labels': dict(collections.Counter(x['label'] for x in rr)),
            'durable_messages': len(pos), 'durable_emitted': sum(x['carried'] for x in pos),
            'durable_missed': sum(not x['carried'] for x in pos),
            'durable_emitted_by_kind': dict(collections.Counter(x['kind'] for x in pos if x['carried'])),
            'durable_by_kind': dict(collections.Counter(x['kind'] for x in pos)),
            'recall': ratio(sum(x['carried'] for x in pos), len(pos)),
            'candidates_by_class': dict(cl), 'messages_with_candidates_by_label': dict(msgs),
            'message_precision': ratio(cl['durable'], scored),
            'noise_candidates': cl['a_other'] + cl['b'] + cl['c'],
            'transcript_missing': sum(x['missing'] for x in rr),
        },
    }
    if args.labels == 'first':
        per[sp]['recall_set']['store_held_a_carrying_record'] = sum(x['store_hit'] for x in pos)
def src_commit(src):
    r = subprocess.run(['git', '-C', src, 'rev-parse', 'HEAD'], capture_output=True, text=True)
    if r.returncode:
        return {'commit': 'not a git checkout', 'dirty': None}
    d = subprocess.run(['git', '-C', src, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.strip()
    return {'commit': r.stdout.strip(), 'dirty': bool(d)}


extra = {'src': src_commit(args.src), 'src_note': 'extract_dump of the --src tree', 'candidates_total': len(cands),
         'turn_alignment': {'candidates_at_recall_turns': align['candidates'], 'text_found_in_message': align['text_in_message']}}
write_counts('a_extract', build, args, per, extra)
# per-item emitted ids for base/candidate comparison (ids and codes only)
t = json.dumps({'precision': {x['id']: x['state'] for x in prec_rows}, 'recall': {x['id']: x['classes'] for x in rec_rows}}, sort_keys=True, indent=0)
check_private(t)
# per-item states carry label classes, held-out ones included: they stay in the private work dir
open(os.path.join(work('a_extract'), 'a_extract_%s_items.json' % build), 'w', newline='\n').write(t)
