#!/usr/bin/env python3
"""Label-free head-to-head (pre-registered in ../PREREGISTRATION.md, "Head-to-head without labels").

Every memory arm (Muninn, claude-mem, agentmemory, agentmemory-inject) learns the same twenty
decisions from the same twenty live `claude -p` sessions — the seed body without "user: " plus one
fixed acknowledgement line — through its own shipped hooks, with no import and no labels. The
seeded data directory of each run is then cloned into each of that run's ten task cells. `off`
has no memory. Oracles and tasks are Gate 3's public-seed ones, unchanged. Results are written in
the Gate 3 layout (`results.jsonl`, `diffs/`, `logs/`) so `revocation/analyze.py`-style tallies
apply; `analyze_h2h.py` computes the pre-registered tests.

Arm plug-ins live in competitors/<arm>/arm.sh with subcommands install|start|claude-args|settle|
snapshot|restore|stop|delivered (see competitors/muninn/arm.sh). Arms that share a fixed port
(agentmemory*) never run at the same time.

Each arm seeding its own store is right when the arms are different products. It is wrong when
two arms are two builds of this one: the stores then differ as well as the cells, and a read-path
change is read through that difference. `--share-seed` makes one arm seed and hands its store to
the others, which is the paired design for a read-path comparison.

Usage:
  run_h2h.py --out <dir> [--runs 3] [--jobs 3] [--arms off,muninn,claude-mem,agentmemory,agentmemory-inject]
             [--only-seed] [--rerun-errors] [--share-seed <arm>] [--code]
"""
import argparse, json, os, random, shutil, signal, subprocess, sys, tempfile, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
REPO = Path("/home/ilien/.local/share/muninn-bench/external/gin")
BASE_REF = "dcaa4296d111981ffb31ac3eba90bb63e1eb5ab9"
MODEL = "claude-sonnet-5"
ACK = "(Reply with one short sentence acknowledging.)"
CONFINE = "Work only inside the current working directory (this repository checkout); write files by paths relative to it and never outside it."
BASE_TOOLS = ("Read,Edit,Write,MultiEdit,Grep,Glob,Bash(git diff *),Bash(git log *),Bash(git status *),Bash(cat *),"
              "Bash(grep *),Bash(awk *),Bash(sed -n *),Bash(head *),Bash(tail *),Bash(wc *),Bash(ls *)")
PORT_GROUP = {"agentmemory": "agentmemory", "agentmemory-inject": "agentmemory"}
_locks: dict[str, threading.Lock] = {}
_ports = iter(range(38100, 39000))
_plock = threading.Lock()


PHRASINGS: list = []
# v42: the order the seed rows are sent in, by index; empty = time order (each change right
# after its decision). "separated" sends every decision, then every change.
SEED_ORDER: list = []
# v4: the decisions are also implemented in the checkout, which is what happens in a real
# project — the value lives in a file and a commit moves it. Every arm gets the same repository
# and the same commits; only a memory that reads them can use them. Empty unless --code.
CODE_PAIRS: list = []
DECISIONS_DIR = "config/decisions"
# deliberately uninformative: a commit subject that named the new value would answer the
# question by itself, and the offline control (loop 9) showed exactly how much that is worth
CODE_COMMIT_MSG = "update dependencies"


def lock_for(arm: str) -> threading.Lock:
    key = PORT_GROUP.get(arm, f"solo:{threading.get_ident()}:{arm}")
    if key.startswith("solo:"):
        return threading.Lock()
    return _locks.setdefault(key, threading.Lock())


def next_port() -> int:
    """The next port in the range that nothing is already listening on.

    An arm that starts a worker refuses a port that already answers, and it is right to —
    talking to somebody else's worker would put a cell's memory in another cell's store. But
    the harness was handing out the numbers blind, so a worker left behind by an interrupted
    run made the next run fail at `start` with "port 38100 already answers", and the whole
    seeding job with it. Observed twice in one morning. Skipping a busy port costs one socket
    call per cell.
    """
    import socket
    with _plock:
        for _ in range(256):
            port = next(_ports)
            with socket.socket() as sk:
                sk.settimeout(0.2)
                if sk.connect_ex(("127.0.0.1", port)) != 0:
                    return port
            print(f"port {port} is already in use, skipping it", flush=True)
        raise RuntimeError("no free port in the range")


