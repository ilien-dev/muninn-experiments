# Reproducing every number

One command per published figure. Each entry says what the command needs, what it prints,
and where the frozen inputs live. Commands run from the repository root after
`cargo build --release`. Grids that call a model need a Claude Code login (`claude`) or a
Codex login (`codex`); the cost and wall time quoted are what the recorded runs measured.

## Inputs that are public and inputs that are not

| input | where | public |
|---|---|---|
| scenarios, seed records, oracles, task prompts | `revocation/`, `cues/`, `tasks.json` | yes |
| the experiment runner and every analysis script | `../src/experiment.rs`, `revocation/analyze.py`, `pmbench/*.py` | yes |
| raw results of every grid (cell logs, patches, score files) | `results/` | yes |
| PM-Bench (benchmark, scorer, released week) | `github.com/genglinliu/PMBench` at commit `e1093c4` | yes |
| the frozen seed transcript used by Gates 2–4 and the boot/cue grids | outside the repository, sha256 `223dcf4d…fa895`, 22 559 233 bytes | **no** — this project's own private sessions |
| pre-registration timestamps | `PREREGISTRATION.md` (git history) and `prereg-stamps/*.ots` (OpenTimestamps, Bitcoin-anchored) | yes |

Grids marked *private seed* below can be re-run only with a seed transcript of your own;
the public-seed Gate 3 grid exists for that reason.

## Latency and budget contracts (no model)

```sh
cargo run --release -p muninn-bench -- perf --strict          # hook p95s at 20 000 records, fails above the contract
cargo run --release -p muninn-cli --features exact-tokens -- init --check-budget   # boot block ≤ 1 000 tokens
MUNINN_FAULT_REPS=200 cargo test -p muninn-cli --release --test fault             # 15 fault scenarios × 200
```

## Gate 1 — rule classifier (no model)

```sh
./target/release/muninn-bench rules --strict --holdout crates/muninn-bench/corpora/claude-md/holdout2.txt --labels crates/muninn-bench/corpora/claude-md/labels2.jsonl
```
Corpus, labels and report: `../corpora/claude-md/GATE1.md`. `--strict` exits non-zero when
the contract is not met, which is how CI guards it.

## Gate 5a — do the compiled controls actually refuse the call? (no model)

```sh
# the gate run (set C): block 0.920, false block 0.000
./target/release/muninn-bench enforce --cases crates/muninn-bench/corpora/claude-md/enforce_cases_holdout3.jsonl
./target/release/muninn-bench enforce --cases <that file> --json   # every case, label, channel, verdict
cargo test -p muninn-cli --test enforce                            # the mechanism, in CI
```
Cases, labels and report: `../corpora/claude-md/GATE5A.md`. Each case builds a throwaway
project holding one corpus rule, runs `compile` → `apply --yes`, and feeds a harness-shaped
payload to `muninn hook PreToolUse`. No model, no network, about a minute.

The development set (`enforce_cases.jsonl`) and the two held-out sets that failed
(`enforce_cases_holdout.jsonl`, `enforce_cases_holdout2.jsonl`) run the same way. Their
registered results are in `results/gate5a-holdout{1,2}/summary.txt`; re-running them on
today's binary gives a different, better number, kept beside it as `rerun-after-fixes.txt`
and not reported as a gate result.

## Gate 2 — literal delivery (private seed, claude-sonnet-5, 90 cells)

```sh
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/tasks.json --jobs 3 --out <dir>
./target/release/muninn-bench experiment --rescore --out <dir>
```
Report `GATE2.md`; raw `results/run2/`. Codex replication: `--config crates/muninn-bench/experiment/tasks-gate2-codex.json` (`results/gate2-codex/`).

## Gate 3 — F1 filter

