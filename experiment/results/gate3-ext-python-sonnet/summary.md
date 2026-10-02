# Gate 2 experiment — 90 cells, model claude-sonnet-5, 3 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| off | 4/30 (13%) | n/a | 0 | 0 | 0.00 | $0.181 |
| unfiltered | 5/30 (17%) | n/a | 0 | 160 | 4.60 | $0.068 |
| literal | 30/30 (100%) | n/a | 0 | 172 | 4.98 | $0.080 |

literal − off (non-inferable): +0.867 [95% CI +0.800, +0.900]

## Per task

| task | inferable | off | unfiltered | literal | 
|---|---|---|---|---|
| revoke-compression | false | 0/3 | 0/3 | 3/3 | 
| revoke-cache-eviction | false | 1/3 | 0/3 | 3/3 | 
| revoke-password-hashing | false | 0/3 | 0/3 | 3/3 | 
| revoke-tls-backend | false | 0/3 | 0/3 | 3/3 | 
| revoke-wire-format | false | 0/3 | 1/3 | 3/3 | 
| revoke-async-runtime | false | 0/3 | 0/3 | 3/3 | 
| revoke-version-scheme | false | 0/3 | 1/3 | 3/3 | 
| revoke-license | false | 0/3 | 0/3 | 3/3 | 
| revoke-tls-verification | false | 3/3 | 3/3 | 3/3 | 
| revoke-internal-http | false | 0/3 | 0/3 | 3/3 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $9.85. Errors are excluded from pass rates and listed in results.jsonl.
