# usage-v4: results

The registration is the section "usage-v4" of `../../PREREGISTRATION.md` with its nineteen
amendments. This file reads every rule on the build that ships, lists every change with what
happened to it, and says where the measurement is weak. Stores are named by label (W01 to W10,
L01) and records by id. No text of a record or a transcript is here.

**The build changed after the reading below.** A review of the whole branch found three
defects no cell reads, the build was fixed, and the cells were read again on the fixed build
`366bb7913a35be7a` (nineteenth amendment). The section "After the final review" has what was
found, the fixed build's figures beside the final build's, and what is still open. Everything
else in this file is the reading of the final build `8ea5e788aecf33e2`, left as it was written.

- **Base:** Muninn 1.2.0, commit `00d691630`, binary `b93d2f5c222c0424`.
- **Final build:** commit `5afb51960` of `feature/usage-review-2-measured-fixes`, binary
  `8ea5e788aecf33e2`, built with Rust 1.99.0 on Windows. It still calls itself 1.2.0: the
  version was set after the reading. The released binary differs from the measured one by
  that string and by one line of the boot block that `init --boot-file` writes (`MUNINN 9/9
  GREEN` for `11/11`); on the 150 replayed prompts it returns the same ids and tokens.
- **Inputs:** the frozen copies under the fixture root (tenth amendment). One run at a time.
- **Counts:** `counts/*_8ea5e788aecf33e2*.json`, and `counts/b_retire_b93d2f5c222c0424.json`
  for the base's B replay, which was run again beside the final build (eighteenth amendment).
  The three E runs are the commits named in section E.

## After the final review: the fixed build

**How the defects were found.** Not by a cell. A reviewer of the whole branch wrote invented
transcripts, put them through the `Stop` hook of the released binary and of 1.2.0, and read the
store. Three things came out, and the registered cells could not have shown any of them:

1. **A statement typed in the turn that hands a copy of it to a worker was lost when the
   worker's session was read first**, which is the order a live session produces. The worker's
   turn typed the sentence, the coordinator's turn revoked that row as an agent's, and the
   person's own sentence then met the revoked row by its hash and was dropped. 1.2.0 keeps the
   statement in both orders. The order probes had "the coordinator's own prompt is a word of
   the user's" and never the case where that word is the sentence the task copies.
2. **The episode of a turn whose command failed was no longer served once the command passed**
   (or failed again with another count). `recall` skipped the episode of any turn holding a row
   retired as superseded, and a dead end is retired that way. 1.2.0 serves it. C3's twin arm
   reads only turns whose typed statement was replaced.
3. **An older statement read after a newer one retired the newer one.** 1.2.0 does the same
   for two sessions read out of order; this plan added a route, the release of a last message
   nobody answered. B1 replays each corpus in one order, and B2 and B3 write their sessions in
   date order.

**The fixed build.** Commits `b2df1cc70` to `7bd930eb7` of the branch, binary
`366bb7913a35be7a`, same toolchain. Each fix has tests that fail on the build before it.
The third fix was narrowed after its first form failed a probe (below). The build also makes
`muninn remember` say when the record it found is retired, and `init` say that the Codex hooks
file names this machine's binary; no cell reads either.

