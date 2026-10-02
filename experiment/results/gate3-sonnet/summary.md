# Gate 2 experiment — 90 cells, model claude-sonnet-5, 3 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| off | 5/30 (17%) | n/a | 0 | 0 | 0.05 | $0.242 |
| unfiltered | 18/30 (60%) | n/a | 0 | 628 | 30.11 | $0.143 |
| literal | 24/30 (80%) | n/a | 0 | 617 | 1.26 | $0.230 |

literal − off (non-inferable): +0.633 [95% CI +0.500, +0.767]

## Per task

| task | inferable | off | unfiltered | literal | 
|---|---|---|---|---|
| revoke-compression | false | 0/3 | 3/3 | 1/3 | 
| revoke-cache-eviction | false | 0/3 | 3/3 | 2/3 | 
| revoke-password-hashing | false | 0/3 | 0/3 | 3/3 | 
| revoke-tls-backend | false | 1/3 | 0/3 | 3/3 | 
| revoke-wire-format | false | 0/3 | 3/3 | 3/3 | 
| revoke-async-runtime | false | 1/3 | 0/3 | 2/3 | 
| revoke-version-scheme | false | 0/3 | 3/3 | 3/3 | 
| revoke-license | false | 0/3 | 3/3 | 1/3 | 
| revoke-tls-verification | false | 3/3 | 3/3 | 3/3 | 
| revoke-internal-http | false | 0/3 | 0/3 | 3/3 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $18.43. Errors are excluded from pass rates and listed in results.jsonl.
