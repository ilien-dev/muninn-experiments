# Gate 2 experiment — 140 cells, model claude-sonnet-5, 5 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| literal | 47/65 (72%) | 5/5 (100%) | 0 | 811 | 3.12 | $0.189 |
| literal-hookboot | 47/65 (72%) | 5/5 (100%) | 0 | 798 | 3.23 | $0.197 |

## Per task

| task | inferable | literal | literal-hookboot | 
|---|---|---|---|
| engine-s12-why-responder | false | 5/5 | 5/5 | 
| fact-userprompt-p95 | false | 5/5 | 4/5 | 
| fact-sessionstart-gate | false | 5/5 | 5/5 | 
| fact-corpus-fetch-limits | false | 5/5 | 4/5 | 
| fact-real-transcript-ingest | false | 0/5 | 0/5 | 
| docs-grammars-control | true | 5/5 | 5/5 | 
| cue-busy-cap | false | 5/5 | 5/5 | 
| cue-stderr-helper | false | 5/5 | 5/5 | 
| cue-azure-pattern | false | 4/5 | 4/5 | 
| cue-artefact-fence | false | 5/5 | 4/5 | 
| cue-size-subcommand | false | 0/5 | 0/5 | 
| cue-timing-stub | false | 4/5 | 2/5 | 
| cue-row-struct | false | 1/5 | 4/5 | 
| cue-router-stub | false | 3/5 | 5/5 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $27.05. Errors are excluded from pass rates and listed in results.jsonl.
