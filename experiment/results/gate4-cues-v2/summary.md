# Gate 2 experiment — 72 cells, model claude-sonnet-5, 3 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| lexical-plain | 10/24 (42%) | n/a | 0 | 503 | 1.36 | $0.231 |
| lexical | 13/24 (54%) | n/a | 0 | 522 | 4.21 | $0.260 |
| literal | 15/24 (62%) | n/a | 0 | 741 | 2.37 | $0.242 |

## Per task

| task | inferable | lexical-plain | lexical | literal | 
|---|---|---|---|---|
| cue-busy-cap | false | 0/3 | 2/3 | 2/3 | 
| cue-stderr-helper | false | 3/3 | 3/3 | 2/3 | 
| cue-azure-pattern | false | 1/3 | 2/3 | 2/3 | 
| cue-artefact-fence | false | 3/3 | 3/3 | 3/3 | 
| cue-size-subcommand | false | 0/3 | 0/3 | 0/3 | 
| cue-timing-stub | false | 0/3 | 0/3 | 2/3 | 
| cue-row-struct | false | 3/3 | 3/3 | 3/3 | 
| cue-router-stub | false | 0/3 | 0/3 | 1/3 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $17.57. Errors are excluded from pass rates and listed in results.jsonl.
