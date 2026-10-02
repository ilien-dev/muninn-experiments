# Head-to-head v4 — the decisions are also in the code

Pre-registered in `../../PREREGISTRATION.md` ("head-to-head v4"). Same twenty live seeding
sessions per run, same held-out phrasings (`h2h/v2/seed_phrasings.json`), same nine
replacement tasks, same Gate 3 oracles as v1, v2 and v3. What `--code` adds, identically for
every arm: one tracked file per decision in the *seeding* checkout, and a commit that swaps
the value immediately after the message announcing the change, with the subject
`update dependencies` — never naming the new value. Task cells get the base checkout, as in
every other head-to-head: a cell whose repository held the current value would be answerable
by `grep`.

## The registered arms

| arm | replacement pass | retired value written |
|---|---|---|
| claude-mem 13.24.23 | **22/27** | 3/27 |
| muninn-loop8 (`01bf7797`) | **6/27** | 1/27 |

Exact Fisher p = 2.7 × 10⁻⁵. **Muninn lost, and not narrowly.**

## What the same cells say the number is

The decomposition was registered after 16 cells had run and before any further cell was read
for it (`h2h/delivered_vs_used.py`). "Delivered" counts what the hooks injected **and** what
the memory's own tools returned when the agent asked — claude-mem ships an MCP search server,
Muninn allows `muninn why`, and counting only the injection scored four cells where
claude-mem's agent searched its store as "passed without memory".

| arm | used | delivered, not used | passed without memory | not delivered | memory asks / cell | repository looks / cell |
|---|---|---|---|---|---|---|
| claude-mem | 19 | 5 | 3 | 0 | 1.5 | 2.1 |
| muninn-loop8 | 6 | 21 | 0 | 0 | 1.3 | 6.0 |

**Muninn put the current decision in front of the agent in 27 cells out of 27.** The agent
acted on it in 6. The gap is not retrieval, and no amount of improving retrieval moves it.
The last column is the tell: the agent with Muninn went looking in the checkout three times as
often, which is what you do when you do not believe what you were told.

## Three causes, all ours, found by reading those cells

1. **The boot summary forbade the task.** Muninn's own startup note said "Do not … paste
   blocks into files"; every task in this grid is to write the current decision into a file.
   It meant *do not copy a block's header and evidence line into your repository*, and it now
   says that.
2. **A hyphen hid a value from its own decision.** A record's words come from text with
   punctuation stripped (`async std`); the diff's words kept it (`async-std`). They could
   never match, so the commit that replaced async-std with tokio retired nothing and **both
   values were served**. The agent wrote that the decision had been revoked and no replacement
   was recorded — which, given what it was shown, was a reasonable reading.
3. **The `topic:` line restated the retired value.** `topic: backend openssl`, printed under
   "Let's use rustls instead", because the filter that was supposed to keep values out of that
   line only knows values spelled like products. The line is gone; the key still inherits
   every word and is indexed.

## The third arm: the fixes did not help

`muninn-now` — the three causes above fixed, plus five measured engine changes — scored
**4/27** against `muninn-loop8`'s 6/27, exact Fisher p = 0.73. Delivered in 27 cells of 27,
used in 4.

The hypothesis was registered before the arm ran and it is wrong. The three defects were
real and the store the arm seeds is measurably more correct; none of it reaches the answer
the cell writes.

Reading *those* transcripts found something the earlier pass had missed, and it is the first
thing that plausibly explains the size of the gap. Both Muninn arms' agents ask
`muninn why` constantly — 22 and 13 calls across their cells — and act on its one-line
verdict. On a real seeded store that verdict read:

```
sufficient: #11 (commit_linked, trust 2) answers directly
[muninn:decision] #11 · commit c9249e6: update dependencies
  files: config/decisions/revoke-cache-eviction.json
```

The decision itself — `Actually LRU with a 300-second TTL would be better`, trust 3 — was
three lines below. A commit log entry was being reported as the answer because the rule was
"first record of trust ≥ 2". And when nothing of trust 2 matched, the same line said
"insufficient: only circumstantial records (trust < 2); **do not fill the gap**", which an
agent reads as "say nothing is recorded" — and did, with a trust-3 decision in the same
output.

That is the fifth arm, pre-registered before seeding.

## The fourth arm: the instructions were wrong and it did not matter either

`muninn-kinds` — the block kinds the engine actually emits, the skill's count corrected, the
"paste blocks into files" sentence gone from the skill too — scored **7/27**, against
`muninn-loop8`'s 6/27 (exact Fisher p = 1) and `muninn-now`'s 4/27. Delivered in 27 cells of
27, used in 7.

Two registered hypotheses about what Muninn *tells* the agent, both measured, both wrong. The
documents were inaccurate and correcting them changed nothing the cell writes.

## Raw data

`results.jsonl` (one row per cell), `diffs/` (what each cell wrote), `logs/` (each cell's
transcript and the memory's own report), `seeding/` (the twenty sessions per run, with each
arm's settle), `config.json` and `FROZEN.jsonl` (the frozen parameters, one line per launch).
