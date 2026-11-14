"""usage-v4, rule F, Codex first clause: what a build stores from a Codex rollout.

    python -I f_codex.py --bin <muninn.exe> --rollouts <file or directory> --set invented|real

Two routes, both in temporary directories with a temporary home and Codex home (the real ones
are never read or written):

  hooks   The route a build installs by itself (sixteenth amendment). `<bin> init` runs in a new
          project on a machine where Codex's home exists; then the commands the project's
          `.codex/hooks.json` registers for SessionStart, UserPromptSubmit, Stop and SessionEnd are
          run in that order through the shell Codex uses, each with the input Codex documents for
          it and the rollout as `transcript_path`. A build that leaves no hooks file runs none.
  direct  The rollout handed over by hand: `<bin> init` on a machine without Codex, then
          `<bin> ingest <rollout>`. Reported, decides nothing.

Counts a rollout: typed records (every kind but `episode`) by kind and by origin, and the
`user_said` records whose turn the rollout does not mark as a person's. That mark is read here,
from the rollout, by this script's own rule: the session's `source` is `cli` or `vscode`, its
`thread_source` is `user` or absent, and the `task_started` before the message has no
`turn_trigger` or `user`. A record is tied to its turn by the byte offset its evidence names.

Only counts are written. `--set real` writes totals and, per rollout, a label `Rnn` in directory
order: no path, name, id or text.
"""
import json, os, shutil, sys, tempfile, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

EVENTS = ['SessionStart', 'UserPromptSubmit', 'Stop', 'SessionEnd']


def read_rollout(path):
    """(session id, first message text, [(line start, person?)] for every UserMessage item)."""
    sid, first, turns = '', '', []
    session_person, turn_person, off = False, True, 0
    with open(path, 'rb') as f:
        for raw in f:
            start, off = off, off + len(raw)
            try:
                v = json.loads(raw)
            except ValueError:
                continue
            p = v.get('payload') if isinstance(v.get('payload'), dict) else {}
            t = v.get('type')
            if t == 'session_meta':
                sid = p.get('id') or sid
                src, th = p.get('source'), p.get('thread_source')
                session_person = (isinstance(src, str) and src.lower() in ('cli', 'vscode')
                                  and (th is None or th == 'user'))
            elif t == 'event_msg' and p.get('type') == 'task_started':
                a = p.get('turn_attribution')
                trig = a.get('turn_trigger') if isinstance(a, dict) else None
                turn_person = trig is None or trig == 'user'
            elif t == 'event_msg' and p.get('type') == 'item_completed':
                it = p.get('item') if isinstance(p.get('item'), dict) else {}
                if it.get('type') == 'UserMessage':
                    text = '\n'.join(b.get('text', '') for b in it.get('content') or []
                                     if isinstance(b, dict) and isinstance(b.get('text'), str))
                    if not text.strip():
                        continue
                    first = first or text
                    turns.append((start, session_person and turn_person))
    return sid, first, turns


def machine(codex):
    root = tempfile.mkdtemp(prefix='f_codex_', dir=C.work('f_codex'))
    os.makedirs(os.path.join(root, 'project', '.git'))
    os.makedirs(os.path.join(root, 'home', '.codex') if codex else os.path.join(root, 'home'))
    env = dict(os.environ, HOME=os.path.join(root, 'home'), USERPROFILE=os.path.join(root, 'home'),
               MUNINN_SESSION_END_INLINE='1')
    env.pop('CODEX_HOME', None)
    return root, os.path.join(root, 'project'), env


def fire(handler, event, payload, project, env):
    """Run one registered command the way Codex does: the session's shell, the session's cwd.
    On Windows that shell is Windows PowerShell: a real `codex exec` session of codex-cli 0.166.0
    ran a probe hook there, and ran nothing for a command only cmd.exe takes. The first version
    of this script used cmd.exe, which is what Codex falls back to when a session has no shell."""
    inp = json.dumps(dict(payload, hook_event_name=event, cwd=project, model='gpt-fixture')).encode('utf-8')
    if os.name == 'nt':
        line = handler.get('commandWindows') or handler['command']
        r = C.run(['powershell.exe', '-NoProfile', '-Command', line], 'fire:' + event, timeout=600, input=inp,
                  env=env, cwd=project)
    else:
        r = C.run(['sh', '-c', handler['command']], 'fire:' + event, timeout=600, input=inp, env=env, cwd=project)
    if r is not None and C._bad_stderr(r.stderr.decode('utf-8', 'replace')):
        C.fail('fire:%s:stderr' % event)
    return r


def stored(binary, project, env, turns):
    out = os.path.join(project, 'f_codex_export.jsonl')
    C.run([binary, '--cwd', project, 'export', '--all', '--out', out], 'export', env=env)
    kinds, origins, not_persons, typed = {}, {}, 0, 0
    if not os.path.isfile(out):
        return dict(typed=0, by_kind={}, by_origin={}, user_said_from_a_turn_not_a_persons=0)
    for l in open(out, encoding='utf-8'):
        r = json.loads(l)
        if r.get('kind') == 'episode':
            continue
        typed += 1
        kinds[r['kind']] = kinds.get(r['kind'], 0) + 1
        origins[r['origin']] = origins.get(r['origin'], 0) + 1
        if r['origin'] != 'user_said':
            continue
        ref = (r.get('transcript_ref') or '').rsplit(':', 1)
        end = int(ref[1]) if len(ref) == 2 and ref[1].isdigit() else None
        mine = [person for (start, person) in turns if end is not None and start < end]
        if not mine or not mine[-1]:
            not_persons += 1
    return dict(typed=typed, by_kind=kinds, by_origin=origins, user_said_from_a_turn_not_a_persons=not_persons)


