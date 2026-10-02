#!/usr/bin/env bash
# Round 4 of Gate 4 §3 (PM-Bench): three arms × three runs, claude-sonnet-5, isolated invocation.
#   muninn_store    — run_muninn_pis.py (calls `claude -p` directly, same flags as the bridge)
#   single_baseline — PM-Bench's own runner through the isolated bridge
#   todo_ledger     — PM-Bench's own runner through the isolated bridge
# Usage: run_round4.sh <PMBench checkout> <out dir> [runs=3] [model=claude-sonnet-5]
set -euo pipefail
PMB=${1:?PMBench checkout}
OUT=${2:?out dir}
RUNS=${3:-3}
ARMS=${ARMS:-"muninn_store single_baseline todo_ledger"}
MODEL=${4:-claude-sonnet-5}
PORT=30002
export MUNINN_BIN=${MUNINN_BIN:-/home/ilien/Projects/muninn/target/release/muninn}
PY="$PMB/.venv/bin/python"
SCN="$PMB/data/synthetic_week_v9.json"
mkdir -p "$OUT"

# the isolated bridge for the two PM-Bench arms
if ! curl -s -o /dev/null "http://127.0.0.1:$PORT/v1"; then
  nohup "$PY" "$PMB/sim/claude_bridge.py" --port $PORT --model "$MODEL" > "$OUT/bridge.log" 2>&1 &
  echo "bridge pid $!" ; sleep 1
fi

pids=()
for i in $(seq 1 "$RUNS"); do
  [[ " $ARMS " == *" muninn_store "* ]] || break
  nohup "$PY" -u "$PMB/sim/run_muninn_pis.py" --scenario "$SCN" --model "$MODEL" --out-dir "$OUT/muninn_store" --score \
    > "$OUT/muninn_store-r$i.log" 2>&1 &
  pids+=($!)
done
for i in $(seq 1 "$RUNS"); do
  [[ " $ARMS " == *" single_baseline "* ]] && \
  nohup "$PY" -u "$PMB/sim/run_eval.py" --setup single_baseline --scenario "$SCN" --backend sglang \
    --base-url "http://127.0.0.1:$PORT/v1" --model "$MODEL" --out-dir "$OUT/single_baseline" --score \
    > "$OUT/single_baseline-r$i.log" 2>&1 &
  pids+=($!); sleep 1.2   # the PM-Bench runner names the log by the launch second
  [[ " $ARMS " == *" todo_ledger "* ]] && \
  nohup "$PY" -u "$PMB/sim/run_eval.py" --setup todo_ledger --scenario "$SCN" --backend sglang \
    --base-url "http://127.0.0.1:$PORT/v1" --model "$MODEL" --out-dir "$OUT/todo_ledger" --score \
    > "$OUT/todo_ledger-r$i.log" 2>&1 &
  pids+=($!); sleep 1.2
done
echo "${pids[*]}" > "$OUT/pids"
echo "launched ${#pids[@]} runs; pids in $OUT/pids"
