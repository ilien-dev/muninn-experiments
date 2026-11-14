# usage-v4 harness

The measurement harness for the pre-registration "usage-v4" (last section of
`../../PREREGISTRATION.md`, with its three amendments). One entry point per section; each takes
`--bin <muninn.exe>`, `--split design|heldout|all` and `--commit <sha>` (the commit the build was
made from; pass it on every cell), prints its counts as JSON and merges them into
`counts/<section>_<build>.json`, where `<build>` is the first 16 hex digits of the binary's
sha256. Counts hold numbers, record ids and label codes only; `common.write_counts` refuses to
write a file that contains a path, a user name or a project name, and refuses to write at all when
any step of the run failed (non-zero exit, timeout, unexpected output, an error on stderr).

Environment: `MUNINN_USAGE_FIXTURES` points at the private fixture root (store copies, item
texts, frozen labels; nothing from it is committed). `MUNINN_USAGE_WORK` is the scratch directory
(default `$MUNINN_USAGE_FIXTURES/work/usage-v4`). Machine paths (project checkouts, the WSL share,
project-to-label map, private names to refuse) are in `$MUNINN_USAGE_FIXTURES/usage-v4.local.json`.
Python 3.12 with `sqlite3`, git, cargo.

```sh
B=<candidate muninn.exe>; BASE=b93d2f5c222c0424; C=<commit>
python -I a_extract.py  --bin $B --src <the build's source tree> --commit $C   # A; builds extract_dump from --src
python -I b_retire.py   --bin $B --commit $C [--parts b1,b2,b3] [--jobs 6]      # B
python -I c_delivery.py --bin $B --commit $C --against $BASE [--parts c12,c3,c4,c5]   # C; --against gives C2
python -I d_removals.py --bin $B --commit $C [--against $BASE]                 # D
python -I e_perf.py     --bin <base exe> --against $B --commit $C \
    --bench-base-src <base tree> --bench-src <candidate tree>   # E, interleaved, machine idle (or --bench-base / --bench paths)
python -I verdict.py $BASE <candidate sha16> [--split heldout]                 # one verdict per rule
python -I make_baseline.py $BASE                                               # regenerates BASELINE.md
```

B1 replays six corpora with usage-v1's `replay.py`: 1,357 s on the base with 6 jobs, and about
1.5 GB of replayed stores under `$MUNINN_USAGE_WORK/b_retire/rp/<build>/`. Each corpus writes a
`<name>.done.json` marker when its replay finishes; scoring refuses corpora without one, so
`--score-only` rescans an earlier, finished run without replaying.

E (harness revision 3, `harness_rev` in the counts) times each build with a `muninn-bench` of its
own source, so each runs on a store its own code created. The base's bench is built from a copy of
the base tree in the work directory with the candidate bench's 8,336-row `fire_ledger` seed added,
so the two seed the same workload; the `workload` key records what was done, and if the two ever
differ the comparison is each build's own contract run, which `verdict.py` prints next to the E
rows. Every run is checked through the store's heartbeat (every hook finished ok, no error) and a
miss blocks the counts. Stop gives each build its own W02 copy and reports the migrating first
write open apart (`first_write_open_ms`) and checks each copy's schema against the one the build
itself creates (`init` in the work directory) and every timed Stop in the copy's heartbeat.
Revision 3 adds: workloads compared build against build by the seed rows' count and sha256
(`seed_rows_and_fingerprint`), each bench's sources hashed (`bench_sources`), and a must-deliver
case (`--must-deliver-item`, default P026, a design item) run on both builds' own migrated W02
copies, which must deliver on both. `verdict.py` reads E only from revision-3 counts; revision-2
counts read `missing`. `e_perf.py --parts gates` runs the must-deliver case and the schema probe
without timing, and `check_e_gates.py <base> <candidate>` checks the gates on doctored counts.

`--labels first` scores against the first labeller instead of the frozen labels and writes
`counts/<section>_<build>-first.json`; on the base binary it reproduces the analysis figures,
which is how the wrappers were checked. `splits/` holds the design and held-out ids, and
`DESIGN_ITEMS.md` says which private files an implementer may read. `BASELINE.md` has the base
figures and marks which reading of each rule is binding.

## Blind-label pool (`c_pool.py`, fourth amendment)

```sh
python -I c_pool.py export --arms <base sha16> <arm sha16> ... [--bins <exe> ...] [--short-prompts <ids>]
python -I c_pool.py ingest --labels $MUNINN_USAGE_FIXTURES/out/usage-v4/pool/labels.jsonl
python -I c_delivery.py --bin <exe> --labels final+pool --parts c12      # counts in <build>-pool
```

