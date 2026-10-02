# Gate 4 — F3: cue-anchored delivery, compaction survival, PM-Bench (measured 2026-09-13; PM-Bench rounds 4–5 the same day)

Gate 4 has three conditions. Two are measured below; the third (PM-Bench) is measured
in the same document once its replicate runs finish.

## §1 Cues vs lexical-only (`results/gate4-cues/`): NOT DISTINGUISHABLE — condition not met

Eight decisions anchored to eight files (one per crate), each naming a token absent
from the repository; one task per file, naming the area but never the file; the record
shares as few words as possible with the task. claude-sonnet-5, 3 runs, 96 cells,
$28.03, 0 errors (one control cell first recorded as an error was the agent running out of turns, now scored as a fail; `PREREGISTRATION.md`, 2026-09-14).

| arm | pass | cells where a dir/symbol cue fired | tokens delivered (mean) |
|---|---|---|---|
| off | 0/24 | — | 0 |
| lexical (cues off) | 12/24 | 0 | 609 |
| literal (cues + lexical, tool-time delivery on) | 14/24 | 15/24 | 1 187 |
| control (length-matched irrelevant) | 2/24 | 0 | 1 039 |

| contrast | point | 95 % bootstrap CI |
|---|---|---|
| literal − lexical | +0.083 | [−0.083, +0.250] |
| literal − off | +0.583 | [+0.458, +0.708] |
| lexical − off | +0.500 | [+0.375, +0.625] |
| control − off | +0.083 | [+0.000, +0.167] |

Pre-registered rule: literal − lexical > 0 with a CI excluding 0. The CI includes 0.
Lexical recall of the prompt already finds the anchored record in half the cells (the
rewritten prompts still share enough vocabulary with the records); the cues fired in 15
of 24 literal cells and added two passes. The length control gains +0.083 with a lower
bound at exactly 0, so part of the literal arm's extra 580 tokens per cell is length.

*Note added 2026-09-14:* in this grid the `control` agent could run `muninn why` against the
real store (only prompt delivery used the foreign store; `PREREGISTRATION.md`, Gate 2 on Codex).
The control arm passed 2/24, so any such leak inflated the control, not the literal arm; the
figures stand and the runner is fixed for later grids.

Consequence, as the plan states it: F3 ships as reinjection on compaction and at
session start (event cues, §2) plus lexical recall; dir/symbol cue delivery at prompt
and tool time stays in the engine, measured, **off by default** (`muninn init --cues`,
`muninn config cues on`, or `MUNINN_CUES=1`). The experiments keep measuring the full
mechanism (`MUNINN_CUES=1` in every arm with Muninn).

What would change the verdict: a repository whose files carry decisions that the
prompt vocabulary cannot reach — the case F3 was designed for — or more runs (the point
estimate is positive). Neither was available here; this grid used this repository and
three runs.

### §1, second grid — query expansion through the symbol graph (`results/gate4-cues-v2/`)

Post-gate change: the read hook adds to the lexical query the definitions of files
whose path contains a prompt word (`expand_terms`), so "the embedding crate" reaches a
record that only says `embed_pending`. Pre-registered in `PREREGISTRATION.md` (after
launch, before any result was read). Same eight tasks and seed, claude-sonnet-5,
3 runs, 72 cells, $17.57, 1 error re-run; cells confined by a PreToolUse deny.

| arm | pass | tokens delivered (mean) | turns (mean) | cost/cell |
|---|---|---|---|---|
| lexical-plain (no cues, no expansion) | 10/24 | 503 | 10.5 | $0.231 |
| lexical (no cues, expansion) | 13/24 | 522 | 12.0 | $0.260 |
| literal (cues + expansion) | 15/24 | 741 | 11.0 | $0.242 |

| contrast | point | 95 % cluster-bootstrap CI (by task) |
|---|---|---|
| lexical − lexical-plain | +0.125 | [+0.000, +0.292] |
| literal − lexical | +0.083 | [−0.083, +0.292] |
| literal − lexical-plain | +0.208 | [−0.042, +0.417] |

Per task, expansion turned `cue-busy-cap` 0/3 → 2/3 and `cue-azure-pattern` 1/3 → 2/3;
the other six are unchanged. Retired records served: 0. The lower bound sits at
exactly zero, so by the rule it ships as an **opt-in** (`muninn config expand on`,
`MUNINN_EXPAND=1`) and the experiments keep it on in the arms that name it. Cues on
top of expansion repeat the first grid's figure (+0.083); the verdict on cues stands.

### Boot-block vehicle — file vs SessionStart hook (`results/boot-vehicle/`)

