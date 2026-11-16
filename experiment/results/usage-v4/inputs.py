#!/usr/bin/env python3
"""Every input the harness reads from outside the fixture root, staged once into
`$MUNINN_USAGE_FIXTURES/fixtures/inputs/` and read from there only (tenth amendment).

  python -I inputs.py stage      # idempotent: a staged file is frozen and never rewritten
  python -I inputs.py check      # counts per group: listed, staged, unrecoverable, changed

Groups (each a list of original transcript paths; the staged copy keeps the file's name, the
directory is a hash of the original path):
  b1:<corpus>  the transcripts usage-v1's replay reads for each B1 corpus (its store's
               transcript_ref targets; L01's through the WSL share)
  a            the transcripts of the sessions that hold the extraction items
  e            the transcripts the W02 copy's log/sessions.jsonl lists (read by Stop in E)
Source of a copy, first found: (1) the copy already staged, (2) the base build's B1 replay copy
of that file (the state the base read), (3) the copy a_extract staged on its first run, (4) the
live file, (5) another build's B1 replay copy. The manifest (`MANIFEST.json`, private: it holds
path hashes, sizes and sha256) records which.

Entry points call `staged(group)`: it returns {original path: staged path} for the files that
exist and match their sha256, and the count of listed files that do not (`unrecoverable` when no
copy was ever found, `changed` when a staged file is gone or altered). A run with a changed file
writes `inputs.status = "missing input"`, which verdict.py prints as `missing`.
"""
import glob, hashlib, json, os, shutil, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fixtures, local

BASE = 'b93d2f5c222c0424'


def root():
    return os.path.join(fixtures(), 'fixtures', 'inputs')


def manifest_path():
    return os.path.join(root(), 'MANIFEST.json')


def phash(p):
    return hashlib.sha256(p.replace('\\', '/').encode()).hexdigest()[:16]


def fsha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def store_refs(db, wsl=''):
    c = sqlite3.connect('file:%s?mode=ro' % db, uri=True)
    r = sorted({t.rsplit(':', 1)[0] for (t,) in c.execute("select distinct transcript_ref from record where transcript_ref like '%.jsonl:%'")})
    c.close()
    return [(wsl + p) if p.startswith('/home/') else p for p in r]


def groups():
    F = fixtures()
    L = local()
    g = {}
    for proj in sorted(os.listdir(F + '/fixtures/usage-v1/stores')):
        g['b1:' + proj] = store_refs(F + '/fixtures/usage-v1/stores/%s/muninn.db' % proj)
    g['b1:W02now'] = store_refs(F + '/stores/W02/muninn.db')
    g['b1:L01now'] = store_refs(F + '/stores/L01/muninn.db', L.get('wsl_root', ''))
    T = json.load(open(F + '/out/extract/transcripts.json', encoding='utf-8'))
    by_sid = {os.path.basename(t['path']).rsplit('.', 1)[0]: t['path'] for t in T}
    sids = set()
    for l in open(F + '/out/extract/recall_items.jsonl', encoding='utf-8'):
        r = json.loads(l)
        by_sid.setdefault(r['session'], r['path'])
        sids.add((r['store'], r['session']))
    for l in open(F + '/out/extract/precision_items.jsonl', encoding='utf-8'):
        p = json.loads(l)
        sids.add((p['store'], p['session']))
    g['a'] = sorted({by_sid[s] for _, s in sids if s in by_sid})
    seen = []
    for l in open(F + '/stores/W02/log/sessions.jsonl', encoding='utf-8', errors='replace'):
        try:
            t = json.loads(l)['transcript']
        except Exception:
            continue
        if t not in seen:
            seen.append(t)
    g['e'] = seen
    return g


def candidates(path):
    F = fixtures()
    name = os.path.basename(path.replace('\\', '/'))
    rp = os.path.join(F, 'work', 'usage-v4', 'b_retire', 'rp')
    base = glob.glob(os.path.join(rp, BASE, '*', '.replay', name))
    sid = name.rsplit('.', 1)[0]
    tx = glob.glob(os.path.join(F, 'work', 'usage-v4', 'a_extract', 'tx', '*', name))
    other = sorted((p for p in glob.glob(os.path.join(rp, '*', '*', '.replay', name)) if p not in base), key=lambda p: -os.path.getsize(p))
    out = [('base-replay-copy', p) for p in base] + [('a-extract-copy', p) for p in tx]
    if os.path.isfile(path):
        out.append(('live', path))
    return out + [('other-replay-copy', p) for p in other]