def checkout(dest: Path, seed: bool = False) -> None:
    """`seed`: a seeding checkout, which under --code also holds one tracked file per decision.

    Outside `--code` a task cell gets the base checkout and nothing else, exactly as in every
    other grid: the decisions exist only in the transcripts, so a cell cannot answer by
    reading the repository. Under `--code` see `cell_checkout`, which gives the cell the
    seeding checkout's own history — v4 gave it a fresh one-commit repository, and nineteen of
    twenty-one failing cells then reasoned from the fact that the commits the memory cited did
    not exist, which measured the fixture rather than the memory."""
    dest.mkdir(parents=True, exist_ok=True)
    arc = subprocess.run(["git", "-C", str(REPO), "archive", BASE_REF], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=arc, check=True)
    if CODE_PAIRS and seed:
        d = dest / DECISIONS_DIR
        d.mkdir(parents=True, exist_ok=True)
        for pair in CODE_PAIRS:
            (d / f"{pair['id']}.json").write_text(json.dumps({"value": pair["old"]}, indent=1) + "\n")
    for a in (["init", "-q"], ["add", "-A"], ["-c", "user.email=cell@h2h", "-c", "user.name=cell", "commit", "-qm", "base"]):
        subprocess.run(["git", "-C", str(dest), *a], check=True, capture_output=True)


def cell_checkout(dest: Path, history: Path) -> None:
    """The checkout a task cell works in.

    Without `--code`, the base checkout. With it, a copy of the seeding checkout's repository
    with one further commit that takes `config/decisions/` out of the working tree. The cell
    then has what a real project has — every commit the memory cites resolves, and `git show`
    answers — and still cannot read the current value out of a file. What it *can* do is
    `git log -p`, which is why `off` runs as a registered arm: if a cell with no memory passes
    on this fixture, the fixture is answering the question and the condition is withdrawn."""
    if not CODE_PAIRS or not history.exists():
        checkout(dest)
        return
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(history, dest)
    d = dest / DECISIONS_DIR
    if d.exists():
        shutil.rmtree(d)
    for a in (["add", "-A"],
              ["-c", "user.email=cell@h2h", "-c", "user.name=cell", "commit", "-qm",
               "move decision config out of the tree"]):
        subprocess.run(["git", "-C", str(dest), *a], check=True, capture_output=True)


def arm_cmd(arm: str, sub: str, env: dict, *extra: str) -> str:
    # output goes to files, not pipes: a server an arm starts in the background inherits the
    # script's descriptors, and a pipe held open by it made `start` never return (pilot 1)
    with tempfile.TemporaryFile("w+") as out, tempfile.TemporaryFile("w+") as err:
        p = subprocess.run([str(HERE / "competitors" / arm / "arm.sh"), sub, *extra], env=env,
                           stdout=out, stderr=err, stdin=subprocess.DEVNULL, text=True, timeout=900)
        out.seek(0); err.seek(0)
        so, se = out.read(), err.read()
    if p.returncode != 0:
        raise RuntimeError(f"{arm} {sub} failed: {se[-400:]}")
    return so.strip()


def clean_path() -> str:
    return ":".join(d for d in os.environ.get("PATH", "").split(":") if not (Path(d) / "muninn").exists())


def session_env(base: dict, spec: dict) -> dict:
    env = dict(base)
    env.pop("CLAUDECODE", None)
    for k, v in (spec.get("env") or {}).items():
        if k == "PATH_PREPEND":
            env["PATH"] = f"{v}:{env['PATH']}"
        else:
            env[k] = v
    return env