The shipped default stopped writing the boot block into the user's CLAUDE.md /
AGENTS.md: the SessionStart hook injects a compact summary (~425 estimated tokens,
`plugin/templates/BOOT.hook.md`) at startup, resume, clear and after compaction, and
the `muninn` skill carries the long form. Pre-registered as a non-inferiority test
(`PREREGISTRATION.md`), 14 tasks (Gate 2's six plus the eight cue tasks), 3 runs,
84 cells, claude-sonnet-5, 0 errors.

| arm | pass | tokens delivered (mean) | turns (mean) | cost/cell |
|---|---|---|---|---|
| literal (long block in CLAUDE.md, as in every gate) | 30/42 | 782 | 10.3 | $0.233 |
| literal-hookboot (no file; compact summary by hook) | 35/42 | 776 | 10.9 | $0.239 |

`literal-hookboot − literal`: **+0.119 [95 % CI +0.000, +0.262]** (cluster bootstrap by
task). Not inferior; if anything better: three cue tasks moved from 1/3 to 2–3/3 with
the summary arriving as the first thing in the session instead of inside the
instruction file. Retired records served: 0. The hook vehicle stays the default;
`muninn init --boot-file` remains for users who want the block in the file.

## §2 Compaction survival (decay probe): 100 % at 10 invariants; the budget holds 16

Reproducible in one command, no model: `python3 crates/muninn-bench/experiment/decay_probe.py
--reps 100` (`results/decay-probe/`). Ten invariants seeded, 100 forced compactions (the
`PreCompact` then the `PostCompact` hook, fed the harness's JSON): **100/100 compactions
delivered all ten** (1000/1000 facts); PostCompact 1.17 ms median, 1.64 ms p95, 1.84 ms max
per hook, process spawn included (commit `8d06b48`). Published without-harness figure:
106/108 losses [K1]; constraint violations 30–59 % after compaction, 0 % when the constraint
survives [C2]. The without-Muninn line is cited, not re-measured.

**Where it stops.** The same probe at 20, 40 and 80 invariants delivered **16** every time
(320/400 facts at 20; `results/decay-probe/inv20..80/`): reinjection runs under the
700-token turn budget, which holds 16 invariants of this probe's size (~30 tokens each with
the block header). Before this probe the rest vanished without a trace; since commit
`6e1cadb` the PostCompact text ends with `[muninn:gated] N more invariant/correction record(s)
exist but did not fit the 700-token turn budget; run muninn why <topic> before assuming a rule
is absent`. The budget itself is a design decision (`design/ENGINE.md`) and is not moved by
this finding; what changed is that the agent is told when it applies. The public sentence is
therefore: invariants survive compaction as long as they fit the turn budget, and the hook
says when they do not.

## §3 PM-Bench [V1]

Setup: the released benchmark (`genglinliu/PMBench`, v9 week, 80 steps) run against
claude-sonnet-5 through an OpenAI-compatible bridge over `claude -p`
(`pmbench/claude_bridge.py`, temperature 0, 256 max tokens); three scaffolds: the
paper's `single_baseline`, its `todo_ledger`, and `muninn_ledger`
(`pmbench/run_muninn_ledger.py`: the same ledger, persisted as Muninn records with
`after`/`keyword` cues on the simulated clock, and at each step the fired intentions
injected as DUE NOW on top of the ledger). Line to beat: 65.1 % set-F1 (the paper's best,
a GPT-5.4 agent).

Round 1 (one run each, first scaffold version that replaced the ledger view with the
fired items):

| scaffold | hit | set precision | set recall | set F1 |
|---|---|---|---|---|
| single_baseline | 49.4 % | 74.1 % | 49.4 % | 59.3 % |
| todo_ledger | 48.1 % | 86.7 % | 48.1 % | 61.9 % |
| muninn_ledger (v1) | 44.4 % | 73.5 % | 44.4 % | 55.4 % |

Round 2 (`muninn_ledger` v2 keeps the full ledger view and adds the fired items on top;
two more runs of each baseline; one baseline run crashed inside the benchmark's own
parser on an odd model reply and is excluded):

| scaffold | runs | set F1 per run | mean |
|---|---|---|---|
| single_baseline | 3 | 59.3 · 58.2 · 65.1 | 60.9 % |
| todo_ledger | 3 | 61.9 · 66.2 · 57.4 | 61.8 % |
| muninn_ledger v2 | 3 | 63.0 · 58.6 · 60.3 | 60.6 % |
| muninn_ledger v1 (ledger view replaced) | 1 | 55.4 | — |

Round 3 (`muninn_ledger` v3, exploratory, not pre-registered: the fired items moved
from the ledger message to the head of the step message, for recency; three runs,
same bridge, `claude -p` now run in a bare directory so no project settings or store
reach the model under test):

| scaffold | runs | set F1 per run | mean | set recall | set precision |
|---|---|---|---|---|---|
| muninn_ledger v3 (DUE NOW next to the step) | 3 | 55.3 · 55.9 · 59.7 | 57.0 % | 40.7–45.7 % | 81.0–89.2 % |

Worse than v2 by 3.6 points on the mean, with recall down (v2: 48–49 %) and precision
up: next to the step, the fired list narrows what the model acts on instead of adding to
it. The scaffold shipped is v2; v3 is kept only as this row (`results/pmbench/v3/`).

Run-to-run spread on this model is ±4 points at temperature 0, larger than any
difference between scaffolds. **Condition not met**: no scaffold reaches 65.1 % on
average, and the Muninn scaffold is not distinguishable from the paper's own ledger.
What the week exercises is the model's own intention discipline (the JSON ledger it
rewrites each step); Muninn's trigger delivery fired correctly (DUE NOW blocks appear
on every due step in the prompt logs) and did not change the outcome. Raw data:
`results/pmbench/` (score logs and trajectories; `pmbench/` has the bridge and the
scaffold to reproduce them).