def stage():
    os.makedirs(root(), exist_ok=True)
    man = json.load(open(manifest_path())) if os.path.isfile(manifest_path()) else {}
    for grp, paths in groups().items():
        m = man.setdefault(grp, {})
        for p in paths:
            k = phash(p)
            if k in m and m[k].get('staged') and os.path.isfile(os.path.join(root(), m[k]['staged'])):
                continue  # frozen
            dst_rel = os.path.join('tx', k, os.path.basename(p.replace('\\', '/'))).replace('\\', '/')
            cands = candidates(p)
            if not cands:
                m[k] = {'staged': None, 'source': None}
                continue
            src_kind, src = cands[0]
            dst = os.path.join(root(), dst_rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            m[k] = {'staged': dst_rel, 'source': src_kind, 'size': os.path.getsize(dst), 'sha256': fsha(dst)}
    json.dump(man, open(manifest_path(), 'w'), indent=0, sort_keys=True)
    return man


def stage_git():
    """A no-checkout clone of each project repository B1 replays, frozen at staging (its HEAD sha in
    the manifest); replay.py clones from these, never from the live checkout."""
    import subprocess
    L = local()
    man = json.load(open(manifest_path())) if os.path.isfile(manifest_path()) else {}
    g = man.setdefault('git', {})
    projs = set(L.get('label_projects', {}).values())
    for proj in sorted(projs):
        live = os.path.join(L['projects_dir'], proj)
        k = phash(live)
        dst = os.path.join(root(), 'git', k)
        if k in g and os.path.isdir(os.path.join(dst, '.git')):
            continue
        if not os.path.isdir(os.path.join(live, '.git')):
            g[k] = {'staged': None}
            continue
        shutil.rmtree(dst, ignore_errors=True)
        r = subprocess.run(['git', '-c', 'core.longpaths=true', 'clone', '-q', '--no-checkout', '--no-hardlinks', live, dst], capture_output=True)
        head = subprocess.run(['git', '-C', dst, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        g[k] = {'staged': os.path.relpath(dst, root()).replace(os.sep, '/') if r.returncode == 0 else None, 'head': head}
    json.dump(man, open(manifest_path(), 'w'), indent=0, sort_keys=True)


def staged_git(proj):
    """The staged clone of a project, or None."""
    L = local()
    man = json.load(open(manifest_path())) if os.path.isfile(manifest_path()) else {}
    e = man.get('git', {}).get(phash(os.path.join(L['projects_dir'], proj)))
    if not e or not e.get('staged'):
        return None
    d = os.path.join(root(), e['staged'])
    return d if os.path.isdir(os.path.join(d, '.git')) else None


def staged(group):
    """{original path: staged path} for the group's files that are staged and intact, and a dict of
    counts: listed, staged, unrecoverable (no copy was ever found), changed (staged file gone or altered)."""
    man = json.load(open(manifest_path())) if os.path.isfile(manifest_path()) else {}
    m = man.get(group)
    if m is None:
        return {}, {'listed': 0, 'staged': 0, 'unrecoverable': 0, 'changed': 0, 'status': 'missing input', 'note': 'group not staged'}
    out, c = {}, {'listed': 0, 'staged': 0, 'unrecoverable': 0, 'changed': 0}
    for p in groups()[group]:
        c['listed'] += 1
        e = m.get(phash(p))
        if not e or not e.get('staged'):
            c['unrecoverable'] += 1
            continue
        fp = os.path.join(root(), e['staged'])
        if not os.path.isfile(fp) or os.path.getsize(fp) != e['size'] or fsha(fp) != e['sha256']:
            c['changed'] += 1
            continue
        out[p] = fp.replace('\\', '/')
        c['staged'] += 1
    c['status'] = 'missing input' if c['changed'] else 'ok'
    return out, c


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('stage', 'check'):
        sys.exit(__doc__)
    if sys.argv[1] == 'stage':
        man = stage()
        stage_git()
    rep = {}
    rep['git'] = {'projects': len(local().get('label_projects', {})),
                  'staged': sum(1 for p in set(local().get('label_projects', {}).values()) if staged_git(p))}
    for grp in groups():
        _, c = staged(grp)
        man = json.load(open(manifest_path()))
        c['by_source'] = {}
        for e in man.get(grp, {}).values():
            c['by_source'][str(e.get('source'))] = c['by_source'].get(str(e.get('source')), 0) + 1
        rep[grp.split(':')[0] + ':' + (local().get('project_labels', {}).get(grp.split(':', 1)[1], grp.split(':', 1)[1]) if ':' in grp else '')] = c
    print(json.dumps(rep, indent=1, sort_keys=True))
