#!/usr/bin/env python3
"""Loop 8 — one store, every scenario, with and without the code (no model).

`loop1/eval_mechanism.py` measures the conversation alone in one shared store; `eval_code.py`
measures one scenario per store with a commit. This one does both at once, because the
interesting question is what happens when the two are combined *and* the change does not
arrive immediately after the decision:

  order   adjacent  a1 b1 a2 b2 … then every c   (a real conversation, and how the
                                                  head-to-head seeds its arms)
          blocks    every a, then every b, then every c — ten decisions are taken before
                    the first of them is revised, so nothing lexical is adjacent any more

  arm     talk      the messages only
          code      the first message of each pair, and a commit that swaps the value
          both      the messages and the commits
          noise     the first message of each pair, and commits that swap something else
                    (the precision control: anything retired here is retired wrongly)

Outcomes are loop 1's, unchanged: retired_a, kept_b, served_ok (and old_served / a_served /
b_served beside them, so a miss can be read as a retirement miss or a delivery miss).

Usage: eval_all.py --muninn <binary> --arm both --order adjacent [--out results.json]
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


def sh(args, cwd=None, env=None):
    return subprocess.run([str(a) for a in args], cwd=cwd and str(cwd), env=env,
                          capture_output=True, text=True)


_commit_n = [0]


def commit(root: Path, message: str) -> None:
    """A commit with a fixed date, so its hash is the same on every run of the grid.

    With wall-clock dates the hash changes between runs, the hash is part of the commit
    record's text, the text is indexed, and BM25 then scores the same store differently:
    one cell in thirty flipped between runs before this."""
    _commit_n[0] += 1
    when = f"2026-09-01T09:{_commit_n[0] % 60:02d}:00Z"
    env = {**os.environ, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
    sh(["git", "add", "-A"], root)
    sh(["git", "commit", "-qm", message], root, env)


def transcript(path: Path, sid: str, ts: datetime, user: str) -> None:
    # deterministic ids: a random session id lands in the episode's subject, which is
    # indexed, so two runs of the same grid scored the same records differently
    u1, u2 = f"{sid}-u", f"{sid}-a"
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--muninn", required=True)
    ap.add_argument("--arm", choices=["talk", "code", "both", "noise"], default="both")
    ap.add_argument("--order", choices=["adjacent", "blocks"], default="adjacent")
    ap.add_argument("--phrasings", default=str(EXP / "loop7" / "heldout_phrasings.json"))
    ap.add_argument("--scenarios", default=str(EXP / "loop7" / "scenarios.json"))
    ap.add_argument("--styles", default="terse,chatty,Spanish")
    ap.add_argument("--out", default=str(HERE / "all_results.json"))
    ap.add_argument("--survivor", action="store_true",
                    help="also write each old value into a second file that no commit ever "
                         "touches, so 'the value is gone from the tree' is false — the position "
                         "three of the nine head-to-head scenarios are in, where the checkout "
                         "already contains the word")
    ap.add_argument("--filler", type=int, default=0,
                    help="unrelated commits to make after each change, so the commit that "
                         "matters falls further back in the history a single maintain reads")
    ap.add_argument("--commit-msg", choices=["names", "opaque"], default="names",
                    help="names: the commit subject names the new value, as many real ones "
                         "do ('use nats'). opaque: it does not ('update dependencies'), so "
                         "the only thing the commit contributes is the diff.")
    a = ap.parse_args()

    items = {i["key"]: i for i in json.load(open(a.phrasings))}
    sc = json.load(open(a.scenarios))
    scenarios = [x for k in sc for x in sc[k] if x.get("new")]
    results = []
    for style in a.styles.split(","):
        _commit_n[0] = 0
        root = Path(tempfile.mkdtemp(prefix=f"loop8-{style}-"))
        tdir = Path(tempfile.mkdtemp(prefix="loop8-t-"))   # outside the checkout
        env = {**os.environ, "MUNINN_ROOT": str(root), "MUNINN_NO_PROJECT": "1"}
        sh(["git", "init", "-q"], root)
        sh(["git", "config", "user.email", "cell@loop8"], root)
        sh(["git", "config", "user.name", "cell"], root)
        cfg = root / "config"
        cfg.mkdir()
        for s in scenarios:
            (cfg / f"{s['id']}.json").write_text(json.dumps({"value": s["old"]}, indent=1) + "\n")
        (cfg / "unrelated.json").write_text(json.dumps({"value": "ripgrep"}, indent=1) + "\n")
        if a.survivor:
            (root / "CHANGELOG.md").write_text(
                "".join(f"- once used {s['old']}\n" for s in scenarios))
        commit(root, "base")
        sh([a.muninn, "--cwd", root, "init", "--keep-native"], root, env)

        t0 = datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc)
        steps = []           # (scenario, part) in time order
        if a.order == "adjacent":
            steps = [(s, p) for s in scenarios for p in ("a", "b")] + [(s, "c") for s in scenarios]
        else:
            steps = [(s, "a") for s in scenarios] + [(s, "b") for s in scenarios] + \
                    [(s, "c") for s in scenarios]

        k = 0
        for s, part in steps:
            it = items.get(f"{s['id']}#{style}")
            if not it:
                continue
            when = t0 + timedelta(minutes=30 * k)
            if part == "b":
                # the code moves at the moment the decision is revised
                if a.arm in ("code", "both"):
                    (cfg / f"{s['id']}.json").write_text(
                        json.dumps({"value": s["new"]}, indent=1) + "\n")
                    commit(root, f"use {s['new']}" if a.commit_msg == "names"
                           else "update dependencies")
                for j in range(a.filler if a.arm in ("code", "both") else 0):
                    (cfg / "unrelated.json").write_text(
                        json.dumps({"value": f"filler-{k}-{j}"}, indent=1) + "\n")
                    commit(root, "chore")
                if a.arm == "noise":
                    (cfg / "unrelated.json").write_text(
                        json.dumps({"value": f"grep{k}"}, indent=1) + "\n")
                    commit(root, "unrelated change")
                if a.arm in ("code", "noise"):
                    k += 1
                    continue
            p = tdir / f"{k:03d}.jsonl"
            transcript(p, f"s{k:03d}", when, it[part])
            sh([a.muninn, "--cwd", root, "ingest", p], root, env)
            k += 1
        sh([a.muninn, "--cwd", root, "maintain"], root, env)

        sh([a.muninn, "--cwd", root, "--json", "export", "--all", "--out", root / "x.jsonl"],
           root, env)
        recs = [json.loads(l) for l in open(root / "x.jsonl")]

        def active_with(text):
            key = text.strip().rstrip(".!;")[:40].lower()
            return [r for r in recs if not r.get("invalid") and key in (r.get("body") or "").lower()]

        for s in scenarios:
            it = items.get(f"{s['id']}#{style}")
            if not it:
                continue
            rec = delivered_text(sh([a.muninn, "--cwd", root, "recall", s["topic"]], root, env).stdout)
            old, new = s["old"].lower(), s["new"].lower()
            snippet = lambda t: t.strip().rstrip(".!;").lower()[:40]
            results.append({
                "arm": a.arm, "order": a.order, "style": style, "id": s["id"],
                "retired_a": not active_with(it["a"]),
                "kept_b": bool(active_with(it["b"])) if a.arm in ("talk", "both") else None,
                "served_ok": (not says(rec, old)) and says(rec, new.split()[0]),
                "old_served": says(rec, old),
                "a_served": snippet(it["a"]) in rec,
                "b_served": snippet(it["b"]) in rec,
            })
        sh(["rm", "-rf", root, tdir])

    json.dump(results, open(a.out, "w"), indent=1)

    def share(key, sub):
        v = [r[key] for r in sub if r[key] is not None]
        return f"{sum(v)}/{len(v)}"
    for grp, sub in [("all", results)] + [(st, [r for r in results if r["style"] == st])
                                          for st in a.styles.split(",")]:
        print(f"{a.arm:5s}/{a.order:8s}/{a.commit_msg:6s}/f{a.filler}{'/surv' if a.survivor else '':5s} {grp:9s} retired_a {share('retired_a', sub):7s} "
              f"kept_b {share('kept_b', sub):7s} served_ok {share('served_ok', sub):7s} "
              f"old_served {share('old_served', sub):7s} b_served {share('b_served', sub)}")


if __name__ == "__main__":
    main()
