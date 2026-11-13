#!/usr/bin/env python3
"""The replay cell of `muninn remember` (eleventh amendment). Not a reading of any rule of
section A: it tests the command's mechanics and decides nothing about the extractor.

  python -I a_remember.py --bin <muninn.exe> --commit <sha> [--split design|heldout|all] [--build <label>]

For every durable message of the recall set that a person wrote (final label `a`), on a fresh
copy of that message's store, the command is called once with the session identified (its id,
and the staged transcript, which the copy's session log is made to note for that session, as a
hook would: the command takes a transcript from the session log only)
and the statement taken word for word from the message at its first anchor that can be found
in it. The message is read from the staged transcript at the item's byte offset (the line that
opens the turn), or from the item's text when that line holds no text.

Counted per split: `user_said_right_turn` (recorded or restated as `user_said` at the item's
turn), `deduped_twin` (found on record at the item's turn already: the extractor typed it),
`user_said_other_turn`, `lower_origin` (a miss of the word-for-word check), `errors`, and
`anchor_not_located` (no anchor of the label could be found in the message text; not called).
Counts only; the per-item states stay in the private work directory.
"""
import collections, json, os, re, shutil, subprocess, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from inputs import staged

ap = parser(__doc__)
args = ap.parse_args()
F = fixtures()
build = build_name(args)
KIND = {'decision': 'decision', 'rule': 'invariant', 'invariant': 'invariant', 'correction': 'correction', 'deadend': 'deadend'}

R = [json.loads(l) for l in open(F + '/out/extract/recall_items.jsonl', encoding='utf-8')]
T = json.load(open(F + '/out/extract/transcripts.json', encoding='utf-8'))
by_sid = {os.path.basename(t['path']).rsplit('.', 1)[0]: t['path'] for t in T}
for r in R:
    by_sid.setdefault(r['session'], r['path'])
staged_a, input_counts = staged('a')
lab = {x['id']: x for x in labels('recall', args.labels)}
anchors = {a['id']: a['anchors'] for a in (json.loads(l) for l in open(F + '/out/usage-v4/labels/recall_anchors.jsonl', encoding='utf-8'))}


def folded(s):
    """`norm` of each character, with the index it came from, so a match maps back to the text."""
    out = []
    for i, ch in enumerate(s):
        d = unicodedata.normalize('NFKD', ch.lower())
        d = ''.join(c for c in d if not unicodedata.combining(c))
        for c in d:
            w = c if re.match(r'[\w%+]', c) else ' '
            if w == ' ' and (not out or out[-1][0] == ' '):
                continue
            out.append((w, i))
    return out


def span(text, anchor):
    """The words of `text` the normalised `anchor` stands for, as typed."""
    f = folded(text)
    flat = ''.join(c for c, _ in f)
    a = norm(anchor)
    if not a:
        return None
    k = flat.find(a)
    if k < 0:
        return None
    lo, hi = f[k][1], f[k + len(a) - 1][1]
    return text[lo:hi + 1].strip()


def line_text(path, offset):
    with open(path, 'rb') as fh:
        fh.seek(offset)
        raw = fh.readline()
    try:
        v = json.loads(raw)
    except ValueError:
        return None
    c = (v.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = []
        for p in c:
            if isinstance(p, dict):
                if p.get('type') == 'text':
                    parts.append(p.get('text') or '')
                elif p.get('type') == 'tool_result':
                    x = p.get('content')
                    parts.append(x if isinstance(x, str) else ' '.join(q.get('text', '') for q in (x or []) if isinstance(q, dict)))
        return '\n'.join(parts) or None
    return None


root = work('a_remember', build)
states = {}
per = {}
for sp in splits_for(args.split):
    per[sp] = collections.Counter()
for r in R:
    L = lab.get(r['uid'])
    if not L or L['label'] != 'a':
        continue
    sp = split_of(r['uid'])
    if not in_split(r['uid'], args.split):
        continue
    src = staged_a.get(by_sid.get(r['session']))
    if not src:
        state = 'transcript_missing'
    else:
        offset = int(r['uid'].rsplit(':', 1)[1])
        text = line_text(src, offset) or r['text_shown']
        stmt = None
        for a in anchors.get(r['uid'], []):
            stmt = span(text, a) or span(r['text_shown'], a)
            if stmt:
                break
        if not stmt:
            state = 'anchor_not_located'
        else:
            proj = os.path.join(root, 'proj')
            shutil.rmtree(proj, ignore_errors=True)
            os.makedirs(os.path.join(proj, '.git'))
            shutil.copytree(os.path.join(F, 'stores', r['store']), os.path.join(proj, '.muninn'))
            tx = os.path.join(root, 'tx')
            shutil.rmtree(tx, ignore_errors=True)
            os.makedirs(tx)
            t = os.path.join(tx, r['session'] + '.jsonl')
            shutil.copyfile(src, t)
            # the session log of the copy notes the transcript for the session, as a hook that
            # sees it does (`sessions::note`): the command takes a transcript only from there
            log = os.path.join(proj, '.muninn', 'log')
            os.makedirs(log, exist_ok=True)
            with open(os.path.join(log, 'sessions.jsonl'), 'a', encoding='utf-8', newline='\n') as fh:
                fh.write(json.dumps({'session': r['session'], 'transcript': t}) + '\n')
            p = subprocess.run([args.bin, '--cwd', proj, '--json', 'remember', '--kind', KIND.get(L.get('kind'), 'decision'),
                                '--session', r['session'], '--transcript', t, '--', stmt],
                               capture_output=True, timeout=300)
            if p.returncode:
                state = 'errors'
            else:
                try:
                    v = json.loads(p.stdout)
                except ValueError:
                    v = None
                if not v:
                    state = 'errors'
                elif v.get('origin') != 'user_said':
                    state = 'lower_origin'
                    # which check the statement missed: the word-for-word one, or the session
                    reason = 'lower_not_found' if 'word for word' in (v.get('lower') or '') else 'lower_other'
                    for s_ in (sp, 'all'):
                        if s_ in per:
                            per[s_][reason] += 1
                elif v.get('turn') != r['turn']:
                    state = 'user_said_other_turn'
                elif v.get('outcome') == 'deduped':
                    state = 'deduped_twin'
                else:
                    state = 'user_said_right_turn'
            shutil.rmtree(proj, ignore_errors=True)
    states[r['uid']] = state
    for s in (sp, 'all'):
        if s in per:
            per[s][state] += 1
            per[s]['durable_messages'] += 1

out = {sp: dict(c) for sp, c in per.items()}
extra = {'inputs': input_counts, 'note': 'replay cell of muninn remember (eleventh amendment); decides nothing under section A'}
write_counts('a_remember', build, args, out, extra)
t = json.dumps(states, sort_keys=True, indent=0)
check_private(t)
open(os.path.join(work('a_remember'), 'a_remember_%s_items.json' % build), 'w', newline='\n').write(t)
