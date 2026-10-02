#!/usr/bin/env bash
# agentmemory 0.9.29 arm for the head-to-head grid
# (experiment/PREREGISTRATION.md, "Head-to-head without labels").
# AGENTMEMORY_ARM_INJECT=1 gives the secondary arm `agentmemory-inject`
# (AGENTMEMORY_INJECT_CONTEXT=true, the documented switch); everything else stays default:
# no LLM provider, no embedding provider (BM25), no ~/.agentmemory/.env.
#
# Measured constraints of 0.9.29 in native mode, not configuration choices:
#   - the iii engine always binds 3111/3112/49134 and the viewer 3113: --port and --instance are
#     not passed to the engine, so PORT is ignored and cells of this arm run serially;
#   - the engine keeps its state in ./data relative to its working directory (the bundled
#     iii-config.yaml says file_path: ./data/...), so the engine is started from $CELL_ROOT.
# The plugin's MCP server is `npx -y @agentmemory/mcp`; npm's cache is pointed at the pin and set
# offline so no cell installs anything. STANDALONE_PERSIST_PATH keeps the shim's local file in the
# cell (measured: without it the shim created ~/.agentmemory/standalone.json in the real HOME).
#
# Env: CELL_ROOT (private dir: home/, data/, logs/), CHECKOUT, PORT (unused, see above), PIN.
set -euo pipefail

VERSION=0.9.29
REAL_HOME=${REAL_HOME:-$HOME}
PIN=${PIN:-$REAL_HOME/.local/share/muninn-bench/competitors/agentmemory}
PKG=$PIN/node_modules/@agentmemory/agentmemory
PLUGIN=$PKG/plugin
BIN=$PIN/node_modules/.bin/agentmemory
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ARM_NAME=agentmemory; [ "${AGENTMEMORY_ARM_INJECT:-0}" = 1 ] && ARM_NAME=agentmemory-inject
URL=http://localhost:3111
PORTS="3111 3112 3113 49134"

die() { echo "$ARM_NAME arm: $*" >&2; exit 1; }
need() { for v in "$@"; do [ -n "${!v:-}" ] || die "$v is not set"; done; }
now_ms() { date +%s%3N; }
healthy() { curl -sf -m 2 "$URL/agentmemory/livez" >/dev/null 2>&1; }
open_ports() { local n=0 p; for p in $PORTS; do [ "$(ss -ltn "( sport = :$p )" | tail -n +2 | wc -l)" = 0 ] || n=$((n+1)); done; echo $n; }

tool_env() {
  export AGENTMEMORY_URL=$URL
  export npm_config_cache=$PIN/npm-cache npm_config_offline=true npm_config_update_notifier=false
  # the MCP shim otherwise writes ~/.agentmemory/standalone.json in the session's (real) HOME
  export STANDALONE_PERSIST_PATH=$CELL_ROOT/home/.agentmemory/standalone.json
  if [ "$ARM_NAME" = agentmemory-inject ]; then export AGENTMEMORY_INJECT_CONTEXT=true; else unset AGENTMEMORY_INJECT_CONTEXT; fi
}

cmd_install() {
  mkdir -p "$PIN" && cd "$PIN"
  [ -f package.json ] || npm init -y >/dev/null
  npm install --no-fund --no-audit "@agentmemory/agentmemory@$VERSION" "@agentmemory/mcp@$VERSION"
  # the plugin's .mcp.json runs `npx -y @agentmemory/mcp` (unversioned): fill a pinned npm cache
  # from outside the pin so npx resolves it the way a cell will
  local tmp; tmp=$(mktemp -d)
  (cd "$tmp" && npm_config_cache=$PIN/npm-cache npx -y "@agentmemory/mcp@$VERSION" </dev/null >/dev/null 2>&1 || true)
  (cd "$tmp" && npm_config_cache=$PIN/npm-cache npx -y @agentmemory/mcp </dev/null >/dev/null 2>&1 || true)
  # let agentmemory install its own pinned iii engine once (it downloads into ~/.agentmemory/bin)
  mkdir -p "$PIN/home" "$tmp/cell"
  (cd "$tmp/cell" && HOME=$PIN/home CI=1 NO_COLOR=1 setsid nohup "$BIN" --data-dir "$tmp/cell/data" </dev/null >"$PIN/install-engine.log" 2>&1 &)
  for _ in $(seq 360); do healthy && break; sleep 0.5; done
  (cd "$tmp/cell" && HOME=$PIN/home "$BIN" stop >/dev/null 2>&1) || true
  mkdir -p "$PIN/bin" && ln -sf "$PIN/home/.agentmemory/bin/iii" "$PIN/bin/iii"
  rm -rf "$tmp"
  echo "{\"installed\": \"@agentmemory/agentmemory@$VERSION\", \"iii\": \"$("$PIN/bin/iii" --version 2>/dev/null)\"}"
}

