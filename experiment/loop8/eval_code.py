#!/usr/bin/env python3
"""Does the repository itself say that a decision was replaced? (loop 8, no model.)

Same scenarios, same held-out phrasings and the same three outcomes as
`loop1/eval_mechanism.py`, with one difference: between the two messages the *code* moves
from the old value to the new one, in a commit, the way it does in a real project. The
conversation is unchanged, so any difference is the commit.

Three arms, chosen on the command line:

  talk   the two messages, no commit                       (what loop 1-7 measured)
  code   the first message and the commit, no second message
  both   the two messages and the commit                   (an ordinary week)
  noise  the first message and a commit that changes something else entirely — the
         precision control: nothing here replaces the decision, so anything retired is a
         false retirement

Measured per scenario, as in loop 1:
  retired_a   the original statement is no longer served
  kept_b      the replacement is still active (only meaningful where there is one)
  served_ok   `muninn recall "<topic>"` returns the new value and not the old one

Usage: eval_code.py --muninn <binary> --arm both [--phrasings ...] [--scenarios ...]
"""
import argparse, json, os, re, subprocess, tempfile, uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent


def delivered_text(stdout: str) -> str:
    """What the blocks actually say, lowercased.

    The oracle asks whether a value appears in what was delivered, and until this existed it
    asked it of the whole stream. That stream also carries a block's own header line — its
    date, its synthetic session id — and, before the binary moved it to stderr, a wall-clock
    timing. A scenario whose value is a short token then matched on the instrument: the
    retry-budget cell reads `7`, and `session s017` or `0.57 ms` made it pass on some runs
    and not others, on a fixture this file's own README calls deterministic."""
    keep = [l for l in stdout.splitlines()
            if not l.startswith("[muninn:") and not l.lstrip().startswith("evidence:")
            and not l.startswith("terms:")]
    return "\n".join(keep).lower()


def says(text: str, value: str) -> bool:
    """`value` as a whole token, so `3` does not match inside `2026-09-01`."""
    return re.search(r"(?<![0-9a-z])" + re.escape(value) + r"(?![0-9a-z])", text) is not None


def sh(args, cwd, env=None):
    return subprocess.run(args, cwd=str(cwd), env=env, capture_output=True, text=True)


def transcript(path: Path, sid: str, ts: datetime, user: str) -> None:
    u1, u2 = str(uuid.uuid4()), str(uuid.uuid4())
    base = {"isSidechain": False, "userType": "external", "cwd": "/work/project", "sessionId": sid}
    rows = [
        {**base, "parentUuid": None, "type": "user", "uuid": u1,
         "timestamp": ts.isoformat().replace("+00:00", "Z"),
         "message": {"role": "user", "content": user}},
        {**base, "parentUuid": u1, "type": "assistant", "uuid": u2,
         "timestamp": (ts + timedelta(seconds=2)).isoformat().replace("+00:00", "Z"),
         "message": {"role": "assistant", "type": "message", "model": "synthetic",
                     "content": [{"type": "text", "text": "Noted."}], "stop_reason": "end_turn"}},
    ]
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


