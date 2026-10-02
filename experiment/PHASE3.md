# Phase 3 — real engine: acceptance (measured 2026-09-13)

Plan acceptance: the literal arm re-run on the real engine is not inferior to the
throwaway store; a real session ingests in < 500 ms; hook p95 < 10 ms at ≥ 20 000
records; fault injection 100 %.

## Literal arm on the real engine (`results/run3-literal-real-engine/`)

Same seed, tasks, oracles, model and base_ref as Gate 2 run 2; only the engine changed
(typed capture, chunked long turns, passage selection, boot block with the trust scale,
Markdown projection, embedding sidecar on the write path).

| | throwaway store (run 2, literal) | real engine (run 3, literal) |
|---|---|---|
| non-inferable pass | 19/25 | 21/25 |
| stored records per cell | 82 | 87 (82 episodes + 3 corrections + 1 invariant + 1 dead end) |
| delivered tokens · records (mean) | 627 · 3.5 | 666 · 3.8 |
| turns · wall time · cost (mean) | 12.5 · 49 s · $0.245 | 10.0 · 46 s · $0.218 |
| UserPromptSubmit p95 per cell: median · max | 1.00 · 1.36 ms | 1.21 · 33.8 ms |

Per task (real engine): s12 5/5, userprompt-p95 5/5, sessionstart-gate 5/5,
corpus-fetch-limits 5/5, real-transcript-ingest 1/5 (the "measure it" wording again).
Not inferior: +2 cells. Not a new gate result — one arm, no control, reported for the
acceptance criterion only.

The 33.8 ms outlier (3 of 25 cells above 10 ms) is the first prompt of a fresh cell
racing the detached `maintain` that embeds the whole seeded store (model load 52 ms +
87 vectors) with three cells running in parallel on one machine. The read hook never
waits on the writer (WAL), so this is CPU contention, not a lock; a warm store shows the
1.2 ms median. Recorded as a known cost of the first session after install.

## Write path

| measurement | value |
|---|---|
| real 22 MB transcript (36 turns) → 87 records + 87 Markdown files + index | 43 ms |
| `muninn maintain` (fold, resume, git capture 3 commits + 1 revert, project) | 2–4 ms |
| embedding: model load · encode 91 records · encode 200 texts | 52 ms · 8.2 ms · 8.5 ms |
| exact kNN, 1 000 repetitions of one query | 1 000/1 000 identical, 0.038 ms/query |
| recall@10, self-retrieval (73 queries): lexical · vector · hybrid RRF | 1.000 · 0.644 · 1.000 |
| binary (with tokenizer, no hub client) | 7.0 MB |

Sidecar sub-gate (plan, Phase 3 §10): "on by default only if it raises recall@10 over
lexical without breaking bit identity". Bit identity holds. On self-retrieval lexical is
already at 1.000, so the sidecar adds nothing measurable here; a paraphrase set is
needed to see the +2.8 pp the literature reports [H4]. Decision: the sidecar stays
**off the read path by design** and feeds only `muninn why` (Phase 4), where its
contribution will be measured on that responder's sufficiency, not here.

## Read path at scale (`muninn-bench perf`, 200 runs)

| store | SessionStart p95 | UserPromptSubmit gated p95 | full p95 | cue ancestor p99 | ingest 200 |
|---|---|---|---|---|---|
| 5 000 records / 15 000 cues (strict, all limits met) | 2.4 ms | 0.75 ms | 1.86 ms | 1.8 ms | 6.8 ms |
| 20 000 records / 30 000 cues | 2.1 ms | 0.86 ms | 3.5 ms | 5.1 ms | 6.1 ms |

The cue evaluator is still the Phase 0 bench prototype; 5.1 ms p99 at 30 000 cues is
above the 3 ms contract set for 15 000 and is the Phase 5 baseline, not a regression.

One regression was caught and fixed by this measurement: with `maintain` spawned on
every SessionStart, 200 starts fanned out into 200 concurrent embedders and the gated
hook p95 went from 0.75 ms to 41 ms. It is now one writer (exclusive lock) at most once
per two minutes.

## Fault injection

15 scenarios × 20 repetitions, all green: the original 11 plus model checksum mismatch
(sidecar cold, nothing else changes), git unavailable, `maintain` and `Stop` ingesting
the same transcript concurrently (no loss, no duplicate), one 200 KB turn. Found and
fixed: a log symlinked to `/dev/full` hung both the detached writer and the SessionEnd
hook — log folds now read regular files only, bounded to 64 MB.

## What Phase 3 did not do

- `claim` records (agent_inferred, trust 0): no reliable extractor without a model; the
  kind exists and is served with an explicit frame, nothing produces it yet.
- Review comments as `correction` → `invariant` (review_accepted): deferred, needs an API.
- PostToolUse still writes nothing (turn context is Phase 5).
- Codex replication of Gate 2: the runner now drives `codex exec` with the same hooks;
  the run itself is pending.
