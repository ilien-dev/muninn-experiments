#!/usr/bin/env python3
"""What a memory tool delivered to the agent in one Claude Code session.

Neither competitor logs its hook output or its MCP results, so the source of truth is the
session transcript Claude Code writes (~/.claude/projects/<cwd>/<session_id>.jsonl): hook
attachments whose command belongs to the tool's plugin, and every MCP call to the tool's
server with its result. Worker-log lines about retrieval are added when a log dir is given.

usage: delivered.py --tool NAME --mcp-prefix PREFIX [--hook-marker S] [--transcript T] [--worker-logs DIR]
"""
import argparse, glob, json, re, sys

ap = argparse.ArgumentParser()
ap.add_argument("--tool", required=True)
ap.add_argument("--mcp-prefix", required=True)
ap.add_argument("--hook-marker", default=None, help="substring of the plugin's hook commands")
ap.add_argument("--hooks-json", default=None, help="the plugin's hooks.json: its exact command strings identify its hooks")
ap.add_argument("--transcript")
ap.add_argument("--worker-logs")
ap.add_argument("--log-pattern", default=r"/api/(search|context|timeline|observations)|context inject|smart-search|/agentmemory/(search|smart-search|context|session/start|enrich)")
a = ap.parse_args()
marker = a.hook_marker or a.tool
commands = set()
if a.hooks_json:
    for groups in json.load(open(a.hooks_json)).get("hooks", {}).values():
        for g in groups:
            for h in g.get("hooks", []):
                commands.add(h.get("command", ""))

def ours(command):
    return bool(command) and (command in commands or marker in command)

out = {"tool": a.tool, "source": None, "hooks": [], "mcp_calls": [], "worker_log_lines": []}

def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") if isinstance(c, dict) else str(c) for c in content)
    return json.dumps(content)

if a.transcript:
    import os
    if not os.path.exists(a.transcript):
        # Claude Code's project slug replaces every non-alphanumeric character; a caller that
        # guessed it differently still names the session id, which is unique
        hits = glob.glob(os.path.expanduser("~/.claude/projects/*/") + os.path.basename(a.transcript))
        if len(hits) == 1:
            a.transcript = hits[0]
    out["source"] = a.transcript
    calls = {}
    try:
        lines = open(a.transcript).read().splitlines()
    except OSError as e:
        out["error"] = f"transcript unreadable: {e}"
        lines = []
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        att = d.get("attachment") or {}
        kind = att.get("type", "")
        if kind == "hook_success" and ours(att.get("command")):
            out["hooks"].append({"event": att.get("hookEvent"), "name": att.get("hookName"),
                                 "exit": att.get("exitCode"), "content": att.get("content", ""),
                                 "stdout": att.get("stdout", ""),
                                 "stderr": att.get("stderr", "")})
        elif kind in ("hook_additional_context", "hook_system_message", "hook_blocking_error", "hook_error"):
            body = text_of(att.get("content"))
            out["hooks"].append({"event": att.get("hookEvent") or kind, "name": att.get("hookName"),
                                 "attachment": kind, "content": body})
        msg = d.get("message") or {}
        if isinstance(msg.get("content"), list):
            for c in msg["content"]:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "tool_use" and str(c.get("name", "")).startswith(a.mcp_prefix):
                    calls[c["id"]] = {"tool": c["name"], "input": c.get("input"), "result": None}
                    out["mcp_calls"].append(calls[c["id"]])
                elif c.get("type") == "tool_result" and c.get("tool_use_id") in calls:
                    calls[c["tool_use_id"]]["result"] = text_of(c.get("content"))
                    calls[c["tool_use_id"]]["is_error"] = bool(c.get("is_error"))
else:
    out["note"] = "no transcript given: the tool itself does not log what it injected or returned"

if a.worker_logs:
    pat = re.compile(a.log_pattern)
    for p in sorted(glob.glob(a.worker_logs.rstrip("/") + "/*.log")):
        for l in open(p, errors="replace"):
            if pat.search(l):
                out["worker_log_lines"].append(l.rstrip()[:500])

json.dump(out, sys.stdout, ensure_ascii=False)
print()
