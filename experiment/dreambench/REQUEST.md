Subject: External-system condition for DreamBench-SWE v2.1 — Muninn (local, deterministic memory engine)

Hello,

I maintain Muninn, an open-source local memory engine for coding agents (SQLite + FTS5, no
server, literal records with provenance, retired facts never served). DreamBench-SWE is the
benchmark that matches what it does, and I would like to measure it under your protocol
rather than under my own.

From the public v2.0.5 tree and the v2.1 release artifact I understand that session-3
scoring needs the hidden pytest oracles and that 25 of the 60 confirmatory traps start from
fixture commits the public `build_env.py` cannot regenerate. Would you consider any of:

1. the reviewer package (`package_artifact.py --private`: oracles and reference solutions)
   and the fixture repositories for the 11 `initial_commit` values, under whatever terms you
   use for reviewers;
2. the v2.1 synthetic conformance corpus, so an external policy can be checked against the
   conformance lock before a run;
3. a pre-registered slot for a `MuninnPolicy` condition (a `MemoryPolicy` subclass: `write()`
   ingests the sanitized episode into a per-run store, `read()` returns at most 6 items /
   1 200 tokens by lexical recall on the instruction) run on your infrastructure with a
   concurrent B0 — I would submit the policy as a pull request and accept whatever result
   your analyzer reports.

Everything I would publish about the run would be your analyzer's output, cited to your
release. Thank you for the care that went into the artifact; the freshness and history
reconstruction guards are the reason I would rather run under your protocol than reproduce
it loosely.

Best regards,
<maintainer>
