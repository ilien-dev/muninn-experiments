#!/usr/bin/env python3
"""Can a local model run Mem0's own extraction prompt on an engineering decision?

The Mem0 arm is pre-registered with a stated handicap: no Anthropic or OpenAI key on this
machine, so Mem0's extractor runs on a local model while claude-mem's runs on Claude. This
probe asks whether the handicap leaves anything to measure at all, and it costs no Claude call.

Mem0 extracts memories by asking its LLM, as a "Personal Information Organizer", to return
`{"facts": [...]}` for the conversation. The head-to-head's material is not personal facts —
it is decisions about databases, routers and secret stores. If a local model reads Mem0's
prompt and returns `{"facts": []}` for "For production secrets we use HashiCorp Vault", then
the arm stores nothing and its 0/27 would be a measurement of the model, not of Mem0.

For each model the probe prints what Mem0's *own* prompt and message formatting produce, and
— as a control — what the same model does with the same sentence under a plainer instruction.
A model that fails the first and passes the second has not failed at extraction; it has
declined Mem0's framing.

  python3 extractor_probe.py --models llama3.1:8b,qwen2.5:14b-instruct [--out probe.json]
"""
import argparse
import json
import pathlib
import sys

import httpx
from mem0.memory.utils import get_fact_retrieval_messages, parse_messages

# Four decisions of the kind the head-to-head seeds, one of them a replacement.
CASES = [
    "For production secrets we use HashiCorp Vault.",
    "We're going with gRPC for service-to-service communication.",
    "Moving to AWS Secrets Manager instead.",
    "The async runtime is tokio, not async-std.",
]
PLAIN = (
    "Extract any durable technical decisions from the message as JSON: "
    '{"facts": ["...", "..."]}. Return {"facts": []} if there are none.'
)


def ask(base, model, system, user):
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_predict": 2000, "top_p": 0.1},
    }
    r = httpx.post(f"{base}/api/chat", json=body, timeout=900)
    r.raise_for_status()
    return r.json()["message"]["content"]


def facts(raw):
    try:
        return json.loads(raw).get("facts", [])
    except Exception:
        return None          # unparseable is different from empty


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="llama3.1:8b")
    ap.add_argument("--base", default="http://127.0.0.1:39177")
    ap.add_argument("--out", type=pathlib.Path)
    a = ap.parse_args()

    report = []
    for model in a.models.split(","):
        row = {"model": model, "mem0_prompt": [], "plain_prompt": []}
        for case in CASES:
            sysp, userp = get_fact_retrieval_messages(parse_messages(
                [{"role": "user", "content": case}]))
            m = facts(ask(a.base, model, sysp, userp + "\n\nPlease respond with valid JSON only."))
            p = facts(ask(a.base, model, PLAIN, f"Message:\n{case}"))
            row["mem0_prompt"].append({"input": case, "facts": m})
            row["plain_prompt"].append({"input": case, "facts": p})
        row["mem0_extracted"] = sum(bool(c["facts"]) for c in row["mem0_prompt"])
        row["plain_extracted"] = sum(bool(c["facts"]) for c in row["plain_prompt"])
        report.append(row)
        print(f"{model:24} Mem0's prompt {row['mem0_extracted']}/{len(CASES)}   "
              f"plain prompt {row['plain_extracted']}/{len(CASES)}")
        for c in row["mem0_prompt"]:
            print(f"    {str(c['facts']):<60} ← {c['input']}")

    usable = [r["model"] for r in report if r["mem0_extracted"] == len(CASES)]
    print(f"\nmodels that extract every decision under Mem0's own prompt: "
          f"{', '.join(usable) if usable else 'none'}")
    if not usable:
        print("→ a Mem0 arm on these models would store nothing, and its score would measure\n"
              "  the model's reading of Mem0's prompt rather than Mem0.")
    if a.out:
        a.out.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
