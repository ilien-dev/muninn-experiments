# Gate 2 experiment — 96 cells, model claude-sonnet-5, 3 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| off | 0/24 (0%) | n/a | 0 | 0 | 0.02 | $0.330 |
| lexical | 12/24 (50%) | n/a | 0 | 609 | 1.49 | $0.271 |
| literal | 14/24 (58%) | n/a | 0 | 1188 | 1.89 | $0.280 |
| control | 2/24 (8%) | n/a | 0 | 1041 | 2.19 | $0.288 |

literal − off (non-inferable): +0.583 [95% CI +0.458, +0.708]
control − off (non-inferable): +0.083 [95% CI +0.000, +0.167]

Gate 2: PASS

## Per task

| task | inferable | off | lexical | literal | control | 
|---|---|---|---|---|---|
| cue-busy-cap | false | 0/3 | 1/3 | 2/3 | 0/3 | 
| cue-stderr-helper | false | 0/3 | 3/3 | 3/3 | 0/3 | 
| cue-azure-pattern | false | 0/3 | 1/3 | 1/3 | 0/3 | 
| cue-artefact-fence | false | 0/3 | 3/3 | 3/3 | 0/3 | 
| cue-size-subcommand | false | 0/3 | 0/3 | 0/3 | 0/3 | 
| cue-timing-stub | false | 0/3 | 0/3 | 2/3 | 1/3 | 
| cue-row-struct | false | 0/3 | 3/3 | 3/3 | 1/3 | 
| cue-router-stub | false | 0/3 | 1/3 | 0/3 | 0/3 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $28.03. Errors are excluded from pass rates and listed in results.jsonl.