**The cells again, final build → fixed build** (`counts/*_366bb7913a35be7a*.json`; inputs
frozen, one run at a time; the base's B replay run again in the same sitting):

| reading | final `8ea5e788aecf33e2` | fixed `366bb7913a35be7a` | counts |
|---|---|---|---|
| A1, A2, A3 and the four arms | as in the table below | equal on every leaf (177 or 178 a file) | `a_extract_*` |
| `remember` replay, both readings | 2 / 46 of 48; 41 / 6 / 1 | equal (24 leaves a file) | `a_remember_*` |
| B1 `loss` retired; both valid items | 5; both retired | 5; both retired (both readings) | `b_retire_*` |
| B1, every labelled item's state | | equal | `b_retire_*` |
| B1 store totals, records retired with an older record as heir | 5 in W02, 5 in W02-now (base 4 and 4) | 0 and 0 | `b_retire_*` |
| B1 store totals, decisions retired | 76 and 111 | 73 and 109 | `b_retire_*` |
| B2, B3 (all four cells) | 0; A not B; 1 of 1; equal to base | equal | `b_retire_*` |
| `b3_path.py` diagnostic | table below | equal (46 leaves) | `b3_path_*` |
| C1 to C5, frozen labels and with the pool | as in the table below | equal on every leaf (291 + 378, 294 + 378) | `c_delivery_*` |
| C3, retired statement served through its episode | 0 of 198 and 0 of 47 | 0 and 0 | `c_delivery_*` |
| D, same ids against `187d91a1431ab6ac` | 150 of 150, B3 equal | 150 of 150, B3 equal | `d_removals_*` |
| D, same ids against the final build | | 150 of 150 | `d_removals_*-vs-8ea5e788aecf33e2` |
| F, Codex first clause | 5 and 79; 0 from a turn not a person's | equal (478 leaves) | `f_codex_*` |
| `verdict.py --split heldout`, `design`, `all` | | every row as on the final build | |

Nothing a rule reads moved. The second fix changes what `recall` returns only for a prompt that
reaches a turn holding a retired dead end, and none of the 150 replayed prompts returns
different ids. The third fix shows in the store totals of the two corpora of one project: on
the final build 5 records of each end retired in favour of an older record, on the fixed
build none, and 3 and 2 decisions fewer are retired. None of those records is a labelled item.

**E on the fixed build**, as the fifteenth amendment says: same-moment copies, three
interleaved runs, each committed before it was read. p95 in ms, base → fixed (ratio):

| row | run 1 | run 2 | run 3 | median ratio | final build's median | verdict |
|---|---|---|---|---|---|---|
| SessionStart | 12.672 → 15.589 (1.230) | 14.172 → 16.079 (1.135) | 14.623 → 17.201 (1.176) | 1.176 | 1.148 | **fail** |
| SubagentStart | 10.308 → 15.411 (1.495) | 12.163 → 15.810 (1.300) | 12.227 → 17.276 (1.413) | 1.413 | 1.274 | **fail** |
| UserPromptSubmit, full | 13.492 → 14.424 (1.069) | 15.203 → 14.547 (0.957) | 15.700 → 15.673 (0.998) | 0.998 | 0.965 | pass |
| UserPromptSubmit, gated | 7.739 → 9.253 (1.196) | 9.302 → 9.445 (1.015) | 10.215 → 11.145 (1.091) | 1.091 | 1.087 | pass |
| `Stop` with ingest, W02, median | 249.3 → 73.2 | 220.6 → 61.7 | 221.1 → 63.5 | | 235.1 → 70.7 | pass |

Rule E reads as on the final build: it fails on the two rows where the base's bench delivers
no block and passes on the other three. Every read row's median ratio is higher than the final
build's. That is not a finding against a fix, for two reasons. No fix touches the session
start or the subagent start, and the one that touches the prompt path changes one condition
of one query. And read against the final build directly, as hook p50 minus process-start p50
(12 rounds of 40, two same-moment copies of each binary on one bench store of 20,000 records,
taken twice), the fixed build is no slower than the spread between copies:

| | final build, two copies | fixed build, two copies | difference of means |
|---|---|---|---|
| SessionStart, first reading | 8.364, 8.215 | 8.556, 8.298 | +0.14 |
| SessionStart, second reading | 9.068, 8.933 | 8.869, 8.672 | −0.23 |
| SubagentStart, first reading | 7.241, 7.127 | 7.120, 7.046 | −0.10 |
| SubagentStart, second reading | 7.793, 7.586 | 7.669, 7.447 | −0.13 |
| gated prompt, first reading | 0.686, 0.658 | 0.737, 0.726 | +0.06 |
| gated prompt, second reading | 0.613, 0.775 | 1.026, 0.702 | +0.17 |

The gated prompt passes narrowly again (1.196, 1.015 and 1.091). Machine state: the owner's
working desktop, in use, as for the final build's reading and against the fifteenth
amendment's condition. A browser, an editor application and the session running the harness
were open; no compiler, harness script or other `muninn` ran beside the runs (checked before
each). Process start p50, base and fixed: 4.951 and 4.990, 6.358 and 6.350, 7.111 and 8.351 ms.

**Order probes** (built against each source tree; `bad` is an order that serves what the same
order with every coordinator first does not, leaves a retired record unmarked, or differs with
no word of the user's between a worker and its coordinator):

| probe | final build's sources | fixed build |
|---|---|---|
| `orderprobe`, default | 5,472 and 3,528 runs, 0 bad | 0 bad |
| `orderprobe typed`, another subject, the same subject | 384 and 384, 0 bad | 0 and 0 bad |
| `orderprobe events`, four lines of 1,920 | 0 bad; fewer active than coordinator-first in 9, 432, 432 and 561 | 0 bad; 9, 435, 435 and 564 |
| `rprobe`, `vprobe`, `qprobe`, `kprobe` | 0 bad, no leak | 0 bad, no leak |
| `orderprobe dates` (new): sessions of the person's read in every order | 4 bad of 8 | 0 bad of 8 |
| `orderprobe stated` (new), the coordinator's prompt never said before | 75 bad of 384 | **5 bad of 384** |
| `orderprobe stated`, said before and current | 0 of 384 | 0 of 384 |
| `orderprobe stated`, said before and since replaced | 64 of 384 | **64 of 384** |

The two new modes were written for the review's shapes after the fixes, and were read first on
the fixed sources, then on the final build's. `stated` puts the sentence a task carries in the
coordinator's own prompt, over two workers and two coordinators in every order, and judges
every statement typed outside a worker's session.

- `events`: three more orders of 1,920 on three lines end with a record retired and marked
  where coordinator-first keeps it active. All are orders with a word of the user's mid-way,
  where that is the ruled outcome. The count is higher than on the final build by 3 orders a
  line, and which of the fixes moved it was not located.
- **The first form of the third fix failed a probe and was changed.** With the plain rule (a
  record is never retired by a statement dated before it), `orderprobe typed` on the same
  subject read 13 bad of 384. A worker's copy moves a statement to the worker's turn; a
  coordinator's own prompt dated before that turn left the statement alone; undone, the copy
  left it active at its earlier date beside its replacement. The shipped rule compares a
  record that a standing restatement moved while active by the date it had before the move.
  This is a change after a figure, recorded under the nineteenth amendment before any other
  cell ran.

**Still open on the fixed build.**

- `stated`, never said before, 5 of 384: with two coordinators and two workers, the row the
  worker typed can be retired by another worker's copy of another statement before the
  person's coordinator is read. The person's sentence then meets a row retired otherwise than
  as an agent's, and is dropped; when the copies are undone the row is revoked. The person's
  statement ends retired and unmarked. All five are orders with a word mid-way.
- `stated`, said before and since replaced, 64 of 384, unchanged by the fixes: the person says
  again, in a coordinator's own prompt, a statement another had replaced, while another
  worker's turn is on record and its coordinator is not. The restatement is dropped and the
  replaced value ends current, where coordinator-first ends with the restated one. These are
  all 64 orders with a word mid-way. 1.2.0 has no restatement at all.
- An older statement read after a newer one is not retired by the newer one. Both stay active;
  the session start lists the newer first and the prompt hook serves it first.
- A statement the person said again while it was current is not kept from an older change read
  later (what the narrowing of the third fix gave up). 1.2.0 and the final build do the same.

`verdict.py b93d2f5c222c0424 8ea5e788aecf33e2 --split heldout` prints the rows below, except
A1, which binds on the filters-only arm (`8ea5e788aecf33e2-filters`, ninth amendment), and E,
which is read from three runs (fifteenth amendment).

## Verdict by rule

| rule | registered text, in short | base | final build | verdict |
|---|---|---|---|---|
| A1 | filters remove ≥ 30 % of the base's held-out noise and lose ≤ 5 % of its durable records | noise 55, durable 13 | filters-only arm: noise 38 (30.9 % removed), durable 13 | pass, by one item |
| A2 | a recall rule adds at least one durable statement per noise record, held-out | durable messages 4, noise candidates 18 | per rule, added durable / added noise: answer pick +1 / +0, wish +4 / +4, correction without opener +1 / +0; full build 10 and 16 | pass, each rule |
| A3 | a new extractor: precision ≥ 2 × base and recall ≥ base, held-out | precision 0.2174, recall 0.16 | no extractor shipped; the shipped rules read 0.4074 and 0.40 | not claimed (see "Tried and not shipped") |
| B1 | retired `loss` items: candidate ≤ base; both valid retirements still happen | 9; both retired | 5; both retired (kind-bound and kind-free readings agree) | pass |
| B2 | reword retires nothing; A-B-A serves A and not B; the reverted commit's record is retired | 7 retired; serves B and not A; 0 of 2 | 0 retired; serves A and not B; 1 of 1 | pass |
| B3 | `loop8/eval_all.py`: `retired_a`, `kept_b` not below base; noise retirements not above base (third amendment) | 18/30, 10/30; 23/30; noise 3/30, 3/30 | the same on all four cells | pass. The evaluator's other cells, `served_ok` and `old_served`, are not equal: see below |
| C1 | held-out unrelated blocks fall ≥ 30 %, useful pairs fall ≤ 1 | unrelated 143, useful 10, of 252 returned | unrelated 72 (−49.7 %), useful 9, of 157 returned, 4 of them unscored | pass |
| C2 | mean tokens of a delivery with the same ids fall; `init --check-budget` passes | 436.9 | 305.1 on the 17 prompts with the same ids (all prompts 563.7 → 252.5); budget check in the CI section | pass |
| C3 | a cut record is offered again in the session | 0 of 12 | 11 of 11 | pass |
| C3 | a record only listed in the catalogue is offered again (eighth amendment) | 0 of 5 | 9 of 9, none excluded | pass |
| C3 | a record delivered before a compaction is offered again after the next `Stop` | 0 of 1 | 1 of 1 | pass |
| C3 | no retired statement served through an episode of its turn | W02 13 of 210 delivered prompts, L01 4 of 49 | 0 of 198 and 0 of 47 | pass |
| C4 | share of session-start slots worth their place does not fall (lenient / strict) | 0.2027 / 0.0997 | 0.2488 / 0.1220, frozen labels only, 167 of the slots it fills unlabelled | pass, weak (see weaknesses) |
| C4 | as amended: corrections and invariants neither shown nor listed do not rise; the closing line is truthful | 213 | 151; truthful in 7 of 7 stores | pass. As registered ("every one shown or listed"): not met by either build |
| C5 | Spanish recall of usage-v2's 30 questions does not fall | 27 | 27 | pass |
| C5 | the 69 gender-form pairs: more than the base's 0 | 0 | 55 | pass |
| C5 | every kind returned by the route that names it | 0 of 15 | 15 of 15 | pass |
| C5 | `--all` uses every word typed | 0 and 18 of 30 | 20 and 21 of 30 | pass |
| D | graph and cues: no ledger row delivered by a dir, symbol, file or tool cue; same ids without the part | 0 of 79,534 rows | removed; ids equal on 150 of 150 prompts and B3 equal against `187d91a1431ab6ac`, the last build that had the parts | removed on the reading |
| D | sidecar: no store holds a vector; usage-v2 recall the same without it | 0 vectors in 11 stores | removed; C5 above | removed on the reading |
| D | commit-subject decisions: no hook delivery names one; B1 to B3 hold without them | 0 deliveries | B2's revert reads 0 of 1 without them (Task 8's arm) | the part stays |
| E | no read hook's p95 more than 10 % over base; `Stop` with ingest lower | | median ratios: SessionStart 1.148, SubagentStart 1.274, full prompt 0.965, gated prompt 1.087; `Stop` 235.1 → 70.7 ms | **fail** on SessionStart and SubagentStart, pass on the other three (section E) |
| F | Codex: typed records where the base yields none, on the route a build installs by itself (sixteenth amendment) | 0 and 0 | 5 from the invented rollout, 79 from 70 real ones; 0 stored as the user's from a turn not a person's | pass |
| F | Codex: the hooks file installs and delivers a block in one real `codex exec` session | | not run again: the committed counts of `209bcab355dcde4c` stand (`9af8f767`), 3 deliveries in one session | pass on those counts |
| F | rule compiler: new patterns raise the held-out enforceable share, every new rule agreed by a reader | 238 of 3,585 | 238 of 3,585: no pattern shipped | nothing to pass |

A, C, F's first clause and the `remember` cell are equal, leaf by leaf, to the readings of the
Task 10 build `bda593036f176419` (173, 287 + 290, 474 and 20 + 20 leaves). The B item states
are equal to that build's too.

The `remember` replay cell decides nothing (eleventh and thirteenth amendments). Anchor phrase
passed: 2 of 48 recorded as the user's at the right turn, 46 at the lower origin. Whole
sentences passed: 41 at the right turn, 6 deduped against the extracted twin, 1 at another
turn, none lower, none not derivable, no errors.

Order probes on the final tree, every line `bad=0`: 5,472 and 3,528 orders by default, 384
twice typed, 1,920 four times with events, and the reviewer's shapes (rprobe, vprobe, qprobe,
kprobe). `muninn-bench replay` on the private fixtures gives the harness's counts: extraction
52, 50 and 50 leaves equal with none differing, delivery 16, 16 and 16.

