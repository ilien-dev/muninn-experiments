# Gate 2 experiment — 84 cells, model claude-sonnet-5, 3 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| literal | 27/39 (69%) | 3/3 (100%) | 0 | 782 | 2.69 | $0.233 |
| literal-hookboot | 32/39 (82%) | 3/3 (100%) | 0 | 776 | 70.53 | $0.239 |

## Per task

| task | inferable | literal | literal-hookboot | 
|---|---|---|---|
| engine-s12-why-responder | false | 3/3 | 3/3 | 
| fact-userprompt-p95 | false | 3/3 | 3/3 | 
| fact-sessionstart-gate | false | 3/3 | 3/3 | 
| fact-corpus-fetch-limits | false | 3/3 | 3/3 | 
| fact-real-transcript-ingest | false | 0/3 | 0/3 | 
| docs-grammars-control | true | 3/3 | 3/3 | 
| cue-busy-cap | false | 3/3 | 3/3 | 
| cue-stderr-helper | false | 3/3 | 3/3 | 
| cue-azure-pattern | false | 1/3 | 3/3 | 
| cue-artefact-fence | false | 3/3 | 3/3 | 
| cue-size-subcommand | false | 0/3 | 0/3 | 
| cue-timing-stub | false | 1/3 | 2/3 | 
| cue-row-struct | false | 3/3 | 3/3 | 
| cue-router-stub | false | 1/3 | 3/3 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $19.85. Errors are excluded from pass rates and listed in results.jsonl.