def hooks_route(binary, rollout):
    root, project, env = machine(codex=True)
    try:
        C.run([binary, '--cwd', project, 'init', '--keep-native'], 'init', env=env)
        sid, first, turns = read_rollout(rollout)
        dest = os.path.join(root, 'home', '.codex', 'sessions', '2026', '11', '14')
        os.makedirs(dest)
        copy = os.path.join(dest, 'rollout-2026-11-14T10-00-00-%s.jsonl' % (sid or 'unknown'))
        shutil.copyfile(rollout, copy)
        hf = os.path.join(project, '.codex', 'hooks.json')
        fired = 0
        if os.path.isfile(hf):
            hooks = json.load(open(hf, encoding='utf-8'))['hooks']
            common = dict(session_id=sid or 'unknown', transcript_path=copy, permission_mode='default')
            inputs = dict(SessionStart=dict(common, source='startup'),
                          UserPromptSubmit=dict(common, turn_id='t1', prompt=first),
                          Stop=dict(common, turn_id='t1', stop_hook_active=False, last_assistant_message=None),
                          SessionEnd=dict(session_id=sid or 'unknown', transcript_path=copy, reason='other'))
            for ev in EVENTS:
                for group in hooks.get(ev, []):
                    for h in group.get('hooks', []):
                        if fire(h, ev, inputs[ev], project, env) is not None:
                            fired += 1
            # the write path SessionStart starts detached: let it end, then run it once more here
            time.sleep(1.0)
            C.run([binary, '--cwd', project, 'maintain'], 'maintain', env=env)
        got = stored(binary, project, env, turns) if os.path.isfile(os.path.join(project, '.muninn', 'muninn.db')) \
            else dict(typed=0, by_kind={}, by_origin={}, user_said_from_a_turn_not_a_persons=0)
        got.update(hooks_file=os.path.isfile(hf), commands_run=fired, messages=len(turns),
                   messages_not_a_persons=len([1 for (_, p) in turns if not p]))
        return got
    finally:
        time.sleep(0.2)
        shutil.rmtree(root, ignore_errors=True)


def direct_route(binary, rollout):
    root, project, env = machine(codex=False)
    try:
        C.run([binary, '--cwd', project, 'init', '--keep-native'], 'init', env=env)
        _, _, turns = read_rollout(rollout)
        dest = os.path.join(root, 'in')
        os.makedirs(dest)
        copy = os.path.join(dest, 'rollout-2026-11-14T10-00-00-direct.jsonl')
        shutil.copyfile(rollout, copy)
        C.run([binary, '--cwd', project, 'ingest', copy], 'ingest', env=env)
        got = stored(binary, project, env, turns)
        got.update(messages=len(turns), messages_not_a_persons=len([1 for (_, p) in turns if not p]))
        return got
    finally:
        shutil.rmtree(root, ignore_errors=True)


def total(rows):
    t = dict(rollouts=len(rows), rollouts_with_a_typed_record=len([r for r in rows if r['typed']]),
             typed=0, by_kind={}, by_origin={}, user_said_from_a_turn_not_a_persons=0, messages=0,
             messages_not_a_persons=0)
    for r in rows:
        for k in ('typed', 'user_said_from_a_turn_not_a_persons', 'messages', 'messages_not_a_persons'):
            t[k] += r[k]
        for g in ('by_kind', 'by_origin'):
            for k, n in r[g].items():
                t[g][k] = t[g].get(k, 0) + n
    if rows and 'hooks_file' in rows[0]:
        t['hooks_file'] = all(r['hooks_file'] for r in rows)
        t['commands_run'] = sum(r['commands_run'] for r in rows)
    return t


def main():
    ap = C.parser(__doc__.split('\n')[0])
    ap.add_argument('--rollouts', required=True, help='a rollout file, or a directory searched for rollout-*.jsonl')
    ap.add_argument('--set', required=True, choices=['invented', 'real'], dest='which')
    args = ap.parse_args()
    if os.path.isdir(args.rollouts):
        files = sorted(os.path.join(d, f) for d, _, fs in os.walk(args.rollouts) for f in fs
                       if f.startswith('rollout-') and f.endswith('.jsonl'))
    else:
        files = [args.rollouts]
    if not files:
        sys.exit('no rollout under --rollouts')
    out = {}
    for route, fn in (('hooks', hooks_route), ('direct', direct_route)):
        rows = [fn(args.bin, f) for f in files]
        out[route] = total(rows)
        if args.which == 'real':
            out[route]['per_rollout'] = {'R%02d' % (i + 1): dict(typed=r['typed'], messages=r['messages'],
                                                                 not_a_persons=r['user_said_from_a_turn_not_a_persons'])
                                         for i, r in enumerate(rows)}
    out['bytes'] = sum(os.path.getsize(f) for f in files)
    C.write_counts('f_codex', C.build_name(args), args, {args.which: out})


if __name__ == '__main__':
    main()
