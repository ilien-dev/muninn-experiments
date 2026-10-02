#!/usr/bin/env bash
# Mem0 0.1.118 arm for the head-to-head grid, on a local extractor
# (experiment/PREREGISTRATION.md, "Mem0 as a head-to-head arm, on a local model").
#
# Read the pre-registration before reading any number this arm produces. Two handicaps are
# declared there and neither can be removed on this machine:
#
#   1. Mem0 extracts with an LLM and retrieves with an embedding model. There is no Anthropic
#      or OpenAI key here, so both run on a pinned local Ollama, while claude-mem's observer
#      runs on Claude through the operator's login. That is a difference between models, not
#      between memory engines, and it runs in Muninn's favour.
#   2. Mem0 ships no Claude Code plugin, so `plugin/` here was written for the experiment —
#      by us, about our competitor. It is two documented calls and nothing else, committed so
#      it can be read.
#
# Consequence, and it is not negotiable by a good result: this arm may not be cited as
# "Muninn beats Mem0". A result where *Mem0 wins* is the informative one, because it would
# hold despite both handicaps.
#
# What is pinned: mem0ai, Ollama, the extractor model, the embedding model. What is per cell:
# the Chroma store under $CELL_ROOT/data, so no cell sees another's memories.
#
# Env: CELL_ROOT (private dir), CHECKOUT, PORT (unused: the Ollama server is shared and
# read-only to the cells), PIN.
set -euo pipefail

MEM0_VERSION=0.1.118
OLLAMA_VERSION=v0.34.2
LLM_MODEL=${MEM0_LLM_MODEL:-llama3.1:8b}
EMBED_MODEL=${MEM0_EMBED_MODEL:-nomic-embed-text}
OLLAMA_PORT=${MEM0_OLLAMA_PORT:-39177}
OLLAMA_BASE=http://127.0.0.1:$OLLAMA_PORT

REAL_HOME=${REAL_HOME:-$HOME}
PIN=${PIN:-$REAL_HOME/.local/share/muninn-bench/competitors/mem0}
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PY=$PIN/.venv/bin/python
OLLAMA=$PIN/ollama/bin/ollama

die() { echo "mem0 arm: $*" >&2; exit 1; }
need() { for v in "$@"; do [ -n "${!v:-}" ] || die "$v is not set"; done; }
data() { echo "$CELL_ROOT/data"; }
ollama_up() { curl -sf -m 3 "$OLLAMA_BASE/api/version" >/dev/null 2>&1; }

start_ollama() {
  ollama_up && return 0
  mkdir -p "$PIN/logs"
  OLLAMA_MODELS=$PIN/models OLLAMA_HOST=127.0.0.1:$OLLAMA_PORT \
    setsid nohup "$OLLAMA" serve >"$PIN/logs/serve.log" 2>&1 &
  for _ in $(seq 120); do ollama_up && return 0; sleep 0.5; done
  die "ollama did not come up on $OLLAMA_BASE: $(tail -5 "$PIN/logs/serve.log")"
}

case "${1:?subcommand}" in
  install)
    # The pin is built by hand once (uv venv + mem0ai, the Ollama tarball, two model pulls);
    # this verb verifies it rather than re-downloading 5 GB on every grid.
    [ -x "$PY" ] || die "no venv at $PY — uv venv $PIN/.venv && uv pip install mem0ai==$MEM0_VERSION chromadb ollama"
    [ -x "$OLLAMA" ] || die "no ollama at $OLLAMA — unpack ollama-linux-amd64.tar.zst ($OLLAMA_VERSION) into $PIN/ollama"
    start_ollama
    for m in "$LLM_MODEL" "$EMBED_MODEL"; do
      OLLAMA_MODELS=$PIN/models OLLAMA_HOST=127.0.0.1:$OLLAMA_PORT "$OLLAMA" show "$m" >/dev/null 2>&1 \
        || die "model $m is not pulled into $PIN/models"
    done
    "$PY" - <<PY
