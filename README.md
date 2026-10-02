# Muninn experiments

The experiments behind the figures in [Muninn](https://github.com/ilien-dev/muninn): pre-registrations,
gate reports, harnesses and raw results. Until Muninn commit
[`e3bf0f0`](https://github.com/ilien-dev/muninn/tree/e3bf0f0ef81c594bb5071913ee29ee911e50b902/crates/muninn-bench)
they lived in that repository under `crates/muninn-bench/experiment/` and
`crates/muninn-bench/pmbench/`. This repository is a byte-for-byte copy of those two folders at
that commit; their earlier history is in the Muninn repository.

`experiment/PREREGISTRATION.md` records each experiment before its first run, and
`experiment/results/` holds what the runs wrote. Muninn 1.0.1 shortened some result paths so the
plugin installs on Windows; `experiment/results/RENAMES.tsv` maps each one to its old name.

The `muninn-bench` binary that runs the Rust experiments stays in the Muninn repository, together
with the rule corpus its CI gates read (`crates/muninn-bench/corpora/`).

License: AGPL-3.0-only, as Muninn.
