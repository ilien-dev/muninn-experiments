"""usage-v4, rule F, rule compiler: the enforceable share of one half of `corpora/claude-md`
for two builds of `muninn-bench`, and the rules whose reading changed between them.

    python -I f_rules.py --prev <muninn-bench> --cand <muninn-bench> --corpus <corpora/claude-md>
                         --half design|design_readable|heldout [--list <out.md>] [--counts <out.json>]

Both builds run `rules --dir <corpus>/files --holdout splits/f_rules_<half>.txt`, once for the
counts (`--json`) and once for the list of enforceable rules (`--list`). A rule is *newly
enforceable* when the candidate lists it and the previous build does not; its control is
*changed* when both list it with different controls. `--list` writes those rules with their
controls, for the reader rule F names: the corpus is public text.
"""
import argparse, hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha16(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]


def run(binary, corpus, names, *flags):
    r = subprocess.run([binary, 'rules', '--dir', os.path.join(corpus, 'files'), '--holdout', names, *flags],
                       capture_output=True)
    if r.returncode:
        sys.exit('rules failed: ' + r.stderr.decode('utf-8', 'replace')[-800:])
    return r.stdout.decode('utf-8', 'replace')


def listed(text):
    """{(file:line, rule text): (pattern, controls)} from `rules --list`."""
    out, lines = {}, text.splitlines()
    for i in range(0, len(lines) - 2, 3):
        pattern, where = lines[i].split()[0], lines[i].split()[-1]
        rule = lines[i + 1].strip()
        out[(where, rule)] = (pattern, lines[i + 2].strip()[2:].strip())
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--prev', required=True)
    ap.add_argument('--cand', required=True)
    ap.add_argument('--corpus', required=True)
    ap.add_argument('--half', required=True, choices=['design', 'design_readable', 'design_unread', 'heldout'])
    ap.add_argument('--list')
    ap.add_argument('--counts')
    a = ap.parse_args()
    names = os.path.join(HERE, 'splits', 'f_rules_%s.txt' % a.half)
    res = {}
    lists = {}
    for who, binary in (('previous', a.prev), ('candidate', a.cand)):
        j = json.loads(run(binary, a.corpus, names, '--json'))
        enforceable = j['candidates'] - j['by_class'].get('interpretive_only', 0)
        res[who] = dict(bench_sha256=sha16(binary), files=j['files'], candidates=j['candidates'],
                        by_class=j['by_class'], by_pattern=j['by_pattern'], enforceable=enforceable,
                        enforceable_share=round(enforceable / j['candidates'], 5) if j['candidates'] else None)
        lists[who] = listed(run(binary, a.corpus, names, '--list'))
    prev, cand = lists['previous'], lists['candidate']
    new = sorted(k for k in cand if k not in prev)
    gone = sorted(k for k in prev if k not in cand)
    changed = sorted(k for k in cand if k in prev and cand[k] != prev[k])
    by_pattern = {}
    for k in new:
        by_pattern[cand[k][0]] = by_pattern.get(cand[k][0], 0) + 1
    res.update(half=a.half, newly_enforceable=len(new), newly_enforceable_by_pattern=by_pattern,
               no_longer_enforceable=len(gone), control_changed=len(changed),
               control_changed_by_pattern={p: sum(1 for k in changed if cand[k][0] == p) for p in sorted({cand[k][0] for k in changed})})
    text = json.dumps(res, indent=1, sort_keys=True)
    print(text)
    if a.counts:
        open(a.counts, 'w', newline='\n').write(text + '\n')
    if a.list:
        with open(a.list, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# %s half: rules the candidate reads differently\n\n' % a.half)
            for title, keys in (('Newly enforceable', new), ('Control changed', changed), ('No longer enforceable', gone)):
                f.write('## %s (%d)\n\n' % (title, len(keys)))
                for n, k in enumerate(keys, 1):
                    where, rule = k
                    f.write('%d. `%s` — %s\n\n   > %s\n\n' % (n, where, (cand.get(k) or prev[k])[0], rule.strip('"')))
                    if k in prev:
                        f.write('   - before: `%s`\n' % prev[k][1])
                    if k in cand:
                        f.write('   - %s: `%s`\n' % ('now' if k in prev else 'control', cand[k][1]))
                    f.write('\n')


if __name__ == '__main__':
    main()
