#!/usr/bin/env python3
"""Round 8 of Gate 4 §3 (PM-Bench): held-out weeks, store ablation, second model family.

Pre-registered in ../experiment/PREREGISTRATION.md ("round 8") before any cell ran. This
launcher is the whole procedure, so a reader can re-run it:

  1. Held-out weeks. Seeds are derived from the pre-registration commit hash
     (sha256("<commit>:<k>") for k = 0, 1, 2 → first 8 hex digits mod 100000, 42 excluded),
     so they could not be chosen after seeing a result. PM-Bench's own generator at its
     pinned commit builds and validates them; nobody reads them before the runs.
  2. One bridge process per model (claude_bridge.py over `claude -p`, codex_bridge.py over
     `codex exec`), isolated: no user or project settings, no tools, no MCP, bare cwd. Its
     /canary answer is recorded before the first run and in every run's manifest.
  3. Every arm goes through that same bridge. Arms: muninn_store (round-7 scaffold, the
     muninn binary inside a network namespace with no interfaces), plain_store (identical
     scaffold, in-process dict, no muninn binary), single_baseline and todo_ledger
     (PM-Bench's own runners, untouched, scored by PM-Bench's own scorer).
  4. Runs per (arm, week): 3. Launches staggered because PM-Bench names logs by the
     launch second. jobs.jsonl records every launch, exit code and wall time; a crash inside
     PM-Bench's own parser is re-run once and both attempts stay on disk.

Usage:
  run_round8.py --pmbench <checkout> --out <dir> --prereg-commit <sha> \
      --model claude-sonnet-5 --bridge claude --port 30002 [--runs 3] [--jobs 8] \
      [--arms muninn_store,plain_store,single_baseline,todo_ledger] [--weeks v9,heldout]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def heldout_seeds(commit: str, n: int = 3) -> list[int]:
    seeds: list[int] = []
    k = 0
    while len(seeds) < n:
        s = int(hashlib.sha256(f"{commit}:{k}".encode()).hexdigest()[:8], 16) % 100000
        k += 1
        if s != 42 and s not in seeds:
            seeds.append(s)
    return seeds


def make_weeks(py: str, pmb: Path, out: Path, commit: str, which: list[str]) -> list[tuple[str, Path]]:
    wdir = out / "weeks"
    wdir.mkdir(parents=True, exist_ok=True)
    weeks: list[tuple[str, Path]] = []
    manifest: dict = {"prereg_commit": commit, "pmbench_commit": git_head(pmb),
                      "generator_sha256": sha256(pmb / "sim" / "week_builder_v9.py"), "weeks": []}
    if "v9" in which:
        p = pmb / "data" / "synthetic_week_v9.json"
        weeks.append(("v9", p))
        manifest["weeks"].append({"name": "v9", "seed": 42, "path": str(p), "sha256": sha256(p)})
    if "heldout" in which:
        for seed in heldout_seeds(commit):
            name = f"heldout-{seed}"
            p = wdir / f"{name}.json"
            if not p.exists():
                r = subprocess.run([py, str(pmb / "sim" / "generate_week_v9.py"), "--seed", str(seed),
                                    "--scenario-name", name, "--out", str(p)], capture_output=True, text=True)
                (wdir / f"{name}.generate.log").write_text(r.stdout + r.stderr)
                if r.returncode != 0:
                    sys.exit(f"week generation failed for seed {seed}: {r.stderr[-500:]}")
            v = subprocess.run([py, str(pmb / "sim" / "pm_bench.py"), "validate", "--scenario", str(p)],
                               capture_output=True, text=True)
            if v.returncode != 0:
                sys.exit(f"PM-Bench validator rejected seed {seed}: {v.stdout[-300:]} {v.stderr[-300:]}")
            weeks.append((name, p))
            manifest["weeks"].append({"name": name, "seed": seed, "path": str(p), "sha256": sha256(p),
                                      "validator": v.stdout.strip()})
    (wdir / "MANIFEST.json").write_text(json.dumps(manifest, indent=1))
    return weeks


def git_head(repo: Path) -> str:
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def http_get(url: str, timeout: int = 320) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode())


def ensure_bridge(py: str, kind: str, port: int, model: str, out: Path) -> str:
    base = f"http://127.0.0.1:{port}"
    try:
        h = http_get(base + "/health", timeout=5)
        if h.get("model") != model:
            sys.exit(f"a bridge on port {port} serves {h.get('model')}, not {model}")
    except Exception:  # noqa: BLE001
        script = HERE / ("claude_bridge.py" if kind == "claude" else "codex_bridge.py")
        log = open(out / f"bridge-{kind}.log", "a")
        args = [py, str(script), "--port", str(port), "--model", model]
        if kind == "codex":
            args += ["--log", str(out / "bridge-codex-requests.jsonl")]
        subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        for _ in range(60):
            time.sleep(1)
            try:
                http_get(base + "/health", timeout=5)
                break
            except Exception:  # noqa: BLE001
                continue
        else:
            sys.exit("bridge did not come up")
    canary = http_get(base + "/canary")
    (out / "canary.json").write_text(json.dumps(canary, indent=1))
    print("canary:", json.dumps(canary)[:300], flush=True)
    try:   # marker-based leak probe (bridges built after the sonnet launch)
        canary2 = http_get(base + "/canary2")
        (out / "canary2.json").write_text(json.dumps(canary2, indent=1))
        print("canary2:", json.dumps(canary2)[:300], flush=True)
    except Exception as exc:  # noqa: BLE001
        print("canary2 unavailable:", exc, flush=True)
    return base + "/v1"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pmbench", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prereg-commit", required=True)
    ap.add_argument("--model", default="claude-sonnet-5")
    ap.add_argument("--bridge", choices=["claude", "codex"], default="claude")
    ap.add_argument("--port", type=int, default=30002)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--arms", default="muninn_store,plain_store,single_baseline,todo_ledger")
    ap.add_argument("--weeks", default="v9,heldout")
    ap.add_argument("--muninn-bin", default=str(HERE.parents[2] / "target" / "release" / "muninn"))
    ap.add_argument("--shadow", action="store_true", help="round 9: muninn_store runs keep a dict shadow store and log both boards at every step")
    ap.add_argument("--resume", action="store_true",
                    help="keep every run that finished with a score file, delete partial run directories, and launch only what is missing; "
                         "refuses if the muninn binary hash differs from the previous FROZEN.json")
    a = ap.parse_args()

    pmb = Path(a.pmbench).resolve()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    py = str(pmb / ".venv" / "bin" / "python")
    arms = a.arms.split(",")
    weeks = make_weeks(py, pmb, out, a.prereg_commit, a.weeks.split(","))
    base_url = ensure_bridge(py, a.bridge, a.port, a.model, out)

    # the muninn binary runs with no network interfaces (unshare -rn); see muninn-nonet
    env = dict(os.environ)
    env["MUNINN_BIN"] = str(HERE / "muninn-nonet")
    env["MUNINN_REAL_BIN"] = a.muninn_bin
    env["PMBENCH_ROOT"] = str(pmb)
    env["PYTHONUNBUFFERED"] = "1"
    frozen = {"launcher_sha256": sha256(Path(__file__)), "scaffold_sha256": sha256(HERE / "run_muninn_pis.py"),
              "claude_bridge_sha256": sha256(HERE / "claude_bridge.py"),
              "codex_bridge_sha256": sha256(HERE / "codex_bridge.py") if (HERE / "codex_bridge.py").exists() else None,
              "muninn_bin_sha256": sha256(Path(a.muninn_bin)), "muninn_commit": git_head(HERE.parents[2]),
              "pmbench_commit": git_head(pmb), "pm_bench_py_sha256": sha256(pmb / "sim" / "pm_bench.py"),
              "run_eval_py_sha256": sha256(pmb / "sim" / "run_eval.py"),
              "model": a.model, "bridge": a.bridge, "base_url": base_url, "runs": a.runs, "arms": arms,
              "weeks": [w for w, _ in weeks], "prereg_commit": a.prereg_commit,
              "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    done: dict[tuple[str, str], int] = {}
    if a.resume and (out / "FROZEN.json").exists():
        prev = json.loads((out / "FROZEN.json").read_text())
        for key in ("muninn_bin_sha256", "scaffold_sha256", "claude_bridge_sha256", "codex_bridge_sha256", "pm_bench_py_sha256"):
            if prev.get(key) != frozen.get(key):
                sys.exit(f"resume refused: {key} changed since the grid started ({prev.get(key)} -> {frozen.get(key)})")
        frozen["resumed"] = prev.get("resumed", []) + [{"at_utc": frozen["started_utc"], "previous_started_utc": prev.get("started_utc")}]
        frozen["started_utc"] = prev.get("started_utc", frozen["started_utc"])
        removed = []
        for wname, _ in weeks:
            for arm in arms:
                d = out / wname / arm
                # a run directory is one whose own log `<dir>/<dir>.jsonl` exists; store arms
                # keep runs at `<arm>/<run>/`, PM-Bench baselines at `<arm>/<model>/<run>/`.
                # complete = its score report exists; partial run directories are removed;
                # anything else (the stores' scratch roots) is left alone. `excess-runs/`
                # (runs beyond the pre-registered count, moved aside) is never counted.
                n = 0
                runs_here = [q for q in (d.rglob("*") if d.exists() else [])
                             if q.is_dir() and "excess-runs" not in q.parts
                             and ((q / f"{q.name}.jsonl").exists() or (q / f"{q.name}.prompt.txt").exists())]
                for rd in sorted(runs_here):
                    if (rd / f"{rd.name}.score.md").exists():
                        n += 1
                    else:
                        removed.append(str(rd.relative_to(out)))
                        subprocess.run(["rm", "-rf", str(rd)], check=True)
                done[(wname, arm)] = n
        frozen["resume_removed_partial_dirs"] = frozen.get("resume_removed_partial_dirs", []) + removed
        print(f"resume: complete runs kept per (week, arm): { {f'{w}/{ar}': n for (w, ar), n in done.items() if n} }; partial dirs removed: {len(removed)}", flush=True)
    (out / "FROZEN.json").write_text(json.dumps(frozen, indent=1))

    jobs: list[dict] = []
    for wname, wpath in weeks:
        for run in range(1, a.runs + 1):
            for arm in arms:
                d = out / wname / arm
                d.mkdir(parents=True, exist_ok=True)
                if run <= done.get((wname, arm), 0):
                    continue
                if arm in ("muninn_store", "plain_store"):
                    cmd = [py, "-u", str(HERE / "run_muninn_pis.py"), "--scenario", str(wpath), "--model", a.model,
                           "--out-dir", str(d), "--score", "--base-url", base_url,
                           "--store", ("muninn-shadow" if a.shadow and arm == "muninn_store" else arm.split("_")[0])]
                else:
                    cmd = [py, "-u", str(pmb / "sim" / "run_eval.py"), "--setup", arm, "--scenario", str(wpath),
                           "--backend", "sglang", "--base-url", base_url, "--model", a.model, "--out-dir", str(d),
                           "--score", "--temperature", "0"]
                jobs.append({"week": wname, "arm": arm, "run": run, "cmd": cmd, "log": str(d / f"r{run}.log")})

    lock = threading.Lock()
    launch_lock = threading.Lock()
    ledger = open(out / "jobs.jsonl", "a", buffering=1)

    def record(j: dict, **kw) -> None:
        with lock:
            ledger.write(json.dumps({**{k: v for k, v in j.items() if k != "cmd"}, **kw}) + "\n")

    def run_job(j: dict) -> None:
        for attempt in (1, 2):
            with launch_lock:
                time.sleep(1.3)   # PM-Bench names its log by the launch second
                t0 = time.time()
                log = open(j["log"] if attempt == 1 else j["log"] + ".retry", "w")
                p = subprocess.Popen(j["cmd"], stdout=log, stderr=subprocess.STDOUT, env=env, cwd=str(pmb))
            record(j, event="start", attempt=attempt, pid=p.pid, cmd=" ".join(j["cmd"]))
            rc = p.wait()
            log.close()
            tail = Path(log.name).read_text(errors="replace")[-600:]
            record(j, event="exit", attempt=attempt, rc=rc, wall_s=round(time.time() - t0, 1))
            parser_crash = rc != 0 and "Traceback" in tail and j["arm"] in ("single_baseline", "todo_ledger")
            if rc == 0 or not parser_crash:
                return
            record(j, event="retry", attempt=attempt, reason="crash inside PM-Bench runner", tail=tail[-300:])

    print(f"{len(jobs)} jobs, {a.jobs} at a time, out={out}", flush=True)
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        list(ex.map(run_job, jobs))
    print("all jobs finished", flush=True)


if __name__ == "__main__":
    main()
