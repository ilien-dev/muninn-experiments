# Gate 2 experiment — 90 cells, model claude-sonnet-5, 5 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| off | 2/25 (8%) | 5/5 (100%) | 0 | 0 | 0.07 | $0.321 |
| literal | 19/25 (76%) | 5/5 (100%) | 0 | 627 | 1.36 | $0.245 |
| control | 4/25 (16%) | 5/5 (100%) | 0 | 542 | 1.75 | $0.355 |

literal − off (non-inferable): +0.680 [95% CI +0.560, +0.800]
control − off (non-inferable): +0.080 [95% CI -0.040, +0.200]

Gate 2: PASS

## Per task

| task | inferable | off | literal | control | 
|---|---|---|---|---|
| engine-s12-why-responder | false | 2/5 | 5/5 | 4/5 | 
| fact-userprompt-p95 | false | 0/5 | 5/5 | 0/5 | 
| fact-sessionstart-gate | false | 0/5 | 5/5 | 0/5 | 
| fact-corpus-fetch-limits | false | 0/5 | 4/5 | 0/5 | 
| fact-real-transcript-ingest | false | 0/5 | 0/5 | 0/5 | 
| docs-grammars-control | true | 5/5 | 5/5 | 5/5 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $27.63. Errors are excluded from pass rates and listed in results.jsonl.