Private seed, two families (`GATE3.md`, `results/gate3-sonnet/`, `results/gate3-haiku/`):
```sh
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/revocation/tasks-revocation.json --jobs 3 --out <dir>
python3 crates/muninn-bench/experiment/revocation/analyze.py <dir>
```
Codex / gpt-5.6-sol (pre-registered, `results/gate3-codex/`):
```sh
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/revocation/tasks-revocation-codex.json --jobs 3 --out <dir>
```
Public seed, no private input at all (pre-registered, `results/gate3-public/`):
```sh
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/revocation/tasks-revocation-public.json --jobs 3 --out <dir>
```
Public seed on three external repositories chosen by rule (`results/gate3-ext-{gin,vue,python}-{codex,sonnet}/`):
```sh
gh repo clone gin-gonic/gin <dir>/gin -- --depth 1        # likewise vuejs/vue, TheAlgorithms/Python; commits in the task files
# edit "repo" in each task file to your clone path, then:
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/revocation/tasks-external-gin-codex.json --jobs 3 --out <dir>
```

## Gate 4 §1 — cues, expansion, boot vehicle (private seed)

```sh
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/cues/tasks-cues.json --jobs 3 --out <dir>            # first grid
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/results/gate4-cues-v2/tasks.json --jobs 3 --out <dir>  # expansion
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/results/boot-vehicle/tasks.json --jobs 3 --out <dir>   # boot vehicle
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/cues/tasks-cues-v2-rep5.json --jobs 3 --out <dir>      # five-run replication
./target/release/muninn-bench experiment --config crates/muninn-bench/experiment/cues/tasks-boot-vehicle-rep5.json --jobs 3 --out <dir> # five-run replication
```

## Gate 5b — does the control change what the agent does?

The grid is regenerated from its committed source, and the instrument is checked before any
cell runs: every fixture must build, every oracle must fire on the forbidden action and stay
silent on the safe alternative, and the compiled hook must deny the call. Run 1 of this gate
was void because none of that was true; the check costs no model call and would have caught it.

```sh
python3 crates/muninn-bench/experiment/rules/scenarios.py              # fixtures + oracles
python3 crates/muninn-bench/experiment/rules/check_instrument.py       # must print INSTRUMENT: PASS
python3 crates/muninn-bench/experiment/rules/forced.py                 # the manipulation-check grid
```

The registered contrast (`written` vs `compiled`), the manipulation check, and the mechanism
contrast that separates the rule from the control (`norule` vs `control-only`):

```sh
cargo run --release -p muninn-bench -- experiment \
    --config crates/muninn-bench/experiment/rules/tasks-rules.json \
    --out crates/muninn-bench/experiment/results/gate5b-run2 --jobs 4
cargo run --release -p muninn-bench -- experiment \
    --config crates/muninn-bench/experiment/rules/tasks-rules-mechanism.json \
    --out crates/muninn-bench/experiment/results/gate5b-mechanism --jobs 4
python3 crates/muninn-bench/experiment/rules/analyze.py \
    crates/muninn-bench/experiment/results/gate5b-mechanism
```

`analyze.py` prints the violation rate per arm, the pre-registered bootstrap difference, and
the enforcement ledger — which is the only evidence inside a grid that the control was live
rather than merely installed.

## Head-to-head — cost and wall clock per cell

```sh
python3 crates/muninn-bench/experiment/h2h/cost_analysis.py \
    crates/muninn-bench/experiment/results/h2h-v2          # and .../h2h-v1
```

Prints, per arm, the median cost, wall clock and turn count over the replacement cells, then the
`muninn-latest / claude-mem` ratio for each, paired by (run, task) with a 95 % bootstrap CI, and
the same table split by outcome — because an arm that solves more cells finishes sooner, and the
split is what shows whether that explains the difference. Exploratory on the v1 and v2 grids,
which were registered for detection.

The grid that registered wall clock as its outcome is `results/h2h-v3-clock/`, and it is the one
that matters, because it is the only one that ran cells **one at a time**:

