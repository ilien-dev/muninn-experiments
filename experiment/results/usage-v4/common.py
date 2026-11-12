"""Shared plumbing for the usage-v4 harness.

Every entry point takes `--bin <muninn.exe>` and `--split design|heldout|all`, prints its counts
as JSON and merges them into `counts/<section>_<build>.json`, where `<build>` is the first 16 hex
digits of the binary's sha256 (or `--build` when given).

Private fixtures (store copies, transcripts, item texts, final labels) are read from
`$MUNINN_USAGE_FIXTURES`; nothing from there is ever written under this directory. Scratch copies
go to `$MUNINN_USAGE_WORK` (default `$MUNINN_USAGE_FIXTURES/work/usage-v4`). Machine-specific
paths (project checkouts, the WSL root, project-name-to-label map) come from
`$MUNINN_USAGE_FIXTURES/usage-v4.local.json`, which is private too.

Item ids and the split rule are those of the usage-v4 pre-registration:
`sha256("usage-v4:" + id)`, even first byte = design, odd = held-out.
"""
import argparse, collections, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTS = os.path.join(HERE, 'counts')
SPLITS = os.path.join(HERE, 'splits')


def fixtures():
    f = os.environ.get('MUNINN_USAGE_FIXTURES')
    if not f or not os.path.isdir(f):
        sys.exit('MUNINN_USAGE_FIXTURES must point at the private fixture root')
    return f.replace('\\', '/')


def work(*parts):
    w = os.environ.get('MUNINN_USAGE_WORK') or os.path.join(fixtures(), 'work', 'usage-v4')
    p = os.path.join(w, *parts)
    os.makedirs(p, exist_ok=True)
    return p.replace('\\', '/')


def local():
    p = os.path.join(fixtures(), 'usage-v4.local.json')
    return json.load(open(p, encoding='utf-8')) if os.path.isfile(p) else {}


def split_of(item_id):
    return 'design' if hashlib.sha256(('usage-v4:' + item_id).encode()).digest()[0] % 2 == 0 else 'heldout'


def in_split(item_id, split):
    return split == 'all' or split_of(item_id) == split


def splits_for(arg):
    return ['design', 'heldout', 'all'] if arg == 'all' else [arg]


def labels(name, which='final'):
    """Final labels (frozen, ids + codes) or the first labeller's, mapped to the same codes."""
    F = fixtures()
    if which == 'final+pool':
        base = labels(name, 'final')
        if name != 'delivery':
            return base
        meta = F + '/out/usage-v4/labels/delivery_pool.ingest.json'
        ext = F + '/out/usage-v4/labels/delivery_pool.jsonl'
        if not os.path.isfile(meta) or not os.path.isfile(ext):
            raise SystemExit('final+pool: no pool extension (run c_pool.py ingest first)')
        m = json.load(open(meta))
        if not m.get('usable'):
            raise SystemExit('final+pool: the pool labels failed their control agreement and are not used')
        if sha16(F + '/out/usage-v4/labels/delivery.jsonl') != m['frozen_sha256'] or sha16(ext) != m['extension_sha256']:
            raise SystemExit('final+pool: the frozen file or the extension changed since ingest')
        have = {(x['item'], x['id']) for x in base}
        extra = [json.loads(l) for l in open(ext, encoding='utf-8')]
        return base + [x for x in extra if (x['item'], x['id']) not in have]
    if which == 'final':
        return [json.loads(l) for l in open(F + '/out/usage-v4/labels/%s.jsonl' % name, encoding='utf-8')]
    if name == 'precision':
        return [{'id': v['key'], 'label': v['class']} for v in (json.loads(l) for l in open(F + '/out/extract/precision_labels.jsonl', encoding='utf-8'))]
    if name == 'recall':
        M = {'D': 'a', 'I': 'a', 'C': 'a', 'E': 'a', 'X': 'nh', 'O': 'opt', '-': 'b', 'c': 'b', 'e': 'b'}
        K = {'D': 'decision', 'I': 'rule', 'C': 'correction', 'E': 'deadend'}
        out = []
        for v in (json.loads(l) for l in open(F + '/out/extract/recall_labels.jsonl', encoding='utf-8')):
            r = {'id': v['uid'], 'label': M[v['primary']], 'hit': v.get('hit') or ''}
            if r['label'] == 'a':
                r['kind'] = K[v['primary']]
            out.append(r)
        return out
    if name == 'delivery':
        M = {'useful': 'u', 'related': 'r', 'unrelated': 'x', 'harmful': 'h'}
        return [{'item': v['item'], 'id': int(v['id']), 'label': M[v['label']]} for v in (json.loads(l) for l in open(F + '/out/delivery/labels/prompt_pass1.jsonl', encoding='utf-8'))]
    raise ValueError(name)