## B3's other cells: what `served_ok` reads now

Rule B3 names `retired_a` and `kept_b`. The same evaluator also prints whether the current
answer was served, and those cells moved:

| cell (registered evaluator) | 1.2.0 | final build |
|---|---|---|
| both / adjacent, `served_ok` | 11/30 | 2/30 |
| both / adjacent, `old_served` | 8/30 | 0/30 |
| both / blocks, `served_ok` | 2/30 | 0/30 |
| both / blocks, `old_served` | 13/30 | 2/30 |
| noise, both orders, `old_served` | 18/30 | 2/30 |

With the dated evaluator `served_ok` reads 19/30 and 16/30 on 1.2.0 and 2/30 and 2/30 on the
final build. Every build of this plan from Task 6 on reads these values, and no report of the
plan said so before this one.

The cause is the instrument. The evaluator asks `muninn recall "<topic>"`, and nine of the ten
topics are three words long. Since Task 3 `muninn recall` applies the gates of the prompt hook,
which has always been silent on a prompt under four words. The command prints something for 21
or 20 of the 30 topics on 1.2.0 and for 2 on the final build.

A diagnostic was added after the result to read the same stores through the path a session
takes (`b3_path.py`, committed before it ran; it decides no rule). It runs the evaluator
unchanged and, for each scenario, reads the prompt hook's context for the question "Which
<topic> do we use in this project now?" and the session start's context. Counts
`b3_path_*.json`, of 30 cells, 1.2.0 → final build:

