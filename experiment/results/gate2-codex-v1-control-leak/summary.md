# Gate 2 experiment — 90 cells, model gpt-5.6-sol, 5 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| off | 4/25 (16%) | 5/5 (100%) | 0 | 0 | 0.00 | $0.000 |
| literal | 15/25 (60%) | 5/5 (100%) | 0 | 774 | 2.54 | $0.000 |
| control | 14/25 (56%) | 5/5 (100%) | 0 | 713 | 3557.80 | $0.000 |

literal − off (non-inferable): +0.440 [95% CI +0.320, +0.600]
control − off (non-inferable): +0.400 [95% CI +0.280, +0.560]

Gate 2: FAIL (see PREREGISTRATION.md decision rule)

## Per task

| task | inferable | off | literal | control | 
|---|---|---|---|---|
| engine-s12-why-responder | false | 4/5 | 2/5 | 1/5 | 
| fact-userprompt-p95 | false | 0/5 | 5/5 | 5/5 | 
| fact-sessionstart-gate | false | 0/5 | 5/5 | 5/5 | 
| fact-corpus-fetch-limits | false | 0/5 | 0/5 | 1/5 | 
| fact-real-transcript-ingest | false | 0/5 | 3/5 | 2/5 | 
| docs-grammars-control | true | 5/5 | 5/5 | 5/5 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $-0.00. Errors are excluded from pass rates and listed in results.jsonl.
