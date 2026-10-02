#!/usr/bin/env python3
"""The two Mem0 calls, wired to Claude Code's hooks. Nothing else.

Mem0 ships no Claude Code plugin, so the head-to-head cannot inject a vendor plugin for this
arm the way it does for `claude-mem` and `agentmemory`. This shim gives Mem0 the same two
operations every other arm performs automatically, and no more:

  Stop              → `Memory.add(messages)` with the session's user turns
  UserPromptSubmit  → `Memory.search(prompt)`, printed so the turn can see it

There is no prompt engineering here, no reranking, no filtering, no retry on a bad parse and
no tuning of `limit`. Both calls are the documented ones with documented arguments. That is
deliberate: the arm's pre-registration records that *we* wrote our competitor's integration,
which is a conflict of interest, and the only defence available is that the integration is
this short, this plain, and committed where anyone can read it.

Configuration comes from the environment, so the arm script owns every choice:
  MEM0_DATA        per-cell directory for the vector store (isolation)
  MEM0_OLLAMA      base URL of the pinned Ollama
  MEM0_LLM         extractor model
  MEM0_EMBEDDER    embedding model
  MEM0_USER        the user id memories are stored under
  MEM0_LOG         a JSONL line per call: what was asked, what came back, how long it took

Exit status is always 0. A memory tool that breaks the agent's session is not being measured
fairly, and neither is one whose failures are hidden — hence the log.
"""
import json
import os
import sys
import time


def log(event, **fields):
    path = os.environ.get("MEM0_LOG")
    if not path:
        return
    try:
        with open(path, "a") as fh:
            fh.write(json.dumps({"at": int(time.time() * 1000), "event": event, **fields}) + "\n")
    except Exception:
        pass


def memory():
    from mem0 import Memory

    base = os.environ["MEM0_OLLAMA"]
    return Memory.from_config({
        "llm": {"provider": "ollama", "config": {
            "model": os.environ["MEM0_LLM"], "temperature": 0.1,
            "max_tokens": 2000, "ollama_base_url": base}},
        "embedder": {"provider": "ollama", "config": {
            "model": os.environ["MEM0_EMBEDDER"], "ollama_base_url": base}},
        "vector_store": {"provider": "chroma", "config": {
            "collection_name": "h2h", "path": os.environ["MEM0_DATA"] + "/chroma"}},
    })


def user_turns(transcript_path):
    """The session's user messages, oldest first — the same text every other arm captures."""
    out = []
    try:
        with open(transcript_path) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("type") != "user":
                    continue
                content = (row.get("message") or {}).get("content")
                if isinstance(content, list):
                    content = " ".join(
                        c.get("text", "") for c in content if isinstance(c, dict)
                    )
                if isinstance(content, str) and content.strip():
                    out.append(content.strip())
    except OSError:
        pass
    return out


def main() -> int:
    event = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    t0 = time.time()

    if event == "Stop":
        turns = user_turns(payload.get("transcript_path", ""))
        if not turns:
            log("stop.empty")
            return 0
        try:
            res = memory().add(
                [{"role": "user", "content": t} for t in turns],
                user_id=os.environ.get("MEM0_USER", "dev"),
            )
            log("stop.add", turns=len(turns), results=len((res or {}).get("results", [])),
                ms=int((time.time() - t0) * 1000))
        except Exception as e:  # a failing memory must not fail the session
            log("stop.error", error=str(e)[:400], ms=int((time.time() - t0) * 1000))
        return 0

    if event == "UserPromptSubmit":
        prompt = payload.get("prompt", "")
        if not prompt.strip():
            return 0
        try:
            res = memory().search(prompt, user_id=os.environ.get("MEM0_USER", "dev"), limit=8)
            items = [m.get("memory", "") for m in (res or {}).get("results", [])]
            log("prompt.search", hits=len(items), ms=int((time.time() - t0) * 1000))
            if items:
                print("[mem0] memories relevant to this turn:")
                for m in items:
                    print(f"- {m}")
        except Exception as e:
            log("prompt.error", error=str(e)[:400], ms=int((time.time() - t0) * 1000))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
