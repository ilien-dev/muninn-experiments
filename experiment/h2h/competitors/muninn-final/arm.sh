#!/usr/bin/env bash
# Muninn arm for the label-free head-to-head, with the same interface as the competitor arms.
# The plugin is used as shipped (plugin/hooks/hooks.json) from a pinned copy whose bin/muninn is
# the frozen build; the store lives in CELL_ROOT/data (MUNINN_ROOT), outside the checkout, like
# every competitor's data directory. No import, no seed file: capture comes from the sessions.
set -euo pipefail
REPO=/home/ilien/Projects/muninn
PIN=${PIN:-$HOME/.local/share/muninn-bench/competitors/muninn-final}
BIN_SHA=20a8385d24c5b270
store() { echo "$CELL_ROOT/data"; }
envs() { printf 'MUNINN_ROOT=%s\nMUNINN_NO_PROJECT=1\nMUNINN_SOURCE_ROOT=%s\n' "$(store)" "$CHECKOUT"; }
case "${1:?subcommand}" in
  install)
    rm -rf "$PIN"; mkdir -p "$PIN"; cp -r "$REPO/plugin" "$PIN/plugin"
    cp "$HOME/.local/share/muninn-bench/muninn-$BIN_SHA" "$PIN/plugin/bin/muninn"
    got=$(sha256sum "$PIN/plugin/bin/muninn" | cut -c1-16)
    [ "$got" = "$BIN_SHA" ] || { echo "pinned binary $got != frozen $BIN_SHA" >&2; exit 1; }
    echo "{\"installed\": \"$PIN/plugin\", \"binary_sha256_prefix\": \"$got\"}" ;;
  start)
    mkdir -p "$(store)/.git" "$CELL_ROOT/home" "$CELL_ROOT/logs"
    [ -d "$(store)/.muninn" ] || env $(envs) "$PIN/plugin/bin/muninn" --cwd "$(store)" init --keep-native >/dev/null
    # the arm under test: the prompt hook delivers nothing, the catalogue and `muninn show`
    # carry the memory (PREREGISTRATION.md, "the closing suite")
    env $(envs) "$PIN/plugin/bin/muninn" --cwd "$(store)" config prompt-delivery off >/dev/null
    echo '{"started": true}' ;;
  claude-args)
    python3 - "$PIN" "$(store)" "$CHECKOUT" <<'PY'
import json,sys
pin,store,checkout=sys.argv[1:4]
print(json.dumps({"args":["--plugin-dir", f"{pin}/plugin"],
  "allowed_tools":["Bash(muninn why *)","Bash(muninn status *)","Bash(muninn show *)","Bash(muninn show:*)","Bash(muninn why:*)","Bash(muninn status:*)"],
  "env":{"MUNINN_ROOT":store,"MUNINN_NO_PROJECT":"1","MUNINN_SOURCE_ROOT":checkout,
         "PATH_PREPEND":f"{pin}/plugin/bin"}}))
PY
    ;;
  settle)
    # the async write path the product runs after sessions (Stop/SessionEnd already queued it)
    env $(envs) "$PIN/plugin/bin/muninn" --cwd "$(store)" maintain >/dev/null 2>&1 || true
    env $(envs) "$PIN/plugin/bin/muninn" --cwd "$(store)" --json export --all --out "$CELL_ROOT/logs/export.jsonl" >/dev/null 2>&1 || true
    python3 - "$CELL_ROOT/logs/export.jsonl" <<'PY'
import json,sys
try: rows=[json.loads(l) for l in open(sys.argv[1])]
except OSError: rows=[]
print(json.dumps({"records":len(rows),"active":sum(1 for r in rows if not r.get("invalid")),
  "by_kind":{k:sum(1 for r in rows if r.get("kind")==k) for k in sorted({r.get("kind") for r in rows})},
  "retired":[{"kind":r.get("kind"),"reason":r.get("invalid_reason"),"body":(r.get("body") or "")[:120]} for r in rows if r.get("invalid")]}))
PY
    ;;
  snapshot) mkdir -p "$2"; cp -a "$(store)/." "$2/" ; echo '{"snapshot": true}' ;;
  restore)  mkdir -p "$(store)"; cp -a "$2/." "$(store)/" ; echo '{"restored": true}' ;;
  stop) echo '{"stopped": true}' ;;
  delivered)
    cat "$(store)/.muninn/log/delivery.jsonl" 2>/dev/null | python3 -c "
import sys,json
ls=[json.loads(l) for l in sys.stdin if l.strip()]
print(json.dumps({'deliveries':len(ls),'tokens':sum(x.get('tokens',0) for x in ls),'reasons':sorted({x.get('reason','').split(':')[0] for x in ls})}))" ;;
  *) echo "unknown subcommand $1" >&2; exit 2 ;;
esac
