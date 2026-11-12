#!/usr/bin/env python3
"""Section C, delivery. Everything runs through the real hooks of --bin on throwaway store copies.

  python -I c_delivery.py --bin <muninn.exe> [--split design|heldout|all] [--labels final|first] [--parts c12,c3,c4,c5]

C1/C2 (`c12`). The 150 labelled prompts of the delivery set (items `P001`..`P150`), as
`scripts/delivery/m1_replay.py` replays them: each store is copied, rewound to each prompt's
moment (records created at or after it minus 5 s deleted, the records they retired reactivated),
and the prompt runs as a fresh session through `hook UserPromptSubmit`. Counted: labelled pairs
returned by label, returned pairs with no label, mean estimated tokens a prompt, and the share of
block characters spent on header and `evidence:` lines. Per-item ids and tokens go to
`counts/c_delivery_<build>_items.json`, so two builds can be compared on items with the same ids.
With `--against <base sha16>`, C2 is the mean tokens on prompts whose returned id set is
the same in both builds (`c2_same_ids`); `mean_tokens` over all prompts is secondary.
The replay reproduces only part of the logged ids (71.8 % in the analysis); compare builds with
each other, never with the log.
C3 (`c3`). (1) A session start, then prompts made of 12 invariants it cut for budget, in the same
session and in fresh ones; (2) the same prompt after a compaction, asked while the epoch line is
pending and after the next Stop folded it; (1b) records only listed in the catalogue, asked for the same
way; (1) and (2) from `scripts/delivery/o1_defect_tests.py`, on a
copy of W02. (3) The stale twin: every user prompt W02 and L01 kept as an episode since 1.2.0,
replayed on rewound copies; counted: prompts whose delivery holds an active episode whose typed
twin (same transcript_ref) is retired as superseded on the copy as rewound to that prompt.
C4 (`c4`). The labelled session starts (items `S01`..), replayed on rewound copies through
`hook SessionStart`; block slots and catalogue lines scored with the session-start labels
(rule, decision = worth the slot leniently; rule = strictly). Then one SessionStart on today's
copy of each store with deliveries: active invariants and corrections shown or listed.
C5 (`c5`). `muninn why`: usage-v2's 30 questions (Spanish and English) on their own store copies;
the W02 and L01 typed records whose own first line the router sends to a route that cannot
return their kind (R-16 A); 30 retired W02 records asked with `--all` by one word, bare and after
"what about" (R-16 B); W02 user-stated records asked by 2-3 rare words with gender flipped (R-15).
"""
import collections, glob, json, os, re, shutil, sqlite3, subprocess, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

ap = parser(__doc__)
ap.add_argument('--parts', default='c12,c3,c4,c5')
ap.add_argument('--against', help='base build (sha16): C2 compares mean tokens on prompts whose returned ids are the same in both builds')
args = ap.parse_args()
F = fixtures()
build = build_name(args)
BIN = os.path.abspath(args.bin).replace('\\', '/')
parts = set(args.parts.split(','))
D = F + '/out/delivery'
CUT = 1793682000000
ENV = {k: v for k, v in os.environ.items() if not k.startswith('MUNINN_')}
CAT = re.compile(r'^#(\d+) ([a-z_]+) · ')


def copy_store(st, name):
    d = work('c_delivery', build, name, st)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d + '/.muninn/log')
    shutil.copyfile(F + '/stores/%s/muninn.db' % st, d + '/.muninn/muninn.db')
    if os.path.isfile(F + '/stores/%s/init.json' % st):
        shutil.copyfile(F + '/stores/%s/init.json' % st, d + '/.muninn/init.json')
    return d


def no_spawn(d):
    # SessionStart spawns `maintain` at most every two minutes; a fresh stamp keeps the copy still
    open(d + '/.muninn/log/maintain.stamp', 'w').write('0')


def rewind(d, at):
    con = sqlite3.connect(d + '/.muninn/muninn.db')
    t = at - 5000
    con.execute('update record set invalid=0, invalidated_by=NULL, invalid_reason=NULL where invalid=1 and invalidated_by in (select id from record where created_at>=?)', (t,))
    for tb in ('cue', 'record_vec'):
        con.execute('delete from %s where record_id in (select id from record where created_at>=?)' % tb, (t,))
    con.execute('delete from fire_ledger where record_id in (select id from record where created_at>=?)', (t,))
    con.execute('delete from record where created_at>=?', (t,))
    con.commit()
    con.close()


