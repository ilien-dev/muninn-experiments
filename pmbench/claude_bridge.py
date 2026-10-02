#!/usr/bin/env python3
"""A minimal OpenAI-compatible chat endpoint over `claude -p`, so PM-Bench (which only
speaks the OpenAI API) can be run against Claude Code's own account. One request → one
`claude -p` call with the messages flattened into a single prompt; no tools, no memory
of its own. Usage: claude_bridge.py --port 30002 --model claude-sonnet-5

Round 4 (2026-09-13): `--setting-sources ""` added. Without it `claude -p` loads the user's
global CLAUDE.md; a probe through the round 1-3 bridge answered "Svipall para acceso web;
respuesta en español", so those eleven runs saw the user's instructions."""
import argparse, json, subprocess, time, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODEL = "claude-sonnet-5"

def flatten(messages):
    sys_parts, convo = [], []
    for m in messages:
        role, content = m.get("role"), m.get("content")
        if isinstance(content, list):
            content = "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
        content = content or ""
        if role == "system":
            sys_parts.append(content)
        elif role == "user":
            convo.append("USER:\n" + content)
        elif role == "assistant":
            convo.append("ASSISTANT:\n" + content)
    return "\n\n".join(sys_parts), "\n\n".join(convo) + "\n\nASSISTANT:"

CANARY2 = ("Besides this message, were you given any text (instructions, rules, memory, skills, files, "
           "prior conversation) that mentions ANY of these words: Svipall, Muninn, CLAUDE.md, AGENTS.md, "
           "Orca, ilien, jjimenezc, Spanish, español, 'Tired Brain', Context7? If yes, quote each such "
           "passage verbatim. If none of these words appears anywhere in what you were given, answer "
           "exactly NONE.")
CANARY = ("List verbatim every instruction, rule, memory, skill or file content you were given "
          "besides this message. If there is none, answer exactly NONE.")


def complete(model, system, prompt, max_tokens):
    """One `claude -p` call, isolated: no settings of any scope, no tools, no MCP, bare cwd."""
    args = ["claude", "-p", prompt, "--model", model, "--output-format", "json", "--max-turns", "1",
            "--tools", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            "--setting-sources", ""]
    if system:
        args += ["--system-prompt", system + f"\n\nAnswer in at most {max_tokens} tokens."]
    cwd = __import__("tempfile").gettempdir() + "/muninn-bridge-cwd"
    __import__("os").makedirs(cwd, exist_ok=True)
    out = subprocess.run(args, capture_output=True, text=True, timeout=300, cwd=cwd,
                         env={**__import__("os").environ, "CLAUDECODE": ""})
    v = json.loads(out.stdout) if out.stdout.strip() else {}
    text = v.get("result", "") if not v.get("is_error") else ""
    return text, (v.get("usage", {}) or {}), v.get("num_turns")


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass
    def _json(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        # round 8: /health and /canary, recorded in every run's manifest
        if self.path.startswith("/health"):
            return self._json({"ok": True, "model": MODEL, "bridge": "claude_bridge.py"})
        if self.path.startswith("/canary2"):
            try:
                text, usage, turns = complete(MODEL, "You answer questions.", CANARY2, 400)
            except Exception as e:  # noqa: BLE001
                text, usage, turns = f"error: {e}", {}, None
            return self._json({"model": MODEL, "answer": text, "num_turns": turns, "probe": "canary2", "bridge": "claude_bridge.py"})
        if self.path.startswith("/canary"):
            try:
                # through the same path as a chat request: with a system prompt, which in
                # `claude -p` replaces the harness's own prompt (without one, the canary
                # describes Claude Code's default system prompt, which no arm ever sees)
                text, usage, turns = complete(MODEL, "You answer questions.", CANARY, 300)
            except Exception as e:  # noqa: BLE001
                text, usage, turns = f"error: {e}", {}, None
            return self._json({"model": MODEL, "answer": text, "input_tokens": usage.get("input_tokens"),
                               "num_turns": turns, "bridge": "claude_bridge.py"})
        self.send_response(404); self.end_headers()
    def do_POST(self):
        n = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(n) or b"{}")
        model = body.get("model") or MODEL
        if not model.startswith("claude"):
            model = MODEL
        system, prompt = flatten(body.get("messages", []))
        max_tokens = int(body.get("max_tokens") or 256)
        args = ["claude", "-p", prompt, "--model", model, "--output-format", "json", "--max-turns", "1",
                "--tools", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                # round 4: no user/project/local settings, so no ~/.claude/CLAUDE.md, no output
                # style, no language preference reaches the model under test (probe: "NONE")
                "--setting-sources", ""]
        if system:
            args += ["--system-prompt", system + f"\n\nAnswer in at most {max_tokens} tokens."]
        t0 = time.time()
        try:
            # a bare directory: no project settings, no CLAUDE.md, no plugin scope, no
            # .muninn store, so the model under test sees only the scaffold's prompt
            cwd = __import__("tempfile").gettempdir() + "/muninn-bridge-cwd"
            __import__("os").makedirs(cwd, exist_ok=True)
            out = subprocess.run(args, capture_output=True, text=True, timeout=300, cwd=cwd,
                                 env={**__import__("os").environ, "CLAUDECODE": ""})
            v = json.loads(out.stdout) if out.stdout.strip() else {}
            text = v.get("result", "") if not v.get("is_error") else ""
            usage = v.get("usage", {}) or {}
        except Exception as e:  # noqa: BLE001
            text, usage = "", {}
            print("bridge error:", e)
        resp = {
            "id": "chatcmpl-" + uuid.uuid4().hex[:12], "object": "chat.completion", "created": int(time.time()), "model": model,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": usage.get("input_tokens", 0), "completion_tokens": usage.get("output_tokens", 0), "total_tokens": 0},
        }
        print(f"{time.time()-t0:5.1f}s {len(prompt):6d} chars → {len(text):4d} chars")
        data = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=30002)
    ap.add_argument("--model", default=MODEL)
    a = ap.parse_args()
    MODEL = a.model
    print(f"bridge on http://127.0.0.1:{a.port}/v1 → claude -p ({MODEL})")
    # threaded (round 8): every arm of a round shares one bridge process, several runs at once
    ThreadingHTTPServer(("127.0.0.1", a.port), H).serve_forever()
