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

`--reading sentences` is the thirteenth amendment's second reading: the statement passed is the
whole sentence, or the consecutive sentences, of the person's words that contain the anchor, cut
by a port of the product's `extract::split_sentences` (below). An item whose anchor cannot be
located in the person's words, or whose derived statement the command refuses on its
whole-sentence check, is `not_derivable` and is not counted as a lower origin. Counts go to
`counts/a_remember_<build>-sentences.json` unless `--build` names them.
"""
import collections, json, os, re, shutil, subprocess, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from inputs import staged

ap = parser(__doc__)
ap.add_argument('--reading', choices=['anchor', 'sentences'], default='anchor',
                help='anchor: the labelled anchor phrase (eleventh amendment); sentences: the whole sentences that hold it (thirteenth)')
args = ap.parse_args()
F = fixtures()
build = build_name(args) if (args.build or args.reading == 'anchor') else build_name(args) + '-sentences'
SENT = args.reading == 'sentences'


# --- the person's words and the product's sentence cut, ported (thirteenth amendment) ---------
ANSWERED = 'Your questions have been answered:'
PASTE = re.compile(r'(?s)<pasted_content\b[^>]*>.*?(?:</pasted_content>|\Z)')
QUOTE = re.compile('"[^"\n]{40,}"|\u201c[^\u201d\n]{40,}\u201d')
PICK = re.compile('"="([^"]*)"')
SPEAKERS = re.compile(r'(?im)^[ \t]*(?:user|assistant|system|human|usuario|asistente)[ \t]*:')


def persons_words(text):
    """`extract::persons_words` of the turn whose opening line holds `text`."""
    up = text.strip()
    if not up:
        return None
    if up.startswith(ANSWERED):
        picks = PICK.findall(up)
        return '\n'.join(picks) if picks else None
    s_ = QUOTE.sub(' ', PASTE.sub(' ', up))
    out, fenced = [], False
    for line in s_.split('\n'):
        t_ = line.lstrip()
        if t_.startswith('```') or t_.startswith('~~~'):
            fenced = not fenced
            continue
        if fenced or t_.startswith('>'):
            continue
        out.append(line + '\n')
    own = ''.join(out)
    return None if len(SPEAKERS.findall(own)) >= 2 else own


WS = b' \t\n\x0c\r'


def split_sentences(s_):
    """A port of `extract::split_sentences`: (start, end) character spans of the pieces."""
    b = s_.encode('utf-8')
    spans, start, depth = [], 0, 0
    def piece(lo, hi):
        txt = b[lo:hi].decode('utf-8')
        stripped = txt.strip()
        if stripped:
            a_ = len(b[:lo].decode('utf-8')) + (len(txt) - len(txt.lstrip()))
            spans.append((a_, a_ + len(stripped)))
    for i, c in enumerate(b):
        if c == ord('('):
            depth += 1
        elif c == ord(')'):
            depth = max(depth - 1, 0)
        j = i
        while j > 0 and (65 <= b[j - 1] <= 90 or 97 <= b[j - 1] <= 122):
            j -= 1
        nxt = next((x for x in b[i + 1:] if x not in WS), None)
        abbrev = c == ord('.') and 1 <= i - j <= 3 and nxt is not None and not (65 <= nxt <= 90)
        end = c == ord('\n') or (c in b'.!;' and not abbrev and depth == 0 and (i + 1 >= len(b) or b[i + 1] in WS))
        if end:
            piece(start, i)
            start = i + 1
    piece(start, len(b))
    return spans


def anchor_at(text, anchor):
    """The character span of `text` the normalised `anchor` stands for."""
    f = folded(text)
    flat = ''.join(c for c, _ in f)
    a = norm(anchor)
    k = flat.find(a) if a else -1
    if k < 0:
        return None
    return f[k][1], f[k + len(a) - 1][1]


def soften_breaks(w):
    """A port of `remember::soften_breaks` (Task 7 fix round 2): a line break ends a sentence only
    after a stop (. ! ? ; : and the ellipsis character) or at a blank line; any other is a space. Same length."""
    out = []
    for i, c in enumerate(w):
        if c != '\n':
            out.append(c)
            continue
        before = ''.join(out).rstrip(' \t\r')[-1:] or None
        after = next((x for x in w[i + 1:] if x not in ' \t\r'), None)
        ends = before is None or before in '.!?;:\u2026\n' or after in (None, '\n')
        out.append('\n' if ends else ' ')
    return ''.join(out)


def sentences_holding(words, anchor):
    words = soften_breaks(words)
    at = anchor_at(words, anchor)
    if not at:
        return None
    lo, hi = at
    hit = [sp_ for sp_ in split_sentences(words) if sp_[0] <= hi and sp_[1] > lo]
    return words[hit[0][0]:hit[-1][1]] if hit else None
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
        if SENT:
            words = persons_words(text)
            for a in anchors.get(r['uid'], []) if words else []:
                stmt = sentences_holding(words, a)
                if stmt:
                    break
        else:
            for a in anchors.get(r['uid'], []):
                stmt = span(text, a) or span(r['text_shown'], a)
                if stmt:
                    break
        if not stmt:
            state = 'not_derivable_not_located' if SENT else 'anchor_not_located'
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
                elif SENT and v.get('origin') != 'user_said' and 'word for word' in (v.get('lower') or ''):
                    # the port and the product, or the reconstructed words, disagree
                    state = 'not_derivable_refused'
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
            if state.startswith('not_derivable'):
                per[s]['not_derivable'] += 1

out = {sp: dict(c) for sp, c in per.items()}
extra = {'inputs': input_counts, 'reading': args.reading,
         'note': ('second reading, whole sentences holding the anchor (thirteenth amendment)' if SENT else 'replay cell of muninn remember (eleventh amendment)') + '; decides nothing under section A'}
write_counts('a_remember', build, args, out, extra)
t = json.dumps(states, sort_keys=True, indent=0)
check_private(t)
open(os.path.join(work('a_remember'), 'a_remember_%s_items.json' % build), 'w', newline='\n').write(t)
