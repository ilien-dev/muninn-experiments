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
