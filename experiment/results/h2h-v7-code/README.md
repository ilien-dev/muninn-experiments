# Head-to-head v7 — the registered replication

Pre-registered in `../../PREREGISTRATION.md` ("v7: the replication, at a size that can answer
the question"), before any cell ran: six runs, 54 replacement cells per arm, a fresh output
directory with its own seeding, one analysis when all 180 cells were in.

## The fixture

Each decision exists in the conversation *and* in the code. The seeding sessions run in a
checkout that holds one tracked file per decision and commits the swap with the uninformative
subject `update dependencies`. The task cell gets **that checkout's own history**, with one
further commit taking `config/decisions/` out of the working tree — so every commit a record
cites resolves where the agent stands, no file holds the current value, and `git log -p` still
reveals it to an agent that goes looking. That last point is why `off` runs as a registered
arm.

## Result

| arm | replacement pass | retired value written |
|---|---|---|
| **muninn-catalog** | **41/54** | 4/54 |
| claude-mem 13.24.23 | 21/54 | 4/54 |
| off (no memory) | 1/54 | 3/54 |

- **Registered primary contrast, exact Fisher two-sided: p = 1.85 × 10⁻⁴.** Threshold α = 0.05,
  fixed before the data. Met.
- Fixture valid by its own control: `off` 1/54 against an invalidating threshold of 12/54.
- It replicates v6's 23/27 on a fresh grid: 41/54.

## Where the difference comes from

| | muninn-catalog | claude-mem |
|---|---|---|
| used | 41 | 19 |
| delivered, not used | 13 | 27 |
| passed without memory | 0 | 2 |
| not delivered | **0** | 6 |
| repository looks / cell | 4.7 | 4.9 |

Six grids before this one delivered the current decision in 27 cells of 27 and the agent acted
on it in 4 to 9. Five of those grids changed what the block said; none moved it. What moved it
was `[muninn:catalog]` — one line per record on the books, once per session, with `replaces #n`
— and `muninn show <id>` to pull one in full. An agent handed a filtered selection cannot tell
a memory that holds nothing about a subject from a query that missed it.

## What it costs

Median injected context, paired by (run, task): **2.587 [2.489, 2.693]** times claude-mem's.
The worst any arm has recorded. It excludes `hook_system_message`, which claude-mem uses
heavily and Muninn does not, so the real window comparison is kinder than this figure; it is
reported the unkind way. v8 tests whether the boot summary's 1 768 characters are load-bearing.

## What it is not

One benchmark, one fixture, one competitor at one version, 54 cells an arm. It says that on
this task — a decision replaced in conversation and in the code, asked about later in wording
neither memory has seen — Muninn is better at getting the agent to act on the current answer.
It says nothing about the other things a memory is for.

## Raw data

`results.jsonl` (one row per cell), `diffs/` (what each cell wrote), `logs/` (each cell's
transcript and the memory's own report), `seeding/` (the twenty sessions per run per arm),
`config.json` and `FROZEN.jsonl`.
