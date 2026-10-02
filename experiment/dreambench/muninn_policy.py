"""MuninnPolicy: a DreamBench-SWE ``MemoryPolicy`` backed by the Muninn CLI.

Mirrors the harness contract used by ``InstancePolicy`` (B5) and
``Mem0LiteralPolicy`` (B5-MEM0-LIT) in ``src/benchmarks/baselines.py``:

* ``write(trajectory)`` stores the sanitized episode literally (no LLM, no
  summarisation) through ``muninn import``: one ``decision`` record with origin
  ``user_said`` per injected event (the harness delivers events as maintainer /
  reviewer feedback), and one ``episode`` record with origin ``tool_observed``
  for the public prompt, outcome and production diff observed by the harness.
* ``read(task)`` runs ``muninn why --json`` with the public task prompt and
  returns at most ``read_limit`` (6) items within the same 1200-token budget the
  Mem0 baselines use, in the item shape of ``_context_from_mem0_result``.

Scope is per sequence, as for Mem0 (namespace = run/condition/seed/sequence):
each sequence gets its own store directory, selected with ``MUNINN_ROOT``.

Nothing here is tuned to the tasks. Environment:
  DREAMBENCH_ROOT               DreamBench-SWE checkout (default ~/Projects/dreambench-swe)
  MUNINN_BIN                    muninn binary (default <muninn repo>/target/release/muninn)
  MUNINN_DREAMBENCH_STORE_ROOT  parent of the per-run stores (default $TMPDIR/dreambench-muninn)
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

HERE = Path(__file__).resolve().parent
DREAMBENCH_ROOT = Path(os.environ.get("DREAMBENCH_ROOT") or Path.home() / "Projects" / "dreambench-swe")
for _p in (DREAMBENCH_ROOT / "src", DREAMBENCH_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from benchmarks.baselines import (  # noqa: E402
    MEM0_READ_TOKEN_BUDGET,
    MemoryPolicy,
    _as_list,
    _assert_mem0_payload_clean,
    _effective_read_limit,
    _episode_from_any,
    _episode_sequence_id,
    _episode_task_id,
    _mem0_clean_text,
    _mem0_sanitized_event_lines,
    _safe_mem0_path_part,
    _sequence_id,
    _task_text,
    _token_count,
)

MUNINN_BIN = Path(os.environ.get("MUNINN_BIN") or HERE.parents[3] / "target" / "release" / "muninn")
MUNINN_BODY_CHARS = 2000  # record.body CHECK in crates/muninn-core/src/schema.sql
CLI_TIMEOUT_SECONDS = 30.0
IMPORT_STATS = re.compile(r"imported (?P<inserted>\d+) of (?P<read>\d+) \((?P<duplicates>\d+) duplicates, (?P<rejected>\d+) rejected\)")


class MuninnPolicy(MemoryPolicy):
    """MUNINN: literal Muninn records per sequence; read via `muninn why --json`."""

    def __init__(
        self,
        *,
        run_id: Optional[str] = None,
        condition_id: Optional[str] = None,
        seed: Optional[int] = None,
        store_root: Optional[Path] = None,
        muninn_bin: Optional[Path] = None,
        read_token_budget: int = MEM0_READ_TOKEN_BUDGET,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.run_id = str(run_id or os.environ.get("DREAMBENCH_RUN_ID") or "manual")
        self.condition_id = str(condition_id or self.name)
        self.seed = seed
        base = Path(store_root or os.environ.get("MUNINN_DREAMBENCH_STORE_ROOT") or Path(tempfile.gettempdir()) / "dreambench-muninn")
        self.store_root = base / _safe_mem0_path_part(self.run_id) / _safe_mem0_path_part(self.condition_id) / f"seed-{seed if seed is not None else 'unknown'}"
        self.muninn_bin = Path(muninn_bin or MUNINN_BIN)
        self.read_token_budget = int(read_token_budget)
        self._imports = 0

    # -- harness contract -------------------------------------------------

    def read(self, task: Any) -> List[Dict[str, Any]]:
        query = _task_text(task)
        sequence_id = _sequence_id(task)
        limit = _effective_read_limit(task, self.read_limit)
        store = self._store(sequence_id)
        if limit <= 0 or not query.strip() or not (store / ".muninn" / "muninn.db").is_file():
            self.last_retrieval_decisions = []
            return self._set_read_context([])

        out = self._cli(store, "why", "--json", "--limit", str(limit), "--budget", str(self.read_token_budget), query, ok_codes=(0, 3))  # 3 = insufficient, still valid JSON
        payload = json.loads(out)
        items = [
            _context_from_muninn_record(entry, repo_scope=sequence_id, rank=rank)
            for rank, entry in enumerate(payload.get("records") or [], start=1)
        ]
        context = self._apply_read_budget(items, limit=limit)
        self.last_retrieval_decisions = [
            {"memory_id": item["id"], "admitted": True, "reason": "muninn_why", "score": item.get("score"), "repo_scope": sequence_id}
            for item in context
        ]
        return self._set_read_context(context)

    def write(self, trajectory: Any) -> None:
        self._reset_write_stats()
        episode = _episode_from_any(trajectory)
        rows = episode_records(episode)
        if not rows:
            return
        store = self._store(_episode_sequence_id(episode))
        self._ensure_store(store)
        self._imports += 1
        path = store / "imports" / f"{self._imports:04d}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
        out = self._cli(store, "import", str(path))
        stats = IMPORT_STATS.search(out)  # `import` prints text even with --json
        if stats is None:
            raise RuntimeError(f"unexpected muninn import output: {out.strip()[:200]}")
        if int(stats["rejected"]):
            raise RuntimeError(f"muninn import rejected {stats['rejected']} record(s) from {path}")
        self.last_write_count = int(stats["inserted"])
        self.last_sleep_tokens = sum(_token_count(row["body"]) for row in rows)

    # -- helpers ----------------------------------------------------------

    def _store(self, sequence_id: str) -> Path:
        return self.store_root / _safe_mem0_path_part(sequence_id)

    def _ensure_store(self, store: Path) -> None:
        if (store / ".muninn" / "muninn.db").is_file():
            return
        store.mkdir(parents=True, exist_ok=True)
        self._cli(store, "init", "--keep-native")
        if not (store / ".muninn" / "muninn.db").is_file():
            raise RuntimeError(f"muninn init did not create a store under {store}")

    def _cli(self, store: Path, *args: str, ok_codes: Sequence[int] = (0,)) -> str:
        env = dict(os.environ)
        env["MUNINN_ROOT"] = str(store)
        env.pop("MUNINN_SOURCE_ROOT", None)
        proc = subprocess.run(
            [str(self.muninn_bin), *args],
            cwd=str(store),
            env=env,
            text=True,
            capture_output=True,
            timeout=CLI_TIMEOUT_SECONDS,
        )
        if proc.returncode not in ok_codes:
            raise RuntimeError(f"muninn {args[0]} exit {proc.returncode}: {proc.stderr.strip()[:500]}")
        return proc.stdout

    def _apply_read_budget(self, context: Sequence[Dict[str, Any]], *, limit: int) -> List[Dict[str, Any]]:
        # Same admission rule as Mem0Policy._apply_read_budget (baselines.py).
        admitted: List[Dict[str, Any]] = []
        used = 0
        for item in context:
            if len(admitted) >= limit or used >= self.read_token_budget:
                break
            content = str(item.get("content") or "")
            remaining = self.read_token_budget - used
            tokens = _token_count(content)
            item = dict(item)
            if tokens > remaining:
                item["content"] = " ".join(content.split()[:remaining])
                tokens = _token_count(item["content"])
            used += tokens
            admitted.append(item)
        return admitted


def episode_records(episode: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """Literal Muninn import rows for one harness episode (no summarisation)."""
    sequence_id = _mem0_clean_text(_episode_sequence_id(dict(episode)))
    task_id = _mem0_clean_text(_episode_task_id(dict(episode)))
    rows: List[Dict[str, Any]] = []

    for index, line in enumerate(_mem0_sanitized_event_lines(episode), start=1):
        _assert_mem0_payload_clean(line)
        rows.append({
            "kind": "decision",
            "origin": "user_said",
            "subject": f"dreambench:{sequence_id}:{task_id}:event:{index}",
            "body": line[:MUNINN_BODY_CHARS],
            "session_id": task_id,
        })

    lines: List[str] = []
    prompt = _mem0_clean_text(str(episode.get("prompt") or episode.get("instruction") or ""))
    if prompt:
        lines.append(f"For sequence {sequence_id}, task {task_id}, the public task prompt was: {prompt}")
    outcome = str(episode.get("outcome") or episode.get("terminal_outcome") or "").lower()
    if outcome:
        lines.append(f"The task outcome was {'passed' if outcome in {'success', 'passed', 'true'} else 'failed'}.")
    error_type = _mem0_clean_text(str(episode.get("error_type") or ""))
    if error_type:
        lines.append(f"The public error type was {error_type}.")
    actions = [a for a in (_mem0_clean_text(x) for x in _as_list(episode.get("actions"))) if a]
    if actions:
        lines.append(f"The public agent actions were: {'; '.join(actions[:12])}.")
    diff = _mem0_clean_text(str(episode.get("production_diff") or episode.get("agent_patch") or episode.get("patch") or ""))
    if diff:
        lines.append(f"The public production diff was: {diff}")
    if lines:
        body = "\n".join(lines)
        _assert_mem0_payload_clean(body)
        rows.append({
            "kind": "episode",
            "origin": "tool_observed",
            "subject": f"dreambench:{sequence_id}:{task_id}:episode",
            "body": body[:MUNINN_BODY_CHARS],
            "session_id": task_id,
        })
    return rows


def _context_from_muninn_record(entry: Mapping[str, Any], *, repo_scope: str, rank: int) -> Dict[str, Any]:
    """Item shape of baselines._context_from_mem0_result, filled from a `why --json` record."""
    record = dict(entry.get("record") or {})
    origin = str(record.get("origin") or "")
    return {
        "id": f"muninn-{record.get('id', rank)}",
        "kind": "memory",
        "content": str(record.get("body") or record.get("object") or ""),
        "type": "human_feedback" if origin in {"user_said", "review_accepted"} else "episodic",
        "status": "retired" if record.get("invalid") else "active",
        "confidence": 1.0,
        "utility_score": 0.5,
        "risk_score": 0.2,
        "staleness_score": 0.0,
        "retrieval_tags": ["muninn", repo_scope, str(record.get("kind") or "")],
        "repo_scope": repo_scope,
        "file_scope": [],
        "task_scope": [repo_scope],
        "superseded_by": [],
        "provenance": {
            "trajectory_ids": [],
            "task_ids": [str(record.get("session_id") or "")],
            "repo_commits": [],
            "file_paths": [],
            "command_outputs": [],
            "human_feedback_ids": [],
        },
        "origin": origin,
        "trust": record.get("trust"),
        "rank": rank,
        "score": entry.get("score"),
    }
