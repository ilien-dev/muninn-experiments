#!/bin/bash
# v40: the shipping build on all five fixtures, Muninn cells only. Cells voided by the account's
# usage window are completed with --rerun-errors after a wait.
cd /home/ilien/Projects/muninn/crates/muninn-bench/experiment/h2h
for fx in v3 v4 v5 v6 v7; do
  out=../results/h2h-v40-$fx
  for attempt in 1 2 3 4 5 6; do
    echo "=== $fx attempt $attempt $(date +%H:%M)"
    python3 run_h2h.py --out $out --runs 6 --jobs 3 --arms muninn-whysaid \
      --seed-phrasings $fx/seed_phrasings.json --rerun-errors >> $out.launcher.log 2>&1
    bad=$(python3 -c "
import json,os
cfg=json.load(open('$out/config.json')); want=len(cfg['tasks'])*6; got=err=0
if os.path.exists('$out/results.jsonl'):
    for l in open('$out/results.jsonl'):
        r=json.loads(l); got+=1; err+= r['status']=='error'
print(want-got+err)")
    [ "$bad" = "0" ] && { echo "  $fx complete $(date +%H:%M)"; break; }
    echo "  $fx: $bad cells missing or errored — waiting 30 min"; sleep 1800
  done
done
echo ALL DONE
