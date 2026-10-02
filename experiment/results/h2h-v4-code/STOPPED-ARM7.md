# The seventh arm, stopped after fifteen cells

`muninn-floor`, pinned to `37afc7ecabf7cb18`, registered as "v4 seventh arm: a block stops
when the matches stop". Its fifteen completed cells are in `stopped-arm7-muninn-floor.jsonl`
and are **not a result**: the build it pinned is identical to the build before it on the path
the hooks take.

The floor it added lives in `recall::deliver`, which the hooks never call —
`hook::deliver_fused` fuses `recall::recall`'s list with the cues and renders that. The
offline harness probed `muninn recall`, measured `deliver`, and reported a change that reached
no cell. Re-run through the real `UserPromptSubmit` hook the two builds return the same
records, the same counts and the same token totals.

The blocks its fifteen cells received said so first: 6.7 records and 4.0 commit records per
cell, against 7.3 and 4.0 for the arm before it. It was stopped there rather than spend three
more hours re-measuring an unchanged engine.

See `../../PREREGISTRATION.md`, "The seventh arm was stopped, and why", and the eighth arm
registered under it.
