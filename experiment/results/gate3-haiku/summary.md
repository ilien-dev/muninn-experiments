# Gate 2 experiment — 90 cells, model claude-haiku-4-5-20251001, 3 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| off | 4/30 (13%) | n/a | 0 | 0 | 0.02 | $0.111 |
| unfiltered | 22/30 (73%) | n/a | 0 | 628 | 1.14 | $0.045 |
| literal | 27/30 (90%) | n/a | 0 | 617 | 1.76 | $0.036 |

literal − off (non-inferable): +0.767 [95% CI +0.700, +0.800]

## Per task

| task | inferable | off | unfiltered | literal | 
|---|---|---|---|---|
| revoke-compression | false | 0/3 | 3/3 | 3/3 | 
| revoke-cache-eviction | false | 0/3 | 3/3 | 3/3 | 
| revoke-password-hashing | false | 0/3 | 2/3 | 3/3 | 
| revoke-tls-backend | false | 1/3 | 0/3 | 3/3 | 
| revoke-wire-format | false | 0/3 | 3/3 | 3/3 | 
| revoke-async-runtime | false | 0/3 | 1/3 | 3/3 | 
| revoke-version-scheme | false | 0/3 | 3/3 | 3/3 | 
| revoke-license | false | 0/3 | 3/3 | 3/3 | 
| revoke-tls-verification | false | 3/3 | 3/3 | 3/3 | 
| revoke-internal-http | false | 0/3 | 1/3 | 0/3 | 

Retired records delivered (all arms, all cells): 0.

Total model cost: $5.77. Errors are excluded from pass rates and listed in results.jsonl.
