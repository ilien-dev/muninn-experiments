# Gate 2 experiment — 75 cells, model claude-sonnet-5, 5 run(s)

| arm | non-inferable pass | inferable pass | errors | delivered tokens (mean) | hook p95 ms (max) | cost/cell (mean) |
|---|---|---|---|---|---|---|
| off | 17/20 (85%) | 3/5 (60%) | 0 | 0 | 0.04 | $0.228 |
| literal | 17/20 (85%) | 4/5 (80%) | 0 | 635 | 1.65 | $0.163 |
| control | 18/20 (90%) | 4/5 (80%) | 0 | 0 | 78.14 | $0.239 |

literal − off (non-inferable): +0.000 [95% CI -0.150, +0.150]
control − off (non-inferable): +0.050 [95% CI -0.100, +0.200]

Gate 2: FAIL (see PREREGISTRATION.md decision rule)

## Per task

| task | inferable | off | literal | control | 
|---|---|---|---|---|
| engine-s12-why-responder | false | 2/5 | 2/5 | 3/5 | 
| engine-s10-build-targets | false | 5/5 | 5/5 | 5/5 | 
| engine-s13-experiment-harness | false | 5/5 | 5/5 | 5/5 | 
| engine-s11-tenth-check | false | 5/5 | 5/5 | 5/5 | 
| engine-grammars-control | true | 3/5 | 4/5 | 4/5 | 

Total model cost: $15.74. Errors are excluded from pass rates and listed in results.jsonl.