def claude(prompt: str, cwd: Path, env: dict, spec: dict, settings: Path, max_turns: int, allowed: str | None, timeout: int = 900):
    args = ["claude", "-p", prompt, "--model", MODEL, "--output-format", "json", "--max-turns", str(max_turns),
            "--setting-sources", "", "--settings", str(settings), *spec.get("args", [])]
    if allowed is not None:
        args += ["--permission-mode", "acceptEdits", "--allowedTools", allowed]
    t0 = time.time()
    # Files, not pipes, and a session of its own — the same lesson `arm_cmd` above already
    # carries, learned again on the v34 grid. A session starts MCP servers, they inherit this
    # process's stdout, and `capture_output=True` then makes the timeout meaningless: killing
    # the session leaves the servers holding the write end, and `subprocess.run` goes on
    # reading a pipe that will never reach EOF. The v34 grid sat for two hours on a 300-second
    # timeout with the seeding log at zero bytes, and three `chroma-mcp` processes alive.
    # `start_new_session` puts the whole tree in one group so the timeout can end all of it.
    with tempfile.TemporaryFile("w+") as fo, tempfile.TemporaryFile("w+") as fe:
        proc = subprocess.Popen(args, cwd=cwd, env=env, stdout=fo, stderr=fe, text=True,
                                stdin=subprocess.DEVNULL, start_new_session=True)
        try:
            proc.wait(timeout=timeout)
            fo.seek(0)
            out = fo.read()
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                proc.kill()
            proc.wait()
            return {"error": "timeout"}, "", time.time() - t0
    try:
        v = json.loads(out) if out.strip() else {}
    except json.JSONDecodeError:
        v = {}
    return v, out, time.time() - t0


# Every arm so far runs with the harness's own memory switched off, so `off` means "no
# memory at all". A native-memory arm needs that one key flipped, and only for itself:
# the file every other arm gets must stay byte-identical, or the v1 and v2 grids already
# measured stop being comparable.
NATIVE_MEMORY_ARMS = {"native"}


def settings_for(arm: str, cell_root: Path | None = None) -> str:
    v = {"autoMemoryEnabled": arm in NATIVE_MEMORY_ARMS}
    if arm in NATIVE_MEMORY_ARMS and cell_root is not None:
        # Auto memory otherwise lands in `~/.claude/projects/<repo>/memory/`, keyed by the
        # git repository, so every cell of every run would share one directory and the
        # operator's own memory for this repository would be in it. `autoMemoryDirectory`
        # is read from any settings scope, `--settings` included, and confines the arm to
        # its own cell. A private HOME would do it too, but it also moves the login, and an
        # unauthenticated cell measures nothing.
        v["autoMemoryDirectory"] = str((cell_root / "memory").resolve())
    return json.dumps(v)


