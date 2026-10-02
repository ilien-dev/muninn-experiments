# Experiments and gates — the reproducibility kit

Every gate in the plan is measured here with an executable oracle, pre-registered in
`PREREGISTRATION.md` (amendments included, in order), and reported with its raw data.
`REPRODUCE.md` gives one command per number; `prereg-stamps/` holds OpenTimestamps proofs
of the pre-registration commits; `docs/claims.md` lists what is and is not claimed in public.

| gate | question | report | raw data |
|---|---|---|---|
| 1 | does the deterministic rule classifier reach 90 % precision? | `../corpora/claude-md/GATE1.md` | `../corpora/claude-md/` |
| 2 | does literal episode delivery by hook change the outcome? | `GATE2.md` | `results/run1/` (invalid instrument), `results/run2/` |
| 3 (Phase 3 acceptance) | is the real engine not inferior to the throwaway store? | `PHASE3.md` | `results/run3-literal-real-engine/` |
| 3 | does the F1 filter change what the agent does? | `GATE3.md` | `results/gate3-sonnet/`, `results/gate3-haiku/` |
| 4 §1 | do cue-anchored deliveries beat lexical-only? | `GATE4.md` | `results/gate4-cues/` |
| 4 §2 | do invariants survive compaction? | `PREREGISTRATION.md` (decay probe) | reproducible in one command, no model |
| 4 §3 | PM-Bench | `GATE4.md` | `results/pmbench/` |
| 4 §3, round 8 | PM-Bench on held-out weeks, store ablation, gpt-5.6-sol, one bridge (pre-registered) | `GATE4.md` (when measured) | `results/pmbench/round8-sonnet/`, `results/pmbench/round8-codex/` |
| 3, Codex | F1 filter on Codex / gpt-5.6-sol (pre-registered; first grid invalid, see `PREREGISTRATION.md`) | `GATE3.md` (when measured) | `results/gate3-codex/`, `results/gate3-codex-v1-leaky/` |
| 3, public seed | F1 filter with no private input (pre-registered) | `GATE3.md` (when measured) | `results/gate3-public/` |
| 4 §1, replications | boot vehicle and query expansion at five runs (pre-registered) | `GATE4.md` (when measured) | `results/boot-vehicle-rep5/`, `results/gate4-cues-v2-rep5/` |
| 5a | does the compiled control refuse the call its rule forbids, and nothing else? | `../corpora/claude-md/GATE5A.md` — PASS on the third held-out set (0.920 / 0.000); the two that failed are reported there | `results/gate5a-holdout{1,2,3}/` |
| 5b | does compiling a written rule change what the agent does? | `PREREGISTRATION.md` — **not run**; grid built and its plan verified (48 cells) | `rules/scenarios.py`, `rules/tasks-rules.json` |
| h2h, native | how does the harness's own automatic memory score on the same grid? | `PREREGISTRATION.md` — **not run**; arm built and smoke-tested | `h2h/competitors/native/arm.sh` |
| 8 | does reading the repository find the replacements the words cannot? | `loop8/README.md` | `loop8/v3_*.json` |
| 9 | the same grid, a second held-out set, the same binary | `loop9/README.md` | `loop9/v3_*.json` |
| 10 | does a later message about something else take a true decision with it? | `loop10/README.md` | `loop10/pairs*.json`, `results*.json` |
| 11 | the value that is a number: in conversation and in the diff | `loop11/README.md` | `loop11/v_*.json` |
| h2h v4 | the same head-to-head with the decisions also implemented in the code | `PREREGISTRATION.md` | `results/h2h-v4-code/`, `results/h2h-v4-nocode/` |
| — | DreamBench-SWE [K2]: not runnable — hidden oracles and 6 of 11 fixture commits are not public; a `MemoryPolicy` port and the request to the authors are in `dreambench/` | `dreambench/STATUS.md` | — |

## Runner

```sh
cargo build --release -p muninn-cli -p muninn-bench
./target/release/muninn-bench experiment --dry-run                       # the cell plan
./target/release/muninn-bench experiment --config <tasks.json> --jobs 3  # a grid
./target/release/muninn-bench experiment --rerun-errors --out <dir>      # infrastructure errors only
./target/release/muninn-bench experiment --rescore --out <dir>           # re-run every oracle on the saved patches
```

Each cell: a single-commit `git archive` of `base_ref` (no branch, reflog or later commit
reachable) → a store **outside** the checkout (`MUNINN_ROOT`), seeded with the frozen
transcripts, the checkout's symbol graph and, for a grid, `seed_records` (JSONL with
explicit cues) → the boot block in the checkout for arms with Muninn → `claude -p` with
the hooks wired through `--settings`, `MUNINN_ARM`, `MUNINN_SOURCE_ROOT`,
`MUNINN_NO_PROJECT` (no Markdown mirror an agent could read) → the task's oracle →
patch, model message, delivery log and fire ledger saved under `<out>/logs/` and
`<out>/diffs/`. Cells run concurrently (`--jobs`), each in its own process group with
drained pipes and a hard timeout.

Arms: `off` (no memory), `literal` (the shipped engine), `control` (length-matched
irrelevant content from `control_transcripts`), `unfiltered` (same records, invalidation
off — the render-matched control of Gate 3), `lexical` (cues off — Gate 4).

Grids: `revocation/scenarios.py` (Gate 3) and `cues/scenarios.py` (Gate 4) generate
their seeds and tasks; `revocation/analyze.py` computes pass / unsafe / retired-served
and the bootstrap CIs. `pmbench/` holds the OpenAI-compatible bridge over `claude -p`
and the Muninn ledger scaffold for PM-Bench.

The seed transcript (this project's own, frozen before any task was written) lives
outside the repository; its size and sha256 are in `PREREGISTRATION.md`.
