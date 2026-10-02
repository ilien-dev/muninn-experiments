#!/usr/bin/env bash
# claude-mem 13.24.23 arm for the head-to-head grid
# (experiment/PREREGISTRATION.md, "Head-to-head without labels").
#
# Defaults only. What this script sets, and why:
#   CLAUDE_MEM_DATA_DIR    confinement of every stored byte to $CELL_ROOT/data (documented setting)
#   CLAUDE_MEM_WORKER_PORT the port the harness assigns (documented setting)
#   CLAUDE_MEM_TELEMETRY   false (pre-registered: telemetry off where the tool has a switch)
#   UV_* / chroma model    the pinned, pre-downloaded chroma-mcp environment, so no cell installs anything
#   CLAUDE_CODE_OAUTH_TOKEN the observer model runs "through the Claude Code login" (claude-mem's
#                          default provider); HOME is private, so the login's access token is
#                          handed to the worker process only and is never printed.
#
# Env: CELL_ROOT (private dir: home/, data/, logs/), CHECKOUT, PORT, PIN.
set -euo pipefail

VERSION=13.24.23
REAL_HOME=${REAL_HOME:-$HOME}
PIN=${PIN:-$REAL_HOME/.local/share/muninn-bench/competitors/claude-mem}
PLUGIN=$PIN/node_modules/claude-mem/plugin
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

die() { echo "claude-mem arm: $*" >&2; exit 1; }
need() { for v in "$@"; do [ -n "${!v:-}" ] || die "$v is not set"; done; }
now_ms() { date +%s%3N; }

tool_env() {
  export CLAUDE_MEM_DATA_DIR=$CELL_ROOT/data
  export CLAUDE_MEM_WORKER_PORT=$PORT
  export CLAUDE_MEM_TELEMETRY=false
  export UV_CACHE_DIR=$PIN/uv-cache UV_PYTHON_INSTALL_DIR=$PIN/uv-python UV_OFFLINE=1
}

base() { echo "http://127.0.0.1:$PORT"; }

healthy() { curl -sf -m 2 "$(base)/api/health" >/dev/null 2>&1; }

oauth_token() {
  if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then printf '%s' "$CLAUDE_CODE_OAUTH_TOKEN"; return; fi
  python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["claudeAiOauth"]["accessToken"], end="")' \
    "$REAL_HOME/.claude/.credentials.json"
}

cmd_install() {
  need PIN
  mkdir -p "$PIN"
  cd "$PIN"
  [ -f package.json ] || npm init -y >/dev/null
  npm install --no-fund --no-audit "claude-mem@$VERSION"
  # the plugin's runtime dependencies, as `npx claude-mem repair` installs them
  (cd "$PLUGIN" && bun install --frozen-lockfile)
  # chroma-mcp exactly as the worker spawns it, into pinned uv dirs
  UV_CACHE_DIR=$PIN/uv-cache UV_PYTHON_INSTALL_DIR=$PIN/uv-python \
    uvx --python 3.13 --with 'onnxruntime>=1.20' --with 'protobuf<7' --from chroma-mcp==0.2.6 chroma-mcp --help >/dev/null
  # chroma's default embedding model is downloaded on first use into ~/.cache/chroma:
  # run one warm cell with a throwaway HOME and keep that cache in the pin
  local warm; warm=$(mktemp -d)
  CELL_ROOT=$warm PORT=${PORT:-37990} CHECKOUT=$warm "$0" start >/dev/null
  CELL_ROOT=$warm PORT=${PORT:-37990} CHECKOUT=$warm "$0" stop >/dev/null
  rm -rf "$PIN/chroma-cache"
  [ -d "$warm/home/.cache/chroma" ] && cp -a "$warm/home/.cache/chroma" "$PIN/chroma-cache"
  rm -rf "$warm"
  echo "{\"installed\": \"claude-mem@$VERSION\", \"pin\": \"$PIN\", \"chroma_cache\": $([ -d "$PIN/chroma-cache" ] && echo true || echo false)}"
}