`export` collects the (prompt, record) pairs any arm returned that no frozen label covers, adds a
seeded sample of at least 60 frozen-labelled pairs the base returned as controls (stratified by
label), shuffles them and writes, under `$MUNINN_USAGE_FIXTURES/out/usage-v4/pool/` (private),
`labelling.jsonl` (opaque ids, prompt and record text, no arm, build, split or label),
`key.json` (kept from the labeller), `LABELLING.md` and `export.json` (counts). `ingest`
refuses a file with a missing or invalid label, measures agreement on the controls, writes the
labels as `out/usage-v4/labels/delivery_pool.jsonl` beside the frozen file (which is never
written) with both sha256 in `delivery_pool.ingest.json`, and marks the extension unusable when
the control kappa on unrelated-or-not is below 0.6. `--labels final+pool` uses frozen plus
extension and refuses an unusable or changed extension; without it nothing changes. `verdict.py`
reads C1 from the `-pool` counts of both builds when they exist, says which label set it used, and
prints how many returned pairs are still unscored.

Session-start slots (seventh amendment) go into the same pool as their own item type: `export`
replays the labelled session starts through each arm with an exe, exports the (store, block or
catalogue line, record id) slots no frozen session-start label covers, plus at least 40 (default
48) labelled slots the base shows as controls, and `ingest` gates them apart (kappa on
worth-its-slot-or-not below 0.6: `out/usage-v4/labels/event_pool.jsonl` is marked unusable and C4
reads frozen labels only, with the unlabelled count). `c_delivery.py` also records, per store, whether
the catalogue's closing line claims the list is whole and whether that is true
(`c4.whole_list_today`; a word-for-word twin of a listed record counts as covered). `verdict.py`
reads C4 as amended: corrections and invariants neither shown nor listed do not rise against base,
the closing line is truthful, and the literal count is printed.

C3's catalogue-only arm (eighth amendment) is scored on the listed records that the build's own
fresh-session control returns (`returned_by_fresh_control`, `same_session_of_those`); the others
are counted in `excluded_not_returned_fresh` with their ids and printed by `verdict.py`. Counts
from before that change read `missing` for this arm until `c_delivery.py --parts c3` is rerun.
`c_delivery.py --counts-out <dir>` writes counts to another directory (used for checks).

## Staged inputs (`inputs.py`, tenth amendment)

The harness used to read some inputs straight from the machine: the transcripts usage-v1's replay
reads for B1 (from the stores' `transcript_ref`, i.e. the live transcripts folder and the WSL
share), the project repositories B1 clones, the transcripts of the extraction items (A, which
re-copied a transcript whenever its size changed), and the transcripts the W02 copy's session log
names (read by `Stop` in E). Transcripts that left the disk silently shrank B1's corpora. Now
`python -I inputs.py stage` copies each of them once into `$MUNINN_USAGE_FIXTURES/fixtures/inputs/`
(directory per original-path hash, file name kept; a manifest with size and sha256, private) and
freezes them; project repositories are staged as no-checkout clones. A, B1 and E read only the
staged copies. `inputs.py check` prints counts per group. A run whose staged copy is gone or
altered records `status: "missing input"` (B1, A) or refuses to write (E), and `verdict.py` prints
those rules as `missing`, never `fail`. Inputs that were already gone when staging ran are counted
as `unrecoverable`; C, D and B2/B3 read only files under the fixture root and this directory.

## Anchors outside a B1 replay (`b1_replay.py`, eighteenth amendment)

A record anchored to an absolute path outside the replay directory used to be hashed and
validated where the path points, a live file on the machine. `b_retire.py` now runs usage-v1's
`replay.py`, unchanged, under `b1_replay.py`, which clears the stored hash of each such record
before every `maintain` and when the replay ends, so the validator skips it. The count per corpus
is in the counts (`replay.<corpus>.anchors_outside_skipped`), and each store total carries
`retired_anchor_changed`. B1 is compared only between replays made under this runner.

## E, harness revision 5 (fourteenth amendment)

The full-prompt row of revisions 1 to 4 timed a prompt that delivered nothing. `e_perf.py` now
gives the base bench copy the candidate bench's `full_prompts` and `run_prompts` (taken from
`--bench-src`, which is therefore required), counts in every bench store the prompts of session
`b` that were given a block (`full_prompts_delivered_per_run`), and fails the run when either arm
has fewer than its 300 runs or when the store check's own prompt delivers nothing.