## §3 rounds 4–5 — Muninn as the intention store (measured 2026-09-13)

Pre-registered in `PREREGISTRATION.md` ("round 4", "round 5") before any cell ran. Two
findings on the round 1–3 data motivated the rounds:

- **The round 1–3 bridge leaked the user's global `~/.claude/CLAUDE.md`** to the model under
  test (`claude -p` without `--setting-sources ""`; probe answer through the old bridge:
  "Svipall para acceso web; respuesta en español"; the round-2 ledger notes are in Spanish).
  All eleven earlier runs share it. The round-4 bridge passes `--setting-sources ""` (probe:
  "NONE", 527 input tokens) and both baselines were re-measured through it.
- **The v1–v3 scaffold read hidden fields** (`step["time"]`, `step["cues"]`) into the store.
  The round-4 scaffold reads only what the model can see (day plan, vignette, options, step
  menu, and the replies to the `check_time` / `query_state` actions it issues).

**Scaffold** (`pmbench/run_muninn_pis.py`, arm `muninn_store`). The model no longer owns a
ledger. Intentions are typed records in a Muninn store (`after` cues for day and clock,
`keyword` cues for channels); lifecycle is code: add / reschedule / override / cancel / done,
daily re-arm of regular intentions, day-scoped carry of cross-day intentions, same-day expiry.
Per step: one **Form/Revise** call (new text → typed ops), code-issued **observation**
(`check_time` while a time intention is pending; while any intention watches a channel, one
`query_state` per channel), **Filter** = `muninn cues --ungated` with the fake clock set from
the queried time, one **Decide** call (eligible board → menu handles). A clock-matched time
intention the model omits would be added by a token-overlap guard; it never fired (0 events in
6 runs). Round 5 changed one rule: a channel-kind intention is eligible only when some channel
reply is new information (not "(no updates)" and different from that channel's previous reply
the same day). Design after PIS `[V2]`; prompts unchanged between rounds.

**Results** — claude-sonnet-5, temperature 0, isolated invocation, the released v9 week (80
steps, 81 due items), 3 runs per arm:

