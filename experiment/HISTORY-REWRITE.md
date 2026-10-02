# History rewrite of 2026-09-14

Before the repository is published, the maintainer's e-mail address was removed from two result
files (`results/pmbench/round8-sonnet/launcher.log` and `canary2.json`: a bridge canary had
quoted the harness's account context). `git filter-repo --replace-text` replaced the address with
`[account e-mail]` in every commit; nothing else changed. Checked on a clone before the refs moved:
the same 105 commits with identical messages, an identical tree at HEAD, and 0 stored objects
containing the address afterwards.

Commit hashes from `19e9e70` onwards changed (27 commits). The full old → new map is
`history-rewrite-map.json`; run manifests and `FROZEN.json` files recorded the old hash that was
HEAD when they ran, and are left as recorded.

## Effect on the timestamp proofs

| proof | commit it names | anchored | after the rewrite |
|---|---|---|---|
| `round8-f173f2d.txt.ots` | `f173f2d` | Bitcoin block 966829 | unchanged |
| `gate3-codex-public-rep5-6313554.txt.ots` | `6313554` | Bitcoin block 966829 | unchanged |
| `instrument-fix-6e1cadb.txt.ots` | `6e1cadb` | Bitcoin block 966832 | unchanged |
| `restart-cd52e86.txt.ots` | `cd52e86` | Bitcoin block 966832 | unchanged |
| `round9-19e9e70.txt.ots` | `19e9e70` | Bitcoin block 966895 | now `d375a26`; re-stamped in `rewrite-2026-09-14.txt.ots` |
| `external-c357381.txt.ots` | `c357381` | Bitcoin block 966933 | now `8d8ca81`; re-stamped in `rewrite-2026-09-14.txt.ots` |
| `gate2-codex-fix-3be3593.txt.ots` | `3be3593` | calendar, pending confirmation | now `742f751`; re-stamped in `rewrite-2026-09-14.txt.ots` |

The four proofs on unchanged commits — including the one that fixes the held-out PM-Bench seeds
(`f173f2d`) — verify against this repository as published. The three on rewritten commits still
prove that the *old* hashes existed at the anchored time; the old objects are kept, private, in a
backup bundle (sha256 below) that can be shown to a reviewer, and the new hashes were stamped again
after the rewrite. Those three pre-registrations (round 9, the external repositories, the Gate 2
Codex fix) are therefore publicly timestamped only from the rewrite date; their order relative to
the results remains visible in the commit sequence, which is not a proof.

Backup bundle (private, not in the repository): sha256 `7f5d374db89e96e94e318a3aba50699e557e7291cabb7f86bce176c118bbb31c`.

# History rewrite of 2026-09-17

Before the repository was first pushed, the maintainer's e-mail address was removed from the
head-to-head pilot transcripts (`results/h2h-pilot/logs/`): Claude Code writes the account's
`session_context` into every session transcript, and the harness copies transcripts. The files had
already been redacted in the working tree (commit "Head-to-head v1 full grid"); `git filter-repo
--replace-text` then replaced the address with `[account e-mail redacted]` in every commit. Checked:
141 commits before and after with identical messages, an identical tree at HEAD, 0 stored objects
containing the address. Five commits changed (`history-rewrite-map-2026-09-17.json`), all after the
pilot commit `a5e772a` → `b8ded74`.

The backup bundle was not written before the rewrite (the command failed on a bad flag and the rewrite
ran anyway). The original commits were rebuilt by applying the inverse replacement to a clone: the
four rewritten commits that held the address came back with their original hashes
(`a5e772a`, `456ab60`, `c72c3fd`, `931e1c1`), and those objects are kept, private, in a bundle
(sha256 `b28d87525cdd8481f3ef09654af67b9f3d2799acaf826e6e1dd8577bdcec240d`)
that can be shown to a reviewer.

| proof | commit it names | after the rewrite |
|---|---|---|
| `h2h-full-a5e772a.txt.ots` | `a5e772a` (full v1 grid registration) | now `b8ded74`; re-stamped in `rewrite-2026-09-17.txt.ots` |
| `h2h-v2-c72c3fd.txt.ots` | `c72c3fd` (v2 registration) | now `7b0d376`; re-stamped in `rewrite-2026-09-17.txt.ots` |

Both old proofs were still waiting for Bitcoin confirmation at the rewrite; once confirmed they prove the
old hashes existed at that time, and the bundle shows those hashes differ from the new ones only by the
address.

# License rewrite of 2026-09-17

Before the repository was first published, every commit declared the MIT license: `Cargo.toml`
(`license = "MIT"`) and `plugin/.claude-plugin/plugin.json` (`"license": "MIT"`) from the first
commit, and a `LICENSE` file with the MIT text from the 0.2.0 release commit. The project is licensed
under AGPL-3.0-only with the attribution terms in `NOTICE`. A published history would have offered
each earlier snapshot under MIT, so the history was rewritten while the repository was still private
(one collaborator, no forks, no releases, no crate published): nobody ever received a copy under MIT.

`git filter-repo` changed, in every commit: those two manifest lines to `AGPL-3.0-only`; the MIT
`LICENSE` text to the AGPL-3.0 text; the README's one-word license section (three commits) to
`AGPL-3.0-only`. The first commit gained the AGPL-3.0 `LICENSE`, so every commit carries it. The
release commit's subject lost the word "MIT"; abbreviated hashes quoted in commit messages were
rewritten to the new ones by `git filter-repo`. Checked on a clone before the refs moved: 145 commits
before and after, identical authors and dates, messages identical apart from those edits, an
identical tree at HEAD, and no commit outside third-party fixtures and recorded experiment outputs
declares MIT. Every commit hash changed; the old → new map is
`history-rewrite-map-2026-09-17-license.json`, and tags were moved with their commits.

Recorded experiment outputs are left as they were produced. Gate 3's `revoke-license` cells ran on
checkouts whose `Cargo.toml` still said MIT (`GATE3.md`, `PREREGISTRATION.md`); in the rewritten
history those checkouts say `AGPL-3.0-only`, so a replay from the public history is not the same
input. The original commits are kept, private, in a bundle (sha256
`207b4f23efb9209fe95b953e94eead22a6cb4d78a876d53b1cfbf8192b36052f`) that can be shown to a reviewer.
Note also that the `revoke-license` oracle rejects any text containing `gpl-3.0`, which
`agpl-3.0` contains: a new run of that scenario on this repository needs a different oracle.

Every timestamp proof in `prereg-stamps/` names a commit whose hash changed. Each proof still shows
that its old hash existed at the anchored time; the bundle shows the old commits differ from the new
ones only by the edits above. The new hash of every named commit (and of the commits named by
`rewrite-2026-09-14.txt` and `rewrite-2026-09-17.txt`, which are the same commits) is listed in
`rewrite-2026-09-17-license.txt` and stamped in `rewrite-2026-09-17-license.txt.ots`, so the
public history is timestamped from the date of this rewrite.

# History rewrite of 2026-09-26

Before 308 unpublished commits were pushed, the maintainer's e-mail address was removed from
them. Claude Code writes the account's address into every session's context, and the raw
head-to-head transcripts committed under `results/*/logs/*.transcript.jsonl` carried it: 5 115
files. `git filter-repo --replace-text` replaced it with `[account e-mail]`, limited to
`origin/master..master`, so no published commit changed. Checked before pushing: the published
history is an ancestor of the new `master`, the 308 commits keep their messages, the tree
differs from the old one in those 5 115 lines and nothing else, and 0 objects in the pushed range
contain the address.

305 of the 308 commits have new hashes (the first three held no transcript). The old → new map is
`history-rewrite-map-2026-09-26.json`. Hashes quoted in `PREREGISTRATION.md` for these
commits (for example `182d4e84`, `2c2eeafa`, `bf40a75d`) are the old ones and are left as
recorded. The old objects are kept, private, in a backup bundle (sha256 prefix `88e2465900cf8d3a`).
