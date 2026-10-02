# Gate 2 experiment — 90 cells, model gpt-5.6-sol, 3 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| off | 21/30 (70%) | n/a | 0 | 0 | 0.06 | $0.000 |
| unfiltered | 3/30 (10%) | n/a | 0 | 844 | 7.44 | $0.000 |
| literal | 30/30 (100%) | n/a | 0 | 812 | 2.40 | $0.000 |

literal − off (non-inferable): +0.300 [95% CI +0.167, +0.433]

## Per task

| task | inferable | off | unfiltered | literal | 
|---|---|---|---|---|
| revoke-compression | false | 3/3 | 0/3 | 3/3 | 
| revoke-cache-eviction | false | 2/3 | 0/3 | 3/3 | 
| revoke-password-hashing | false | 3/3 | 0/3 | 3/3 | 
| revoke-tls-backend | false | 1/3 | 0/3 | 3/3 | 
| revoke-wire-format | false | 1/3 | 0/3 | 3/3 | 
| revoke-async-runtime | false | 1/3 | 0/3 | 3/3 | 
| revoke-version-scheme | false | 2/3 | 0/3 | 3/3 | 
| revoke-license | false | 2/3 | 0/3 | 3/3 | 
| revoke-tls-verification | false | 3/3 | 3/3 | 3/3 | 
| revoke-internal-http | false | 3/3 | 0/3 | 3/3 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $-0.00. Errors are excluded from pass rates and listed in results.jsonl.
