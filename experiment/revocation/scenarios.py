#!/usr/bin/env python3
"""Revocation grid (plan, Phase 4 §6a; modelled on [K7]): ten policies, each with a
retired value and, in eight of them, a replacement. Emits seed.jsonl (records for the
store) and tasks-revocation.json (one task per scenario). Every value was checked to be
absent from the repository at base_ref (git grep, 2026-09-13)."""
import json, sys

T0 = 1789100000000  # 2026-09-11
S = [
 # slug, topic, old value, new value (None = revoked without replacement), how old was retired, trust origin
 ("compression", "the transport compression codec", "gzip", "zstd", "superseded", "user_said"),
 ("cache-eviction", "the cache eviction policy", "LFU", "LRU with a 300-second TTL", "superseded", "user_said"),
 ("password-hashing", "the password hashing algorithm", "bcrypt", "argon2id", "superseded", "review_accepted"),
 ("tls-backend", "the TLS backend", "openssl", "rustls", "superseded", "review_accepted"),
 ("wire-format", "the wire serialisation format", "msgpack", "cbor", "superseded", "user_said"),
 ("async-runtime", "the async runtime", "async-std", "tokio", "reverted", "user_said"),
 ("version-scheme", "the version numbering scheme", "calver", "semver", "revoked", "user_said"),
 ("license", "the source license", "GPL-3.0", "Apache-2.0", "superseded", "user_said"),
 ("tls-verification", "TLS certificate verification in development builds", "certificate verification disabled in dev builds", None, "revoked", "user_said"),
 ("internal-http", "plain HTTP for internal hosts", "plain http allowed for internal hosts", "https everywhere, no plaintext exception", "superseded", "review_accepted"),
]

def rec(kind, subject, obj, body, origin, created, invalid=False, reason=None):
    return {"kind": kind, "subject": subject, "relation": "is", "object": obj, "body": body,
            "origin": origin, "session_id": "seed-revocation", "created_at": created,
            "invalid": invalid, "invalid_reason": reason}

seed, tasks = [], []
for i, (slug, topic, old, new, how, origin) in enumerate(S):
    subj = f"policy.{slug}"
    t_old = T0 + i * 3_600_000
    t_new = t_old + 1_800_000
    old_body = f"user: for {topic} we go with {old}.\n"
    seed.append(rec("decision", subj, old, old_body, "user_said", t_old, invalid=True, reason=how))
    if new is not None:
        # the replacement never names the retired value: the oracle's "old absent"
        # must measure the filter, not what the agent copied from the new record
        nb = {"user_said": f"user: change of plan — {topic} is now {new}.\n",
              "review_accepted": f"review comment accepted: use {new} for {topic}.\n",
              }[origin]
        seed.append(rec("decision", subj, new, nb, origin, t_new))
    else:
        seed.append(rec("correction", f"correction:seed#{i}", f"the {topic} exception is withdrawn", f"user: forget the {topic} exception, it is withdrawn with no replacement: verify certificates everywhere, no dev-build special case.\n", "user_said", t_new))
    f = f"docs/policies/{slug}.md"
    prompt = (f"Create {f} with a one-paragraph statement of this project's current recorded decision on {topic}. "
              "Use only the project's recorded decisions; if nothing current is recorded, write that nothing is recorded. "
              "Do not invent a value and do not describe alternatives that were retired.")
    flat = f"flat=$(tr '\\n' ' ' < {f} | tr 'A-Z' 'a-z')"
    old_l = old.lower()
    checks = [f"set -e; f={f}; test -f $f; {flat}", f"! echo \"$flat\" | grep -qF '{old_l}'"]
    if new is not None:
        # the replacement's key term, language-neutral: "https everywhere" is written
        # as "HTTPS en todo" by a Spanish-speaking agent, so only the token that cannot
        # be paraphrased is required
        key = new.lower().split(',')[0].split(' with')[0].strip()
        if slug == "internal-http":
            key = "https"
        checks.append(f"echo \"$flat\" | grep -qF '{key}'")
    tasks.append({"id": f"revoke-{slug}", "inferable": False, "scenario": {"old": old, "new": new, "retired_by": how},
                  "prompt": prompt, "oracle": "; ".join(checks)})

with open("seed.jsonl", "w") as fh:
    for r in seed:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
cfg = json.load(open("../tasks.json"))
cfg.update({"arms": ["off", "unfiltered", "literal"], "runs": 3, "seed_records": "crates/muninn-bench/experiment/revocation/seed.jsonl", "tasks": tasks})
json.dump(cfg, open("tasks-revocation.json", "w"), indent=1, ensure_ascii=False)
print(len(seed), "records,", len(tasks), "tasks")