| | both / adjacent | both / blocks | noise (both orders) |
|---|---|---|---|
| new value in either context and old value in neither | 18 → 20 | 15 → 17 | 1 → 1 |
| old value in either context | 10 → 8 | 15 → 13 | 23 → 21 |
| new value in the prompt hook's context | 12 → 12 | 4 → 2 | 0 → 0 |
| old value in the prompt hook's context | 8 → 6 | 13 → 11 | 18 → 15 |
| new value in the session start's context | 27 → 27 | 29 → 29 | 2 → 2 |
| old value in the session start's context | 2 → 2 | 2 → 2 | 14 → 14 |

Through a session's two paths together the final build puts the current answer in front of
the assistant, with the old one absent, at least as often as 1.2.0 in every cell, and the old
value no more often. One sub-cell goes the other way: in the prompt hook alone, in blocks
order, the new value is in 2 of 30 contexts where 1.2.0 had it in 4. The diagnostic's prompt
is one template, written for this reading. On the noise arm the old value is the current one
(nothing replaced it), so its presence there is correct.

## E. Latency and cost

Registered: `perf --strict`, seven interleaved runs a build on one machine; no read hook's p95
rises by more than 10 % over base; `Stop` with an ingest on a copy of the largest store, 20
runs, the candidate's median lower. Read as the fifteenth amendment says: both binaries run
from copies made at the same moment in one directory, three interleaved runs of `e_perf.py`
(harness revision 5), a row's ratio the median of the three. Commits `bcf2d65d`, `74af983e`,
`590a1369`. p95 in ms, base → final (ratio):

| row | run 1 | run 2 | run 3 | median ratio | verdict |
|---|---|---|---|---|---|
| SessionStart | 14.878 → 17.081 (1.148) | 14.768 → 16.335 (1.106) | 15.567 → 18.697 (1.201) | 1.148 | **fail** |
| SubagentStart | 12.942 → 16.483 (1.274) | 11.178 → 15.846 (1.418) | 14.419 → 16.382 (1.136) | 1.274 | **fail** |
| UserPromptSubmit, full | 15.664 → 15.114 (0.965) | 14.895 → 15.245 (1.023) | 17.450 → 15.477 (0.887) | 0.965 | pass |
| UserPromptSubmit, gated | 10.186 → 10.208 (1.002) | 9.009 → 9.793 (1.087) | 9.911 → 11.123 (1.122) | 1.087 | pass |
| `Stop` with ingest, W02, median | 244.3 → 74.4 | 230.8 → 67.7 | 235.1 → 70.7 | | pass |

