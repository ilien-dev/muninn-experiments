#!/usr/bin/env bash
# Claude Code's own automatic memory, as a head-to-head arm.
#
# `docs/claims.md` has carried "Better than the harness's native memory — not measured" since
# the first release, and it is the comparison every reader asks for: the native memory is
# already there and costs nothing. This arm answers it on the same grid, the same seeding
# sessions and the same oracle as every other arm.
#
# Nothing is installed and nothing is started. The whole arm is a per-cell memory directory
# plus `autoMemoryEnabled: true` in the per-cell settings — both written by `run_h2h.py` for
# the arms named in NATIVE_MEMORY_ARMS, and only for those. The settings file every other arm
# receives stays byte-identical, so the v1 and v2 grids already measured remain comparable.
#
# Isolation is by `autoMemoryDirectory`, not by a private HOME. Auto memory otherwise lands in
# `~/.claude/projects/<project>/memory/`, keyed by the git repository, so every cell of every
# run would share one directory — and the operator's own memory for that repository would be
# sitting in it. A private HOME confines it too, but it also moves the login: measured, a cell
# with HOME pointed at itself returns `Not logged in · Please run /login` and stores nothing,
# which is a cell that measures nothing. `autoMemoryDirectory` is read from any settings
# scope, `--settings` included (Claude Code docs, "Auto memory"), and the grid passes
# `--setting-sources ''`, so the cell's settings file is the only scope in play.
set -euo pipefail

mem() { echo "$CELL_ROOT/memory"; }

case "${1:?subcommand}" in
  install)
    # nothing to install: the memory ships with the harness
    echo '{"installed": "claude-code built-in", "version": "harness"}' ;;

  start)
    mkdir -p "$(mem)" "$CELL_ROOT/logs"
    echo '{"started": true}' ;;

  claude-args)
    # No env of its own: the memory directory travels in the settings file, and HOME stays
    # the operator's so the cell keeps its login.
    echo '{"args": [], "allowed_tools": [], "env": {}}' ;;

  settle)
    # the harness writes its memory during the session; there is no queue to drain
    python3 - "$(mem)" <<'PY'
import json, os, sys
root = sys.argv[1]
files = []
for dirpath, _dirs, names in os.walk(root):
    for n in names:
        p = os.path.join(dirpath, n)
        if n.endswith((".md", ".json")):
            files.append({"path": os.path.relpath(p, root), "bytes": os.path.getsize(p)})
files.sort(key=lambda f: f["path"])
print(json.dumps({"files": len(files), "bytes": sum(f["bytes"] for f in files), "entries": files[:40]}))
PY
    ;;

  snapshot) mkdir -p "$2"; cp -a "$(mem)/." "$2/" 2>/dev/null || true; echo '{"snapshot": true}' ;;
  restore)  mkdir -p "$(mem)"; cp -a "$2/." "$(mem)/" 2>/dev/null || true; echo '{"restored": true}' ;;
  stop) echo '{"stopped": true}' ;;

  delivered)
    # `MEMORY.md` is what the harness loads at the start of every session (its first 200 lines
    # or 25 KB); topic files are read on demand by the agent, with its own file tools. So the
    # bytes loaded up front are countable, and that is what is reported. `_lib/delivered.py`
    # cannot see the injection itself — it is system context, not a hook attachment or an MCP
    # result — and this arm does not guess at it: `deliveries` is null, not a number.
    python3 - "$(mem)" <<'PY'
import json, os, sys
root = sys.argv[1]
index = os.path.join(root, "MEMORY.md")
total = 0
topics = 0
for dirpath, _dirs, names in os.walk(root):
    for n in names:
        if n.endswith(".md"):
            total += os.path.getsize(os.path.join(dirpath, n))
            topics += os.path.join(dirpath, n) != index
print(json.dumps({"deliveries": None, "tokens": None, "memory_bytes": total,
                  "index_bytes": os.path.getsize(index) if os.path.exists(index) else 0,
                  "topic_files": topics,
                  "note": "native memory is injected by the harness as system context and is not observable here"}))
PY
    ;;

  *) echo "unknown subcommand $1" >&2; exit 2 ;;
esac
