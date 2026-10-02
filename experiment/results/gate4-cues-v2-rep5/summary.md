# Gate 2 experiment — 120 cells, model claude-sonnet-5, 5 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| lexical-plain | 15/40 (38%) | n/a | 0 | 503 | 1.42 | $0.242 |
| lexical | 10/40 (25%) | n/a | 0 | 522 | 5.76 | $0.234 |
| literal | 9/40 (22%) | n/a | 0 | 784 | 3.47 | $0.231 |

## Per task

| task | inferable | lexical-plain | lexical | literal | 
|---|---|---|---|---|
| cue-busy-cap | false | 5/5 | 5/5 | 3/5 | 
| cue-stderr-helper | false | 0/5 | 0/5 | 0/5 | 
| cue-azure-pattern | false | 3/5 | 0/5 | 0/5 | 
| cue-artefact-fence | false | 4/5 | 3/5 | 3/5 | 
| cue-size-subcommand | false | 0/5 | 0/5 | 0/5 | 
| cue-timing-stub | false | 3/5 | 2/5 | 3/5 | 
| cue-row-struct | false | 0/5 | 0/5 | 0/5 | 
| cue-router-stub | false | 0/5 | 0/5 | 0/5 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $28.29. Errors are excluded from pass rates and listed in results.jsonl.