def prov_chars(text):
    hdr = ev = tot = 0
    inblock = False
    for l in text.split('\n'):
        if HDR.match(l):
            inblock = True
            hdr += len(l) + 1
        elif l.startswith('[muninn:'):
            inblock = False
        elif inblock and l.startswith('  evidence: '):
            ev += len(l) + 1
        if inblock:
            tot += len(l) + 1
    return hdr, ev, tot


def ratio(a, b):
    return round(a / b, 4) if b else None


per = collections.defaultdict(dict)
extra = {}
items_out = {}

# -------------------------------------------------------------------------------------- events
sample = [json.loads(l) for l in open(D + '/sample_prompt.jsonl', encoding='utf-8')]
pairs = {(p['store'], p['session'], p['at']): p for p in (json.loads(l) for l in open(D + '/pairs.jsonl', encoding='utf-8')) if p['reason'] == 'literal'}
starts = [e for e in (json.loads(l) for l in open(D + '/sample_events.jsonl', encoding='utf-8')) if e['group'] == 'S']


def prompts_from_episodes(st):
    c = sqlite3.connect('file:%s/stores/%s/muninn.db?mode=ro' % (F, st), uri=True)
    out, seen = [], set()
    for rid, subj, body, at, sid in c.execute("select id, subject, body, created_at, session_id from record where kind='episode' and created_at>=? and body like 'user: %' order by created_at, id", (CUT,)):
        tk = subj
        if subj.startswith('session:') and '.' in subj:
            head, tail = subj.rsplit('.', 1)
            if tail.isdigit() or tail == '':
                tk = head
        if tk in seen:
            continue
        seen.add(tk)
        b = body[6:]
        i = b.find('\nassistant: ')
        out.append({'at': at, 'prompt': b[:i] if i >= 0 else b})
    c.close()
    return out


STALE_SQL = ("select e.id from record e join record t on t.transcript_ref=e.transcript_ref and t.id<>e.id where e.kind='episode' and e.invalid=0 "
             "and t.kind<>'episode' and t.invalid=1 and t.invalid_reason='superseded' and e.transcript_ref is not null")


def stale_now(d):
    """Active episodes whose typed twin is retired as superseded, on the copy as rewound now."""
    c = sqlite3.connect('file:%s/.muninn/muninn.db?mode=ro' % d, uri=True)
    s = set(r[0] for r in c.execute(STALE_SQL))
    c.close()
    return s


ev = collections.defaultdict(list)
if 'c12' in parts:
    for s in sample:
        ev[s['store']].append((s['at'], 'prompt', s))
if 'c4' in parts:
    for s in starts:
        ev[s['store']].append((s['at'], 'start', s))
if 'c3' in parts:
    for st in ('W02', 'L01'):
        ps = prompts_from_episodes(st)
        for p in ps:
            ev[st].append((p['at'], 'twin', p))

res_prompt, res_start, res_twin = {}, {}, collections.Counter()
for st in sorted(ev):
    d = copy_store(st, 'replay')
    for at, kind, s in sorted(ev[st], key=lambda e: -e[0]):
        rewind(d, at)
        if kind == 'prompt':
            p = pairs[(st, s['session'], s['at'])]
            text = hook(BIN, 'UserPromptSubmit', d, {'session_id': 'replay-' + s['item'], 'prompt': p['prompt']}, env=ENV)
            res_prompt[s['item']] = {'ids': block_ids(text), 'tokens': est(text), 'prov': prov_chars(text)}
        elif kind == 'twin':
            text = hook(BIN, 'UserPromptSubmit', d, {'session_id': 'twin-%d' % at, 'prompt': s['prompt']}, env=ENV)
            ids = block_ids(text)
            res_twin[st + ':prompts'] += 1
            res_twin[st + ':delivered'] += bool(ids)
            st_set = stale_now(d) if ids else set()  # twin retired as of this prompt's moment
            n = sum(1 for i in ids if i in st_set)
            res_twin[st + ':stale_twin_blocks'] += n
            res_twin[st + ':prompts_with_stale_twin'] += bool(n)
        else:
            no_spawn(d)
            text = hook(BIN, 'SessionStart', d, {'session_id': 'start-' + s['item'], 'source': 'startup'}, env=ENV)
            cat = [int(m.group(1)) for m in (CAT.match(l) for l in text.split('\n')) if m]
            res_start[s['item']] = {'store': st, 'blocks': block_ids(text), 'cat': cat, 'tokens': est(text)}

