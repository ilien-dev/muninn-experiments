#!/usr/bin/env bash
# Is Claude Code's automatic memory available to the cells of this grid?
#
# Every cell of the head-to-head runs as a non-interactive `claude -p` session. This probe
# asks whether auto memory operates there at all, because an arm whose memory never stores
# anything measures nothing — and a grid that reports 0/27 for such an arm would be reporting
# its own instrument.
#
# Three checks, each a single cheap session:
#   1. with the arm's own settings (autoMemoryEnabled + autoMemoryDirectory, --setting-sources '')
#   2. with the operator's default settings, where auto memory is on by default
#   3. whether a session told to remember something writes any file into the memory directory
#
# Re-run it against a later Claude Code and the answer may change; that is the point of
# keeping it. Prints a JSON summary on the last line.
#
#   bash crates/muninn-bench/experiment/h2h/competitors/native/probe.sh [out-dir]
set -euo pipefail

OUT=${1:-$(mktemp -d)}
MODEL=${MODEL:-claude-sonnet-5}
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)   # the probe cds into the fixture; every path below must be absolute
CELL=$OUT/cell
PROJ=$OUT/proj
rm -rf "$CELL" "$PROJ"
mkdir -p "$CELL/memory" "$PROJ"
git -C "$PROJ" init -q .
printf 'x\n' > "$PROJ/a.txt"
git -C "$PROJ" add -A
git -C "$PROJ" -c user.email=probe@local -c user.name=probe commit -qm base

cat > "$OUT/settings.json" <<EOF
{ "autoMemoryEnabled": true, "autoMemoryDirectory": "$CELL/memory" }
EOF

ask() { # ask <label> <extra-args...> -- <prompt>
  local label=$1; shift
  claude -p "$@" --model "$MODEL" --output-format json --max-turns 5 \
    < /dev/null 2>"$OUT/$label.err" > "$OUT/$label.json" || true
  python3 -c '
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("(no json)"); raise SystemExit
print(repr((d.get("result") or "")[:200]))' "$OUT/$label.json"
}

Q="Do you have an auto-memory directory available in this session? If yes, print its exact path. If not, say exactly: no memory."

cd "$PROJ"
echo "1. arm settings          : $(ask arm_settings "$Q" --setting-sources '' --settings "$OUT/settings.json")"
echo "2. operator defaults     : $(ask defaults "$Q")"
echo "3. asked to remember     : $(ask remember 'Remember for later: the payment worker retry budget is 7 attempts, not 3. Acknowledge briefly.' --setting-sources '' --settings "$OUT/settings.json")"

FILES=$(find "$CELL/memory" -type f 2>/dev/null | wc -l)
echo "memory files written     : $FILES"
python3 -c '
import json, sys
out, files = sys.argv[1], int(sys.argv[2])
def res(name):
    try:
        return (json.load(open(f"{out}/{name}.json")).get("result") or "")
    except Exception:
        return ""
avail = not all("no memory" in res(n).lower() for n in ("arm_settings", "defaults"))
print(json.dumps({
    "auto_memory_available_in_print_mode": avail,
    "memory_files_written": files,
    "claude_version": __import__("subprocess").run(["claude","--version"],capture_output=True,text=True).stdout.strip(),
}))' "$OUT" "$FILES" | tee "$OUT/probe.json"
