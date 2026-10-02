# Project rules

- Never force-push to `main`.
- You MUST NEVER run `rm -rf` targeting `/`, `~`, `$HOME`, `.`, `..`, or `*`.
- NEVER use `--no-verify` when committing or pushing.
- NEVER use `git add -A` or `git add .` — these sweep up changes from other agents.
- Do NOT modify `generated/manifest.json` — the server manages it.
- Never run a build with `sudo`.
- NEVER commit `.env` to git.
- Never run the full test suite — it takes hours. Run targeted tests only.