# -------------------------------------------------------------------------------------- C1/C2
if 'c12' in parts:
    lab = {(x['item'], x['id']): x['label'] for x in labels('delivery', args.labels)}
    for sp in splits_for(args.split):
        its = [s['item'] for s in sample if in_split(s['item'], sp)]
        c = collections.Counter()
        tok, hdr, evc, tot = [], 0, 0, 0
        for it in its:
            r = res_prompt[it]
            c['prompts'] += 1
            c['prompts_with_delivery'] += bool(r['ids'])
            for i in r['ids']:
                c['returned'] += 1
                c['returned:' + {'u': 'useful', 'r': 'related', 'x': 'unrelated', 'h': 'harmful'}.get(lab.get((it, i)), 'unlabelled')] += 1
            tok.append(r['tokens'])
            hdr += r['prov'][0]
            evc += r['prov'][1]
            tot += r['prov'][2]
        tot_l = collections.Counter(v for (i, _), v in lab.items() if i in set(its))
        per[sp]['c12'] = {
            'prompts': c['prompts'], 'prompts_with_delivery': c['prompts_with_delivery'], 'returned': c['returned'],
            'useful_returned': c['returned:useful'], 'useful_labelled': tot_l['u'],
            'unrelated_returned': c['returned:unrelated'], 'unrelated_labelled': tot_l['x'],
            'related_returned': c['returned:related'], 'related_labelled': tot_l['r'],
            'harmful_returned': c['returned:harmful'], 'unlabelled_returned': c['returned:unlabelled'],
            'mean_tokens': round(sum(tok) / len(tok), 1) if tok else None,  # all prompts; C2 reads c2_same_ids
            'header_chars': hdr, 'evidence_chars': evc, 'block_chars': tot, 'provenance_share': ratio(hdr + evc, tot),
        }
    items_out['c12'] = {k: {'ids': v['ids'], 'tokens': v['tokens']} for k, v in sorted(res_prompt.items())}
    if args.against:
        bp = os.path.join(COUNTS, 'c_delivery_%s_items.json' % args.against)
        if not os.path.isfile(bp):
            fail('c2:no_base_items')
        else:
            base = json.load(open(bp))['c12']
            for sp in splits_for(args.split):
                same = [k for k, v in res_prompt.items() if in_split(k, sp) and k in base and sorted(base[k]['ids']) == sorted(v['ids']) and v['ids']]
                per[sp]['c12']['c2_same_ids'] = {
                    'against': args.against, 'prompts': len(same),
                    'mean_tokens_this': round(sum(res_prompt[k]['tokens'] for k in same) / len(same), 1) if same else None,
                    'mean_tokens_against': round(sum(base[k]['tokens'] for k in same) / len(same), 1) if same else None}

