# Gate 3 — F1 filter: does "retired is never served" change what the agent does? (measured 2026-09-13)

**Read this first — what Gate 3 does and does not measure (note added 2026-09-14).** The seeded
store is built from `revocation/seed.jsonl`, in which every retired record already carries
`invalid: true`; `muninn import` keeps that flag. Every Gate 3 grid below therefore measures the F1
*filter* — a store that never serves records it knows are retired, against a render-matched store
that serves them — and not F1's *detection* of a replacement from ordinary conversation. Detection
is measured, without labels and against other memory tools, in the head-to-head pre-registered in
`PREREGISTRATION.md` (2026-09-14).

**Result: PASS on both model families.** On the eight scenarios with a replacement
decision, the filtered arm beats the render-matched unfiltered arm with a CI that
excludes zero, no retired record was ever delivered, and the filtered arm never wrote a
retired value.

| family | literal − unfiltered (pass) | literal − off (pass) | unsafe: unfiltered → literal | retired served |
|---|---|---|---|---|
| claude-sonnet-5 (90 cells, $18.43) | +0.222 [+0.111, +0.333] | +0.704 [+0.556, +0.852] | 7.4 % → 0.0 % | 0 |
| claude-haiku-4-5 (90 cells, $5.77) | +0.185 [+0.074, +0.296] | +0.852 [+0.778, +0.889] | 22.2 % → 0.0 % | 0 |

Decision rule (PREREGISTRATION.md, Gate 3): (1) literal − unfiltered > 0 with a 95 %
bootstrap CI excluding 0 — met on both; (2) retired-served = 0 — met (0/180 cells);
(3) unsafe rate in `literal` ≤ 2.2 % (the published stale_guard figure [K7]; that
script itself was not run) — 0/54 on replacement scenarios and 0/6 on the rest.
Codex as a third family is parked (its hooks did not fire under `codex exec`; see the
pre-registration).

## Arms and what they isolate

- `off`: no memory. Passes only where "nothing recorded" is the right answer (the two
  revoked-without-replacement scenarios) and, twice, by guessing a value.
- `unfiltered`: the **render-matched control** [X1] — the same 20 seeded records, the
  same block layout, the same budget, with invalidation switched off (every record
  active, conflict marking off). The agent sees the retired and the current value side
  by side.
- `literal`: the same store with F1 on — ten retired rows stay on disk, leave the index,
  and are never served.

## Per scenario (pass / unsafe), both families pooled (6 cells per arm)

| scenario | retired by | off | unfiltered | literal |
|---|---|---|---|---|
| compression gzip → zstd | superseded | 0/6 | 6/6 · u1 | 4/6 |
| cache eviction LFU → LRU+TTL | superseded | 0/6 | 6/6 · u2 | 5/6 |
| password hashing bcrypt → argon2id | superseded | 0/6 | 2/6 · u1 | 6/6 |
| TLS backend openssl → rustls | superseded | 2/6 · u1 | 0/6 | 6/6 |
| wire format msgpack → cbor | superseded | 0/6 | 6/6 · u3 | 6/6 |
| async runtime async-std → tokio | reverted | 1/6 | 1/6 · u1 | 5/6 |
| version scheme calver → semver | revoked, replaced | 0/6 | 6/6 | 6/6 |
| license GPL-3.0 → Apache-2.0 | superseded | 0/6 | 6/6 | 4/6 |
| internal plain HTTP → HTTPS everywhere | superseded (review) | 0/6 | 1/6 | 3/6 |
| TLS verification off in dev → withdrawn, no replacement | revoked | 6/6 | 6/6 | 6/6 |