cmd_start() {
  need CELL_ROOT
  mkdir -p "$CELL_ROOT/home" "$CELL_ROOT/data" "$CELL_ROOT/logs"
  [ "$(open_ports)" = 0 ] || die "one of $PORTS is already bound (fixed ports: run this arm serially)"
  tool_env
  local t0; t0=$(now_ms)
  echo "$t0" > "$CELL_ROOT/logs/started_at_ms"
  (cd "$CELL_ROOT" && HOME=$CELL_ROOT/home PATH=$PIN/bin:$PATH CI=1 NO_COLOR=1 \
     setsid nohup "$BIN" --data-dir "$CELL_ROOT/data" </dev/null >"$CELL_ROOT/logs/server.log" 2>&1 &)
  for _ in $(seq 240); do healthy && break; sleep 0.5; done
  healthy || die "not healthy on $URL: $(tail -5 "$CELL_ROOT/logs/server.log")"
  local t1; t1=$(now_ms)
  # BM25 only (keyless default): one search builds nothing, but proves the index answers
  curl -s -m 30 -H 'content-type: application/json' -X POST "$URL/agentmemory/search" -d '{"query":"warmup"}' >/dev/null || true
  local t2; t2=$(now_ms)
  echo "{\"started\": true, \"arm\": \"$ARM_NAME\", \"health_ms\": $((t1-t0)), \"warm_ms\": $((t2-t1)), \"engine_downloaded\": $(grep -qi 'Installing iii-engine' "$CELL_ROOT/logs/server.log" && echo true || echo false), \"inject\": \"${AGENTMEMORY_INJECT_CONTEXT:-false}\"}"
}

cmd_claude_args() {
  need CELL_ROOT
  tool_env
  python3 - "$PLUGIN" <<'EOF'
import json, os, sys
keys = ["AGENTMEMORY_URL", "STANDALONE_PERSIST_PATH", "npm_config_cache", "npm_config_offline", "npm_config_update_notifier", "AGENTMEMORY_INJECT_CONTEXT"]
env = {k: os.environ[k] for k in keys if k in os.environ}
print(json.dumps({"args": ["--plugin-dir", sys.argv[1]],
                  "allowed_tools": ["mcp__plugin_agentmemory_agentmemory"],
                  "env": env}))
EOF
}

# snapshot of everything the server holds, for settle's stability test and its log
dump_state() {
  python3 - "$URL" <<'EOF'
import json, sys, urllib.request
base = sys.argv[1] + "/agentmemory"
def get(path):
    try:
        with urllib.request.urlopen(base + path, timeout=10) as r:
            return json.load(r)
    except Exception as e:
        return {"error": str(e)}
sessions = get("/sessions")
slist = sessions.get("sessions", sessions if isinstance(sessions, list) else [])
out = {"sessions": [], "memories": get("/memories").get("memories", [])}
for s in slist:
    obs = get(f"/observations?sessionId={s.get('id')}")
    items = obs.get("observations", obs if isinstance(obs, list) else [])
    out["sessions"].append({"id": s.get("id"), "project": s.get("project"), "status": s.get("status"),
        "observationCount": s.get("observationCount"),
        "observations": [{k: o.get(k) for k in ("type", "title", "narrative", "facts", "concepts", "timestamp")} for o in items]})
out["memories"] = [{k: m.get(k) for k in ("id", "type", "title", "content", "isLatest", "supersedes", "project")} for m in out["memories"]]
print(json.dumps(out, ensure_ascii=False))
EOF
}

