#!/usr/bin/env python3
"""Cue experiment (plan, Phase 5 §8a; Gate 4 condition 1): eight decisions anchored to
files of the repository at base_ref. Each names a token (absent from the repository)
that the change to that file must carry. The task prompt names the file and the
change, never the token, and shares as few words as possible with the record, so a
lexical match is unlikely and the delivery has to come from a cue (dir / symbol) fired
by touching the file. Emits seed.jsonl and tasks-cues.json."""
import json

T0 = 1789100000000
S = [
 # path, slug, task (names the area, never the file), record body (never names the file or the task's words), token
 ("crates/muninn-core/src/db.rs", "busy-cap",
  "in the core crate, give the database busy handler a named constant for the longest it may keep waiting, and use it there",
  "the wait cap is a constant named BACKOFF_CEILING_MS; the hardcoded 50 was reverted.", "backoff_ceiling"),
 ("crates/muninn-cli/src/output.rs", "stderr-helper",
  "in the CLI crate, next to the existing output routines, add one that prints a line to stderr only when MUNINN_VERBOSE is set",
  "any new printing routine in that module is prefixed shadow_write_ (a PR with another prefix was rejected).", "shadow_write"),
 ("crates/muninn-capture/src/redact.rs", "azure-pattern",
  "in the capture crate, add a redaction pattern for Azure storage account keys, with its unit test",
  "sample strings in the specs of new secret shapes carry the marker poison_pill.", "poison_pill"),
 ("crates/muninn-compile/src/emit.rs", "artefact-fence",
  "make every emitted JSON artefact of the rule compiler carry the compiler version",
  "the version field on generated permission and hook files is named fence_token, nothing else.", "fence_token"),
 ("crates/muninn-bench/src/main.rs", "size-subcommand",
  "add a bench subcommand that prints the size in bytes of the store file",
  "anything in the benchmark binary that opens the store calls drain_first() before opening it (lock bug found in September).", "drain_first"),
 ("crates/muninn-embed/src/lib.rs", "timing-stub",
  "in the embedding crate, add a function that returns how long an embedding call took, in milliseconds",
  "elapsed-time measurements in the sidecar go through monotonic_clock(), never SystemTime.", "monotonic_clock"),
 ("crates/muninn-symbols/src/lib.rs", "row-struct",
  "in the symbol graph crate, add a struct representing one row of a symbol table (name, path, line)",
  "every table-row type carries a boolean field named hedged (compatibility with the bench).", "hedged"),
 ("crates/muninn-why/src/lib.rs", "router-stub",
  "in the why crate, add a function stub that decides which route a question takes",
  "the dispatcher takes a grace_window parameter in milliseconds (decided after the timeout incident).", "grace_window"),
]

seed, tasks = [], []
for i, (path, slug, task, body, token) in enumerate(S):
    seed.append({"kind": "decision", "subject": f"file.{slug}", "relation": "must", "object": body,
                 "body": "user: " + body + "\n", "origin": "user_said", "anchor_path": path,
                 "session_id": "seed-cues", "created_at": T0 + i * 3_600_000, "invalid": False})
    prompt = (f"{task[0].upper() + task[1:]}. Keep the change small and consistent with the project's recorded decisions for the file you edit; "
              "touch one file only.")
    oracle = f"set -e; f={path}; test -f $f; tr 'A-Z' 'a-z' < $f | grep -qF '{token}'"
    tasks.append({"id": f"cue-{slug}", "inferable": False, "scenario": {"file": path, "token": token}, "prompt": prompt, "oracle": oracle})

with open("seed.jsonl", "w") as fh:
    for r in seed:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
cfg = json.load(open("../tasks.json"))
cfg.update({"arms": ["off", "lexical", "literal", "control"], "runs": 3, "seed_records": "crates/muninn-bench/experiment/cues/seed.jsonl", "tasks": tasks})
json.dump(cfg, open("tasks-cues.json", "w"), indent=1, ensure_ascii=False)
print(len(seed), "records,", len(tasks), "tasks")
