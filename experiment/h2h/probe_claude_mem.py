#!/usr/bin/env python3
"""Exit 0 iff claude-mem's worker settles one session, i.e. its observer is working."""
import json, os, subprocess, tempfile, shutil, sys
from pathlib import Path
H = Path("/home/ilien/Projects/muninn/crates/muninn-bench/experiment/h2h")
root = Path(tempfile.mkdtemp(prefix="cmprobe-")); (root / "cell").mkdir()
co = root / "gin"; co.mkdir()
for a in (["init", "-q"], ["-c", "user.email=a@b", "-c", "user.name=c", "commit", "-q", "--allow-empty", "-m", "i"]):
    subprocess.run(["git", "-C", str(co), *a], capture_output=True)
env = dict(os.environ, CELL_ROOT=str(root / "cell"), CHECKOUT=str(co), PORT="38990")
arm = str(H / "competitors/claude-mem/arm.sh")
run = lambda sub: subprocess.run([arm, sub], env=env, capture_output=True, text=True, timeout=900)
ok = False
try:
    run("start")
    spec = json.loads(run("claude-args").stdout)
    e = dict(env); e.pop("CLAUDECODE", None)
    for k, v in (spec.get("env") or {}).items():
        e["PATH"] = f"{v}:{e['PATH']}" if k == "PATH_PREPEND" else e.get("PATH")
        if k != "PATH_PREPEND": e[k] = v
    (root / "s.json").write_text("{}")
    subprocess.run(["claude", "-p", "gzip\n\n(Reply with one short sentence acknowledging.)", "--model", "claude-sonnet-5",
                    "--output-format", "json", "--max-turns", "3", "--setting-sources", "", "--settings", str(root / "s.json"),
                    *spec.get("args", [])], cwd=co, env=e, capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
    st = json.loads(run("settle").stdout or "{}")
    ok = st.get("settled") is True
    print(json.dumps({"settled": st.get("settled"), "settle_ms": st.get("settle_ms")}))
finally:
    try: run("stop")
    except Exception: pass
    shutil.rmtree(root, ignore_errors=True)
sys.exit(0 if ok else 1)