def sha16(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()[:16]


def version(binary):
    try:
        return subprocess.run([binary, '--version'], capture_output=True, text=True).stdout.strip()
    except OSError:
        return '?'


def parser(desc):
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument('--bin', required=True, help='muninn binary to measure')
    ap.add_argument('--split', choices=['design', 'heldout', 'all'], default='all')
    ap.add_argument('--build', help='label for counts/<section>_<build>.json (default: sha256 prefix of --bin)')
    ap.add_argument('--labels', choices=['final', 'first', 'final+pool'], default='final',
                    help='final = frozen usage-v4 labels; first = the first labeller (reproduces the analysis figures); '
                         'final+pool = frozen delivery labels plus the pool extension (c_pool.py ingest), counts in <build>-pool')
    ap.add_argument('--commit', help='commit the measured build was made from (recorded in the counts)')
    return ap


def _forbidden():
    words = ['wsl.localhost', 'documents/projects', 'appdata', '/home/', 'users/', '.jsonl'] + [w.lower() for w in local().get('forbidden', [])]
    m = os.path.join(fixtures(), 'stores', 'map.txt')
    if os.path.isfile(m):
        for l in open(m, encoding='utf-8'):
            p = l.strip().split('|', 1)[-1].strip('/').split('/')
            for seg in p:
                if seg and seg not in ('.muninn', 'Documents', 'Projects', 'home', 'Untitled', 'muninn') and len(seg) > 3:
                    words.append(seg.lower())
    for k in local().get('project_labels', {}):
        words.append(k.lower())
    return sorted(set(words))


def check_private(text):
    low = text.lower()
    bad = [w for w in _forbidden() if w in low]
    if bad:
        raise SystemExit('refusing to write counts: they contain %d forbidden term(s)' % len(bad))


def write_counts(section, build, args, per_split, extra=None):
    """Merge {split: counts} into counts/<section>_<build>.json and print it."""
    if FAILS:
        raise SystemExit('refusing to write counts: %d failed step(s): %s' % (sum(FAILS.values()), dict(FAILS)))
    os.makedirs(COUNTS, exist_ok=True)
    p = os.path.join(COUNTS, '%s_%s.json' % (section, build))
    cur = json.load(open(p)) if os.path.isfile(p) else {}
    cur.setdefault('section', section)
    cur['build'] = build
    cur['binary_sha256'] = sha16(args.bin)
    cur['binary_version'] = version(args.bin)
    cur['labels'] = args.labels
    if getattr(args, 'commit', None):
        cur['commit'] = args.commit
    elif getattr(args, 'drop_commit', False):
        cur.pop('commit', None)
    cur.setdefault('splits', {})
    for sp, v in per_split.items():
        if isinstance(cur['splits'].get(sp), dict) and isinstance(v, dict):
            cur['splits'][sp].update(v)  # a rerun of one part keeps the others
        else:
            cur['splits'][sp] = v
    if extra:
        cur.update(extra)
    text = json.dumps(cur, indent=1, sort_keys=True, ensure_ascii=True)
    check_private(text)
    open(p, 'w', newline='\n').write(text + '\n')
    print(text)
    return p


def build_name(args):
    if args.labels == 'first' and not args.build:
        return sha16(args.bin) + '-first'
    if args.labels == 'final+pool' and not args.build:
        return sha16(args.bin) + '-pool'
    return args.build or sha16(args.bin)


def norm(s):
    import unicodedata
    s = unicodedata.normalize('NFKD', (s or '').lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^\w%+]+', ' ', s).strip()


def est(s):
    """tokens::estimate — ceil(chars/3)."""
    return -(-len(s) // 3)


HDR = re.compile(r'^\[muninn:([a-z_]+)([^\]]*)\] #(\d+) ')


def block_ids(text):
    """Record ids of the blocks a hook rendered, in order."""
    return [int(m.group(3)) for m in (HDR.match(l) for l in text.split('\n')) if m]


FAILS = collections.Counter()


def fail(what):
    """Count a failed step. write_counts refuses to write while any is counted."""
    FAILS[what] += 1


def run(cmd, what, timeout=900, ok_codes=(0,), **kw):
    """subprocess.run that counts a timeout or an unexpected exit code as a failure of `what`."""
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout, **kw)
    except subprocess.TimeoutExpired:
        fail(what + ':timeout')
        return None
    except OSError:
        fail(what + ':cannot_start')
        return None
    if r.returncode not in ok_codes:
        fail(what + ':exit')
    return r


def _bad_stderr(err):
    e = err.lower()
    return 'panic' in e or 'error' in e or 'unable to open' in e


def hook(binary, event, cwd, payload, env=None):
    """Run one hook. A hook exits 0 and may print nothing (a gated prompt), so a failure is: no
    store at --cwd, a timeout, a non-zero exit, stdout that is not the hook JSON, or an error on
    stderr. Each is counted (see FAILS); the text returned is then ''."""
    if not os.path.isfile(os.path.join(cwd, '.muninn', 'muninn.db')):
        fail('hook:%s:no_store' % event)
        return ''
    inp = json.dumps(dict(payload, hook_event_name=event, cwd=cwd))
    out = run([binary, 'hook', event, '--cwd', cwd], 'hook:' + event, timeout=120, input=inp.encode('utf-8'), env=env)
    if out is None:
        return ''
    err = out.stderr.decode('utf-8', 'replace')
    if _bad_stderr(err):
        fail('hook:%s:stderr' % event)
    so = out.stdout.decode('utf-8', 'replace').strip()
    if not so:
        return ''
    try:
        return json.loads(so)['hookSpecificOutput']['additionalContext']
    except Exception:
        fail('hook:%s:bad_stdout' % event)
        return ''
