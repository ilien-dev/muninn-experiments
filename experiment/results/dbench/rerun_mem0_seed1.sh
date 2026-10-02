#!/usr/bin/env bash
# infrastructure re-run: B5-MEM0-LIT seed 1 crashed at policy start (embedding model not yet cached)
OUT=$HOME/Projects/muninn/crates/muninn-bench/experiment/results/dreambench-public
until [ -f $OUT/grid.done ]; do sleep 60; done
mv $OUT/logs/B5-MEM0-LIT-seed1.log $OUT/logs/B5-MEM0-LIT-seed1.crash1.log
sed -e 's/^for seed in 1 2 3; do for cond in B0 B5 B5-MEM0-LIT MUNINN; do echo "$seed $cond"; done; done/echo "1 B5-MEM0-LIT"/' -e 's|echo done > $OUT/grid.done|echo done > $OUT/rerun.done|' $OUT/run_grid.sh > $OUT/run_rerun.sh
bash $OUT/run_rerun.sh
