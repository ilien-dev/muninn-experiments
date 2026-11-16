#!/usr/bin/env python3
"""Section D, the readings a removal needs, over the eleven store copies (read-only).

  python -I d_removals.py --bin <muninn.exe> [--against <other build>]

Readings per store and in total:
- fire_ledger rows by channel: prompt (`literal:literal`), event (`cue:event:*`), catalogue,
  gated (budget / intent), silence, epoch marks, other; and rows whose reason names a dir,
  symbol, file, glob, keyword, post_tool or pre_edit cue.
- the symbol graph: rows in `symbol`, `cue` rows by kind.
- the embedding sidecar: rows in `record_vec`, whether `meta.embed_model` is set.
- `commit_linked` records: active, by subject shape (`commit:` = a commit subject, `said:` = a
  line a commit swapped in, other); delivered ledger rows naming one, by channel and shape.
- PostToolUse: heartbeat rows (log), turn-context log size in bytes.

`--bin` names the build only; the stores are not touched by it. With `--against B`, the delivery
ids of this build and of build B are compared item by item (from `counts/c_delivery_*_items.json`)
together with the B3 rows of both builds, which is the second half of each removal reading.
"""
import collections, json, os, re, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

ap = parser(__doc__)
ap.add_argument('--against')
args = ap.parse_args()
F = fixtures()
build = build_name(args)
STORES = ['W01', 'W02', 'W03', 'W04', 'W05', 'W06', 'W07', 'W08', 'W09', 'W10', 'L01']


def channel(reason):
    r = reason
    if r.startswith(':epoch:'):
        return 'epoch'
    if 'gated:budget' in r:
        return 'gated_budget'
    if 'gated:intent' in r:
        return 'gated_intent'
    if 'silence' in r:
        return 'silence'
    if r.endswith(':catalog'):
        return 'catalogue'
    if ':cue:event:' in r:
        return 'event'
    if r.endswith(':literal'):
        return 'prompt'
    return 'other:' + re.sub(r'\d+', 'N', r)


CUEISH = re.compile(r'(dir|symbol|file|glob|keyword|post_tool|pre_edit|after|cooldown)')
tot = collections.Counter()
per_store = {}
for st in STORES:
    c = sqlite3.connect('file:%s/stores/%s/muninn.db?mode=ro' % (F, st), uri=True)
    q = lambda s, *a: c.execute(s, a).fetchall()
    tables = {r[0] for r in q("select name from sqlite_master where type='table'")}
    s = collections.Counter()
    for reason, n in q('select reason, count(*) from fire_ledger group by 1'):
        s['ledger:' + channel(reason)] += n
        if CUEISH.search(reason.split(':', 1)[-1]) and 'event' not in reason:
            s['ledger:named_cue_rows'] += n
    s['symbol_rows'] = q('select count(*) from symbol')[0][0] if 'symbol' in tables else 0
    for k, n in q('select kind, count(*) from cue group by 1'):
        s['cue:' + k] = n
    s['record_vec_rows'] = q('select count(*) from record_vec')[0][0] if 'record_vec' in tables else 0
    s['embed_model_set'] = int(bool(q("select value from meta where key='embed_model'")))
    for shape, n in q("select case when subject like 'commit:%' then 'commit' when subject like 'said:%' then 'said' else 'other' end, count(*) "
                      "from record where origin='commit_linked' and invalid=0 group by 1"):
        s['commit_linked_active:' + shape] = n
    for reason, shape, n in q("select f.reason, case when r.subject like 'commit:%' then 'commit' when r.subject like 'said:%' then 'said' else 'other' end, count(*) "
                              "from fire_ledger f join record r on r.id=f.record_id where r.origin='commit_linked' group by 1, 2"):
        ch = channel(reason)
        if ch in ('prompt', 'event', 'catalogue'):
            s['commit_linked_delivered:%s:%s' % (ch, shape)] += n
    hb = os.path.join(F, 'stores', st, 'log', 'heartbeat.jsonl')
    n = 0
    for p in (hb, hb + '.1'):
        if os.path.isfile(p):
            with open(p, 'rb') as f:
                n += sum(1 for l in f if b'"PostToolUse"' in l)
    s['posttooluse_heartbeats'] = n
    tc = os.path.join(F, 'stores', st, 'log', 'turn_context.jsonl')
    s['turn_context_bytes'] = os.path.getsize(tc) if os.path.isfile(tc) else 0
    c.close()
    per_store[st] = dict(s)
    tot.update(s)
reading = {
    'ledger_rows_naming_dir_symbol_file_or_tool_cue': tot['ledger:named_cue_rows'],
    'symbol_rows': tot['symbol_rows'], 'stores_with_symbols': sum(1 for v in per_store.values() if v.get('symbol_rows')),
    'record_vec_rows': tot['record_vec_rows'], 'stores_with_embed_model': tot['embed_model_set'],
    'commit_linked_delivered_by_hook': {k.split(':', 1)[1]: v for k, v in tot.items() if k.startswith('commit_linked_delivered:')},
    'commit_linked_active': {k.split(':', 1)[1]: v for k, v in tot.items() if k.startswith('commit_linked_active:')},
    'posttooluse_heartbeats': tot['posttooluse_heartbeats'], 'turn_context_bytes': tot['turn_context_bytes'],
    'ledger_by_channel': {k.split(':', 1)[1]: v for k, v in tot.items() if k.startswith('ledger:') and k != 'ledger:named_cue_rows'},
}
extra = {'per_store': per_store}
if args.against:
    def items(b):
        p = os.path.join(COUNTS, 'c_delivery_%s_items.json' % b)
        return json.load(open(p))['c12'] if os.path.isfile(p) else {}
    a, b = items(build), items(args.against)
    cmp = {}
    for sp in splits_for(args.split):
        ks = [k for k in a if k in b and in_split(k, sp)]
        cmp[sp] = {'prompts_compared': len(ks), 'same_ids': sum(a[k]['ids'] == b[k]['ids'] for k in ks)}
    def b3(bb):
        p = os.path.join(COUNTS, 'b_retire_%s.json' % bb)
        return json.load(open(p))['splits']['all'].get('b3') if os.path.isfile(p) else None
    extra['against'] = {'build': args.against, 'delivery_ids': cmp, 'b3_equal': b3(build) == b3(args.against) and b3(build) is not None}
write_counts('d_removals', build, args, {'all': reading}, extra)