# -------------------------------------------------------------------------------------- C4
if 'c4' in parts:
    units = [json.loads(l) for l in open(D + '/sample_event_units.jsonl', encoding='utf-8')]
    labs = [json.loads(l) for l in open(D + '/labels/event_units_pass1.jsonl', encoding='utf-8')]
    ul = {}
    for u, v in zip(units, labs):
        assert u['unit'] == v['unit']
        ul.setdefault((u['store'], u['form'], u['id']), v['label'])
    pool_units = 0
    if args.labels == 'final+pool':
        # session-start slots labelled blind in the pool (seventh amendment), only if they passed
        # their control gate; without the option nothing here changes
        pm = F + '/out/usage-v4/labels/event_pool.ingest.json'
        pe = F + '/out/usage-v4/labels/event_pool.jsonl'
        if os.path.isfile(pm) and os.path.isfile(pe):
            m = json.load(open(pm))
            if m.get('usable') and sha16(pe) == m.get('extension_sha256') and sha16(D + '/labels/event_units_pass1.jsonl') == m.get('frozen_sha256'):
                for x in (json.loads(l) for l in open(pe, encoding='utf-8')):
                    if (x['store'], x['form'], x['id']) not in ul:
                        ul[(x['store'], x['form'], x['id'])] = x['label']
                        pool_units += 1
            elif not m.get('usable'):
                pool_units = -1  # recorded: the pool's session-start labels failed their gate
    for sp in splits_for(args.split):
        c = collections.Counter()
        for it, r in res_start.items():
            if not in_split(it, sp):
                continue
            c['starts'] += 1
            for form, ids in (('B', r['blocks']), ('C', r['cat'])):
                for i in ids:
                    l = ul.get((r['store'], form, i))
                    c[form + ':slots'] += 1
                    c[form + ':' + (l or 'unlabelled')] += 1
                    c[form + ':lenient'] += l in ('rule', 'decision')
                    c[form + ':strict'] += l == 'rule'
            c['tokens'] += r['tokens']
        out = {'starts': c['starts']}
        for form, name in (('B', 'blocks'), ('C', 'catalogue')):
            n, lab_n = c[form + ':slots'], c[form + ':slots'] - c[form + ':unlabelled']
            out[name] = {'slots': n, 'unlabelled': c[form + ':unlabelled'], 'worth_lenient': c[form + ':lenient'], 'worth_strict': c[form + ':strict'],
                         'share_lenient_of_labelled': ratio(c[form + ':lenient'], lab_n), 'share_strict_of_labelled': ratio(c[form + ':strict'], lab_n),
                         'labels': {k.split(':', 1)[1]: v for k, v in c.items() if k.startswith(form + ':') and k.split(':', 1)[1] not in ('slots', 'lenient', 'strict')}}
        n = c['B:slots'] + c['C:slots'] - c['B:unlabelled'] - c['C:unlabelled']
        out['all_slots'] = {'share_lenient_of_labelled': ratio(c['B:lenient'] + c['C:lenient'], n), 'share_strict_of_labelled': ratio(c['B:strict'] + c['C:strict'], n)}
        out['mean_tokens'] = round(c['tokens'] / c['starts'], 1) if c['starts'] else None
        if args.labels == 'final+pool':
            out['pool_units_used'] = pool_units
        per[sp]['c4'] = out
    cov = {}
    whole = {}
    for st in ('L01', 'W02', 'W05', 'W06', 'W07', 'W08', 'W10'):
        d = copy_store(st, 'today')
        no_spawn(d)
        text = hook(BIN, 'SessionStart', d, {'session_id': 'cov-' + st, 'source': 'startup'}, env=ENV)
        shown = set(block_ids(text))
        listed = set(int(m.group(1)) for m in (CAT.match(l) for l in text.split('\n')) if m)
        con = sqlite3.connect('file:%s/.muninn/muninn.db?mode=ro' % d, uri=True)
        act = {k: set(r[0] for r in con.execute("select id from record where invalid=0 and kind=?", (k,))) for k in ('invariant', 'correction')}
        eobj = {r[0]: (norm(r[1]), norm(r[2])) for r in con.execute("select id, object, body from record where invalid=0 and kind in ('decision','invariant','correction') and subject not like 'commit:%'")}
        elig = set(eobj)
        # a word-for-word twin (same object or same body) of a shown or listed record counts as
        # covered: the catalogue drops twins
        seen_text = {t for i in elig & (shown | listed) for t in eobj[i]}
        twins = {i for i in elig - shown - listed if eobj[i][0] in seen_text or eobj[i][1] in seen_text}
        con.close()
        # the line after the last catalogue entry says whether the list is whole
        ls = [l for l in text.split('\n') if l.strip()]
        idx = [i for i, l in enumerate(ls) if CAT.match(l)]
        tail = ls[idx[-1] + 1] if idx and idx[-1] + 1 < len(ls) else ''
        claim = True if tail.startswith('That is every') else (False if 'not listed' in tail else None)
        miss = len(elig - shown - listed - twins)
        # a store with nothing eligible and no catalogue has nothing to claim and is not misleading
        whole[st] = {'claims_whole': claim, 'eligible': len(elig), 'twins_of_listed': len(twins), 'eligible_neither': miss,
                     'truthful': (True if (claim is None and not elig) else None) if claim is None else claim == (miss == 0)}
        cov[st] = {k: {'active': len(v), 'shown': len(v & shown), 'listed_only': len((v & listed) - shown), 'neither': len(v - shown - listed)} for k, v in act.items()}
    per['all'].setdefault('c4', {})['coverage_today'] = cov
    per['all']['c4']['whole_list_today'] = whole
    items_out['c4'] = {k: {'blocks': v['blocks'], 'cat': v['cat']} for k, v in sorted(res_start.items())}