# Where a value lives in a project. One file per scenario, named so that the value is the
# only thing that changes: the commit is a value swap and nothing else.
MANIFEST = "config/stack.json"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--muninn", required=True)
    ap.add_argument("--arm", choices=["talk", "code", "both", "noise"], default="both")
    ap.add_argument("--phrasings", default=str(EXP / "loop7" / "heldout_phrasings.json"))
    ap.add_argument("--scenarios", default=str(EXP / "loop7" / "scenarios.json"))
    ap.add_argument("--styles", default="terse,chatty,Spanish")
    ap.add_argument("--out", default=str(HERE / "code_results.json"))
    ap.add_argument("--fixture", choices=["value", "topic"], default="value",
                    help="value: the file holds the value alone, as a manifest entry does. "
                         "topic: it also holds the topic sentence, which leaves the topic's "
                         "words in the tree and blocks the 'gone from the code' test for any "
                         "value that shares one.")
    a = ap.parse_args()

    items = {i["key"]: i for i in json.load(open(a.phrasings))}
    sc = json.load(open(a.scenarios))
    scenarios = [x for k in sc for x in sc[k]]
    results = []
    for style in a.styles.split(","):
        for s in scenarios:
            it = items.get(f"{s['id']}#{style}")
            if not it or not s.get("new"):
                continue
            root = Path(tempfile.mkdtemp(prefix=f"loop8-{s['id']}-"))
            env = {**os.environ, "MUNINN_ROOT": str(root), "MUNINN_NO_PROJECT": "1"}
            # a repository whose code holds the old value
            sh(["git", "init", "-q"], root)
            sh(["git", "config", "user.email", "cell@loop8"], root)
            sh(["git", "config", "user.name", "cell"], root)
            f = root / MANIFEST
            f.parent.mkdir(parents=True, exist_ok=True)
            def manifest(value):
                body = {"value": value} if a.fixture == "value" else {"topic": s["topic"], "value": value}
                return json.dumps(body, indent=1) + "\n"

            f.write_text(manifest(s["old"]))
            sh(["git", "add", "-A"], root)
            sh(["git", "commit", "-qm", "base"], root)
            sh([a.muninn, "--cwd", str(root), "init", "--keep-native"], root, env)
            # transcripts live outside the checkout: a real one is in ~/.claude, and a
            # copy inside the repository would keep the old value in a tracked file
            tdir = Path(tempfile.mkdtemp(prefix="loop8-t-"))
            t0 = datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc)

            def ingest(k, text, when):
                p = tdir / f"{k:03d}.jsonl"
                transcript(p, str(uuid.uuid4()), when, text)
                sh([a.muninn, "--cwd", str(root), "ingest", str(p)], root, env)

            ingest(0, it["a"], t0)
            if a.arm in ("code", "both"):
                f.write_text(manifest(s["new"]))
                sh(["git", "add", "-A"], root)
                sh(["git", "commit", "-qm", f"use {s['new']} for {s['topic']}"], root)
            if a.arm == "noise":
                # a commit of the same shape, about something the decision never mentioned
                other = root / "config" / "unrelated.json"
                other.write_text(json.dumps({"value": "ripgrep"}, indent=1) + "\n")
                sh(["git", "add", "-A"], root)
                sh(["git", "commit", "-qm", "unrelated change"], root)
                other.write_text(json.dumps({"value": "ugrep"}, indent=1) + "\n")
                sh(["git", "add", "-A"], root)
                sh(["git", "commit", "-qm", "swap the unrelated one"], root)
            if a.arm in ("talk", "both"):
                ingest(1, it["b"], t0 + timedelta(minutes=30))
            ingest(2, it["c"], t0 + timedelta(minutes=60))
            sh([a.muninn, "--cwd", str(root), "maintain"], root, env)

            sh([a.muninn, "--cwd", str(root), "--json", "export", "--all", "--out",
                str(root / "x.jsonl")], root, env)
            recs = [json.loads(l) for l in open(root / "x.jsonl")]

            def active_with(text):
                key = text.strip().rstrip(".!;")[:40].lower()
                return [r for r in recs if not r.get("invalid") and key in (r.get("body") or "").lower()]

            rec = delivered_text(sh([a.muninn, "--cwd", str(root), "recall", s["topic"]], root, env).stdout)
            old, new = s["old"].lower(), s["new"].lower()
            results.append({
                "arm": a.arm, "style": style, "id": s["id"],
                "retired_a": not active_with(it["a"]),
                "kept_b": bool(active_with(it["b"])) if a.arm in ("talk", "both") else None,
                "kept_a": bool(active_with(it["a"])),
                "served_ok": (not says(rec, old)) and says(rec, new.split()[0]),
                "old_served": says(rec, old),
                "new_served": new.split()[0] in rec,
            })
            subprocess.run(["rm", "-rf", str(root), str(tdir)])

    json.dump(results, open(a.out, "w"), indent=1)
    def share(key, sub):
        v = [r[key] for r in sub if r[key] is not None]
        return f"{sum(v)}/{len(v)}"
    for grp, sub in [("all", results)] + [(st, [r for r in results if r["style"] == st])
                                          for st in a.styles.split(",")]:
        print(f"{a.arm:5s}/{a.fixture:5s} {grp:9s} retired_a {share('retired_a', sub):7s} kept_b {share('kept_b', sub):7s} "
              f"served_ok {share('served_ok', sub):7s} old_served {share('old_served', sub):7s} "
              f"new_served {share('new_served', sub):7s} kept_a {share('kept_a', sub)}")


if __name__ == "__main__":
    main()
