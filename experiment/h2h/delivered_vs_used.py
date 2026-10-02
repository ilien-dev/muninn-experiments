#!/usr/bin/env python3
"""Was the memory wrong, or was the answer? (PREREGISTRATION.md, same title.)

A head-to-head cell fails two ways that are not the same thing: the memory did not put the
current decision in front of the agent, or it did and the agent wrote something else. The
first is a memory result; the second is a statement about how an agent treats injected
context, and counting it against the memory makes a grid that improving the memory cannot
move.

For every cell, this reads the cell's own transcript for what the memory put in front of the
model: the `hook_additional_context` and `hook_system_message` attachments, **and the results
of the memory's own tools** — claude-mem ships an MCP search server and Muninn allows
`muninn why` / `muninn status`, so either agent can ask for more. Counting only the injection
would have scored a cell where the agent searched claude-mem's store and found the answer as
"passed without memory", which it plainly did not; four cells of the first grid were exactly
that. Crossed with the oracle:

    used                        delivered and the oracle passed
    delivered and not used      delivered and the oracle failed
    passed without memory       not delivered and the oracle passed anyway
    not delivered               not delivered and the oracle failed

Beside those four counts, two more that say what the agent did with what it was given: how
often it asked its memory for more, and how often it went looking in the repository instead
(`Bash`, `Grep`, `Glob`, `Read`). An agent that believes what it was told does not need to go
looking.

It is a floor on delivery: a substring search cannot tell a block that states the value from
one that merely contains the word, and it says nothing about whether the block was legible.

  delivered_vs_used.py <results dir> [<results dir> ...]
"""
import argparse
import json
import pathlib

INJECTED = ("hook_additional_context", "hook_system_message")
# a tool call is the memory's own if its name or its command names the memory
MEMORY_TOOL = ("claude-mem", "agentmemory", "mem0")
MEMORY_CMD = ("muninn why", "muninn status", "muninn recall")


def injected_text(path: pathlib.Path) -> str:
    """Everything the memory put in front of the model: what its hooks injected, and what its
    own tools returned when the agent asked."""
    if not path.exists():
        return ""
    out, memory_calls = [], set()
    for line in path.open(errors="replace"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        at = r.get("attachment") or {}
        if r.get("type") == "attachment" and at.get("type") in INJECTED:
            c = at.get("content")
            out.append(" ".join(c) if isinstance(c, list) else str(c))
            continue
        content = (r.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for x in content:
            if not isinstance(x, dict):
                continue
            if x.get("type") == "tool_use":
                name = str(x.get("name", "")).lower()
                cmd = str((x.get("input") or {}).get("command", "")).lower()
                if any(t in name for t in MEMORY_TOOL) or any(c in cmd for c in MEMORY_CMD):
                    memory_calls.add(x.get("id"))
            elif x.get("type") == "tool_result" and x.get("tool_use_id") in memory_calls:
                out.append(json.dumps(x.get("content")))
    return " ".join(out).lower()


SEARCH_TOOLS = ("bash", "grep", "glob", "read")


def tool_counts(path: pathlib.Path) -> tuple:
    """(memory asks, repository looks) in one cell."""
    if not path.exists():
        return (0, 0)
    asks = looks = 0
    for line in path.open(errors="replace"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        content = (r.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for x in content:
            if not isinstance(x, dict) or x.get("type") != "tool_use":
                continue
            name = str(x.get("name", "")).lower()
            cmd = str((x.get("input") or {}).get("command", "")).lower()
            if any(t in name for t in MEMORY_TOOL) or any(c in cmd for c in MEMORY_CMD):
                asks += 1
            elif name in SEARCH_TOOLS:
                looks += 1
    return (asks, looks)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    a = ap.parse_args()
    print("| grid | arm | used | delivered, not used | passed without memory | not delivered "
          "| memory asks / cell | repository looks / cell |")
    print("|---|---|---|---|---|---|---|---|")
    for d in a.dirs:
        d = pathlib.Path(d)
        if not (d / "results.jsonl").exists():
            continue
        cfg = json.loads((d / "config.json").read_text())
        sc = {t["id"]: t["scenario"] for t in cfg["tasks"]}
        rows = [json.loads(l) for l in (d / "results.jsonl").read_text().splitlines() if l.strip()]
        tally: dict = {}
        for r in rows:
            s = sc[r["task"]]
            if s["new"] is None or r.get("error"):
                continue
            if r["arm"] == "off":
                continue
            text = injected_text(d / "logs" / f"r{r['run']}-{r['task']}-{r['arm']}.transcript.jsonl")
            new = s["new"].lower().split(" with ")[0]
            delivered = new in text
            passed = r["status"] == "pass"
            key = (delivered, passed)
            t = tally.setdefault(r["arm"], {k: 0 for k in
                                            [(True, True), (True, False), (False, True), (False, False)]})
            t[key] += 1
            asks, looks = tool_counts(
                d / "logs" / f"r{r['run']}-{r['task']}-{r['arm']}.transcript.jsonl")
            t["asks"] = t.get("asks", 0) + asks
            t["looks"] = t.get("looks", 0) + looks
            t["cells"] = t.get("cells", 0) + 1
        for arm, t in sorted(tally.items()):
            n = max(t.get("cells", 1), 1)
            print(f"| {d.name} | {arm} | {t[(True, True)]} | {t[(True, False)]} | "
                  f"{t[(False, True)]} | {t[(False, False)]} | {t.get('asks', 0) / n:.1f} | "
                  f"{t.get('looks', 0) / n:.1f} |")


if __name__ == "__main__":
    main()