Rule E fails on the final build on two of its five rows. They are the two rows the fourteenth
and fifteenth amendments say this about: the base's bench writes directory and symbol cue
rows, so the base delivers no block at SessionStart and SubagentStart while the candidate
does. Each run's own check confirms it (`check_prompts_delivered`: SessionStart false on the
base, true on the final build). The comparison on those rows is between a build that
delivers and one that does not, and the registered threshold was not written for that.

Each run: workloads equal, 0 hook errors, full prompts answered 299 of 300 on the base and 300
of 300 on the final build. Process start p50, base and final: 7.587 and 7.253, 7.160 and
6.397, 7.823 and 8.425 ms. In Task 9's runs it read 4.4 to 4.7. The commit message of the
first run says nothing else was running; that is true of the experiment's own processes
(no compiler, no harness script, no other `muninn`) and not of the machine: the owner's
desktop was in use, and a test runner of another project was seen running minutes after the
third run. The three runs stand as the reading and were not repeated.

**The two session-start rows against the previous build** (fifteenth amendment; no threshold).
Hook p50 minus process-start p50 in ms, median over 12 rounds of 40 runs, the log folded
before every block, two same-moment copies of each binary on one bench store of 20,000
records; previous build `038cec3c4a3f53ef`:

| | previous build, two copies | final build, two copies | difference of means | spread between copies |
|---|---|---|---|---|
| SessionStart, first reading | 7.939, 7.927 | 8.128, 8.078 | +0.17 | 0.01 and 0.05 |
| SessionStart, second reading | 8.463, 8.880 | 8.239, 8.317 | −0.39 | 0.42 and 0.08 |
| SubagentStart, first reading | 6.866, 6.675 | 6.618, 6.693 | −0.12 | 0.19 and 0.08 |
| SubagentStart, second reading | 7.498, 7.597 | 7.050, 7.306 | −0.37 | 0.10 and 0.26 |

SubagentStart reads no slower than the previous build in either reading. SessionStart reads
0.17 ms slower in one and 0.39 ms faster in the other. The +0.35 ms that Task 9 left open
(against a spread of 0.27) is neither confirmed nor located: the sign changes between two
readings of one procedure, and the procedure does not resolve under about 0.4 ms here.

**`perf --strict`.** Under Linux (WSL, Rust 1.98.1, the tree of the final build), limits as
written, three runs: exit 0 each. p95 in ms: SessionStart 5.297, 5.180, 5.350; SubagentStart
5.143, 5.100, 5.216; gated prompt 1.347, 1.346, 1.338 with process start at 1.26 to 1.28; full
prompt 4.383, 4.477, 4.437; `Stop` 26.3, 24.3, 25.5; `SessionEnd` 96.2, 94.6, 101.0. With CI's
`MUNINN_PERF_LIMIT_SCALE=1.5`: exit 0. On the Windows machine it does not hold for either
build: over the 21 `perf --strict` runs of each arm inside the three E runs, the base passed
every contract in 2 and the final build in 4. Three more runs of each by hand, taken while the
machine was under another project's load (process start 9 to 12 ms p50), exited 0, 1, 1 for
the base and 1, 0, 1 for the final build; under that load a contract with a process-start
floor passes on what Muninn adds, so those exit codes say little.

**The read hook that parses a transcript.** PostCompact parses the whole transcript when its
input carries a compaction summary that claims a result. It had no `perf` row. On a Codex
rollout of 160 KB, the median size of the 70 real ones (the largest is 108 MB), its p95 reads
8.517, 8.380 and 8.568 ms on a quiet Windows machine and 2.920, 2.855 and 2.816 ms under
Linux. The new contract is 17 ms, twice the largest p95 read. Under the load above it read
19.7, 16.6 and 12.6 ms on Windows. Codex's documented PostCompact input carries no summary,
so with Codex as documented the parse is not reached; with Claude Code it is, on a Claude
transcript, and that case has no row.

## Every change

Shipped means it is in the final build. A change read by no cell is marked unmeasured with what
covers it.