cmd_start() {
  need CELL_ROOT PORT
  mkdir -p "$CELL_ROOT/home" "$CELL_ROOT/data" "$CELL_ROOT/logs"
  if [ -d "$PIN/chroma-cache" ] && [ ! -d "$CELL_ROOT/home/.cache/chroma" ]; then
    mkdir -p "$CELL_ROOT/home/.cache" && cp -a "$PIN/chroma-cache" "$CELL_ROOT/home/.cache/chroma"
  fi
  healthy && die "port $PORT already answers"
  tool_env
  local t0; t0=$(now_ms)
  echo "$t0" > "$CELL_ROOT/logs/started_at_ms"
  (cd "$CELL_ROOT" && HOME=$CELL_ROOT/home CLAUDE_CODE_OAUTH_TOKEN=$(oauth_token) \
     bun "$PLUGIN/scripts/worker-service.cjs" start) >"$CELL_ROOT/logs/start.log" 2>&1 || die "worker start failed: $(tail -3 "$CELL_ROOT/logs/start.log")"
  for _ in $(seq 120); do healthy && break; sleep 0.5; done
  healthy || die "worker not healthy on $PORT"
  local t1; t1=$(now_ms)
  # warm the vector index: the first search spawns chroma-mcp and loads the model
  local warm_out=""
  for _ in $(seq 12); do
    warm_out=$(curl -s -m 180 "$(base)/api/search?query=warmup" || true)
    grep -q "Connected to chroma-mcp successfully" "$CELL_ROOT"/data/logs/*.log 2>/dev/null && break
    sleep 5
  done
  local t2; t2=$(now_ms)
  python3 - "$t1" "$t0" "$t2" "$warm_out" "$CELL_ROOT" <<'EOF'
import json, sys, glob
t1, t0, t2, warm, cell = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
logs = "".join(open(p, errors="replace").read() for p in glob.glob(cell + "/data/logs/*.log"))
print(json.dumps({"started": True, "health_ms": t1 - t0, "warm_ms": t2 - t1,
                  "chroma_connected": "Connected to chroma-mcp successfully" in logs}))
EOF
}

cmd_claude_args() {
  need CELL_ROOT PORT
  tool_env
  python3 - "$PLUGIN" <<'EOF'
import json, os, sys
env = {k: os.environ[k] for k in ("CLAUDE_MEM_DATA_DIR", "CLAUDE_MEM_WORKER_PORT", "CLAUDE_MEM_TELEMETRY",
                                  "UV_CACHE_DIR", "UV_PYTHON_INSTALL_DIR", "UV_OFFLINE")}
print(json.dumps({"args": ["--plugin-dir", sys.argv[1]],
                  "allowed_tools": ["mcp__plugin_claude-mem_mcp-search"],
                  "env": env}))
EOF
}

cmd_settle() {
  need CELL_ROOT PORT CHECKOUT
  healthy || die "worker is not running"
  local t0 project; t0=$(now_ms); project=$(basename "$(git -C "$CHECKOUT" rev-parse --show-toplevel 2>/dev/null || echo "$CHECKOUT")")
  # The observer is a long-lived SDK session per Claude session: /api/processing-status reads idle
  # while it is still answering. Settled = no pending queue rows AND every user prompt captured since `start` has
  # an observer response (or error) in the worker log, stable for 3 polls. SETTLE_TIMEOUT_S caps it.
  local idle=0 status="" pending=""
  for _ in $(seq "${SETTLE_TIMEOUT_S:-600}"); do
    status=$(curl -s -m 5 "$(base)/api/processing-status" || true)
    pending=$(python3 - "$CELL_ROOT/data" "$(cat "$CELL_ROOT/logs/started_at_ms")" <<'EOF'
import sqlite3, sys, glob, re
d, since = sys.argv[1], int(sys.argv[2])
db = sqlite3.connect(f"file:{d}/claude-mem.db?mode=ro", uri=True)
queued = db.execute("select count(*) from pending_messages").fetchone()[0]
prompts = db.execute("select s.id, p.prompt_number from user_prompts p join sdk_sessions s on s.content_session_id = p.content_session_id where p.created_at_epoch >= ?", (since,)).fetchall()
logs = "".join(open(p, errors="replace").read() for p in glob.glob(d + "/logs/*.log"))
answered = set((int(a), int(b)) for a, b in re.findall(r"\[session-(\d+)\] ← Response received \(\d+ chars\) \{promptNumber=(\d+)\}", logs))
failed = set(int(a) for a in re.findall(r"\[session-(\d+)\][^\n]*(?:ERROR|failed|aborted)", logs))
waiting = [p for p in prompts if (p[0], p[1]) not in answered and p[0] not in failed]
print(queued + len(waiting))
EOF
)
    if [ "$pending" = 0 ]; then idle=$((idle+1)); [ $idle -ge 3 ] && break; else idle=0; fi
    sleep 1
  done
  local t1; t1=$(now_ms)
  python3 - "$(base)" "$project" "$((t1-t0))" "$status" "$pending" <<'EOF'
import json, sys, urllib.request
base, project, ms, status, pending = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
def get(path):
    with urllib.request.urlopen(f"{base}{path}", timeout=10) as r:
        return json.load(r)
out = {"project": project, "settle_ms": ms, "settled": pending == "0", "unanswered": pending,
       "processing_status": json.loads(status or "{}")}
for kind in ("observations", "summaries", "prompts"):
    items = get(f"/api/{kind}?project={project}&limit=1000").get("items", [])
    out[kind] = {"count": len(items), "items": [
        {k: v for k, v in it.items() if k in ("id", "type", "title", "subtitle", "narrative", "facts", "concepts",
            "request", "investigated", "learned", "completed", "next_steps", "prompt_text", "created_at")}
        for it in items]}
print(json.dumps(out, ensure_ascii=False))
EOF
}

cmd_snapshot() {
  need CELL_ROOT; local dest=${1:?snapshot <dir>}
  # the harness snapshots before `stop`: quiesce the worker first so SQLite and chroma are
  # copied closed (stop is idempotent, the harness's own `stop` afterwards is a no-op)
  if [ -n "${PORT:-}" ] && healthy; then cmd_stop >/dev/null; fi
  mkdir -p "$dest"
  cp -a "$CELL_ROOT/data/." "$dest/"
  rm -f "$dest/worker.pid" "$dest/supervisor.json"; rm -rf "$dest/logs"
  echo "{\"snapshot\": \"$dest\", \"bytes\": $(du -sb "$dest" | cut -f1)}"
}

cmd_restore() {
  need CELL_ROOT; local src=${1:?restore <dir>}
  [ -e "$CELL_ROOT/data" ] && [ -n "$(ls -A "$CELL_ROOT/data" 2>/dev/null)" ] && die "$CELL_ROOT/data is not empty"
  mkdir -p "$CELL_ROOT/data" "$CELL_ROOT/home" "$CELL_ROOT/logs"
  cp -a "$src/." "$CELL_ROOT/data/"
  echo "{\"restored\": \"$src\", \"into\": \"$CELL_ROOT/data\"}"
}

cmd_stop() {
  need CELL_ROOT PORT
  tool_env
  (cd "$CELL_ROOT" && HOME=$CELL_ROOT/home bun "$PLUGIN/scripts/worker-service.cjs" stop) >>"$CELL_ROOT/logs/stop.log" 2>&1 || true
  for _ in $(seq 40); do healthy || break; sleep 0.5; done
  # chroma-mcp children of this cell (their --data-dir is inside the cell)
  local pids; pids=$(pgrep -f "[c]hroma-mcp.*--data-dir $CELL_ROOT/" || true)
  [ -n "$pids" ] && kill $pids 2>/dev/null || true
  sleep 1
  local open; open=$(ss -ltn "( sport = :$PORT )" | tail -n +2 | wc -l)
  local left; left=$(pgrep -f "[c]hroma-mcp.*--data-dir $CELL_ROOT/" | wc -l || true)
  echo "{\"stopped\": $([ "$open" = 0 ] && [ "$left" = 0 ] && echo true || echo false), \"port_open\": $open, \"chroma_left\": $left}"
  [ "$open" = 0 ]
}

cmd_delivered() {
  need CELL_ROOT
  # claude-mem does not log what its hooks inject or what its MCP tools return; the session
  # transcript (Claude Code's own record) does. Pass it as the first argument.
  python3 "$HERE/../_lib/delivered.py" --tool claude-mem --mcp-prefix "mcp__plugin_claude-mem_" --hooks-json "$PLUGIN/hooks/hooks.json" \
    --worker-logs "$CELL_ROOT/data/logs" ${1:+--transcript "$1"}
}

case "${1:-}" in
  install) shift; cmd_install "$@" ;;
  start) shift; cmd_start "$@" ;;
  claude-args) shift; cmd_claude_args "$@" ;;
  settle) shift; cmd_settle "$@" ;;
  snapshot) shift; cmd_snapshot "$@" ;;
  restore) shift; cmd_restore "$@" ;;
  stop) shift; cmd_stop "$@" ;;
  delivered) shift; cmd_delivered "$@" ;;
  *) echo "usage: $0 install|start|claude-args|settle|snapshot <dir>|restore <dir>|stop|delivered [transcript]" >&2; exit 2 ;;
esac
