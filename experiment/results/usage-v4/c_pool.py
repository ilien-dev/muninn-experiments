#!/usr/bin/env python3
"""The blind-label pool for the delivery set (fourth amendment: C1 is read once, after the
(prompt, block) pairs no frozen label covers have been labelled blind to the arm).

  python -I c_pool.py export --arms <build sha16> [<build sha16> ...] [--bins <muninn.exe> ...]
                             [--base b93d2f5c222c0424] [--controls 80] [--seed 20261111]
                             [--short-prompts <ids file>] [--out <dir under $F/out/usage-v4/pool>]
  python -I c_pool.py ingest --labels <the labeller's file> [--out <same dir>]

export. For every labelled prompt of the delivery set (all splits), the record ids each arm
returned are read from `counts/c_delivery_<arm>_items.json` (with `--bins`, given in the order of
`--arms`, an arm without that file is first run with `c_delivery.py --parts c12`). Pairs that a
frozen label (or an earlier pool extension) already covers are dropped. A seeded sample of pairs
the base arm returned that do carry a frozen label is added as controls, stratified by label
(every useful and harmful one up to a quarter of the target each, the rest from related and
unrelated). `--short-prompts` adds prompts outside the labelled set (ids of
`out/delivery/sample_silence.jsonl`, one per line), each replayed through every arm in `--bins`
on a store copy rewound to its moment. Everything is shuffled with the seed and written, under the
private pool directory, as:
  labelling.jsonl   one line per item: opaque id, prompt text, record kind, age, retired flag and
                    text, and an empty `label`. No arm, build, split or existing label.
  key.json          item id -> prompt id, record id, arms that returned it, control or not.
                    The labeller never opens it.
  LABELLING.md      the instructions for the labeller.
  export.json       counts only.
ingest. Every item of the labeller's file must carry one of useful / related / unrelated /
harmful. Agreement on the controls against the frozen labels is computed (raw and Cohen's kappa,
four labels and unrelated-or-not). The new labels are written as an extension next to the frozen
file (`out/usage-v4/labels/delivery_pool.jsonl`, with `delivery_pool.ingest.json` holding both
files' sha256 and the agreement); the frozen file is never written. If the control kappa on
unrelated-or-not is below 0.6, the extension is marked unusable and `--labels final+pool`
refuses it. Prints counts only.
"""
import argparse, collections, hashlib, json, os, random, re, shutil, sqlite3, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fixtures, work, sha16, hook, block_ids, check_private, FAILS, COUNTS, HERE

CODE = {'useful': 'u', 'related': 'r', 'unrelated': 'x', 'harmful': 'h'}
WORD = {v: k for k, v in CODE.items()}
ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('step', choices=['export', 'ingest'])
ap.add_argument('--arms', nargs='*', default=[])
ap.add_argument('--bins', nargs='*', default=[])
ap.add_argument('--base', default='b93d2f5c222c0424')
ap.add_argument('--controls', type=int, default=80)
ap.add_argument('--seed', type=int, default=20261111)
ap.add_argument('--short-prompts')
ap.add_argument('--labels')
ap.add_argument('--out')
a = ap.parse_args()
F = fixtures()
POOL_ROOT = os.path.join(F, 'out', 'usage-v4', 'pool').replace('\\', '/')
out = os.path.abspath(a.out or POOL_ROOT).replace('\\', '/')
if not out.startswith(os.path.abspath(POOL_ROOT).replace('\\', '/')):
    sys.exit('--out must be under $MUNINN_USAGE_FIXTURES/out/usage-v4/pool')
LAB = os.path.join(F, 'out', 'usage-v4', 'labels')
EXT = os.path.join(LAB, 'delivery_pool.jsonl')
META = os.path.join(LAB, 'delivery_pool.ingest.json')
FROZEN = os.path.join(LAB, 'delivery.jsonl')
D = F + '/out/delivery'


