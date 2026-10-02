# DreamBench-SWE public subset: four-condition feasibility (B0, B5, B5-MEM0-LIT, MUNINN)

Date: 2026-09-14. DreamBench-SWE checkout `~/Projects/dreambench-swe` at `d340bb2`.
The v2.1 release artifact path given in the brief (`.../scratchpad/v21/x/`) does not exist on this
machine; everything below uses the git checkout. File:line citations refer to that commit.

Verdict: **feasible, with a large construct gap**. The harness runs end to end locally with Codex in
Docker, and a MUNINN condition plugs in without editing DreamBench. But the only public, locally
scorable material is the 24-task pilot (v0), which is scored in the harness's legacy per-task mode,
with oracle tests visible in the checkout and each session reset to the reference solution. It is
not the paper's confirmatory protocol and its numbers are not comparable to the paper's.

## 1. What is public and scorable

| Source | Records | Multi-session | Oracle present | Scorable locally |
|---|---|---|---|---|
| `experiments/env/tasks.jsonl` | 24 tasks = 6 sequences x 4 sessions | yes | yes, `oracle_cmd` + `reference_patch` per task | **24 / 24** |
| `experiments/env/sequences.jsonl` | 22 sequences x 3 sessions | yes | no: `oracles/` and `refsol/` absent | 0 |
| `experiments/env/sequences_synth.jsonl` | 8 x 3 | yes | no | 0 |
| `experiments/env/sequences_confirmatory_v2.jsonl` | 60 x 3 (the paper's traps) | yes | no | 0 |

Sequences in `tasks.jsonl`: `expr-convention`, `expr-generated` (exprmini), `config-stale`,
`config-reviewer` (configly), `todo-flaky`, `todo-convention` (todolite). Sequence records resolve
oracles only from `experiments/env/oracles/<seq>/sN_test.py` (`experiments/env/load_env.py:203-243`);
that tree is not in the public checkout.

Validation actually run (all measured on this machine):

| Command | Result |
|---|---|
| `python3 experiments/env/build_env.py` (venv python first on PATH) | builds `repos/{exprmini,configly,todolite}` in 5.7 s |
| `python3 experiments/env/load_env.py` | `validated 24/24 tasks` (base ref fails, reference patch passes) |
| `python3 scripts/run_smoke.py` | runs; it is a synthetic stub over 60 fixture tasks, prints "NOT EXPERIMENTAL RESULTS, DO NOT CITE" |
| `python3 experiments/validate_trap.py --selftest` | 22/22 sequences FAIL: missing `refsol/` and S3 oracle files |
| `python3 src/experiments/run_bench.py --selftest` | OK, 2 stub tasks |
| `run_bench_ext.py --dry-run --include-live-baselines --conditions B0,B5,B5-MEM0-LIT,MUNINN --sequence-records experiments/env/sequences.jsonl --seq config-stale-merge` | OK, gate report written for all four conditions (stub agent, stub oracle) |

Hazards in the fixture builder, hit during this study and repaired with `git checkout`:
- `build_env.py` hardcodes `python3 -m pytest` (`build_env.py:17`); with no pytest on the system
  python it fails after deleting `tasks.jsonl` (`build_env.py:2212-2213`).
- On success it overwrites `experiments/env/load_env.py` with an older embedded copy (529 lines
  removed; the old copy lacks `load_sequence_records` and `score_agent_diff`). Restore it before any run.

## 2. One real run under the harness (measured)

```
python3 src/experiments/run_bench.py --condition B0 --seq expr-convention --model gpt-5.5 --seed 1
```

| | B0 | MUNINN (`run_bench_ext.py --condition MUNINN`, same flags) |
|---|---|---|
| Agent sessions | 4 | 4 |
| Wall time | 261 s (65 s per session) | 272 s (68 s per session) |
| Sessions passed (oracle) | 4 / 4 | 4 / 4 |
| Isolation, model | `container`, `gpt-5.5` on every record | same |
| Memory items admitted, sessions 1 to 4 | 0, 0, 0, 0 | 0, 1, 1, 2 (all `episode` records) |
| Policy write time, 4 sessions total | 0 s | 0.012 s |
| Output | `results.json`, `summary.md`, `trajectories/00N-*.json` | same |

On this sequence no `user_said` event record was admitted: `muninn why` ranks by lexical overlap,
and the next session's prompt shared no terms with the feedback text. Both conditions sit at the
ceiling here, so this pair says nothing about memory effect (n = 4 sessions each, one seed).

- Docker image: `docker build -t dreambench-swe-codex-agent:latest -f scripts/Dockerfile.codex-agent .`
  took 62 s. The harness would also build it on first use (`src/agents/llm_agents.py:1190-1204`).
- Auth: the jail mounts `~/.codex` read-only and needs `auth.json` and `config.toml`
  (`llm_agents.py:1164-1169`); the existing ChatGPT login worked unchanged.
- Model: `_agent_for_model` accepts only `codex`/`gpt-5.5` and hardcodes `CodexAgent("gpt-5.5")`
  (`src/experiments/run_bench.py:1199-1207`). `gpt-5.5` is listed in `~/.codex/models_cache.json` and
  served every session. `gpt-5.6-sol` would need a harness edit; it was not tried.
- Image Codex CLI is 0.142.0 (`Dockerfile.codex-agent:10`), the version the paper pins
  (`analysis/fold/REPRO-MANIFEST.md`); the host's 0.154.0 is not used.
- Only 8 agent sessions were spent in total (B0 and MUNINN on one sequence, seed 1). These are
  instrument checks in the scratchpad, not experiment cells, and are not committed.

## 3. Mem0 offline (B5-MEM0-LIT)

`Mem0Policy._construct_client` only builds the hosted `MemoryClient` from `MEM0_API_KEY`
(`src/benchmarks/baselines.py:472-486`); `_mem0_default_config` (`:1680`) is never used to build a
client. The paper's B5-MEM0 / B5-MEM0-LIT rows are the pinned hosted Mem0
(`analysis/investigation-evidence/MEM0-ROW-FOLD-REPORT.md:52`). Offline therefore needs an injected
OSS client, which `Mem0Policy(client=...)` accepts (`baselines.py:369,394`); `run_bench_ext.py` does
this when `DREAMBENCH_MEM0_OFFLINE=1`.

Installed in the checkout venv: `mem0ai 2.0.20`, `fastembed 0.8.0`, `qdrant-client 1.19.0`.
Config (from `run_bench_ext.py::mem0_offline_config`):

```python
{"embedder": {"provider": "fastembed", "config": {"model": "BAAI/bge-small-en-v1.5"}},
 "vector_store": {"provider": "qdrant", "config": {"collection_name": "dreambench",
                  "path": "<run>/qdrant", "embedding_model_dims": 384, "on_disk": True}},
 "llm": {"provider": "openai", "config": {"model": "unused-infer-false", "api_key": "unused-infer-false",
         "openai_base_url": "http://127.0.0.1:9/v1"}},   # constructed by mem0, never called with infer=False
 "history_db_path": "<run>/history.db"}
```

Smoke (measured; second run with `HF_HUB_OFFLINE=1` and `socket.connect` patched to raise):

```python
m = Memory.from_config(cfg)
m.add([{"role": "user", "content": "All public expression failures use EXPR_<CODE>: <message>."}], user_id="seq-a", infer=False)
m.add([{"role": "user", "content": "Generated operator help must be regenerated after editing operators.py."}], user_id="seq-a", infer=False)
m.search("which error message convention should safe_evaluate keep", top_k=1, filters={"user_id": "seq-a"})
# -> [{'memory': 'All public expression failures use EXPR_<CODE>: <message>.', 'score': 0.3577, ...}]  0.6 s
```

The embedding model (65 MB on disk, `qdrant/bge-small-en-v1.5-onnx-q`) is downloaded once from
Hugging Face into `/tmp/fastembed_cache` by default; set `FASTEMBED_CACHE_PATH` to a persistent
directory. After that the path is network-free. The OSS `ollama` LLM provider cannot be used as the dummy: it needs the `ollama`
package. Through the harness (stub agent, 8 public tasks) the policy read 1, 2, 3 items in sessions
2 to 4 of each sequence, with no sleep errors.

## 4. MuninnPolicy

`muninn_policy.py` subclasses `MemoryPolicy` (`baselines.py:59`) with the same `read(task)` /
`write(trajectory)` contract as `InstancePolicy` (`:307`) and `Mem0LiteralPolicy` (`:590`).

- `write`: `_episode_from_any(trajectory)`; one `decision` record, origin `user_said`, per injected
  event line (`_mem0_sanitized_event_lines`, the harness's own sanitizer); one `episode` record, origin
  `tool_observed`, holding prompt, outcome, error type, actions and production diff, clipped to
  Muninn's 2000-character body. Rows go through `muninn import` into a per-sequence store
  `<MUNINN_DREAMBENCH_STORE_ROOT>/<run_id>/MUNINN/seed-<n>/<sequence_id>` selected with `MUNINN_ROOT`
  (same scoping as the Mem0 namespace). The same leak guard as Mem0 (`_assert_mem0_payload_clean`) runs on every body.
- `read`: `muninn why --json --limit <=6 --budget 1200 <task prompt>`; exit 3 ("insufficient") is a
  valid empty answer. Items use the key set of `_context_from_mem0_result` (`baselines.py:1511`), plus
  `origin` and `trust`; `type` is `human_feedback` for `user_said` records, else `episodic`. The Mem0
  admission rule (6 items, 1200 harness tokens) is applied after Muninn's own budget.
- No tuning to the tasks: no prompts, weights or thresholds were chosen by looking at outcomes.

Tests (`test_muninn_policy.py`, fabricated trajectories, no model): 6 passed in 0.23 s. Through the
harness with the stub agent over all 24 public tasks: no task exceptions, 0 to 6 items admitted per session.

`run_bench_ext.py` registers `MUNINN` in `BASELINE_REGISTRY` and wraps `_policy_for_condition`, so
`run_bench`'s own argument parser, agent, oracle scoring and output files are used unchanged.
`scripts/run_grid.py` cannot be used: it launches `python -m experiments.run_bench` subprocesses
(`run_grid.py:636`) and validates against a fixed `VALID_CONDITIONS` (`:34`), so the grid below is a
shell loop.

## 5. Commands for the public-subset grid

Prerequisite in this repository: pre-register in `crates/muninn-bench/experiment/PREREGISTRATION.md`
before the first cell.

```bash
DB=$HOME/Projects/dreambench-swe
EXT=$HOME/Projects/muninn/crates/muninn-bench/experiment/dreambench
OUT=$HOME/Projects/muninn/crates/muninn-bench/experiment/results/dbench

# one-time setup
cd $DB
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python pytest==8.4.2 mem0ai==2.0.20 fastembed==0.8.0
PATH=$DB/.venv/bin:$PATH python3 experiments/env/build_env.py
git checkout -- experiments/env/load_env.py experiments/env/tasks.jsonl   # undo build_env side effects
PATH=$DB/.venv/bin:$PATH python3 experiments/env/load_env.py              # expect: validated 24/24 tasks
docker build -t dreambench-swe-codex-agent:latest -f scripts/Dockerfile.codex-agent .
(cd $EXT && DREAMBENCH_ROOT=$DB $DB/.venv/bin/python -m pytest -q -p no:cacheprovider test_muninn_policy.py)

# download the embedding model once, then the grid runs with HF_HUB_OFFLINE=1
(cd $EXT && FASTEMBED_CACHE_PATH=$HOME/.cache/fastembed $DB/.venv/bin/python -c "from fastembed import TextEmbedding; TextEmbedding('BAAI/bge-small-en-v1.5')")

# grid: 4 conditions x 3 seeds x 24 sessions
export PATH=$DB/.venv/bin:$PATH DREAMBENCH_ROOT=$DB PYTHONDONTWRITEBYTECODE=1
export DREAMBENCH_MEM0_OFFLINE=1 MEM0_TELEMETRY=False FASTEMBED_CACHE_PATH=$HOME/.cache/fastembed
export DREAMBENCH_MEM0_FIXTURE_ROOT=$OUT/m0x DREAMBENCH_MEM0_OFFLINE_ROOT=$OUT/m0s
export MUNINN_DREAMBENCH_STORE_ROOT=$OUT/mns HF_HUB_OFFLINE=1
mkdir -p $OUT/raw $OUT/logs
for seed in 1 2 3; do
  for cond in B0 B5 B5-MEM0-LIT MUNINN; do
    python3 $EXT/run_bench_ext.py --include-live-baselines --condition $cond \
      --model gpt-5.5 --seed $seed --results-root $OUT/raw > $OUT/logs/$cond-seed$seed.log 2>&1
  done
done
```

Omitting `--seq` runs all 24 tasks of `tasks.jsonl`, ordered by sequence and session
(`run_bench.py:1210-1224`). Each (condition, seed) is one process with a fresh policy; the 12
processes are independent (unique run ids, separate stores) and can run in parallel.

| | Value |
|---|---|
| Agent sessions | 4 x 3 x 24 = **288** |
| Wall time, serial | about 5.3 h (estimate: 288 x 67 s, the mean per-session time of the two measured runs) |
| Wall time, 4 processes in parallel | about 1.3 h (estimate; ChatGPT-plan rate limits not measured) |

## 6. Deviations from the paper's protocol a reader must be told

1. **Public pilot only.** 24 v0 tasks in 6 sequences, not the 60 confirmatory v2 sequences whose
   S3 pass@1 is the paper's outcome (`analysis/investigation-evidence/CONFIRMATORY-FOLD.md`).
2. **Legacy per-task mode, not sequence continuation.** Without `sessions[]` records,
   `_execute_sequence` materialises every session from its own `base_ref` (`run_bench.py:948-949`);
   there is no S3 slice scorer, no gate report and none of the hygiene metrics
   (`run_bench.py:825-832`). Outcome available: per-session `final_passed` / `pass_at_1`.
3. **Each session starts from the reference solution of the previous one.** Tag
   `tasks/expr-convention/s02/base` sits on the commit "session 1 reference fix"; the agent's own
   earlier code never carries forward.
4. **Oracles are visible.** The failing test is committed at the base ref (e.g. `s02/base` adds
   `tests/test_evaluate_many.py`); the paper hides oracles outside the container. Test edits are
   stripped before scoring (`load_env.py:score_agent_diff`). The agent container has no Python
   (`node:22-slim`), so the agent can read the tests but not run them, as in the paper.
5. **Ceiling risk.** B0 and MUNINN each passed 4/4 on `expr-convention` (one sequence, one seed). Headroom for any
   memory condition may be small on this subset; not measured on the other five sequences.
6. **Event timing is the harness's.** A session's injected event is written after that session and
   is first readable in the next (`run_bench.py:1035-1041`, `:1423-1447`), for every condition.
   Payloads with two fields (stale plus correction) are joined into one string (`run_bench.py:1317-1337`).
7. **Mem0 is OSS offline, not hosted.** mem0ai 2.0.20, fastembed `BAAI/bge-small-en-v1.5`, local
   Qdrant, default search threshold, spaCy absent (mem0 logs that lemma models are unavailable), and
   `metadata.run_id` is dropped by OSS `add()`. Retrieval can differ from the pinned hosted Mem0.
8. **MUNINN is a new condition** outside the paper, used as a CLI store: lexical FTS5 retrieval only
   (`vector_used: false`), no hooks, no cues, no supersession on import.
9. **Same model name, different time and host.** `gpt-5.5` via Codex 0.142.0 as pinned, but
   served in September instead of July 2026, on Linux Docker 29.7.2 instead of OrbStack Docker 29.4.0.
   Seeds set `random.seed` and store namespaces only; Codex sampling is not seeded.
10. **Token and cost columns are not trustworthy.** Codex 0.142.0 prints `tokens used` then the
    number on the next line; `_parse_usage` (`llm_agents.py:1464-1476`) does not match it, so wake
    tokens fall back to a text-length estimate. The B0 manifest reports 11,559 wake tokens for 4
    sessions while Codex printed 26,153 for session 1 alone.
11. **Write counts.** `counts.sleep_writes` is 0 for MUNINN and B5-MEM0-LIT because both leave
    `last_write_items` empty, as Mem0 already did; the per-record `sleep_write_count` holds the real count.
12. Analysis scripts (`scripts/analyze_confirmatory_v2.py`, `fold_results.py`) expect `SLICE-*`
    sequence runs and will not fold these legacy runs; a small per-session aggregation is needed.

## Files

- `muninn_policy.py` MuninnPolicy
- `run_bench_ext.py` drop-in `run_bench` wrapper: MUNINN registration, offline Mem0 injection
- `test_muninn_policy.py` offline unit tests