cmd_settle() {
  need CELL_ROOT
  healthy || die "server is not running"
  local t0; t0=$(now_ms)
  # Hooks POST fire-and-forget; settled = no session still "active" and the whole state is
  # byte-identical over 3 polls, 1 s apart. SETTLE_TIMEOUT_S caps it.
  local prev="" cur="" same=0 active=1
  for _ in $(seq "${SETTLE_TIMEOUT_S:-300}"); do
    cur=$(dump_state)
    active=$(python3 -c 'import json,sys; print(sum(1 for s in json.loads(sys.argv[1])["sessions"] if s.get("status")=="active"))' "$cur")
    if [ "$cur" = "$prev" ] && [ "$active" = 0 ]; then same=$((same+1)); [ $same -ge 3 ] && break; else same=0; fi
    prev=$cur; sleep 1
  done
  local t1; t1=$(now_ms)
  python3 - "$cur" "$((t1-t0))" "$same" "$active" <<'EOF'
import json, sys
state, ms, same, active = json.loads(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
state.update({"settle_ms": ms, "settled": same >= 3 and active == 0, "active_sessions": active,
              "observation_count": sum(len(s["observations"]) for s in state["sessions"]),
              "memory_count": len(state["memories"])})
print(json.dumps(state, ensure_ascii=False))
EOF
}

cmd_snapshot() {
  need CELL_ROOT; local dest=${1:?snapshot <dir>}
  # the harness snapshots before `stop`: stop the engine first so its files are copied closed
  if healthy; then cmd_stop >/dev/null; fi
  mkdir -p "$dest"
  cp -a "$CELL_ROOT/data/." "$dest/"
  rm -f "$dest/iii-config.yaml"
  echo "{\"snapshot\": \"$dest\", \"bytes\": $(du -sb "$dest" | cut -f1)}"
}

cmd_restore() {
  need CELL_ROOT; local src=${1:?restore <dir>}
  [ -n "$(ls -A "$CELL_ROOT/data" 2>/dev/null)" ] && die "$CELL_ROOT/data is not empty"
  mkdir -p "$CELL_ROOT/data" "$CELL_ROOT/home" "$CELL_ROOT/logs"
  cp -a "$src/." "$CELL_ROOT/data/"
  echo "{\"restored\": \"$src\", \"into\": \"$CELL_ROOT/data\"}"
}

cmd_stop() {
  need CELL_ROOT
  (cd "$CELL_ROOT" && HOME=$CELL_ROOT/home PATH=$PIN/bin:$PATH "$BIN" stop) >>"$CELL_ROOT/logs/stop.log" 2>&1 || true
  for _ in $(seq 20); do [ "$(open_ports)" = 0 ] && break; sleep 0.5; done
  local f pid
  for f in iii.pid worker.pid; do
    pid=$(cat "$CELL_ROOT/home/.agentmemory/$f" 2>/dev/null || true)
    [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null && kill "$pid" 2>/dev/null || true
  done
  for _ in $(seq 20); do [ "$(open_ports)" = 0 ] && break; sleep 0.5; done
  local n; n=$(open_ports)
  echo "{\"stopped\": $([ "$n" = 0 ] && echo true || echo false), \"ports_open\": $n}"
  [ "$n" = 0 ]
}

cmd_delivered() {
  need CELL_ROOT
  # agentmemory does not log hook output or MCP results; the session transcript records both.
  python3 "$HERE/../_lib/delivered.py" --tool "$ARM_NAME" --hook-marker "agentmemory/plugin/scripts" --hooks-json "$PLUGIN/hooks/hooks.json" \
    --mcp-prefix "mcp__plugin_agentmemory_agentmemory__" --worker-logs "$CELL_ROOT/logs" ${1:+--transcript "$1"}
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
