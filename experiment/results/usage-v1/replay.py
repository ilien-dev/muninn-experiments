#!/usr/bin/env python3
"""usage-v1 replay. Usage: replay.py <arm-binary> <arm> <project> <workdir>
Prints counts only, as JSON, and keeps project text out of stdout."""
import json, os, sqlite3, subprocess, sys, shutil, time, datetime as D
BIN, ARM, PROJ, WORK = sys.argv[1:5]
SP = os.path.dirname(os.path.abspath(__file__))
STORE = f"{SP}/stores/{PROJ}/muninn.db"
SRC = os.path.join(os.environ["PROJECTS_DIR"], PROJ)  # the local checkout of each project
root = f"{WORK}/{ARM}/{PROJ}"
shutil.rmtree(root, ignore_errors=True)
os.makedirs(os.path.dirname(root), exist_ok=True)
is_git = os.path.isdir(SRC + "/.git")
env = dict(os.environ, USERPROFILE=f"{WORK}/home", HOME=f"{WORK}/home", MUNINN_NO_PROJECT="1")
os.makedirs(f"{WORK}/home", exist_ok=True)
def run(args, **k):
    return subprocess.run(args, cwd=root, env=env, capture_output=True, **k)
if is_git:
    subprocess.run(["git", "-c", "core.longpaths=true", "clone", "-q", "--no-checkout", "--local", "--no-hardlinks", "-c", "core.longpaths=true", SRC, root], capture_output=True, check=True)
else:
    os.makedirs(root)
    subprocess.run(["git", "init", "-q"], cwd=root)
r = run([BIN, "init", "--keep-native", "--no-boot-block"])
if not os.path.exists(root + "/.muninn/muninn.db"):
    print(json.dumps({"p": PROJ, "arm": ARM, "error": "init", "out": r.stderr.decode(errors="replace")[:200]})); sys.exit(0)
db = root + "/.muninn/muninn.db"
src = sqlite3.connect(STORE)
paths = sorted({t.rsplit(":", 1)[0] for (t,) in src.execute(
    "select distinct transcript_ref from record where transcript_ref like '%.jsonl:%'")})
src.close()
def stamp(s):
    try:
        return int(D.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())
    except Exception:
        return None
sessions = []
for p in paths:
    try:
        lines = open(p, "rb").read().split(b"\n")
    except OSError:
        continue
    first = last = None; cuts = []; off = 0
    for i, raw in enumerate(lines):
        if b'"timestamp"' not in raw:
            continue
        try:
            v = json.loads(raw)
        except Exception:
            continue
        ts = stamp(v.get("timestamp", ""))
        if ts:
            first = first or ts; last = ts
        a = v.get("attachment") or {}
        human = (v.get("type") == "user" and not v.get("isMeta") and not v.get("toolUseResult")) or \
                (v.get("type") == "attachment" and a.get("type") == "queued_command" and a.get("commandMode") == "prompt")
        if human:
            cuts.append(i)
    if first:
        sessions.append((first, last, p, lines, cuts))
sessions.sort(key=lambda s: s[0])
t0 = time.time(); batches = 0
os.makedirs(f"{root}/.replay", exist_ok=True)
for first, last, p, lines, cuts in sessions:
    name = f"{root}/.replay/{os.path.basename(p)}"
    open(name, "wb").close()
    bounds = cuts[1:] + [len(lines)]
    start = 0
    for b in bounds:
        with open(name, "ab") as f:
            f.write(b"\n".join(lines[start:b]))
            if b < len(lines) or lines[-1] != b"":
                f.write(b"\n")
        start = b
        run([BIN, "ingest", name]); batches += 1
    if is_git:
        rev = subprocess.run(["git", "rev-list", "-1", f"--before={last}", "HEAD@{0}" if False else "origin/HEAD"],
                             cwd=root, capture_output=True, text=True).stdout.strip()
        if rev:
            subprocess.run(["git", "checkout", "-q", "--detach", "-f", rev], cwd=root, capture_output=True)
            c = sqlite3.connect(db, timeout=30)
            for k in ("git_watermark_ms", "values_watermark_ms"):
                prev = c.execute("select value from meta where key=?", (k,)).fetchone()
                c.execute("insert or replace into meta(key,value) values(?,?)", (k, str(first * 1000)))
            c.commit(); c.close()
            run([BIN, "maintain"])
print(json.dumps({"p": PROJ, "arm": ARM, "sessions": len(sessions), "batches": batches, "git": is_git, "s": round(time.time() - t0)}))
