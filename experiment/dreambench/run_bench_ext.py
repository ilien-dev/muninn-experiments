"""Drop-in wrapper around DreamBench-SWE ``src/experiments/run_bench.py``.

Adds two things without editing the DreamBench checkout:

* condition ``MUNINN`` -> ``MuninnPolicy`` (registered in ``BASELINE_REGISTRY`` so the
  harness's own ``--condition`` choices accept it, and built with run_id/seed like the
  Mem0 conditions);
* ``DREAMBENCH_MEM0_OFFLINE=1`` -> ``B5-MEM0-LIT`` gets an injected local mem0 OSS
  ``Memory`` client (fastembed embedder, local Qdrant, ``infer=False`` so no LLM call)
  instead of the hosted ``MemoryClient`` the paper used (baselines.py ``_construct_client``).

Every other argument, the agent, the oracle scoring and the output files are the
harness's own. Usage: identical to run_bench.py, e.g.

    python run_bench_ext.py --condition MUNINN --seq expr-convention --model gpt-5.5 --seed 1
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

from muninn_policy import MuninnPolicy  # also puts DreamBench src/ and root on sys.path

from benchmarks.baselines import BASELINE_REGISTRY, BaselineSpec, Mem0LiteralPolicy, _safe_mem0_path_part  # noqa: E402
from experiments import run_bench  # noqa: E402

MUNINN_CONDITION = "MUNINN"
MEM0_OFFLINE_EMBEDDER = os.environ.get("DREAMBENCH_MEM0_EMBEDDER", "BAAI/bge-small-en-v1.5")
MEM0_OFFLINE_DIMS = int(os.environ.get("DREAMBENCH_MEM0_EMBEDDING_DIMS", "384"))

BASELINE_REGISTRY.setdefault(
    MUNINN_CONDITION,
    BaselineSpec(MUNINN_CONDITION, "Muninn", MuninnPolicy, "Literal Muninn records per sequence, read via muninn why."),
)

_original_policy_for_condition = run_bench._policy_for_condition


def mem0_offline_config(run_id: str, seed: Optional[int]) -> dict:
    root = Path(os.environ.get("DREAMBENCH_MEM0_OFFLINE_ROOT") or Path(tempfile.gettempdir()) / "dreambench-mem0-offline")
    path = root / _safe_mem0_path_part(run_id) / f"seed-{seed}"
    path.mkdir(parents=True, exist_ok=True)
    return {
        "embedder": {"provider": "fastembed", "config": {"model": MEM0_OFFLINE_EMBEDDER}},
        "vector_store": {
            "provider": "qdrant",
            "config": {"collection_name": "dreambench", "path": str(path / "qdrant"), "embedding_model_dims": MEM0_OFFLINE_DIMS, "on_disk": True},
        },
        # Never called with infer=False; mem0 still constructs an LLM object, so give it
        # an unreachable endpoint and a dummy key rather than a real provider.
        "llm": {"provider": "openai", "config": {"model": "unused-infer-false", "api_key": "unused-infer-false", "openai_base_url": "http://127.0.0.1:9/v1"}},
        "history_db_path": str(path / "history.db"),
    }


def _policy_for_condition(condition: str, *, judge_client: Any = None, include_live_baselines: bool = False, run_id: Optional[str] = None, seed: Optional[int] = None):
    normalized = run_bench._normalize_condition(condition, include_live_baselines=include_live_baselines)
    if normalized == MUNINN_CONDITION:
        return MuninnPolicy(
            name=MUNINN_CONDITION,
            label="Muninn",
            description=BASELINE_REGISTRY[MUNINN_CONDITION].description,
            run_id=run_id,
            condition_id=MUNINN_CONDITION,
            seed=seed,
        )
    if normalized == run_bench.MEM0_LITERAL_CONDITION and os.environ.get("DREAMBENCH_MEM0_OFFLINE") == "1":
        os.environ.setdefault("MEM0_TELEMETRY", "False")
        from mem0 import Memory

        client = Memory.from_config(mem0_offline_config(str(run_id or "manual"), seed))
        policy = Mem0LiteralPolicy(
            name=run_bench.MEM0_LITERAL_CONDITION,
            label="Mem0Literal",
            description="mem0ai OSS (offline: fastembed + local Qdrant), infer=False literal storage.",
            client=client,
            run_id=run_id,
            condition_id=run_bench.MEM0_LITERAL_CONDITION,
            seed=seed,
        )
        policy.client_backend = "oss-offline"
        return policy
    return _original_policy_for_condition(
        condition, judge_client=judge_client, include_live_baselines=include_live_baselines, run_id=run_id, seed=seed
    )


run_bench._policy_for_condition = _policy_for_condition

if __name__ == "__main__":
    raise SystemExit(run_bench.main(sys.argv[1:]))
