#!/usr/bin/env python3
"""A diagnostic, added after the Result of usage-v4 was written. It decides no rule.

  python -I b3_path.py --bin <muninn.exe> [--commit <sha>]

Why. `loop8/eval_all.py` reads its `served_ok` and `old_served` cells from `muninn recall
"<topic>"`. Nine of the ten loop 8 topics are three words long. Since Task 3 of this plan
`muninn recall` applies the gates of the prompt hook, and the hook has always been silent on a
prompt under four words, so the command prints nothing for those topics. On every build from
Task 6 on those cells read 2/30 or 0/30 where 1.2.0 reads 11/30 and 8/30; rule B3 names only
`retired_a` and `kept_b`, which are equal. This script asks whether the product delivers the
current answer less, or whether the instrument stopped seeing it.

How. `eval_all.py` runs unchanged (the registered evaluator, arms `both` and `noise`, orders
`adjacent` and `blocks`). Each time it asks `muninn recall <topic>` of a scenario's store, this
wrapper first reads the same store through the two paths a session takes:

- the prompt hook, `hook UserPromptSubmit`, with the prompt
  "Which <topic> do we use in this project now?" in a session of its own;
- the session start, `hook SessionStart`, in another session of its own: its blocks and its
  catalogue.

From each context the lines that open with `[muninn:` and the `evidence:` lines are dropped, as
`eval_all.delivered_text` drops them, and a value is looked for as a whole token, as
`eval_all.says` does. Counted per arm and order, out of the 30 cells:

- `recall_printed`: `muninn recall <topic>` printed anything (the instrument);
- `prompt_new`, `prompt_old`: the new value, the old value, in the prompt hook's context;
- `start_new`, `start_old`: the same in the session start's context;
- `context_ok`: the new value in either context and the old value in neither;
- `context_old`: the old value in either.

Both builds are read the same way. A session start may start a detached `maintain`; the
evaluator has run `maintain` on the store just before, so it finds nothing new.
Counts only: `counts/b3_path_<build>.json`.
"""
import argparse, collections, json, os, re, runpy, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import COUNTS, HERE, check_private, sha16, version

ap = argparse.ArgumentParser()
ap.add_argument('--bin', required=True)
ap.add_argument('--commit')
a = ap.parse_args()
BIN = os.path.abspath(a.bin).replace('\\', '/')
EXP = os.path.dirname(os.path.dirname(HERE))
EVAL = os.path.join(EXP, 'loop8', 'eval_all.py')
PROMPT = 'Which %s do we use in this project now?'
scen = json.load(open(os.path.join(EXP, 'loop8', 'scenarios.json')))
VALUES = {x['topic']: (x['old'].lower(), x['new'].lower().split()[0]) for k in scen for x in scen[k] if x.get('new')}
_run = subprocess.run
cells = []
n = [0]


def says(text, value):
    return re.search(r'(?<![0-9a-z])' + re.escape(value) + r'(?![0-9a-z])', text) is not None


def context(root, env, event, payload):
    inp = json.dumps(dict(payload, hook_event_name=event, cwd=root))
    r = _run([BIN, 'hook', event, '--cwd', root], input=inp, capture_output=True, text=True, cwd=root, env=env, encoding='utf-8', errors='replace')
    try:
        text = json.loads(r.stdout)['hookSpecificOutput']['additionalContext']
    except Exception:
        text = ''
    keep = [l for l in text.splitlines() if not l.startswith('[muninn:') and not l.lstrip().startswith('evidence:')]
    return '\n'.join(keep).lower()


def run(args, *x, **k):
    args = [str(v) for v in args]
    if len(args) == 5 and args[1] == '--cwd' and args[3] == 'recall':
        root, topic = args[2], args[4]
        old, new = VALUES[topic]
        n[0] += 1
        p = context(root, k.get('env'), 'UserPromptSubmit', {'session_id': 'diag-p-%d' % n[0], 'prompt': PROMPT % topic})
        s = context(root, k.get('env'), 'SessionStart', {'session_id': 'diag-s-%d' % n[0]})
        r = _run(args, *x, **k)
        cells.append({'recall_printed': bool((r.stdout or '').strip()),
                      'prompt_new': says(p, new), 'prompt_old': says(p, old),
                      'start_new': says(s, new), 'start_old': says(s, old),
                      'context_ok': (says(p, new) or says(s, new)) and not (says(p, old) or says(s, old)),
                      'context_old': says(p, old) or says(s, old)})
        return r
    return _run(args, *x, **k)


subprocess.run = run
out = {}
os.environ.pop('CLAUDE_CODE_SESSION_ID', None)
for arm in ('both', 'noise'):
    for order in ('adjacent', 'blocks'):
        del cells[:]
        f = os.path.join(tempfile.mkdtemp(prefix='b3path-'), 'rows.json')
        sys.argv = [EVAL, '--muninn', BIN, '--arm', arm, '--order', order,
                    '--phrasings', os.path.join(EXP, 'loop8', 'heldout_phrasings.json'),
                    '--scenarios', os.path.join(EXP, 'loop8', 'scenarios.json'), '--out', f]
        runpy.run_path(EVAL, run_name='__main__')
        rows = json.load(open(f))
        if len(rows) != 30 or len(cells) != 30:
            sys.exit('b3_path: %d rows and %d cells, expected 30 and 30' % (len(rows), len(cells)))
        t = collections.Counter()
        for row, c in zip(rows, cells):
            for key in ('retired_a', 'served_ok', 'old_served'):
                t[key] += bool(row[key])
            for key, v in c.items():
                t[key] += bool(v)
        out['%s/%s' % (arm, order)] = {k: '%d/30' % t[k] for k in sorted(set(t) | {'retired_a', 'served_ok', 'old_served', 'recall_printed', 'prompt_new', 'prompt_old', 'start_new', 'start_old', 'context_ok', 'context_old'})}
res = {'section': 'b3_path', 'diagnostic': 'added after the Result of usage-v4; decides no rule', 'binary_sha256': sha16(a.bin),
       'binary_version': version(a.bin), 'prompt_template': PROMPT, 'cells': out}
if a.commit:
    res['commit'] = a.commit
text = json.dumps(res, indent=1, sort_keys=True)
check_private(text)
open(os.path.join(COUNTS, 'b3_path_%s.json' % sha16(a.bin)), 'w', newline='\n').write(text + '\n')
print(text)