def report(d):
    t = json.dumps(d, indent=1, sort_keys=True)
    check_private(t)
    print(t)


def kappa(pairs):
    n = len(pairs)
    if not n:
        return None
    po = sum(x == y for x, y in pairs) / n
    ca, cb = collections.Counter(x for x, _ in pairs), collections.Counter(y for _, y in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0


def cut(s, n):
    s = re.sub(r'\s+', ' ', s or '').strip()
    return s if len(s) <= n else s[:n] + '…'


LABELLING = """# Labelling the delivery pool

Open `labelling.jsonl` in this directory and nothing else: not `key.json`, not any other file of
this directory or of the fixtures, not the stores, not the analysis reports. Every line is one item:
a prompt a person sent to a coding agent, and one memory block a memory engine could inject next to
that prompt (`record.kind`; `record.age_days`, days between the record and the prompt;
`record.retired_today`, whether the record has been retired since; `record.text`, its text,
truncated). Judge the block only against this prompt.

Fill `label` with exactly one of these, the definitions both earlier passes used:

- `useful`    the agent answers or carries out this prompt better with the block than without:
              it states a rule, decision, fact or earlier result that the prompt asks about or that
              constrains how the requested work must be done. Be strict: "could conceivably help"
              is not useful.
- `related`   same feature / topic / task thread as the prompt, but the agent does not need it
              (already implied by the prompt, restates it, earlier chatter about the same area).
- `unrelated` different subject; shares only incidental words with the prompt (names, common
              verbs, tool names), or is a command log / fragment that says nothing about it.
- `harmful`   would mislead: visibly stale, superseded or contradicted by a newer block in the same
              item or by the prompt itself, or an old instruction the prompt explicitly reverses.

If the prompt is a pure continuation ("ok do it", long pasted notification) with no identifiable
subject, blocks are `unrelated` unless they clearly govern the action.

Write the file back with every line kept and only `label` filled (save it as `labels.jsonl` next
to this file). Do not add, remove or reorder lines, and do not write reasons or quotes anywhere
else. Several items share a prompt; label each on its own.
"""


# ---------------------------------------------------------------------------------------- export
def export():
    if not a.arms:
        sys.exit('--arms is required')
    if a.bins and len(a.bins) != len(a.arms):
        sys.exit('--bins must be given in the order of --arms, one per arm')
    binof = dict(zip(a.arms, a.bins))
    for k, b in binof.items():
        if sha16(b) != k:
            sys.exit('--bins: %s does not hash to its arm key' % b)
    frozen = {(x['item'], x['id']): x['label'] for x in (json.loads(l) for l in open(FROZEN, encoding='utf-8'))}
    covered = set(frozen)
    if os.path.isfile(EXT):
        covered |= {(x['item'], x['id']) for x in (json.loads(l) for l in open(EXT, encoding='utf-8'))}
    items = {}
    arms = list(dict.fromkeys(a.arms + [a.base]))
    for arm in arms:
        p = os.path.join(COUNTS, 'c_delivery_%s_items.json' % arm)
        if not os.path.isfile(p):
            if arm not in binof:
                sys.exit('no per-item file for %s and no --bins path to run it' % arm)
            r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'c_delivery.py'), '--bin', binof[arm], '--parts', 'c12'], capture_output=True, text=True)
            if r.returncode or not os.path.isfile(p):
                sys.exit('c_delivery.py failed for %s' % arm)
        items[arm] = json.load(open(p))['c12']
    sample = {s['item']: s for s in (json.loads(l) for l in open(D + '/sample_prompt.jsonl', encoding='utf-8'))}
    every = [json.loads(l) for l in open(D + '/pairs.jsonl', encoding='utf-8')]
    pairs_by = {(p['store'], p['session'], p['at']): p for p in every}
    prompt = {}
    store = {}
    at = {}
    for it, s in sample.items():
        prompt[it] = pairs_by[(s['store'], s['session'], s['at'])]['prompt']
        store[it], at[it] = s['store'], s['at']
    returned = collections.defaultdict(set)  # (prompt id, record id) -> arms
    for arm in a.arms:
        for it, v in items[arm].items():
            for rid in v['ids']:
                returned[(it, rid)].add(arm)
    # short prompts (R-20), replayed through every arm with a binary
    if a.short_prompts:
        if not binof:
            sys.exit('--short-prompts needs --bins')
        sil = {s['item']: s for s in (json.loads(l) for l in open(D + '/sample_silence.jsonl', encoding='utf-8'))}
        want = [l.strip() for l in open(a.short_prompts) if l.strip()]
        for it in want:
            s = sil[it]
            prompt[it], store[it], at[it] = pairs_by[(s['store'], s['session'], s['at'])]['prompt'], s['store'], s['at']
        for arm, b in binof.items():
            for it in sorted(want, key=lambda i: (store[i], -at[i])):
                d = work('c_pool', arm, it)
                shutil.rmtree(d, ignore_errors=True)
                os.makedirs(d + '/.muninn/log')
                shutil.copyfile(F + '/stores/%s/muninn.db' % store[it], d + '/.muninn/muninn.db')
                con = sqlite3.connect(d + '/.muninn/muninn.db')
                t = at[it] - 5000
                con.execute('update record set invalid=0, invalidated_by=NULL, invalid_reason=NULL where invalid=1 and invalidated_by in (select id from record where created_at>=?)', (t,))
                for tb in ('cue', 'record_vec'):
                    con.execute('delete from %s where record_id in (select id from record where created_at>=?)' % tb, (t,))
                con.execute('delete from fire_ledger where record_id in (select id from record where created_at>=?)', (t,))
                con.execute('delete from record where created_at>=?', (t,))
                con.commit()
                con.close()
                env = {k: v for k, v in os.environ.items() if not k.startswith('MUNINN_')}
                for rid in block_ids(hook(b, 'UserPromptSubmit', d, {'session_id': 'pool-' + it, 'prompt': prompt[it]}, env=env)):
                    returned[(it, rid)].add(arm)
                shutil.rmtree(d, ignore_errors=True)
        if FAILS:
            sys.exit('a short-prompt replay failed: %s' % dict(FAILS))
    todo = sorted(k for k in returned if k not in covered)
    # controls: labelled pairs the base arm returned, stratified by label
    rnd = random.Random(a.seed)
    base_lab = collections.defaultdict(list)
    for it, v in sorted(items[a.base].items()):
        for rid in v['ids']:
            if (it, rid) in frozen:
                base_lab[frozen[(it, rid)]].append((it, rid))
    target = max(60, a.controls)
    q = -(-target // 4)
    ctrl = []
    for lab in ('u', 'h'):
        ctrl += rnd.sample(base_lab[lab], min(q, len(base_lab[lab])))
    rest = target - len(ctrl)
    big = [l for l in ('r', 'x') if base_lab[l]]
    for i, lab in enumerate(big):
        n = min(len(base_lab[lab]), rest // len(big) + (1 if i < rest % len(big) else 0))
        ctrl += rnd.sample(base_lab[lab], n)
    ctrl = [c for c in ctrl if c not in set(todo)]
    # write
    os.makedirs(out, exist_ok=True)
    dbs = {}

    def rec(st, rid):
        if st not in dbs:
            dbs[st] = sqlite3.connect('file:%s/stores/%s/muninn.db?mode=ro' % (F, st), uri=True)
        return dbs[st].execute('select kind, created_at, invalid, body from record where id=?', (rid,)).fetchone()

    allp = [(k, False) for k in todo] + [(k, True) for k in ctrl]
    rnd.shuffle(allp)
    key = {}
    with open(os.path.join(out, 'labelling.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        for n, ((it, rid), is_ctrl) in enumerate(allp, 1):
            iid = 'Q%04d' % n
            r = rec(store[it], rid)
            line = {'item': iid, 'prompt': cut(prompt[it], 1500),
                    'record': {'kind': r[0] if r else '?', 'age_days': round((at[it] - r[1]) / 86400000, 1) if r else None,
                               'retired_today': bool(r[2]) if r else None, 'text': cut(re.sub(r'^user:\s*', '', r[3]) if r else '', 1500)},
                    'label': ''}
            f.write(json.dumps(line, ensure_ascii=False) + '\n')
            key[iid] = {'prompt': it, 'record': rid, 'arms': sorted(returned.get((it, rid), set())), 'control': is_ctrl}
    json.dump(key, open(os.path.join(out, 'key.json'), 'w'), indent=0, sort_keys=True)
    open(os.path.join(out, 'LABELLING.md'), 'w', encoding='utf-8', newline='\n').write(LABELLING)
    stats = {'items': len(allp), 'to_label': len(todo), 'controls': len(ctrl),
             'controls_by_frozen_label': dict(collections.Counter(frozen[c] for c in ctrl)),
             'to_label_by_arm': {arm: sum(1 for k in todo if arm in returned[k]) for arm in a.arms},
             'short_prompts': len([l for l in open(a.short_prompts) if l.strip()]) if a.short_prompts else 0,
             'arms': a.arms, 'base': a.base, 'seed': a.seed,
             'labelling_sha256': sha16(os.path.join(out, 'labelling.jsonl'))}
    json.dump(stats, open(os.path.join(out, 'export.json'), 'w'), indent=1)
    report(stats)


# ---------------------------------------------------------------------------------------- ingest
def ingest():
    if not a.labels:
        sys.exit('--labels is required')
    key = json.load(open(os.path.join(out, 'key.json')))
    got = {}
    bad = collections.Counter()
    for l in open(a.labels, encoding='utf-8'):
        if not l.strip():
            continue
        v = json.loads(l)
        lab = str(v.get('label', '')).strip().lower()
        if v.get('item') not in key:
            bad['unknown_item'] += 1
        elif lab not in CODE:
            bad['invalid_or_empty_label'] += 1
        else:
            got[v['item']] = CODE[lab]
    missing = sorted(set(key) - set(got))
    if bad or missing:
        report({'refused': True, 'problems': dict(bad), 'items_without_a_label': len(missing)})
        sys.exit(1)
    frozen = {(x['item'], x['id']): x['label'] for x in (json.loads(l) for l in open(FROZEN, encoding='utf-8'))}
    cp = [(frozen[(key[i]['prompt'], key[i]['record'])], got[i]) for i in key if key[i]['control']]
    un = [(x == 'x', y == 'x') for x, y in cp]
    usable = (kappa(un) or 0) >= 0.6
    ext = sorted(({'item': key[i]['prompt'], 'id': key[i]['record'], 'label': got[i]} for i in key if not key[i]['control']),
                 key=lambda r: (r['item'], r['id']))
    os.makedirs(LAB, exist_ok=True)
    with open(EXT, 'w', encoding='utf-8', newline='\n') as f:
        for r in ext:
            f.write(json.dumps(r, sort_keys=True) + '\n')
    meta = {'frozen_sha256': sha16(FROZEN), 'extension_sha256': sha16(EXT), 'labelling_input_sha256': sha16(a.labels),
            'controls': len(cp), 'control_agree': sum(x == y for x, y in cp), 'control_kappa_4': kappa(cp),
            'control_agree_unrelated': sum(x == y for x, y in un), 'control_kappa_unrelated': kappa(un),
            'usable': usable, 'threshold': 'kappa on unrelated-or-not >= 0.6',
            'labelled': len(ext), 'labelled_by_code': dict(collections.Counter(r['label'] for r in ext))}
    json.dump(meta, open(META, 'w'), indent=1, sort_keys=True)
    report(meta)


export() if a.step == 'export' else ingest()