# -------------------------------------------------------------------------------------- C3
if 'c3' in parts:
    out = {}
    d = copy_store('W02', 'defect')

    def log_lines():
        p = d + '/.muninn/log/delivery.jsonl'
        return [json.loads(l) for l in open(p, encoding='utf-8')] if os.path.isfile(p) else []

    no_spawn(d)
    hook(BIN, 'SessionStart', d, {'session_id': 't1-session', 'source': 'startup'}, env=ENV)
    lines = [l for l in log_lines() if l.get('session') == 't1-session']
    cut = next((l['ids'] for l in lines if str(l.get('reason', '')).startswith('gated:budget')), [])
    con = sqlite3.connect('file:%s/.muninn/muninn.db?mode=ro' % d, uri=True)
    ok = ctl = tried = 0
    for target in cut[:12]:
        row = con.execute('select body from record where id=?', (target,)).fetchone()
        if not row:
            continue
        prompt = re.sub(r'^user:\s*', '', row[0])[:400]
        if len(prompt.split()) < 6:
            continue
        tried += 1
        ok += target in block_ids(hook(BIN, 'UserPromptSubmit', d, {'session_id': 't1-session', 'prompt': prompt}, env=ENV))
        ctl += target in block_ids(hook(BIN, 'UserPromptSubmit', d, {'session_id': 't1-control-%d' % target, 'prompt': prompt}, env=ENV))
    out['t1_cut_for_budget'] = {'cut_at_start': len(cut), 'tried': tried, 'same_session': ok, 'fresh_session': ctl}
    # T1b: records only listed in the session-start catalogue (a title line, no block), asked for
    # by their own words later in the same session, and in a fresh session as the control
    no_spawn(d)
    st_text = hook(BIN, 'SessionStart', d, {'session_id': 't1c-session', 'source': 'startup'}, env=ENV)
    shown = set(block_ids(st_text))
    listed = [int(m.group(1)) for m in (CAT.match(l) for l in st_text.split('\n')) if m]
    listed = [i for i in listed if i not in shown]
    ok = ctl = tried = 0
    for target in listed:
        row = con.execute('select body from record where id=?', (target,)).fetchone()
        if not row:
            continue
        prompt = re.sub(r'^user:\s*', '', row[0])[:400]
        if len(prompt.split()) < 6:
            continue
        tried += 1
        ok += target in block_ids(hook(BIN, 'UserPromptSubmit', d, {'session_id': 't1c-session', 'prompt': prompt}, env=ENV))
        ctl += target in block_ids(hook(BIN, 'UserPromptSubmit', d, {'session_id': 't1c-control-%d' % target, 'prompt': prompt}, env=ENV))
        if tried >= 12:
            break
    out['t1_listed_in_catalogue'] = {'listed_not_shown': len(listed), 'tried': tried, 'same_session': ok, 'fresh_session': ctl}
    prompt = re.sub(r'^user:\s*', '', con.execute("select body from record where invalid=0 and kind='episode' and length(body)>200 order by id desc limit 1 offset 40").fetchone()[0])[:300]
    con.close()
    t2 = {}
    for name, fold_first in (('t2-a', False), ('t2-b', True)):
        first = block_ids(hook(BIN, 'UserPromptSubmit', d, {'session_id': name, 'prompt': prompt}, env=ENV))
        hook(BIN, 'Stop', d, {'session_id': name}, env=ENV)
        hook(BIN, 'PostCompact', d, {'session_id': name, 'trigger': 'auto'}, env=ENV)
        if fold_first:
            hook(BIN, 'Stop', d, {'session_id': name}, env=ENV)
        again = block_ids(hook(BIN, 'UserPromptSubmit', d, {'session_id': name, 'prompt': prompt}, env=ENV))
        t2[name] = (len(first), len(set(first) & set(again)))
    out['t2_after_compaction'] = {'epoch_line_pending': {'first_blocks': t2['t2-a'][0], 'served_again': t2['t2-a'][1]},
                                  'after_next_stop': {'first_blocks': t2['t2-b'][0], 'served_again': t2['t2-b'][1]},
                                  'offered_again_after_stop': int(t2['t2-b'][1] > 0)}
    out['t3_stale_twin'] = dict(res_twin)
    for st in ('W02', 'L01'):
        out['t3_stale_twin'][st + ':share'] = ratio(res_twin[st + ':prompts_with_stale_twin'], res_twin[st + ':delivered'])
    per['all']['c3'] = out

