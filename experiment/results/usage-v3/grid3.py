#!/usr/bin/env python3
"""usage-v3 cells. Usage: grid3.py <muninn.exe> <workdir> <model>"""
import json, os, re, shutil, subprocess, sys, glob, sqlite3, concurrent.futures as F
BIN, WORK, MODEL = sys.argv[1:4]
T = [
 ("csv", "CSV exports use a semicolon delimiter, never a comma.",
  "write export_users.py with a function that writes a list of dicts to a CSV file",
  r"delimiter\s*=\s*['\"];|sep\s*=\s*['\"];|['\"];['\"]\.join"),
 ("http", "Every HTTP call times out after exactly 7 seconds.",
  "write fetch_status.py with a function that GETs a URL using urllib and returns the status code",
  r"timeout\s*=\s*7\b|TIMEOUT\w*\s*=\s*7\b"),
 ("money", "Money is always integer cents, never a float.",
  "write invoice.py with a function that totals line items, each with a quantity and a unit price",
  r"cents"),
 ("retry", "Retries are exactly 4 attempts, with no backoff and no sleep.",
  "write retry.py with a decorator that retries a function when it raises",
  r"(attempts|retries|times|tries|max_\w+)\s*(:\s*int\s*)?=\s*4\b"),
 ("log", "Every log line starts with the literal prefix [svc].",
  "write logger_setup.py with a function that configures the logging module for the app",
  r"\[svc\]"),
 ("time", "Timestamps are UTC ISO-8601 with a Z suffix, never an offset.",
  "write stamp.py with a function that returns the current timestamp as a string",
  r"Z['\"]|['\"]Z"),
]
H = lambda ev, to: [{"hooks": [{"type": "command", "command": f'"{BIN}" hook {ev}', "timeout": to}]}]
def cell(task, arm):
    name, rule, ask, rx = task
    root = f"{WORK}/{arm}-{name}"
    shutil.rmtree(root, ignore_errors=True); os.makedirs(root + "/.claude")
    env = dict(os.environ, MUNINN_ROOT=root, MUNINN_NO_PROJECT="1")
    env.pop("CLAUDECODE", None)
    subprocess.run(["git", "init", "-q"], cwd=root)
    subprocess.run([BIN, "--cwd", root, "init", "--keep-native", "--no-boot-block"], env=env, capture_output=True)
    db = sqlite3.connect(root + "/.muninn/muninn.db")
    for i, (_, r, _, _) in enumerate(T, 1):
        db.execute("insert into record(kind,subject,relation,object,body,origin,trust,session_id,dedup_hash,created_at) values('invariant',?,'must',?,?,'user_said',3,'seed',?,?)",
                   (r.lower()[:60], r, f"user: {r}\n", f"h{i}", 1790000000000 + i))
    db.commit(); db.close()
    if arm == "on":
        subprocess.run([BIN, "--cwd", root, "config", "subagent-delivery", "on"], env=env, capture_output=True)
    json.dump({"hooks": {"SessionStart": H("SessionStart", 10), "UserPromptSubmit": H("UserPromptSubmit", 5),
                         "SubagentStart": H("SubagentStart", 5)}}, open(root + "/.claude/settings.json", "w"))
    prompt = f"Use the Agent tool to delegate this to a general-purpose subagent, and do no file work yourself: {ask}. Say nothing else to the subagent than this task."
    r = subprocess.run(["claude", "-p", prompt, "--model", MODEL, "--setting-sources", "project", "--dangerously-skip-permissions",
                        "--output-format", "json"], cwd=root, env=env, capture_output=True, timeout=600)
    code = ""
    for f in glob.glob(root + "/*.py") + glob.glob(root + "/**/*.py", recursive=True):
        code += open(f, encoding="utf8", errors="replace").read()
    try:
        j = json.loads(r.stdout); cost = j.get("total_cost_usd", 0)
    except Exception:
        cost = None
    subs = glob.glob(os.path.expanduser("~/.claude/projects/*" + os.path.basename(root) + "*/*/subagents/*.jsonl"))
    return {"task": name, "arm": arm, "pass": bool(re.search(rx, code)), "wrote": bool(code), "cost": cost, "subagents": len(subs)}
with F.ThreadPoolExecutor(4) as ex:
    res = list(ex.map(lambda a: cell(*a), [(t, a) for t in T for a in ("off", "on")]))
print(json.dumps(res, indent=0))
print("off", sum(r["pass"] for r in res if r["arm"] == "off"), "on", sum(r["pass"] for r in res if r["arm"] == "on"),
      "cost", round(sum(r["cost"] or 0 for r in res), 2))
