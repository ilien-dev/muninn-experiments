"""Offline unit tests for MuninnPolicy against a fabricated trajectory.

Run: DREAMBENCH_ROOT=~/Projects/dreambench-swe <venv>/bin/python -m pytest -q test_muninn_policy.py
Needs the muninn release binary; no model, no network.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from muninn_policy import MUNINN_BIN, MuninnPolicy, episode_records

from dream_memory.trajectory_logger import Step, Trajectory  # DreamBench, on sys.path via muninn_policy


def fabricated_trajectory(session: int, *, events, outcome="success", diff="") -> Trajectory:
    task_id = f"expr-convention-s{session:02d}"
    raw = {
        "trajectory_id": f"{task_id}-MUNINN-stub",
        "task_id": "expr-convention",
        "benchmark_task_id": task_id,
        "session_id": task_id,
        "sequence_id": "expr-convention",
        "repo_scope": "expr-convention",
        "prompt": "Add evaluate_many(text) returning one result per non-empty line.",
        "actions": ["codex exec"],
        "agent_patch": diff,
        "production_diff": diff,
        "observations": ["4 passed"],
        "failure_observations": ["hidden detail that must not be stored"],
        "outcome": outcome,
        "terminal_outcome": outcome,
        "error_type": None if outcome == "success" else "oracle_failed",
    }
    if events:
        raw["injected_memory_events"] = events
        raw["injected_memory_event"] = events[0]
    return Trajectory(
        task_id=task_id, session_id=task_id, model_id="stub", condition_id="MUNINN", seed=1,
        budget={}, repo_commit="", steps=[Step(action="codex exec", observation="ok")],
        file_diffs=[], memory_reads=[], final_outcome=outcome, raw_episode=raw,
    )


EVENT = {
    "event_id": None, "after_session": None, "event_type": "human_feedback", "kind": "human_feedback",
    "content": "All public expression failures use EXPR_<CODE>: <message>.",
    "payload": {"learned": "All public expression failures use EXPR_<CODE>: <message>."},
    "scope": None, "labels": [], "memory_type": "human_feedback", "confidence": 0.9,
}
TASK = {
    "id": "expr-convention-s03", "sequence_id": "expr-convention", "seq_id": "expr-convention",
    "session_index": 3, "instruction": "Keep the EXPR error convention when adding tokenizer identifiers.",
    "prompt": "Keep the EXPR error convention when adding tokenizer identifiers.", "files": [],
}


@unittest.skipUnless(MUNINN_BIN.is_file(), f"muninn binary missing at {MUNINN_BIN}")
class MuninnPolicyTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.policy = MuninnPolicy(name="MUNINN", label="Muninn", description="test", run_id="unit", seed=1, store_root=Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_read_before_any_write_is_empty(self) -> None:
        self.assertEqual(self.policy.read(TASK), [])

    def test_records_are_literal_and_typed_by_origin(self) -> None:
        rows = episode_records(fabricated_trajectory(2, events=[EVENT]).raw_episode_view())
        self.assertEqual([(r["kind"], r["origin"]) for r in rows], [("decision", "user_said"), ("episode", "tool_observed")])
        self.assertEqual(rows[0]["body"], EVENT["content"])
        self.assertNotIn("hidden detail", json.dumps(rows))

    def test_write_then_read_returns_harness_item_shape(self) -> None:
        self.policy.write(fabricated_trajectory(1, events=[], diff="diff --git a/x.py b/x.py\n+def safe_evaluate(): pass\n"))
        self.assertEqual(self.policy.last_write_count, 1)
        self.policy.write(fabricated_trajectory(2, events=[EVENT]))
        self.assertEqual(self.policy.last_write_count, 2)

        items = self.policy.read(TASK)
        self.assertTrue(1 <= len(items) <= 6)
        contents = [item["content"] for item in items]
        self.assertIn(EVENT["content"], contents)
        for item in items:
            for key in ("id", "kind", "content", "type", "status", "repo_scope", "task_scope", "provenance"):
                self.assertIn(key, item)
            self.assertEqual(item["repo_scope"], "expr-convention")
        feedback = next(item for item in items if item["content"] == EVENT["content"])
        self.assertEqual((feedback["type"], feedback["origin"], feedback["trust"]), ("human_feedback", "user_said", 3))
        self.assertEqual(len(self.policy.last_retrieval_decisions), len(items))

    def test_no_lexical_match_is_empty_not_an_error(self) -> None:
        self.policy.write(fabricated_trajectory(1, events=[]))
        self.assertEqual(self.policy.read(dict(TASK, prompt="zzqx wvyk", instruction="zzqx wvyk")), [])

    def test_sequences_do_not_share_a_store(self) -> None:
        self.policy.write(fabricated_trajectory(2, events=[EVENT]))
        other = dict(TASK, id="todo-convention-s03", sequence_id="todo-convention", seq_id="todo-convention")
        self.assertEqual(self.policy.read(other), [])

    def test_read_limit_and_token_budget(self) -> None:
        for session in range(1, 12):
            self.policy.write(fabricated_trajectory(session, events=[dict(EVENT, content=f"{EVENT['content']} note {session}")], diff="x " * 900))
        items = self.policy.read(TASK)
        self.assertLessEqual(len(items), 6)
        from benchmarks.baselines import _token_count

        self.assertLessEqual(sum(_token_count(item["content"]) for item in items), 1200)
        self.assertEqual(self.policy.read(dict(TASK, read_budget_event_target=0)), [])


if __name__ == "__main__":
    unittest.main()
