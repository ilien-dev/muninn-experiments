#!/usr/bin/env bash
# DreamBench-SWE public pilot grid (PREREGISTRATION.md, 2026-09-14): 4 conditions x 3 seeds, 4 at a time.
set -uo pipefail
DB=$HOME/Projects/dreambench-swe
EXT=$HOME/Projects/muninn/crates/muninn-bench/experiment/dreambench
OUT=$HOME/Projects/muninn/crates/muninn-bench/experiment/results/dreambench-public
export PATH=$DB/.venv/bin:$PATH DREAMBENCH_ROOT=$DB PYTHONDONTWRITEBYTECODE=1
export DREAMBENCH_MEM0_OFFLINE=1 MEM0_TELEMETRY=False FASTEMBED_CACHE_PATH=$HOME/.cache/fastembed
export DREAMBENCH_MEM0_FIXTURE_ROOT=$OUT/mem0-exchanges DREAMBENCH_MEM0_OFFLINE_ROOT=$OUT/mem0-stores
export MUNINN_DREAMBENCH_STORE_ROOT=$OUT/muninn-stores HF_HUB_OFFLINE=1
export MUNINN_BIN=$HOME/.local/share/muninn-bench/muninn-fdcb4606
cd $DB
for seed in 1 2 3; do for cond in B0 B5 B5-MEM0-LIT MUNINN; do echo "$seed $cond"; done; done | \
  xargs -P 4 -L 1 bash -c 'python3 '"$EXT"'/run_bench_ext.py --include-live-baselines --condition $1 --model gpt-5.5 --seed $0 --results-root '"$OUT"'/raw > '"$OUT"'/logs/$1-seed$0.log 2>&1; echo "$1 seed$0 exit $?" >> '"$OUT"'/logs/exits.txt'
echo done > $OUT/grid.done