```sh
python3 crates/muninn-bench/experiment/h2h/run_h2h.py \
    --out crates/muninn-bench/experiment/results/h2h-v3-clock \
    --arms muninn-latest,claude-mem --runs 3 --jobs 1 \
    --seed-phrasings crates/muninn-bench/experiment/h2h/v2/seed_phrasings.json
```

`--jobs 1` is the whole point: with cells running concurrently the v1 and v2 grids agreed on a
ratio near 0.59, and serially it is 0.972 [0.681, 1.368]. The effect was contention, not the
tools `[Z6]`. Any future grid whose outcome is a clock runs serially.

## Native memory — why the head-to-head arm cannot run

```sh
bash crates/muninn-bench/experiment/h2h/competitors/native/probe.sh <out dir>
```

Three cheap sessions. On Claude Code 2.1.268 it reports
`auto_memory_available_in_print_mode: false` and 0 memory files written, which is why the
`native` arm is registered as blocked rather than scored. Re-run it against a later version.

## Supersession loops — held-out measurement and the two closed routes

```sh
python3 crates/muninn-bench/experiment/loop1/eval_mechanism.py --muninn ./target/release/muninn \
    --phrasings crates/muninn-bench/experiment/loop7/heldout_phrasings.json \
    --scenarios crates/muninn-bench/experiment/loop7/scenarios.json --order adjacent
cargo run -p muninn-capture --example supersede_probe -- \
    crates/muninn-bench/experiment/loop6/heldout_phrasings.json --misses      # [Z5]
cargo run --release -p muninn-bench --example name_cosine -- \
    crates/muninn-bench/experiment/loop5/heldout_phrasings.json               # [Z4]
```

Run `eval_mechanism.py` with `--order blocks` as well: the guard that loop 7 shipped shows up
there and nowhere else, and the change loop 7 withdrew showed up only in `adjacent` on the
sets it was developed on.

## Gate 4 §2 — compaction survival (no model)

```sh
python3 crates/muninn-bench/experiment/decay_probe.py --reps 100      # 10 invariants, 100 forced compactions; writes results/decay-probe/
```

## Gate 4 §3 — PM-Bench

Rounds 4–7 (`GATE4.md`, `results/pmbench/round4..7/`):
```sh
bash crates/muninn-bench/pmbench/run_round4.sh <PMBench checkout> <out dir> 3 claude-sonnet-5
python3 crates/muninn-bench/pmbench/aggregate_round4.py <out dir>
```
Round 8 — held-out weeks, store ablation, second family, one bridge (`results/pmbench/round8-*/`):
```sh
python3 crates/muninn-bench/pmbench/run_round8.py --pmbench <PMBench checkout> --out <dir> \
    --prereg-commit f173f2dc75625b89f7b0543004ed7cf44c51b399 --model claude-sonnet-5 --bridge claude --port 30002
python3 crates/muninn-bench/pmbench/run_round8.py --pmbench <PMBench checkout> --out <dir-codex> \
    --prereg-commit f173f2dc75625b89f7b0543004ed7cf44c51b399 --model gpt-5.6-sol --bridge codex --port 30003
python3 crates/muninn-bench/pmbench/analyze_round8.py sonnet=<dir> codex=<dir-codex>
```
Round 9 — shadow store (`results/pmbench/round9-*/`): the same launcher with `--shadow --weeks heldout --arms muninn_store,plain_store`.
The held-out seeds are a function of the pre-registration commit hash (`run_round8.py`,
`heldout_seeds`); the launcher regenerates and validates them with PM-Bench's own tools and
writes `weeks/MANIFEST.json` with their hashes. Grids resume with `--resume` (complete runs kept, partial ones removed, refused if a frozen hash changed); experiment grids re-run infrastructure errors with `--rerun-errors --config <the grid's own file>` and rescore with `--rescore --config <same>` (the runner refuses another file). Every run writes a `*.manifest.json` with the
hashes of the scaffold, the scorer, the scenario, the muninn binary and the bridge's canary
answer.