| change | rule | figure | state |
|---|---|---|---|
| Retirements carry a time and a cause; the record a commit writes is the heir (schema 3) | B | | shipped, unmeasured: tests |
| A one-line hunk retires only in a manifest or as a quantity, one statement a hunk | B2 | reword 7 → 0 | shipped |
| Reverts found by hash; every record of the reverted commit retired, what it retired put back | B2 | 0 of 2 → 1 of 1 | shipped |
| A statement typed again in the same words comes back | B2 | serves A and not B | shipped |
| No invariant retired for being past sixty | B | | shipped, unmeasured: tests |
| Restore pass, index counter, dates in µs or ns, `doctor` remedies, import at trust 0 | B | | shipped, unmeasured: tests |
| A swap rule for decisions only | B3 | dated evaluator 30 and 29 → 27 and 25 of 30; design grid 24 → 18 of 24 retired | tried and not shipped |
| A change retires an episode of its own session only; "link, do not retire" | B1 to B3 | design grid 8 → 7 and 6 of 24 retired, `kept_b` 17 → 15 | tried and not shipped |
| The swapped word must be one of the record's name tokens | B | | tried and not shipped |
| A record cut for budget, or only listed, is offered again; the ledger keeps the epoch | C3 | 0 of 12 → 11 of 11; 0 of 5 → 9 of 9; 0 → 1 | shipped |
| One compaction is delivered and counted once | C3 | | shipped, unmeasured: test |
| An episode of a replaced statement's turn is not served | C3 | 13 and 4 prompts → 0 and 0 | shipped |
| Equal scores go newest first | C1 | equal with and without it on held-out | shipped (fourth amendment) |
| `muninn recall` prints what the prompt hook delivers | | | shipped, unmeasured: test |
| Short prompts of one to three words answered | | 6 of 12 against 0 of 12 on one store, no labels | not shipped: no rule reads it |
| Relevance floor and at most two matches beside the rules | C1 | unrelated 143 → 72, useful 10 → 9 | shipped |
| Shorter block header, no `evidence:` line in hook blocks | C2 | 436.9 → 305.1 tokens | shipped |
| Corrections shown at session and subagent start, rules first in the catalogue, questions and acknowledgements left out of it | C4 | 0.2027 / 0.0997 → 0.2488 / 0.1220; 213 → 151 | shipped |
| Rules read as their own catalogue pages | E | about 3 ms of a cold session start | tried and not shipped |
| Two invariants for each correction at session start | C4 | design strict 0.0909 | tried and not shipped |
| The chars/3 token estimate | | p5 2.64 chars a token, largest delivery 557 exact tokens | measured, not changed |
| Subagent delivery matched to the subagent's task | | the hook's input carries no task | not built |
| `why` searches every kind on every route, skips a record too long for the budget, `--all` uses every word, newest first among equals | C5 | 0 of 15 → 15 of 15; 0 → 20 of 30 | shipped |
| Spanish gender and number forms, in `why` only | C5 | 0 → 55 of 69 | shipped |
| The same forms on the path the hooks share | C1 | 59 of 69, and held-out useful pairs 9 → 7 | tried and not shipped |
| A word's rarity counted once a record | C1 | held-out unrelated 74 → 72 against the build before it, useful 9 → 9 | shipped |
| An event delivery keeps its "did not fit" line inside 700 tokens | C4 | | shipped, unmeasured: test |
| A prompt an agent handed over, a line the harness marks as not a person's, and question text are not the user's | A1 (origin fixes) | counted in 55 → 38 | shipped |
| No correction from a question or from "it does not let me"; pasted blocks and long quotations not typed | A1 | counted in 55 → 38 | shipped |
| A prompt that opens three sessions word for word | A1 | removes no noise | tried and not shipped |
| A sentence that opens by pointing back | A1 | 0 of 55 alone on held-out | tried and not shipped |
| Answer pick of a dialog of two or more questions; wishes, one a message; a correction with no opener | A2 | +1 / +0; +4 / +4; +1 / +0 | shipped |
| Every pick typed with its question; every wish sentence | A2 | 5 against 6; 4 against 8 on design | tried and not shipped |
| Exit 0 read from the result's shape; a dead end retired by a later success; an unanswered last message stored; episodes of failed commands only | B, E | not readable by A | shipped, unmeasured: tests |
| The restatement journal and the undo that fails safe when an agent's prompt is found out | | 0 bad orders in the probes above | shipped, unmeasured by a rule: tests and probes |
| One record a statement; dead ends keyed on the error line; change markers; trust 2 from an exit code | | | not built |
| `muninn remember` | eleventh amendment | the cell above | shipped on its tests |
| A structural extractor, one record a turn | A3, B1 | precision 0.2174 → 0.6111, recall 0.16 → 0.44; B1's valid item `v1:W05:380` left active | tried and not shipped |
| Embedding sidecar | D | 0 vectors; C5 equal | removed |
| Symbol graph, dir and symbol cues, `PostToolUse`, turn-context log | D | 0 of 79,534 ledger rows; ids 150 of 150 | removed |
| Commit-subject decisions | D | B2 revert 0 of 1 without them | kept |
| A commit's observation of a file left out of the catalogue | none (ruling) | design decisions listed 18 → 20; held-out C4 was seen before the second version | shipped, not a clean reading |
| `VACUUM` once after the migration | none | 69.3 → 33.8 MB on one copy | shipped, not in the plan |
| Session log compacted; Markdown mirror written only where it is behind; no transaction across git; heartbeat rows kept thirty days; `maintain` not spawned inline; the log folded before a write hook closes; `index.md` not sorted on every ingest | E (Stop) | Stop with nothing to ingest 219.5 → 35.9 ms on a W02 copy; section E | shipped |
| Phase timings on the write hooks, on a read hook only when `MUNINN_PHASES` is set | E | +1.05 and +0.45 ms on SessionStart with them always on | shipped behind the switch |
| Windows home paths shortened in new bodies; an evidence file that is gone is said to be gone | | 527 of 527; 1,718 of 4,175 | shipped, unmeasured: tests |
| Pruning the fire ledger, compact snapshots, `wm:*` keys, epoch files | | 959 rows, 70,494 bytes in eleven stores for the last two | not built |
| Codex: `init`, `clean`, `status`; rollouts read by speaker marks | F | 0 → 5 and 79 | shipped |
| Rule compiler: a path named in one clause and a pronoun in the next; a flag forbidden for a named command, and a tool forbidden outright; an invocation written out with its flags | F | 2 of 4 held-out rules wrong; 0 of 3,585; 238 → 238 once the sentence both halves hold is left out | tried and not shipped, all three |
| `muninn-bench replay` | none | reproduces the harness, above | shipped (a tool) |
| `perf` row for PostCompact against a Codex rollout | E (contract) | section E | shipped |
| After the reading: what the person types in the turn that hands a copy of it to a worker is kept in either read order, and a statement put back from an agent's revocation replaces what a new one replaces | none (final review) | `orderprobe stated`, never said before: 75 → 5 bad of 384 | shipped in the fixed build, unmeasured by a rule: tests and probes |
| After the reading: `recall` skips an episode only for a retired statement of its turn, not for a retired dead end | none (final review) | C equal on every leaf | shipped in the fixed build, unmeasured: tests |
| After the reading: a statement retires nothing said after it; a record a standing restatement moved is compared by the date before the move | none (final review) | `orderprobe dates` 4 → 0 bad of 8; records retired with an older heir 5 → 0 in two corpora | shipped in the fixed build, unmeasured by a rule: tests and probes |
| The same rule on the record's date alone | probes | `orderprobe typed` 13 bad of 384 | tried and not shipped |
| After the reading: `remember` says when the record it found is retired; `config cues` refused; `init` says the Codex hooks file is for this machine; a session id cut at a whole character | none (final review) | | shipped in the fixed build, unmeasured: tests |