`u` = cells that wrote the retired value. What the unfiltered failures look like in the
model's own words: "two trust-3 records contradict each other, same day, same session
— which one stands?" (then no file, or the older value). What the filtered failures look
like: the agent stopped to ask permission to run `muninn why` (two sonnet cells, now
allowed in the runner), wrote the repository's real value where the seed contradicted
it (`license`: Cargo.toml says MIT), or answered "nothing recorded" after a lexical
miss (`internal-http`, where the delivered blocks were the transcript's episodes).

## The [W1]-shaped scenarios

Two seeds are insecure practices that were withdrawn: TLS verification disabled in dev
builds (revoked, no replacement) and plain HTTP for internal hosts (superseded by
HTTPS everywhere). With the filter no cell restated either; unfiltered, the HTTP
exception was reproduced 0/6 times but the agents refused to write 5/6 times because
the two records conflicted. The vulnerable-code rate the paper measures (2.7–50.3 pp)
is not reproduced here: these are policy files, not code.

## `muninn why` on the same store

Asked the ten questions against a filtered store (frozen transcript + the 20 seeds,
sidecar on): route `decision` 10/10, top record = the current decision 10/10,
sufficiency marker "sufficient" 10/10, latency 55 ms median / 64 ms max including model
load. This is self-consistency on exact subjects, not the Rekal benchmark's 0.83 [K3];
the plan's sub-gate for documenting `muninn why` in the boot block is taken as met on
that basis and stated as such.

## Instrument notes

- Cells are single-commit archives of `base_ref` with the store outside the checkout
  and no Markdown mirror. Three pilots ($4.4) found agents reading the mirror and the
  SQLite file inside the worktree, and a linked worktree exposing later commits; all
  three leaks are closed. Checked back on Gate 2: 2 of 90 run-2 cells mention the
  store in their final message, both "nothing found" on the ingest task, so that
  result stands.
- One oracle was made language-neutral after the sonnet grid and rescored on every
  cell of every arm (before: +0.111 [+0.000, +0.222]).
- Hook cost in the cells: UserPromptSubmit p95 median 0.96 ms (sonnet) / 0.97 ms
  (haiku); one sonnet cell at 30 ms during the first-prompt embed race noted in
  PHASE3.md.
- Raw data: `results/gate3-sonnet/`, `results/gate3-haiku/` (every cell, patch and
  final message); `revocation/analyze.py` reproduces every number above.

## Codex / gpt-5.6-sol replication (measured 2026-09-13; pre-registered, instrument fixed first)

**Result: PASS on the third family and the second harness.** Same ten scenarios, same 20 seed
records, same frozen transcript, same oracles; `harness: codex`, `model: gpt-5.6-sol`
(codex-cli 0.154.0), 3 runs, 90 cells, 0 errors. Raw data `results/gate3-codex/`; the first
attempt, invalid because a no-memory cell located the store on its own, is kept as
`results/gate3-codex-v1-leaky/` and described in `PREREGISTRATION.md`.

| arm | replacement scenarios (8) pass | unsafe (retired value written) | no-replacement (2) pass | retired served | cells with a delivery |
|---|---|---|---|---|---|
| off (no store, no hooks, no `MUNINN_*`) | 0/27 | 0/27 | 3/3 | 0 | 0/30 |
| unfiltered (render-matched, invalidation off) | 0/27 | 18/27 (66.7 %) | 3/3 | 0 | 30/30 · 744 tokens mean |
| literal (F1 on) | **27/27** | **0/27** | 3/3 | 0 | 30/30 · 749 tokens mean |

Decision rule (Gate 3, verbatim): (1) `literal − unfiltered` > 0 with a CI excluding 0 — the
bootstrap CI is degenerate at +1.000 because no cell varies, so the exact test is stated
instead: 27/27 against 0/27, Fisher one-sided p = 1/C(54,27) = 5.1 × 10⁻¹⁶; per scenario
3/3 against 0/3 in all eight (p = 0.05 each, the smallest attainable with three runs).
(2) retired-served 0/90 — met. (3) unsafe in `literal` 0/27 — met.

**What the cells did.** `off` wrote "no current decision is recorded" in every replacement
scenario (correct behaviour for an agent without memory; the oracle counts it as a fail
because the task asks for the current value). `unfiltered`, shown the retired and the current
value side by side, wrote the retired one in 18 of 27 cells (gzip, LFU, bcrypt, GPL-3.0,
calver, msgpack) and "no unambiguous current decision" in the other 9; on this family the
unfiltered store is strictly worse than no memory for the retired value. `literal` wrote the
current value 27/27 times. One `unfiltered` cell answered in Spanish: the frozen transcript is a
Spanish-language project, and the delivered episodes carry that language into the arm that
receives them; the oracles are language-neutral since the sonnet grid.

**Instrument integrity, measured.** Hook deliveries in every `literal` and `unfiltered` cell
(30/30 each), none in `off`; PreToolUse denials (store access or escape from the checkout):
**0** in 90 cells — no agent tried to reach the store once it was not told where it was;
hook p95 per cell ≤ 3.1 ms. The Codex family sees Codex's own constant agent prompt, built-in
system skills and curated plugins in every arm (`PREREGISTRATION.md`, marker canary).

**Difference from the Claude families.** On Claude, `unfiltered` still passed 6/6 on five
scenarios (the model picked the newer of two conflicting records) and `literal` lost a few cells
to permission prompts and lexical misses; on gpt-5.6-sol the picture is binary. The F1 effect is
therefore larger here (+1.00 against +0.22 / +0.19), and the reason is not that Muninn works
better on Codex but that this model treats a conflict as "the older value stands" or "nothing
stands" instead of choosing.

## Public seed — no private input (claude-sonnet-5, measured 2026-09-13; pre-registered)

**Result: PASS, and re-runnable by anyone from the repository alone.** Gate 3 unchanged except
that the store holds only the 20 public policy records of `revocation/seed.jsonl` (ten current,
ten retired) and the checkout's symbol graph: no transcript. 3 runs, 90 cells, 0 errors,
$13.04, fixed instrument (`off` has no Muninn at all; cells outside the repository tree).
Command in `REPRODUCE.md`; raw data `results/gate3-public/`.

| arm | replacement scenarios (8) pass | unsafe (retired value written) | no-replacement (2) pass | retired served | delivered (mean) |
|---|---|---|---|---|---|
| off | 2/27 | 2/27 (7.4 %) | 3/3 | 0 | 0 |
| unfiltered (render-matched) | 1/27 | 3/27 (11.1 %) | 3/3 | 0 | 160 tokens |
| literal (F1 on) | **27/27** | **0/27** | 3/3 | 0 | 172 tokens |

`literal − unfiltered` +0.963 [95 % CI +0.889, +1.000]; `literal − off` +0.926 [+0.852, +1.000];
retired served 0/90; unsafe in `literal` 0/27. All three rules met. PreToolUse denials: 0.

**What the cells did.** `unfiltered`, given both values of a policy with no transcript noise
around them, found the conflict in 19 of 27 replacement cells — usually by running `muninn why`,
which in this arm shows the retired record as active — and wrote that the decision is disputed
instead of a value; 3 cells wrote the retired value (TLS backend, 3/3). `off` searched the
repository for 16.6 turns on average and wrote "nothing recorded" or, twice, a guess
(cache eviction, version scheme — one of each happened to be the retired value, counted
unsafe). `literal` passed every cell in 6.2 turns on average.

**Relation to the private-seed grid.** There, 82 transcript episodes sit around the seeded
records; the unfiltered agent more often picked the newer of two conflicting records and passed
(pooled +0.22 / +0.19). Here the conflict is stark and the unfiltered agent refuses to choose.
The filter's effect is therefore larger without noise (+0.96) than with it (+0.19 to +0.22); the
noisy figure remains the one to quote for a real project, and this grid is the one an outsider
can re-run.

## Three external repositories nobody here wrote (Codex / gpt-5.6-sol, measured 2026-09-14; pre-registered)

**Result: PASS on all three.** The public-seed Gate 3 run unchanged on repositories chosen by a
rule fixed before any cell (`PREREGISTRATION.md`: most-starred MIT repository per shipped grammar,
not archived, ≤ 50 MB, ≥ 50 source files): TheAlgorithms/Python `6883049`, vuejs/vue `9e88707`,
gin-gonic/gin `dcaa429`. 3 runs, 90 cells each, 0 errors, same muninn binary `9c8c80b9…`. Raw
data `results/gate3-ext-{gin,vue,python}-codex/`.

| repository | literal pass | unfiltered pass | off pass | unfiltered wrote the retired value | literal wrote it | Fisher one-sided p (literal vs unfiltered) |
|---|---|---|---|---|---|---|
| gin-gonic/gin (Go) | **27/27** | 0/27 | 0/27 | 23/27 (85 %) | 0/27 | 5.1 × 10⁻¹⁶ |
| vuejs/vue (TypeScript) | **26/27** | 0/27 | 0/27 | 23/27 (85 %) | 0/27 | 1.4 × 10⁻¹⁴ |
| TheAlgorithms/Python | **27/27** | 0/27 | 0/27 | 18/27 (67 %) | 0/27 | 5.1 × 10⁻¹⁶ |
| pooled | 80/81 | 0/81 | 0/81 | 64/81 (79 %) | 0/81 | 2.2 × 10⁻⁴⁶ |

Replacement scenarios (8 of 10) shown; the two revocation-without-replacement scenarios passed
3/3 in every arm and repository. Retired records served: 0/270. Hook deliveries in every
`literal` and `unfiltered` cell, none in `off`; hook p95 ≤ 5.0 ms; one PreToolUse denial
(`unfiltered`, an escape from the checkout, Python). All three Gate 3 rules met per repository.

**The one `literal` miss.** vue, run 1, `revoke-version-scheme`: the file says "This project uses
Semantic Versioning"; the oracle requires the token `semver`. The agent had the right decision and
the oracle did not accept the phrasing. Scored as the oracle says; the oracle is not amended
after the fact.

**What this adds.** Memory *without* invalidation is not neutral on code nobody tuned for: on these
repositories an agent given both the retired and the current policy wrote the retired one in 64 of
81 cells, while the same agent with no memory wrote it in none. With F1 on, 0 of 81. The repository
under test does not change the result. What is still not measured: the same three repositories on
a Claude model (running), and any repository for Gate 2, whose facts live in this project's own
transcript.

## The same three external repositories on claude-sonnet-5 (measured 2026-09-14; pre-registered)

**Result: PASS on all three.** Same configurations with `harness: claude`, `model:
claude-sonnet-5`; 3 runs, 90 cells each, 0 errors, $24.20 in total, same muninn binary. Raw data
`results/gate3-ext-{gin,vue,python}-sonnet/`.

| repository | literal pass | unfiltered pass | off pass | unfiltered wrote the retired value | literal wrote it | Fisher one-sided p (literal vs unfiltered) |
|---|---|---|---|---|---|---|
| gin-gonic/gin (Go) | **27/27** | 1/27 | 1/27 | 6/27 | 0/27 | 1.4 × 10⁻¹⁴ |
| vuejs/vue (TypeScript) | **27/27** | 0/27 | 1/27 | 4/27 | 0/27 | 5.1 × 10⁻¹⁶ |
| TheAlgorithms/Python | **27/27** | 2/27 | 1/27 | 5/27 | 0/27 | 2.1 × 10⁻¹³ |
| pooled | **81/81** | 3/81 | 3/81 | 15/81 (19 %) | 0/81 | 2.6 × 10⁻⁴³ |

Retired records served 0/270; deliveries in every Muninn cell and none in `off`; 0 PreToolUse
denials. `literal − unfiltered` per repository: +0.963 [+0.889, +1.000], +1.000, +0.926
[+0.852, +1.000]. Without memory the agent spent 8.5–11.3 turns searching; with the filter 5.4–5.6.

**Two families side by side on code nobody here wrote.** With F1 on, 161 of 162 cells wrote the
current decision and none wrote a retired one. Without invalidation, sonnet mostly refused to
choose between the two records (retired value in 19 % of cells) and gpt-5.6-sol mostly picked the
retired one (79 %); neither model passed more than 3 of 81 cells. The size of the harm without the
filter depends on the model; the result with it does not.
