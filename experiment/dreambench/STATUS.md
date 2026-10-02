# DreamBench-SWE — status (2026-09-13)

DreamBench-SWE (arXiv 2608.20664, `github.com/iroiro147/dreambench-swe`) is the public
multi-session memory-hygiene benchmark for software agents and the closest match to what
Muninn does (`research/00-evidence-log.md` [K2]). Its published lines: no memory 21/180
(11.7 %), literal event memory 82/180, reference probe 83/180, Mem0 literal 97/180 (53.9 %),
v2.1 successor audit, Codex `gpt-5.5` as the agent.

## What a Muninn number would need, and what is not public

Read from the public checkout (`d340bb2`) and the v2.1 release artifact:

- The scored unit is session 3 of a three-session trap, judged by a hidden pytest oracle
  (`experiments/env/oracles/<seq>/s3_test.py`). The oracles are excluded from the public
  package (`scripts/package_artifact.py`). **0 of 180 cells can be scored locally.**
- 25 of the 60 traps start from repository commits that the public `build_env.py` cannot
  regenerate (`load_env.py` maps 5 of the 11 `initial_commit` values). **35 of 60 traps can be
  materialised, none scored.**
- Memory is a harness-side `MemoryPolicy` (`src/benchmarks/baselines.py`): `write(trajectory)`
  after each scored session, `read(task)` → at most 6 items / 1 200 tokens pasted into the
  agent prompt. A Muninn condition is a `MemoryPolicy` subclass registered in
  `run_bench._policy_for_condition` and `run_grid.VALID_CONDITIONS`; Claude Code hooks do not
  take part, and the agent is fixed to Codex `gpt-5.5` in Docker for comparability.
- Statistics: exact sign-flip test paired by trap with Holm correction over a fixed family,
  each condition against a concurrent no-memory baseline (`analyze_confirmatory_v2.py`).

## What is honest to say

No DreamBench-SWE number for Muninn exists and none can be produced without the authors'
private package. The only public subset with executable oracles is the 24-task v0 pilot
(`experiments/env/tasks.jsonl`); a number on it would not be comparable with the paper and is
not reported as one.

## Request to the authors (drafted, not sent)

Sent by the maintainer, not by an automated process. Text in `REQUEST.md`. Asks for:
the reviewer package (`--private`: oracles + reference solutions), the fixture repositories
for the 11 initial commits, the v2.1 synthetic conformance corpus, and a pre-registered slot
for an external `MuninnPolicy` condition run with a concurrent B0 on their infrastructure —
or acceptance of a pull request that adds the policy so they can run it.

## Public pilot run under the benchmark's own harness (2026-09-14; pre-registered)

Four conditions — B0 (no memory), B5 (the harness's literal event memory), B5-MEM0-LIT (Mem0 OSS offline,
`infer=False`), MUNINN (`muninn_policy.py`) — × seeds 1–3 on the 24 public v0 tasks, Codex 0.142.0 in
Docker, `gpt-5.5`. Raw data `results/dbench/` (renamed from `dreambench-public/` to fit Windows path limits; old to new paths in `results/RENAMES.tsv`).

**The grid stopped on the ChatGPT plan's usage limit** at 10:18 UTC: every later session failed with
"You've hit your usage limit" (`agent_error`). Complete runs (24/24 sessions `completed`):

| condition | seed | sessions passed |
|---|---|---|
| B0 | 1 | 24/24 |
| B0 | 2 | 24/24 |
| MUNINN | 1 | 24/24 |
| B5 | 1 | 23/24 |

Every other run is partial or empty because of the limit (B5, B5-MEM0-LIT, MUNINN seeds 2–3, B0 seed 3,
B5-MEM0-LIT seed 1; the first B5-MEM0-LIT seed-1 attempt had crashed at start on an uncached embedding
model and was re-run, then hit the limit).

**Verdict by the pre-registered rule: not discriminating.** The rule required B0 below 90 % of sessions for
any contrast to count; B0 passed 48/48 (100 %). On this subset the agent solves every session without
memory — each session starts from the previous session's reference solution and the failing test is in
the checkout — so no memory condition can show an effect, positive or negative. The partial runs were not
re-run: more sessions cannot move a contrast the rule already declares uninformative. Nothing is claimed
from this grid beyond "Muninn runs as a `MemoryPolicy` inside DreamBench's harness without errors (24/24
completed sessions)". The confirmatory 60 traps still require the authors' private oracles (`REQUEST.md`).
