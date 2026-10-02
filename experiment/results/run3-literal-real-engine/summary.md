# Gate 2 experiment — 25 cells, model claude-sonnet-5, 5 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| literal | 21/25 (84%) | n/a | 0 | 666 | 33.79 | $0.218 |

## Per task

| task | inferable | literal | 
|---|---|---|
| engine-s12-why-responder | false | 5/5 | 
| fact-userprompt-p95 | false | 5/5 | 
| fact-sessionstart-gate | false | 5/5 | 
| fact-corpus-fetch-limits | false | 5/5 | 
| fact-real-transcript-ingest | false | 1/5 | 

Total model cost: $5.45. Errors are excluded from pass rates and listed in results.jsonl.
