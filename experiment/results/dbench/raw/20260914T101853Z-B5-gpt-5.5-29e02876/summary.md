# DreamBench-SWE Run 20260914T101853Z-B5-gpt-5.5-29e02876

- condition: B5
- model: gpt-5.5
- tasks: 24
- seed: 2
- tokens: 39370
- estimated cost: 0.193050

## Metrics

- AdmittedMemoryTokensPerTask: 158.291667
- ContradictionRepairAccuracy: 0.000000
- CostPerSuccessfulTask: 0.019305
- HarmfulMemoryRate: 0.000000
- MemoryBloat: 1.000000
- Pass@1: 0.375000
- ProvenanceCompleteness: 1.000000
- RegressionAfterUpdate: NA
- RepeatedErrorRate: 1.000000
- ScopeAccuracy: 1.000000
- SleepCostShare: 0.000000
- StaleMemoryActivationRate: NA
- TaskSuccess: 0.416667
- TotalLatency: 929.023908
- TotalTokens: 39370.000000
- TransferScore: NA
- UsefulMemoryPrecision: 1.000000

## Tasks

- config-reviewer-s01: pass
- config-reviewer-s02: pass
- config-reviewer-s03: pass
- config-reviewer-s04: pass
- config-stale-s01: pass
- config-stale-s02: pass
- config-stale-s03: pass
- config-stale-s04: fail
- expr-convention-s01: pass
- expr-convention-s02: pass
- expr-convention-s03: pass
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