import json, mem0
print(json.dumps({"installed": "mem0ai==" + getattr(mem0, "__version__", "$MEM0_VERSION"),
                  "ollama": "$OLLAMA_VERSION", "llm": "$LLM_MODEL", "embedder": "$EMBED_MODEL"}))
PY
    ;;

  start)
    need CELL_ROOT
    mkdir -p "$(data)" "$CELL_ROOT/logs"
    start_ollama
    echo "{\"started\": true, \"ollama\": \"$OLLAMA_BASE\", \"llm\": \"$LLM_MODEL\"}" ;;

  claude-args)
    need CELL_ROOT
    "$PY" - "$HERE" "$(data)" "$PIN" "$OLLAMA_BASE" "$LLM_MODEL" "$EMBED_MODEL" "$CELL_ROOT" <<'PY'
import json, sys
here, data, pin, base, llm, emb, cell = sys.argv[1:8]
print(json.dumps({
    "args": ["--plugin-dir", f"{here}/plugin"],
    "allowed_tools": [],
    "env": {"MEM0_DATA": data, "MEM0_OLLAMA": base, "MEM0_LLM": llm,
            "MEM0_EMBEDDER": emb, "MEM0_USER": "dev",
            "MEM0_PYTHON": f"{pin}/.venv/bin/python",
            "MEM0_LOG": f"{cell}/logs/mem0.jsonl",
            # chroma and posthog otherwise write into the operator's real HOME
            "ANONYMIZED_TELEMETRY": "False", "CHROMA_TELEMETRY_IMPL": "none"},
}))
PY
    ;;

  settle)
    # `add` runs inside the Stop hook and the harness waits for it, so there is no queue to
    # drain. What is reported is what the store holds and what the shim logged.
    need CELL_ROOT
    "$PY" - "$(data)" "$CELL_ROOT/logs/mem0.jsonl" <<'PY'
import json, os, sys
data, logp = sys.argv[1], sys.argv[2]
adds = errors = hits = 0
try:
    for line in open(logp):
        row = json.loads(line)
        adds += row.get("results", 0) if row["event"] == "stop.add" else 0
        errors += row["event"].endswith(".error")
        hits += row.get("hits", 0) if row["event"] == "prompt.search" else 0
except OSError:
    pass
size = sum(os.path.getsize(os.path.join(dp, f))
           for dp, _d, fs in os.walk(data) for f in fs)
print(json.dumps({"memories_added": adds, "errors": errors, "search_hits": hits, "bytes": size}))
PY
    ;;

  snapshot) need CELL_ROOT; mkdir -p "$2"; cp -a "$(data)/." "$2/" 2>/dev/null || true; echo '{"snapshot": true}' ;;
  restore)  need CELL_ROOT; mkdir -p "$(data)"; cp -a "$2/." "$(data)/" 2>/dev/null || true; echo '{"restored": true}' ;;
  # the Ollama server is shared and stateless across cells; nothing per-cell is running
  stop) echo '{"stopped": true}' ;;

  delivered)
    need CELL_ROOT
    "$PY" - "$CELL_ROOT/logs/mem0.jsonl" <<'PY'
import json, sys
deliveries = tokens = 0
try:
    for line in open(sys.argv[1]):
        row = json.loads(line)
        if row["event"] == "prompt.search" and row.get("hits"):
            deliveries += 1
            tokens += row["hits"]          # memories, not tokens: the shim prints one line each
except OSError:
    pass
print(json.dumps({"deliveries": deliveries, "tokens": None, "memories_delivered": tokens,
                  "note": "the shim prints one line per memory; token counts are not comparable across arms"}))
PY
    ;;

  *) echo "usage: $0 install|start|claude-args|settle|snapshot <dir>|restore <dir>|stop|delivered" >&2; exit 2 ;;
esac