## Checking the pre-registration timestamps

```sh
ots verify crates/muninn-bench/experiment/prereg-stamps/<file>.ots     # needs a Bitcoin node or the public calendars
git log --format='%H %cI %s' -- crates/muninn-bench/experiment/PREREGISTRATION.md
```
An `.ots` file is "pending" until the calendar's Bitcoin transaction confirms (hours); `ots
upgrade <file>.ots` completes it afterwards.

## Loops 8 and 9 — the repository as a second signal (no model)

Two held-out sets, four arms, two orders, every cell deterministic. `talk` is the
conversation alone, `code` is the first message of each pair plus a commit, `both` is an
ordinary week, `noise` is the precision control.

```sh
cargo build --release
E=crates/muninn-bench/experiment
for L in loop8 loop9; do for o in adjacent blocks; do for arm in talk code both noise; do
  python3 $E/loop8/eval_all.py --muninn target/release/muninn \
      --arm $arm --order $o --commit-msg opaque \
      --phrasings $E/$L/heldout_phrasings.json --scenarios $E/$L/scenarios.json \
      --out /tmp/$L-$arm-$o.json
done; done; done
```

The controls that changed what the engine does, and are worth re-running before trusting it:

```sh
# the commit subject names the new value: it answers the question by itself (30/30 on loop 9)
... --commit-msg names
# the old value survives in a file no commit touches: the disappearance rule alone dies here
... --survivor
# unrelated commits between the change and the maintain that reads it
... --filler 20
```

## Head-to-head v4 — the decisions are also in the code

```sh
cd crates/muninn-bench/experiment/h2h
python3 run_h2h.py --out ../results/h2h-v4-code   --runs 3 --jobs 2 \
    --arms muninn-loop8,claude-mem --code --seed-phrasings v2/seed_phrasings.json
python3 run_h2h.py --out ../results/h2h-v4-nocode --runs 3 --jobs 2 \
    --arms muninn-loop8,claude-mem        --seed-phrasings v2/seed_phrasings.json
python3 analyze_v4.py ../results/h2h-v4-code ../results/h2h-v4-nocode
```

`--code` adds, identically for every arm, one tracked file per decision in the *seeding*
checkout and a commit with an uninformative subject when the decision changes. Task cells get
the base checkout, as in every other head-to-head: a cell whose repository held the current
value would be answerable by `grep`.

## Loop 10 — precision: what a later message must not take with it (no model)

```sh
for p in pairs pairs2 pairs3; do
  python3 crates/muninn-bench/experiment/loop10/eval_precision.py \
      --muninn target/release/muninn \
      --pairs crates/muninn-bench/experiment/loop10/$p.json --out /tmp/$p.json
done
```

`pairs3.json` is the one that carries the failure mode on purpose — the later message using
*migration*, *replacement*, *cambios*, *swap*, *switch* or *rollback* as an ordinary noun.

## Loop 11 — the value that is a number (no model)

```sh
for arm in talk code both noise; do
  python3 crates/muninn-bench/experiment/loop8/eval_all.py --muninn target/release/muninn \
      --arm $arm --order adjacent --commit-msg opaque \
      --phrasings crates/muninn-bench/experiment/loop11/heldout_phrasings.json \
      --scenarios crates/muninn-bench/experiment/loop11/scenarios.json --out /tmp/l11-$arm.json
done
```

## The same input, the same store (no model)

```sh
python3 crates/muninn-bench/experiment/loop8/same_input_same_store.py \
    --muninn target/release/muninn --stores 3
python3 crates/muninn-bench/experiment/h2h/reproducible.py /tmp/muninn-h2h/<grid>   # per arm
```

## Reading a head-to-head for something other than the pass rate

```sh
python3 crates/muninn-bench/experiment/h2h/delivered_vs_used.py <results dir>   # memory or agent
python3 crates/muninn-bench/experiment/h2h/context_cost.py     <results dir>   # window taken
```