## Texts written after a figure

The registration and the first amendment were written before the base was measured. Nine
later texts say of themselves that they follow a figure they bear on:

1. **Seventh amendment** (C4), after the design-split C4 figure and before any held-out C4
   cell. The clause "every active correction and invariant is either shown or listed" became
   "that count does not rise against the base, and the closing line is truthful". Looser: the
   literal clause fails on both builds (213 and 151).
2. **Eighth amendment** (C3, catalogue arm), after the arm read 9 of 10. The denominator became
   the listed records the build's own fresh-session control returns. Looser by one record at
   the time; on the final build nothing is excluded.
   Not self-declared, and listed here because both followed E figures: the **fifth
   amendment** was written after the E figures of four builds had been read and found void
   (the base had timed an error path); it gives each build its own bench and a common ledger
   seed. The **body of the fourteenth** was written after every earlier E run had been read
   and the full-prompt row found to time no delivery; it gives both arms 300 prompts that
   deliver. Neither moves a threshold. Both change what the E rows measure, on both arms.
3. **Twelfth amendment** (B1), after the valid clause read `fail` for Task 7's build. It adds a
   kind-free reading that binds where an item reads `absent`. It could go either way and went
   against the change: the extractor was reverted.
4. **Thirteenth amendment** (`remember` cell), after the 2 of 48 reading. It adds the
   whole-sentence reading. Neither reading has a threshold.
5. **Addendum to the fourteenth amendment** (E's delivery gate), after the first revision-5 run
   failed its gate. "Every full prompt answered on both arms" became "at least 285 of 300".
   Looser, for the base's sake: 1.2.0 answers 299.
6. **Fifteenth amendment** (E), after three E runs had been read. It fixes same-moment copies,
   three runs and the median ratio. It can read more leniently than one run would; every
   single run is committed.
7. **Sixteenth amendment** (F, Codex first clause), after seeing that the base types six
   records from a rollout handed to it by hand. The clause is read on the route a build
   installs by itself. Looser: as registered it is false of the base.
8. **Seventeenth amendment** (F, rule compiler), after the 238 → 239 figure. A held-out
   sentence the design half also holds does not count. Stricter: the last pattern was not
   shipped.

9. **Nineteenth amendment**, after the Result and every figure in it. It changes no rule: it
   says the build was changed after the final reading and which cells are repeated on the
   fixed build. Its **dated note** follows a probe figure on the first fixed build
   (`4617c4d527b399f0`, 13 bad of 384) and records that one fix was narrowed for it. Looser
   for that fix: the narrowed rule protects fewer records than the one first written.

Others were written after the base figures, or after another task's figure, and before the
cells they govern. They are listed because a base figure is a figure:

- **Second amendment**: B1's valid clause is read on the earliest matching row, after seeing
  that the registered scorer reads one valid item as active on the base. Looser for both
  builds alike.
- **Third amendment**, all of it after the base figures: B3's noise clause reads "not above
  the base's 3/30" where the text says "stays 0" (looser), and the registered evaluator binds.
  B2's reword became "0 retirements of any kind" (stricter). B1's loss clause binds by
  `score.py`'s rule and its valid clause by the earliest row. C4 must hold on both the lenient
  and the strict share (stricter). C2 is read on prompts with the same ids. C3's stale-twin
  arm takes the retirement on the store as rewound to each prompt, "so that a read-path fix
  can reach 0" (it favours the candidate). C3's catalogue arm was defined then, with the
  base's 0 of 5 already read. A missing input reads `missing`, never `pass` (stricter).
- **Fourth amendment**: C1 is read once, on Task 4's combined build, after Task 3's ranking
  change alone read 104 → 104 unrelated on held-out. It moved the reading to a later build and
  added the blind pool; the ranking change shipped on an arm that read equal with and without
  it.
- **Ninth amendment**: A1's gate binds on the filters read together, after the base counts
  showed no single noise class reaches 30 %. Looser than a gate on each filter alone. It also sets the durable loss
  allowed to zero on both splits, stricter than the registered 5 %. Its dated
  note, after Task 6's held-out reading, applies the drop test on held-out (stricter: one
  filter dropped) and names a third origin fix that is not submitted to it.
