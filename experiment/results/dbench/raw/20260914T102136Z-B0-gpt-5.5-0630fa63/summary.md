# DreamBench-SWE Run 20260914T102136Z-B0-gpt-5.5-0630fa63

- condition: B0
- model: gpt-5.5
- tasks: 24
- seed: 3
- tokens: 32269
- estimated cost: 0.161345

## Metrics

- AdmittedMemoryTokensPerTask: 1.000000
- ContradictionRepairAccuracy: NA
- CostPerSuccessfulTask: 0.016134
- HarmfulMemoryRate: NA
- MemoryBloat: NA
- Pass@1: 0.375000
- ProvenanceCompleteness: NA
- RegressionAfterUpdate: NA
- RepeatedErrorRate: 1.000000
- ScopeAccuracy: NA
- SleepCostShare: 0.000000
- StaleMemoryActivationRate: NA
- TaskSuccess: 0.416667
- TotalLatency: 762.416079
- TotalTokens: 32269.000000
- TransferScore: NA
- UsefulMemoryPrecision: NA

## Tasks

- config-reviewer-s01: pass
- config-reviewer-s02: pass
- config-reviewer-s03: pass
- config-reviewer-s04: pass
- config-stale-s01: pass
- config-stale-s02: pass
- config-stale-s03: pass
- config-stale-s04: pass
- expr-convention-s01: pass
- expr-convention-s02: pass
- expr-convention-s03: fail
- expr-convention-s04: fail
- expr-generated-s01: fail
- expr-generated-s02: fail
- expr-generated-s03: fail
- expr-generated-s04: fail
- todo-convention-s01: fail
- todo-convention-s02: fail
- todo-convention-s03: fail
- todo-convention-s04: fail
- todo-flaky-s01: fail
- todo-flaky-s02: fail
- todo-flaky-s03: fail
- todo-flaky-s04: fail