def seed_arm(arm: str, run: int, out: Path, work: Path, seed_rows: list) -> Path:
    snap = work / f"snap-r{run}-{arm}"
    if (snap / ".done").exists():
        return snap
    root = work / f"seed-r{run}-{arm}"
    shutil.rmtree(root, ignore_errors=True)
    (root / "cell").mkdir(parents=True)
    co = root / REPO.name   # tools key state by the checkout basename: same name in seed and task cells
    checkout(co, seed=True)
    settings = root / "settings.json"
    settings.write_text(settings_for(arm, root / "cell"))
    log = (out / "seeding").joinpath(f"r{run}-{arm}.jsonl")
    log.parent.mkdir(parents=True, exist_ok=True)
    with lock_for(arm):
        env = dict(os.environ, CELL_ROOT=str(root / "cell"), CHECKOUT=str(co), PORT=str(next_port()), PATH=clean_path())
        try:
            arm_cmd(arm, "start", env)
            spec = json.loads(arm_cmd(arm, "claude-args", env))
            # Line-buffered on purpose. Buffered, this file stays at zero bytes for the first
            # dozen sessions, and a seeding job that is merely slow is indistinguishable from
            # one that is hung — which is exactly how the v34 grid was read as hung when it was
            # running. Progress a watcher can see is worth one syscall a session.
            unsettled = 0
            with open(log, "w", buffering=1) as fh:
                for i in SEED_ORDER or range(len(seed_rows)):
                    r = seed_rows[i]
                    body = r["body"].strip()
                    body = body[len("user: "):] if body.startswith("user: ") else body
                    if PHRASINGS:   # v2: row 2k is pair k's original decision, row 2k+1 its change
                        body = PHRASINGS[i // 2]["a" if i % 2 == 0 else "b"]
                    prompt = f"{body}\n\n{ACK}"
                    v, raw, secs = claude(prompt, co, session_env(env, spec), spec, settings, 3, None, timeout=300)
                    if CODE_PAIRS and i % 2 == 1:
                        # row 2k+1 is pair k's change: the code moves with it
                        pair = CODE_PAIRS[i // 2] if i // 2 < len(CODE_PAIRS) else None
                        if pair and pair.get("new"):
                            f = co / DECISIONS_DIR / f"{pair['id']}.json"
                            f.write_text(json.dumps({"value": pair["new"]}, indent=1) + "\n")
                            for g in (["add", "-A"], ["-c", "user.email=cell@h2h", "-c", "user.name=cell",
                                      "commit", "-qm", CODE_COMMIT_MSG]):
                                subprocess.run(["git", "-C", str(co), *g], capture_output=True)
                    settled = arm_cmd(arm, "settle", env)
                    st = json.loads(settled or "{}")
                    unsettled += st.get("settled") is False
                    fh.write(json.dumps({"i": i, "created_at": r["created_at"], "prompt": prompt, "reply": str(v.get("result"))[:300],
                                         "is_error": v.get("is_error"), "secs": round(secs, 1), "settle": st}) + "\n")
            # A competitor that does not finish processing its sessions is not the competitor
            # as it ships. v39's first attempt ran claude-mem with its observer rejected by the
            # account's five-hour usage window: every settle hit its ten-minute timeout, the
            # store held raw prompts and no observations, and the grid would have measured
            # Muninn against a crippled arm without saying so. A seeding where most sessions
            # never settled is a failed seeding, and its cells are not run.
            if unsettled * 2 > len(seed_rows):
                raise RuntimeError(f"{arm}: {unsettled} of {len(seed_rows)} seeding sessions never "
                                   "settled — the arm is not working as it ships (check its worker "
                                   "log, e.g. a usage limit on its observer)")
            snap.mkdir(parents=True, exist_ok=True)
            arm_cmd(arm, "snapshot", env, str(snap))
            if CODE_PAIRS:
                # v5: the cells get this checkout's history, so every commit a record cites
                # resolves where the agent can look. Kept beside the store snapshot so a
                # resumed run finds it without re-seeding.
                hist = work / f"hist-r{run}-{arm}"
                shutil.rmtree(hist, ignore_errors=True)
                shutil.copytree(co, hist)
            (snap / ".done").write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        finally:
            try:
                arm_cmd(arm, "stop", env)
            except Exception as exc:  # noqa: BLE001
                print(f"stop failed for {arm}: {exc}", flush=True)
    return snap


def run_cell(cfg: dict, task: dict, arm: str, run: int, out: Path, work: Path) -> dict:
    cell = {"run": run, "task": task["id"], "arm": arm, "inferable": False, "status": "error", "oracle_exit": None,
            "num_turns": None, "cost_usd": None, "duration_ms": 0, "error": None}
    root = work / f"cell-r{run}-{task['id']}-{arm}"
    shutil.rmtree(root, ignore_errors=True)
    (root / "cell").mkdir(parents=True)
    co = root / REPO.name
    t0 = time.time()
    lk = lock_for(arm) if arm != "off" else threading.Lock()
    with lk:
        env = dict(os.environ, CELL_ROOT=str(root / "cell"), CHECKOUT=str(co), PORT=str(next_port()), PATH=clean_path())
        settings = root / "settings.json"
        settings.write_text(settings_for(arm, root / "cell"))
        spec: dict = {}
        started = False
        try:
            cell_checkout(co, work / f"hist-r{run}-{arm}")
            allowed = BASE_TOOLS
            if arm != "off":
                arm_cmd(arm, "restore", env, str(work / f"snap-r{run}-{arm}"))
                arm_cmd(arm, "start", env)
                started = True
                spec = json.loads(arm_cmd(arm, "claude-args", env))
                if spec.get("allowed_tools"):
                    allowed = allowed + "," + ",".join(spec["allowed_tools"])
            v, raw, secs = claude(task["prompt"] + "\n\n" + CONFINE, co, session_env(env, spec), spec, settings, 25, allowed)
            logs = out / "logs"
            logs.mkdir(parents=True, exist_ok=True)
            (logs / f"r{run}-{task['id']}-{arm}.json").write_text(raw or json.dumps(v))
            cell["num_turns"] = v.get("num_turns")
            cell["cost_usd"] = v.get("total_cost_usd")
            if v.get("error") == "timeout":
                cell["error"] = "timeout"
            elif v.get("is_error") and v.get("subtype") != "error_max_turns":
                cell["error"] = f"claude is_error: {str(v.get('result'))[:200]}"
            if arm != "off":
                sid = v.get("session_id") or ""
                slug = "".join(ch if ch.isalnum() else "-" for ch in str(co))   # Claude Code's project-dir slug
                transcript = Path.home() / ".claude" / "projects" / slug / f"{sid}.jsonl"
                (logs / f"r{run}-{task['id']}-{arm}.delivered.json").write_text(arm_cmd(arm, "delivered", env, str(transcript)) or "{}")
                if transcript.exists():
                    shutil.copy(transcript, logs / f"r{run}-{task['id']}-{arm}.transcript.jsonl")
            subprocess.run(["git", "-C", str(co), "add", "-A"], check=True, capture_output=True)
            diff = subprocess.run(["git", "-C", str(co), "diff", "--cached"], capture_output=True, text=True).stdout
            (out / "diffs").mkdir(parents=True, exist_ok=True)
            (out / "diffs" / f"r{run}-{task['id']}-{arm}.patch").write_text(diff)
            if cell["error"] is None:
                o = subprocess.run(["bash", "-c", task["oracle"]], cwd=co, capture_output=True, text=True)
                cell["oracle_exit"] = o.returncode
                cell["status"] = "pass" if o.returncode == 0 else "fail"
        except Exception as exc:  # noqa: BLE001
            cell["error"] = f"harness: {exc}"
        finally:
            if started:
                try:
                    arm_cmd(arm, "stop", env)
                except Exception as exc:  # noqa: BLE001
                    cell["error"] = cell["error"] or f"stop: {exc}"
            shutil.rmtree(root, ignore_errors=True)
    cell["duration_ms"] = int((time.time() - t0) * 1000)
    return cell


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--arms", default="off,muninn,claude-mem,agentmemory,agentmemory-inject")
    ap.add_argument("--only-seed", action="store_true")
    ap.add_argument("--rerun-errors", action="store_true")
    ap.add_argument("--seed-phrasings", default=None,
                    help="v2: JSON list of {key,a,b}, one per seed pair in time order, used instead of the seed bodies")
    ap.add_argument("--tasks", default=str(EXP / "revocation" / "tasks-revocation-public.json"))
    ap.add_argument("--share-seed", default=None, metavar="ARM",
                    help="Seed once with ARM and give every other arm named muninn* a copy of "
                         "its store, instead of letting each arm build its own from its own live "
                         "sessions. Two builds compared across grids differ in their stores as "
                         "well as in their cells: measured on v32, four fixtures where the code "
                         "under test provably never ran still read -5, -3, 0 and -4 cells, "
                         "200/216 against 188/216. Sharing the snapshot pairs a read-path "
                         "comparison on the store and leaves only the agent stochastic. It is "
                         "valid ONLY for a change that cannot alter what capture writes; the "
                         "caller asserts that, the harness cannot check it, and the assertion is "
                         "recorded in FROZEN.jsonl.")
    ap.add_argument("--seed-order", default="adjacent", choices=["adjacent", "separated"],
                    help="v42: adjacent (row 2k then 2k+1, the default) or separated (every "
                         "decision first, then every change: the order where the rules' anaphora "
                         "path, which takes the latest episode, cannot reach the right record)")
    ap.add_argument("--code", action="store_true",
                    help="v4: also implement each decision in the checkout — one tracked file per "
                         "scenario holding its value, and a commit with an uninformative subject "
                         "when the decision changes. Identical for every arm.")
    a = ap.parse_args()

    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.gettempdir()) / "muninn-h2h" / out.name
    work.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(Path(a.tasks).read_text())
    seed_rows = sorted((json.loads(l) for l in open(EXP / "revocation" / "seed.jsonl")), key=lambda r: r["created_at"])
    arms = a.arms.split(",")
    global PHRASINGS, CODE_PAIRS, SEED_ORDER
    if a.seed_order == "separated":
        SEED_ORDER = list(range(0, len(seed_rows), 2)) + list(range(1, len(seed_rows), 2))
    if a.code:
        CODE_PAIRS = [{"id": t["id"], "old": t["scenario"]["old"], "new": t["scenario"]["new"]}
                      for t in cfg["tasks"]]
    if a.seed_phrasings:
        PHRASINGS = json.loads(Path(a.seed_phrasings).read_text())
        assert len(PHRASINGS) * 2 == len(seed_rows), "one phrasing pair per seed pair"
    if a.share_seed and a.share_seed not in arms:
        raise SystemExit(f"--share-seed {a.share_seed} is not one of --arms {a.arms}")
    shared = [x for x in arms if x.startswith("muninn") and x != a.share_seed] if a.share_seed else []
    frozen = {"arms": arms, "runs": a.runs, "code": bool(a.code),
              "share_seed": a.share_seed, "share_seed_receivers": shared, "model": MODEL, "repo": str(REPO), "base_ref": BASE_REF, "ack": ACK,
              "tasks_file": a.tasks, "seed_phrasings": a.seed_phrasings, "seed_order": a.seed_order, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "harness_sha256": subprocess.run(["sha256sum", __file__], capture_output=True, text=True).stdout[:64],
              "arm_scripts_sha256": {arm: subprocess.run(["sha256sum", str(HERE / "competitors" / arm / "arm.sh")], capture_output=True, text=True).stdout[:64]
                                     for arm in arms if arm != "off"}}
    (out / "config.json").write_text(json.dumps(cfg, indent=1))
    with open(out / "FROZEN.jsonl", "a") as fh:
        fh.write(json.dumps(frozen) + "\n")

    results = out / "results.jsonl"
    done: dict = {}
    if results.exists():
        for l in open(results):
            r = json.loads(l)
            done[(r["run"], r["task"], r["arm"])] = r
    rlock = threading.Lock()

    # seeding: per run, per memory arm (arms of one port group serialise through their lock).
    # Under --share-seed the receivers are left out here and given the seeder's snapshot below.
    seed_jobs = [(arm, run) for run in range(a.runs) for arm in arms
                 if arm != "off" and arm not in shared]
    def seed_one(j):
        try:
            return j[0], j[1], seed_arm(j[0], j[1], out, work, seed_rows), None
        except Exception as exc:  # noqa: BLE001
            return j[0], j[1], None, exc
    failed_seed = set()
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for arm, run, snap, exc in ex.map(seed_one, seed_jobs):
            if exc is not None:
                failed_seed.add((run, arm))
                print(f"SEEDING FAILED r{run} {arm}: {exc}", flush=True)
            else:
                print(f"seeded r{run} {arm} -> {snap}", flush=True)
    # The receivers get the seeder's store, byte for byte, and its checkout history under
    # --code so every commit a record cites still resolves. A receiver whose seeder failed is
    # marked failed with it rather than run against a store that is not there.
    for run in range(a.runs):
        if (run, a.share_seed) in failed_seed:
            for arm in shared:
                failed_seed.add((run, arm))
            continue
        for arm in shared:
            src, dst = work / f"snap-r{run}-{a.share_seed}", work / f"snap-r{run}-{arm}"
            if not (src / ".done").exists():
                failed_seed.add((run, arm))
                print(f"SHARE FAILED r{run} {arm}: {src} has no snapshot", flush=True)
                continue
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)
            hsrc, hdst = work / f"hist-r{run}-{a.share_seed}", work / f"hist-r{run}-{arm}"
            if hsrc.exists():
                shutil.rmtree(hdst, ignore_errors=True)
                shutil.copytree(hsrc, hdst)
            print(f"shared r{run} {a.share_seed} -> {arm}", flush=True)

    if a.only_seed:
        return

    plan = []
    for run in range(a.runs):
        cells = [(t, arm) for t in cfg["tasks"] for arm in arms]
        random.Random(f"h2h:{run}").shuffle(cells)
        plan += [(run, t, arm) for t, arm in cells]
    todo = [(run, t, arm) for run, t, arm in plan
            if (run, arm) not in failed_seed
            and ((run, t["id"], arm) not in done or (a.rerun_errors and done[(run, t["id"], arm)]["status"] == "error"))]
    if failed_seed:
        print(f"cells of arms whose seeding failed are not run: {sorted(failed_seed)}", flush=True)
    print(f"{len(plan)} cells planned, {len(todo)} to run", flush=True)

    def go(job):
        run, t, arm = job
        c = run_cell(cfg, t, arm, run, out, work)
        with rlock:
            done[(run, t["id"], arm)] = c
            with open(results, "w") as fh:
                for r in done.values():
                    fh.write(json.dumps(r) + "\n")
        print(f"r{run} {t['id']} {arm} -> {c['status']} ({c['duration_ms']/1000:.0f}s){' ' + c['error'] if c['error'] else ''}", flush=True)

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        list(ex.map(go, todo))
    print("all cells finished", flush=True)


if __name__ == "__main__":
    main()