# -------------------------------------------------------------------------------------- C5
STOP = set("""the and for that this with from into have has are was were not but you your can will should
would could there here what when where which how why who then than also just please make sure need want let
use using que los las una uno para por con del como pero más mas esto esta este también tambien hacer puedes
podrias podrías quiero necesito sobre donde cuando porque todo toda todos algo muy ser está esta estan están
hay sin ahora code file files function add fix update change implement create new run test tests error issue
problem thing things""".split())


def fts_term(w):
    out = []
    for ch in w.lower():
        dd = unicodedata.normalize('NFD', ch)
        f = dd[0] if len(dd) > 1 and 'a' <= dd[0].lower() <= 'z' else {'ø': 'o', 'đ': 'd', 'ł': 'l', 'ħ': 'h', 'ı': 'i'}.get(ch)
        if f is not None:
            out.append(f)
        elif ch.isalnum() or ch == '_':
            out.append(ch)
    t = ''.join(out)
    return None if len(t.encode()) < 2 or all(ch == '_' for ch in t) else t


def why(d, query, all_=False, limit=8):
    a = [BIN, '--cwd', d, '--json', 'why'] + (['--all'] if all_ else []) + (['--limit', str(limit)] if limit else []) + ['--', query]
    r = run(a, 'why', timeout=120, ok_codes=(0, 3), text=True, encoding='utf-8', env=ENV)  # 3 = answer not sufficient
    if r is None:
        return []
    try:
        return [f['record']['id'] for f in json.loads(r.stdout)['records']]
    except Exception:
        fail('why:bad_stdout')
        return []


def route(qs):
    l = qs.strip().lower()
    if l and all(ch.isdigit() for ch in l):
        return 'id'
    has = lambda ws: any(w in l for w in ws)
    if any(7 <= len(w) <= 40 and all(ch in '0123456789abcdef' for ch in w) for w in l.split()) or has(['commit', 'qué cambió', 'que cambio', 'what changed']):
        return 'commit'
    if has(['prohibid', 'forbidden', 'not allowed', "why can't", 'por qué no puedo', 'regla', 'rule', 'nunca', 'never', 'siempre', 'always']):
        return 'rule'
    if has(['no funciona', "doesn't work", 'does not work', 'falló', 'failed', 'descart', 'abandon', 'dead end', 'callejón', 'por qué no', 'why not', "why didn't", "why doesn't"]):
        return 'deadend'
    if '/' in l or any('.' in w and not w.endswith('.') and len(w) > 3 for w in l.split()) or has(['quién toca', 'who touches', 'historia de', 'history of', 'fichero', 'archivo', 'file ']):
        return 'file'
    if has(['por qué', 'porque', 'why', 'decid', 'eleg', 'chose', 'choose', 'razón', 'reason']):
        return 'decision'
    return 'all'


KINDS = {'decision': {'decision', 'invariant', 'correction', 'claim'}, 'deadend': {'deadend', 'correction', 'episode'},
         'commit': {'decision', 'deadend', 'episode'}, 'file': {'decision', 'deadend', 'invariant', 'claim', 'episode'},
         'rule': {'invariant', 'correction', 'decision'}}


def gender(w):
    if w.endswith('o'):
        return w[:-1] + 'a'
    if w.endswith('a'):
        return w[:-1] + 'o'
    if w.endswith('os'):
        return w[:-2] + 'as'
    if w.endswith('as'):
        return w[:-2] + 'os'
    return None


