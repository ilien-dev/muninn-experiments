#!/bin/bash
# v39, patient: a fixture whose seeding fails (the competitor never settles, usually a usage
# limit on its observer) or whose cells error is retried after the window has had time to reset.
cd /home/ilien/Projects/muninn/crates/muninn-bench/experiment/h2h
probe() {  # the competitor's observer works iff a one-line session settles
  timeout 60 claude -p "ok" --model claude-sonnet-5 --output-format json --max-turns 1 --setting-sources "" >/dev/null 2>&1
}
for fx in v3 v4 v5 v6 v7; do
  out=../results/h2h-v39-$fx
  for attempt in $(seq 1 12); do
    until timeout 900 python3 /home/ilien/Projects/muninn/crates/muninn-bench/experiment/h2h/probe_claude_mem.py >/dev/null 2>&1; do
      echo "  competitor's observer not settling $(date +%H:%M) — waiting 20 min"; sleep 1200
    done
    echo "=== $fx attempt $attempt $(date +%H:%M)"
    python3 run_h2h.py --out $out --runs 6 --jobs 3 --arms claude-mem,muninn-whysaid \
      --seed-phrasings $fx/seed_phrasings.json --rerun-errors >> $out.launcher.log 2>&1
    bad=$(python3 -c "
import json,os
cfg=json.load(open('$out/config.json'))
want=len(cfg['tasks'])*6*2
got=0; err=0
if os.path.exists('$out/results.jsonl'):
    for l in open('$out/results.jsonl'):
        r=json.loads(l); got+=1; err+= r['status']=='error'
print(want-got+err)")
    if grep -q "SEEDING FAILED" $out.launcher.log; then
      sed -i 's/SEEDING FAILED/seeding failed (retried)/' $out.launcher.log; bad=1
    fi
    [ "$bad" = "0" ] && { echo "  $fx complete $(date +%H:%M)"; break; }
    echo "  $fx: $bad cells missing or errored — retrying once the observer settles again"
  done
done
echo ALL DONE
