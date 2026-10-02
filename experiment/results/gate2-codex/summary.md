# Gate 2 experiment — 90 cells, model gpt-5.6-sol, 5 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| off | 5/25 (20%) | 5/5 (100%) | 0 | 0 | 0.00 | $0.000 |
| literal | 10/25 (40%) | 5/5 (100%) | 0 | 774 | 3.24 | $0.000 |
| control | 4/25 (16%) | 5/5 (100%) | 0 | 47909 | 3.67 | $0.000 |

literal − off (non-inferable): +0.200 [95% CI +0.200, +0.200]
control − off (non-inferable): -0.040 [95% CI -0.120, +0.000]

Gate 2: PASS

## Per task

| task | inferable | off | literal | control | 
|---|---|---|---|---|
| engine-s12-why-responder | false | 5/5 | 0/5 | 4/5 | 
| fact-userprompt-p95 | false | 0/5 | 5/5 | 0/5 | 
| fact-sessionstart-gate | false | 0/5 | 5/5 | 0/5 | 
| fact-corpus-fetch-limits | false | 0/5 | 0/5 | 0/5 | 
| fact-real-transcript-ingest | false | 0/5 | 0/5 | 0/5 | 
| docs-grammars-control | true | 5/5 | 5/5 | 5/5 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $-0.00. Errors are excluded from pass rates and listed in results.jsonl.