- **Tenth and eighteenth amendments**: inputs staged, and anchors outside a replay skipped.
  They change what the harness reads and no rule. The tenth followed B1 lines that read `fail`
  on a missing input.

## Weaknesses of the measurement

- **The labellers were not independent.** The second labeller had read the four analysis
  reports, which give totals and name about ten items with their labels. `useful`, the label
  C1's second clause counts, had a kappa of 0.136 between the two passes.
- **C4 rests on frozen labels over a minority of what the final build shows.** The blind pool
  for session-start slots failed its control (kappa 0.56 lenient, 0.291 strict) and was not
  used; 167 of the held-out slots the final build fills carry no label. Eleven catalogue lines
  render differently in the two builds and share one label, taken on the candidate's rendering.
- **C1's blind pool passed its control** (kappa 0.866 on unrelated or not, 80 controls) with one
  labeller; 4 of the 157 held-out pairs the final build returns are unscored.
- **Held-out was read more than once.** C1 and C4 on each measured build from Task 4 on; one
  catalogue change (Task 8) was rewritten after its held-out C4 figure had been seen; one
  version of the Spanish forms was dropped on a held-out C1 reading and the narrower one built
  after it; A1 on two builds, with the drop test applied on held-out; the rule compiler's
  held-out half three times, and one of its sentences was in the design half too.
- **A1 passes by one item** (38 against a limit of 38.5) and fails on design (26.6 %) and on
  both splits together (28.4 %).
- **The binding E reading departs from the fifteenth amendment's own condition.** The
  amendment asks for three runs "on a machine with nothing else running". They were taken on
  the owner's working desktop, in use: process start read 6.4 to 8.4 ms p50 where earlier
  runs read 4.4 to 4.7, and another project's test runner was seen minutes after the third
  run. The runs were not repeated. This bears on the rows that pass as well as on those that
  fail: the gated prompt passes at a median of 1.087 with runs of 1.002, 1.087 and 1.122.
- **`served_ok` was not watched.** Loop 8's delivery cells fell from Task 3 on because the
  instrument stopped printing, and nobody read them until the review of this result. Any
  statement of the plan that leaned on `served_ok` after Task 3 leaned on a gated command.
- **E's base arm does less at SessionStart and SubagentStart.** The base's bench writes
  directory and symbol cue rows, so the base delivers no block there. Those two rows compare
  a build that delivers with one that does not.
- **Process start varies by file.** Byte-identical copies of one binary read 3 to 4 ms apart
  at process start depending on the file. Every E reading before the fifteenth amendment is
  exposed to it, in either direction.
- **Earlier E rows were less than their name.** Until harness revision 5 the full-prompt row
  timed a prompt that delivered nothing, on both arms; revisions 1 and 2 were void for other
  reasons (fifth amendment).
- **B1 replays read live files.** Until the eighteenth amendment a replay hashed 15 corrections'
  anchors at their live paths. One labelled item ever fell on such a record (`v1:W02:2342`,
  `old_not_a_fact`, neither a `loss` nor a `valid` item), on the base and the Task 2 builds; of
  the replays still on disk one holds a record retired that way (W02-now #4317 on
  `deb218345d4c700c`, not a labelled item). No B1 rule row could have moved; a store total
  could.
- **B1 figures between 2026-11-12 04:51 and the tenth amendment** were read on fewer sessions
  than the base's and are not readings.
- **The 13 retirements since 1.2.0 in B1 are single-labelled.**
- **F's second clause** was read once, on one machine, in a `codex exec` session, where `Stop`
  does not run. The plugin's own Codex route was not run in a real session.
- **One machine, one person's stores.** Every latency figure is from one Windows desktop and
  its WSL; every store is one person's.

## Open, as measured

- The four items under "Still open on the fixed build", in the section on the final review.
- **Three defects reached the final reading unseen.** Every cell passed on a build that lost
  a typed statement in the usual read order. The cells read what the registration named; the
  probes that found the defects were written by a reviewer afterwards.
- Rule E fails on SessionStart and SubagentStart against a base that delivers nothing there.
  Against the previous build the final one reads no slower beyond the spread. Whether that
  is accepted is a decision for the project's owner; nothing was tuned or reverted for it.

- A no-subject later word typed in another session, while an agent's prompt holds a statement
  retired, picks an older unrelated statement and the pick is not undone (orderprobe `pick`).
  Nothing is served that should not be; a current fact goes unserved until restated.
- A statement an agent's prompt retired stays retired when the user typed anything, or
  `maintain`, `revoke` or `import` acted, before the agent's prompt was found out. `muninn
  doctor` lists it.
- `perf --strict` exits 1 on the Windows machine for the base and for the final build, and 0
  under Linux (section E).