if 'c5' in parts:
    out = {}
    # usage-v2's 30 questions, each on its own store copy
    Q = json.load(open(F + '/fixtures/usage-v2/why2/questions.json', encoding='utf8'))
    out['usage_v2_questions_sha256'] = sha16(F + '/fixtures/usage-v2/why2/questions.json')
    hits = collections.Counter()
    fresh_why2 = set()
    for q in Q:
        src = F + '/fixtures/usage-v2/why2/s/%s/.muninn' % q['p']
        dd = work('c_delivery', build, 'why2', q['p'])
        if q['p'] not in fresh_why2:  # a fresh copy per run, once per store
            shutil.rmtree(dd + '/.muninn', ignore_errors=True)
            shutil.copytree(src, dd + '/.muninn')
            fresh_why2.add(q['p'])
        for lang in ('es', 'en'):
            hits[lang] += int(q['id']) in why(dd, q[lang], limit=None)
    out['usage_v2'] = {'items': len(Q), 'spanish_reached': hits['es'], 'english_reached': hits['en']}
    # routed away (R-16 A) and --all (R-16 B)
    away_n, away_found, ctl_n, ctl_found = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    for st in ('W02', 'L01'):
        dd = copy_store(st, 'why')
        con = sqlite3.connect('file:%s/stores/%s/muninn.db?mode=ro' % (F, st), uri=True)
        typed = con.execute("select id, kind, object from served_record where kind in ('decision','invariant','correction') and subject not like 'commit:%' order by id").fetchall()
        aw, ok = [], []
        for rid, kind, obj in typed:
            first = next((x.strip() for x in obj.splitlines() if x.strip()), '')[:300]
            rt = route(first)
            (aw if rt in KINDS and kind not in KINDS[rt] else ok).append((rid, first))
        for rid, first in aw:
            away_n[st] += 1
            away_found[st] += rid in why(dd, first)
        for rid, first in ok[:40]:
            ctl_n[st] += 1
            ctl_found[st] += rid in why(dd, first)
        if st == 'W02':
            ret = con.execute("select id, object from record where invalid=1 and kind<>'episode' order by id desc limit 200").fetchall()
            n = a_ok = b_ok = 0
            for rid, obj in ret:
                words = [w for w in (fts_term(x) for x in obj.split()) if w and len(w) >= 6 and w not in STOP]
                if not words:
                    continue
                w = max(words, key=len)
                if con.execute('select count(*) from record where body like ?', ('%' + w + '%',)).fetchone()[0] > 20:
                    continue
                n += 1
                a_ok += rid in why(dd, w, all_=True, limit=20)
                b_ok += rid in why(dd, 'what about ' + w, all_=True, limit=20)
                if n >= 30:
                    break
            out['all_flag'] = {'asked': n, 'one_word_found': a_ok, 'what_about_found': b_ok}
            # gender flip (R-15), W02
            users = con.execute("select id, object from served_record where kind in ('decision','invariant','correction') and origin='user_said' order by id").fetchall()
            gn = gf = 0
            for rid, obj in users:
                ws = sorted(set(w for w in (fts_term(x) for x in obj.split()) if w and w.isalpha() and len(w) >= 6 and w not in STOP))
                scored = []
                for w in ws:
                    dc = con.execute('select count(*) from record_fts where record_fts match ?', ('"%s"' % w,)).fetchone()[0]
                    if 0 < dc <= 30:
                        scored.append((dc, w))
                scored.sort()
                pick = [w for _, w in scored[:3]]
                if len(pick) < 2:
                    continue
                mut = [gender(w) for w in pick]
                if sum(m is not None for m in mut) < 2:
                    continue
                gn += 1
                gf += rid in why(dd, ' '.join(m for m in mut if m))
            out['gender_flip_W02'] = {'asked': gn, 'found_top8': gf}
        con.close()
    out['routed_away'] = {'records': sum(away_n.values()), 'returned': sum(away_found.values()), 'by_store': {k: [away_n[k], away_found[k]] for k in away_n},
                          'control_records': sum(ctl_n.values()), 'control_returned': sum(ctl_found.values())}
    per['all']['c5'] = out

BINDING = {'c1': 'held-out unrelated_returned and useful_returned', 'c2': 'c12.c2_same_ids (needs --against); mean_tokens is secondary',
           'c3': 't1 same_session == tried; t2 offered_again_after_stop == 1; t3 prompts_with_stale_twin == 0',
           'c4': 'all_slots share_lenient_of_labelled and share_strict_of_labelled, neither may fall; coverage_today neither == 0',
           'c5': 'usage_v2.spanish_reached, gender_flip_W02.found_top8, routed_away.returned, all_flag.what_about_found'}
write_counts('c_delivery', build, args, dict(per), {'binding': BINDING})
if items_out:
    p = os.path.join(COUNTS, 'c_delivery_%s_items.json' % build)
    cur = json.load(open(p)) if os.path.isfile(p) else {}
    cur.update(items_out)
    t = json.dumps(cur, sort_keys=True, indent=0)
    check_private(t)
    open(p, 'w', newline='\n').write(t)