| arm | set F1 per run | mean (sd) | cross-day miss | update miss | time-modality hit | proactive-monitoring hit | FA/step |
|---|---|---|---|---|---|---|---|
| single_baseline (PM-Bench's own) | 79.7 · 76.7 · 77.2 | **77.9 (1.6)** | 0.0 % | 40.7 % | 70.8 % | 44.4 % | 7.5 % |
| todo_ledger (PM-Bench's own) | 78.3 · 80.0 · 81.1 | **79.8 (1.4)** | 9.5 % | 33.3 % | 63.9 % | 39.3 % | 2.5 % |
| muninn_store, round 4 | 96.2 · 96.2 · 92.4 | **94.9 (2.2)** | 0.0 % | 11.1 % | 100 % | 96.6 % | 2.9 % |
| muninn_store, round 5 | 96.2 · 95.7 · 96.9 | **96.3 (0.6)** | 0.0 % | 11.1 % | 100 % | 100 % | 1.7 % |
| muninn_store, round 6 (negative) | 95.0 · 95.7 · 95.6 | 95.4 (0.4) | 0.0 % | 11.1 % | 100 % | 94.9 % | 3.4 % |
| muninn_store, round 7 (ships) | 95.7 · 97.5 · 96.9 | **96.7 (0.9)** | 0.0 % | 14.8 % | 100 % | 97.4 % | 2.1 % |

Lines from the literature: 65.1 % (the paper's best scaffold, a GPT-5.4 agent `[V1]`) and
82.9 % (PIS on DeepSeek-Chat `[V2]`). Both are other models; PIS's code is not released, so it
was not run on claude-sonnet-5. The within-model comparison is the two rows above.

Where the points come from, on the round-5 traces: all 39 due items that need a channel
query (24 clock, 15 hidden channels) are hit in every run; the remaining errors (4 misses and
1–3 false alarms per run) are judge decisions on ambiguous vignettes ("You rinse a dish" taken as dinner, "your package is
visible behind the counter" not taken as reaching it, a follow-up text read one step late).
The one update miss per run is the same item in all six runs (Friday's dry-cleaning override,
whose new cue arrives in the same sentence as dinner).

Cost: `muninn_store` 167 model calls and 129–133 k estimated input tokens per week, 8.5–9.4
min wall-clock (direct `claude -p`, three runs in parallel); the baselines' surviving prompt
logs show 1.19 M (single, 126 calls) and 1.49 M (ledger, 80 calls) estimated input tokens —
one run each, and the file was shared by three concurrent writers, so indicative only. The
store keeps each call short: the model sees the store, not the growing conversation.

**Data.** `results/pmbench/round4/` and `results/pmbench/round5/`: action logs, score
reports, the scaffold's per-step traces (board, ops, replies, decisions) and final store dumps.
The three baseline runs of each arm were launched in the same second and PM-Bench's runner
names the log by that second, so their action logs overwrote one file; each run's console
output was kept and `pmbench/reconstruct_from_stdout.py` rebuilt the three logs from it. On the
run whose original log survived the rebuilt entries are identical (80/80, both arms); the
collided originals are kept under `original-collided/`. The launcher now staggers launches.

**Rounds 6 and 7 — the residual judge and Form errors.** Round 6 tried seven prompt rules at
once plus querying channels at every step: the two targeted classes disappeared in every run
(Monday's follow-up text matched; "You rinse a dish" no longer taken as dinner) but typing "a
message that reaches the person" as an event made the judge fire the dry-cleaning and receipt
intentions on Friday's rack vignette, and on Tuesday step 8 the model returned a handle that was
not on the menu; 95.4 %, below round 5, reverted. Round 7 kept the four rules that held (a
scene is not an instruction; the cue is the event without its purpose; the cue must be
explicitly present; intentions sharing a cue are due together): 96.7 %, not below round 5 and
within the run-to-run spread of it, so it ships on the strength of the traces, not the mean.
What remains in every round-7 run: Thursday's "your package is visible behind the counter"
(the benchmark counts "reach the counter" as due; the judge does not), and Friday's dry
cleaning, whose override says "wait for the confirmation email": typed as an email-channel cue
it fires one step early on the receipt's confirmation email in the channel, while the benchmark
delivers the dry-cleaning cue in the next vignette. Both are ambiguities of the week; forcing
either trades false alarms elsewhere. Data: `results/pmbench/round6/`, `results/pmbench/round7/`.

**Decision rule, applied.** Pre-registered: claim only if mean set-F1 ≥ 82.9 % and above both
baselines by more than the round-2 spread (±4). Round 5: 96.3 % vs 79.8 % and 77.9 %. Met.
Round 5 is not below round 4, so the round-5 rule ships; round 7 (96.7 %) is the shipped
prompt set, round 6 (95.4 %) was reverted. Caveats that stay
attached to the claim: the 82.9 % line is another model; three runs per arm; the scaffold is an
in-loop agent for PM-Bench, not the harness delivery path of F3 — what transfers to F3 is the
mechanism (lifecycle in code, cue firing by the store, the model only forms and decides).

## Verdict

- §1 cues vs lexical: not distinguishable → dir/symbol cue delivery ships off by default.
- §2 compaction survival: 100/100 → event reinjection ships on by default.
- §3 PM-Bench rounds 1–3: below the line, and equal to the paper's ledger → not claimed (bridge later found contaminated, scaffold peeked at hidden fields).
- §3 PM-Bench rounds 4–5: Muninn as the intention store, isolated bridge — 96.3 % set F1 (3 runs) vs 79.8 % / 77.9 % for the paper's two scaffolds on the same model, above the 82.9 % PIS line (another model) → claimed, with the caveats in §3 rounds 4–5.

As the plan states for this outcome, F3 in the MVP is reinjection on compaction and at
session start, plus lexical recall; the rest of F3 stays measurable and switchable.

## §3 round 8 — held-out weeks, store ablation, one bridge (claude-sonnet-5, measured 2026-09-13)

Pre-registered before any cell (`PREREGISTRATION.md`, "round 8"; commit `f173f2d`, OpenTimestamps
proof in `prereg-stamps/`). Three held-out weeks generated by PM-Bench's own generator from seeds
derived from that commit's hash (76233, 10517, 77013), plus the released week (v9, the development
week, reported separately). Four arms through one bridge process (`claude -p`, no settings of any
scope, no tools, no MCP; canary: only the harness's environment reminders and the account e-mail).
3 runs per (week, arm), 48 runs, 0 errors; `muninn` binary `9c8c80b9…` in a network namespace with
no interfaces, one hash across every manifest. Raw data `results/pmbench/round8-sonnet/`
(score reports, per-step traces, final stores, manifests; prompt logs gzipped; the account e-mail
redacted from canaries and manifests). Analysis: `pmbench/analyze_round8.py`, output in
`analysis.json`.

| week | muninn_store | plain_store | single_baseline | todo_ledger |
|---|---|---|---|---|
| heldout-76233 | 92.7 · 93.3 · 94.7 → **93.6** | 95.4 · 95.4 · 94.7 → 95.2 | 84.3 · 82.3 · 78.9 → 81.8 | 82.1 · 77.0 · 77.6 → 78.9 |
| heldout-10517 | 97.8 · 84.6 · 85.5 → **89.3** | 97.8 · 97.1 · 97.1 → 97.3 | 85.5 · 84.8 · 83.3 → 84.5 | 80.3 · 80.0 · 83.5 → 81.3 |
| heldout-77013 | 87.2 · 98.8 · 87.8 → **91.3** | 96.3 · 97.5 · 95.7 → 96.5 | 73.6 · 78.1 · 74.6 → 75.4 | 74.5 · 75.8 · 77.0 → 75.8 |
| v9 (development) | 96.2 · 96.8 · 98.8 → **97.3** | 96.2 · 97.5 · 96.9 → 96.9 | 78.6 · 78.1 · 78.9 → 78.5 | 78.1 · 77.2 · 78.9 → 78.1 |

Pooled over the three held-out weeks (exact stratified permutation, 8 000 relabelings; cluster
bootstrap by week, coarse with three clusters):

| contrast | Δ mean | one-sided p | two-sided p | 95 % CI | weeks where every A run beat every B run |
|---|---|---|---|---|---|
| muninn_store − single_baseline | +10.8 | 5/8 000 | 10/8 000 | [+4.6, +16.6] | 2/3 |
| muninn_store − todo_ledger | +12.7 | 1/8 000 | 2/8 000 | [+7.5, +17.2] | 3/3 |
| plain_store − single_baseline | +15.7 | 1/8 000 | 2/8 000 | [+12.3, +20.6] | 3/3 |
| muninn_store − plain_store | −5.0 | 7 866/8 000 | 288/8 000 | [−9.4, −1.2] | 0/3 |

**Decision rules, as pre-registered.**
- R1 line: held-out mean 91.4 % ≥ 82.9 % — **met**.
- R1 spread rule (mean above each baseline by more than the largest within-arm range on every
  held-out week) — **not met**: on heldout-10517 the `muninn_store` range is 13.2 points (97.8 vs
  84.6) and the margins are +4.8 and +8.0. The public claim therefore reads "on the development
  week" for the round-7 figure, and "held-out mean 91.4 % against 80.6 % and 78.7 %, every week's
  mean above both baselines, with 4 of 9 runs between 84.6 and 87.8" for the generalisation.
- R2 ablation band ±2 — **not met**: `plain_store` is higher by 5.0 pooled. By the rule this is
  published as "the store implementation made a difference, in the wrong direction".
- R4 invocation path: v9 through the bridge 97.3 % vs round 7 direct 96.7 % — not lower.

**What the traces show about R2.** The two store arms run the identical scaffold on identical
prompts, and the day-1 plan FORM prompt is byte-identical between arms in every week (sha256
prefixes `e6cf9fed…`, `fbb9d8f5…`, `96deb94e…`, `82ef219b…`, one per week, same in all six runs).
The four low `muninn_store` runs (84.6, 85.5, 87.2, 87.8) are exactly the four runs in which that
first call typed the daily antibiotic as `{"kind":"time"}` instead of a daily event; the other five
`muninn_store` runs and all twelve `plain_store` runs typed it as an event. A time-typed daily
medication is eligible only when the clock query returns its hour, so it is missed on the
benchmark's event steps and acted on off-step (false alarms per step 3.2 % vs 0.0 %). This
decision is taken before the first store operation; the muninn binary was not involved in it, and
no muninn call failed (0 failures in 1 080 store calls under eight-way load in a separate stress
run). The gap is therefore the model's run-to-run variation at temperature 0 landing on one arm —
that is a statement about the cause, not a revision of the rule: R2 is reported as not met, and
round 9 (pre-registered below) is designed to separate store equivalence from sampling with no
model call at stake.

**Cost.** `muninn_store` and `plain_store`: 167 model calls and ~130 k estimated input tokens per
week; `single_baseline` 126 calls and `todo_ledger` 80 calls with 1.2–1.5 M estimated input
tokens (their own prompt logs, one per run this time). Wall time per run through the shared
bridge, eight runs in parallel: 5–9 min store arms, 6–14 min baselines.

## §1 replications at five runs (measured 2026-09-14; pre-registered)

Fresh grids, same tasks, seed, model (claude-sonnet-5) and oracles as the originals, five runs,
randomised order, the fixed instrument. Two interruptions by the account's session limit; those
cells were re-run as infrastructure errors. Cells in which the agent used all 25 turns are scored
by their oracle (5 in the boot grid, 7 in the expansion grid; 9 of the 12 had already written a
passing file). 0 remaining errors, 0 PreToolUse denials. Contrasts: cluster bootstrap by task, the
originals' own `analyze.py` (4 000 resamples, seed 7 — the pre-registration said 10 000; the
originals' script was used unchanged so the figures are comparable). Raw data
`results/boot-vehicle-rep5/`, `results/gate4-cues-v2-rep5/`.

### Boot vehicle — hook summary vs file block (140 cells, $27.05)

| arm | pass | tokens (mean) | turns (mean) |
|---|---|---|---|
| literal (block in CLAUDE.md) | 52/70 | 811 | 11.9 |
| literal-hookboot (SessionStart summary) | 52/70 | 798 | 12.9 |

`literal-hookboot − literal`: replication **+0.000 [−0.114, +0.129]**; pooled with the original 84
cells **+0.045 [−0.045, +0.152]**. Rule: non-inferiority, lower bound > −0.10. **Not met on the
replication alone** (−0.114); met pooled. The pre-registered consequence (re-examine the default)
was tied to a negative point estimate, which did not occur. The hook stays the default; the public
statement is "not worse than the file block within the precision measured", with the replication's
interval quoted, not the original's +0.119.

| task | literal | hookboot | task | literal | hookboot |
|---|---|---|---|---|---|
| cue-artefact-fence | 5/5 | 4/5 | docs-grammars-control | 5/5 | 5/5 |
| cue-azure-pattern | 4/5 | 4/5 | engine-s12-why-responder | 5/5 | 5/5 |
| cue-busy-cap | 5/5 | 5/5 | fact-corpus-fetch-limits | 5/5 | 4/5 |
| cue-router-stub | 3/5 | 5/5 | fact-real-transcript-ingest | 0/5 | 0/5 |
| cue-row-struct | 1/5 | 4/5 | fact-sessionstart-gate | 5/5 | 5/5 |
| cue-size-subcommand | 0/5 | 0/5 | fact-userprompt-p95 | 5/5 | 4/5 |
| cue-stderr-helper | 5/5 | 5/5 | | | |
| cue-timing-stub | 4/5 | 2/5 | | | |

### Query expansion through the symbol graph (120 cells, $28.29) — replication negative

| arm | pass | tokens (mean) | turns (mean) |
|---|---|---|---|
| lexical-plain (no cues, no expansion) | 15/40 | 503 | 15.8 |
| lexical (expansion) | 10/40 | 522 | 15.1 |
| literal (cues + expansion) | 9/40 | 784 | 14.9 |

`lexical − lexical-plain`: replication **−0.125 [−0.275, −0.025]**; pooled with the original 72
cells **−0.031 [−0.125, +0.062]**. `literal − lexical` −0.025 [−0.150, +0.075] (pooled +0.016).
Rule: point ≤ 0 on the replication → the opt-in is removed. **Applied**: expansion is no longer
advertised or recommended anywhere; the original +0.125 was a three-run result that did not
replicate. The code path stays behind `MUNINN_EXPAND` until no grid that hashes the binary is
running, then it is removed in its own commit.

| task | lexical-plain | lexical | literal |
|---|---|---|---|
| cue-artefact-fence | 4/5 | 3/5 | 3/5 |
| cue-azure-pattern | 3/5 | 0/5 | 0/5 |
| cue-busy-cap | 5/5 | 5/5 | 3/5 |
| cue-router-stub | 0/5 | 0/5 | 0/5 |
| cue-row-struct | 0/5 | 0/5 | 0/5 |
| cue-size-subcommand | 0/5 | 0/5 | 0/5 |
| cue-stderr-helper | 0/5 | 0/5 | 0/5 |
| cue-timing-stub | 3/5 | 2/5 | 3/5 |

**An anomaly, checked and left as measured.** `cue-stderr-helper` passed 15/15 in the boot
replication and 0/15 in this one, in every arm. Same binary, same seed, same task text and oracle,
and byte-identical deliveries (session-start ids 83, 84; turn delivery ids 87, 81, 64, 475
tokens) in both grids. The agents in this grid received the recorded naming decision and wrote
that it "contradicted what's actually in the file, so I went with what the code itself shows";
in the boot grid they followed it. No instrument difference was found, the arms of each grid ran
interleaved in random order, so the within-grid contrasts are unaffected; across grids, it is the
run-to-run behaviour of the model on a task where memory and code disagree, and it is reported as
such.

**Consequence for §1 as a whole.** Across three grids and 288 cells, nothing layered on top of
plain lexical recall of literal records — dir/symbol cues, query expansion — has a replicated
positive effect. F3's shipped delivery is lexical recall plus event reinjection, which is what
the plan already defaulted to.

## §3 round 8 on gpt-5.6-sol through Codex (measured 2026-09-14; pre-registered, R3)

Same weeks, arms, scaffold (sha256 `bccb89f2…`) and muninn binary (`9c8c80b9…`) as the sonnet grid;
`codex exec` through `codex_bridge.py` (`--ephemeral --ignore-user-config --ignore-rules -s
read-only`, private `CODEX_HOME`, empty cwd; no temperature control exists in Codex). 48 counted
runs, 0 non-zero exits, 9 792 bridge requests, 0 bridge errors, 12 of them in which the model ran a
read-only shell command in the empty directory. Canaries: refusals, and a marker probe that named
only `AGENTS.md` (Codex's own prompt; `PREREGISTRATION.md`). A launcher defect started 11 extra
baseline runs; by the rule fixed before any score was read, the first three by launch time count
and the rest sit in `excess-runs/` unused. Raw data `results/pmbench/round8-codex/`.

| week | muninn_store | plain_store | single_baseline | todo_ledger |
|---|---|---|---|---|
| heldout-76233 | 98.7 · 96.2 · 96.7 → **97.2** | 95.5 · 96.7 · 98.7 → 97.0 | 78.4 · 82.4 · 78.9 → 79.9 | 83.0 · 77.6 · 80.5 → 80.4 |
| heldout-10517 | 97.8 · 98.6 · 97.1 → **97.8** | 94.2 · 96.4 · 97.8 → 96.1 | 85.7 · 87.9 · 83.1 → 85.6 | 87.1 · 87.1 · 84.3 → 86.2 |
| heldout-77013 | 98.2 · 96.9 · 96.9 → **97.3** | 98.1 · 98.1 · 98.1 → 98.1 | 73.9 · 77.6 · 77.1 → 76.2 | 72.5 · 75.0 · 76.6 → 74.7 |
| v9 (development) | 98.1 · 98.8 · 98.1 → **98.3** | 97.5 · 96.9 · 95.0 → 96.5 | 79.7 · 80.0 · 80.0 → 79.9 | 79.2 · 83.3 · 81.6 → 81.4 |

| contrast, held-out pooled | Δ mean | one-sided p (exact, 8 000) | 95 % CI (coarse) | weeks where every A run beat every B run |
|---|---|---|---|---|
| muninn_store − single_baseline | +16.9 | 1/8 000 | [+12.6, +21.0] | 3/3 |
| muninn_store − todo_ledger | +17.0 | 1/8 000 | [+12.0, +22.4] | 3/3 |
| plain_store − single_baseline | +16.5 | 1/8 000 | [+11.0, +21.6] | 3/3 |
| muninn_store − plain_store | +0.4 | 2 149/8 000 | [−0.9, +1.9] | 0/3 |

**Rules.** R1 line (97.5 % ≥ 82.9 %) — met. R1 spread rule (margin above every baseline larger than
the largest within-arm range, every held-out week) — **met**: the smallest margin is +11.7 against a
range of 4.8. R2 ablation band ±2 — pooled +0.4, met. One reading has to be stated: on heldout-76233
the worst-case gap `min(muninn) − max(plain)` is −2.5. The analysis script reads the band as "no
week where every run of one arm beats every run of the other by more than 2 points" (a negative gap
means the runs overlap, which is what "not distinguishable" means); read literally as "the number
must lie within ±2", that week would fail the band. The first reading is the one the rule was
written for; both are printed here so the reader can apply the other.

**Store equivalence, from the traces.** On Codex every one of the 24 store runs typed the daily
antibiotic as an event on day 1 (12/12 per arm), and the two stores score the same. On sonnet the
four low `muninn_store` runs were exactly the four with a clock-time typing, on prompts identical
to the dict arm's. Across both families the store implementation never produced a different board
from the same operations in the traces checked; round 9 measures that at every step.

**Both families, held-out weeks.** `muninn_store` 91.4 % (sonnet) and 97.5 % (gpt-5.6-sol) against
the paper's two scaffolds at 78.7–80.6 % (sonnet) and 80.4–80.6 % (gpt-5.6-sol) on the same model, same bridge, same
weeks; exact p ≤ 5/8 000 for every baseline contrast in both families. The worst-case rule held on
gpt-5.6-sol and failed on sonnet in one week.

## §3 round 9 — store equivalence by shadowing (measured 2026-09-14; pre-registered)

**Question.** Round 8 on sonnet put `plain_store` 5.0 points above `muninn_store` on the held-out
weeks, and the traces tied every low run to one day-1 decision of the model. Round 9 tests the two
explanations directly. 3 `muninn_store` runs with a shadow dict store and 3 `plain_store` runs per
held-out week, per family: 36 runs, 0 non-zero exits, same weeks, bridges and muninn binary
(`9c8c80b9…`). Raw data `results/pmbench/round9-{sonnet,codex}/`.

**S1 — do the stores ever disagree on the same operations?** Inside every `muninn_store` run the
dict rule was evaluated on the same records at every step. **0 disagreements in 1 458 boards**
(729 per family, every step of every week). On this benchmark the engine's cue evaluation and the
dict implementation are the same function.

**S2 — is the round-8 gap an arm effect or sampling?** Day-1 typing of the daily antibiotic, rounds
8 + 9, held-out weeks:

| family | muninn_store: clock time / event | plain_store: clock time / event | Fisher two-sided |
|---|---|---|---|
| claude-sonnet-5 | 7 / 11 | 3 / 15 | p = 0.264 |
| gpt-5.6-sol | 0 / 18 | 0 / 18 | p = 1.000 |

In round 9 the clock-time typing landed on both arms on sonnet, and it predicts the score exactly:
every run that typed it scored 84.6–86.5 %, every run that did not scored 92.7–98.6 %, in both arms
(`muninn_store` 85.5, 85.7, 86.5 against `plain_store` 85.5, 84.6, 86.5). By the rule, the round-8
gap is reported as sampling variation of the model on byte-identical prompts, with S1 as the
mechanism check. Round 8's R2 verdict on sonnet ("not met") stays in the record as measured.

| week | sonnet muninn | sonnet plain | gpt-5.6-sol muninn | gpt-5.6-sol plain |
|---|---|---|---|---|
| heldout-76233 | 92.7 · 94.7 · 94.8 | 96.8 · 93.4 · 96.1 | 98.1 · 98.7 · 99.4 | 97.4 · 98.7 · 97.4 |
| heldout-10517 | 98.6 · 85.5 · 98.6 | 85.5 · 97.8 · 84.6 | 98.6 · 99.3 · 97.8 | 97.8 · 96.4 · 95.7 |
| heldout-77013 | 85.7 · 97.5 · 86.5 | 97.5 · 96.9 · 86.5 | 98.1 · 97.5 · 97.5 | 97.5 · 95.0 · 98.2 |
| mean | 92.7 | 92.8 | 98.3 | 97.1 |

Round 9's runs are reported on their own, as pre-registered; R1 is not re-evaluated on a pool of
rounds 8 and 9.

**What this settles for the public claim.** Muninn's store is not what makes the PM-Bench scaffold
score; the typed-intention mechanism is, and any correct store gives the same boards. The claim
stays worded as the mechanism, and the one sentence that may be said about the engine is that it
implements that mechanism exactly (0 of 1 458 boards differ).

*Bridge log note (round 9, gpt-5.6-sol).* Round 9 reused the Codex bridge process started for round
8, whose request log lives in `results/pmbench/round8-codex/`. Requests after round 9's start time
(`round9-codex/FROZEN.json`): 3 060, 0 tool calls, 1 bridge error (an empty completion, retried by
the scaffold).
