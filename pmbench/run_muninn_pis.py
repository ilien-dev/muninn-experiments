#!/usr/bin/env python3
"""
PM-Bench scaffold, rounds 4-7: Muninn as the prospective intention store.

The model does not own a ledger. Intentions are typed records in a Muninn store; lifecycle
(add / reschedule / override / cancel / done, daily re-arm, day-scoped carry, same-day expiry)
is code. Per step:

  1. Form/Revise  — one model call reads the new text (day plan, vignette) and emits typed ops.
  2. Observe      — code issues check_time (while a time intention is pending) and, while any
                    intention watches a channel, one query_state per channel. Time and channel
                    state reach the store only through these replies.
  3. Filter       — `muninn cues --ungated` with the fake clock set from the queried time and
                    keyword cues for the channels that answered; the fired records are the board.
  4. Decide       — one model call maps the board to menu handles; code validates, marks done,
                    and adds a clock-matched time intention the model omitted (guard, logged).

The scaffold reads only what the model could see: start_instructions, step text and options,
the step action menu, and the replies to the queries it issues. `step["time"]`, `step["cues"]`,
`step["state_events"]`, `groundtruth` and task definitions are never read (see `StepView`).

Actions are logged in the standard JSONL format so `pm_bench.py score` can score them.
Design after the Prospective Intention Store (arXiv:2609.01272): Form → Revise → Filter → Decide.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import hashlib
import urllib.request
import platform
import sys
import tempfile
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

# the PMBench checkout: the symlink location (sim/..), not the resolved repository path
PROJECT_ROOT = Path(os.environ.get("PMBENCH_ROOT") or Path(os.path.abspath(__file__)).parents[1])
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _load_pm_bench_module():
    pm_bench_path = PROJECT_ROOT / "sim" / "pm_bench.py"
    spec = importlib.util.spec_from_file_location("pm_bench", pm_bench_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load pm_bench module from {pm_bench_path}")
    pm_bench = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pm_bench)
    return pm_bench


PM_BENCH = _load_pm_bench_module()

MUNINN_BIN = os.environ.get("MUNINN_BIN", "muninn")
FAKE_EPOCH = 1_800_000_000_000
DAY_MS = 86_400_000
GUARD_OVERLAP = 0.5

# ---------------------------------------------------------------------------------
# What the scaffold is allowed to see
# ---------------------------------------------------------------------------------


@dataclass
class StepView:
    """The visible part of a step. Hidden fields (time, cues, state_events, groundtruth,
    updates) are deliberately not copied."""

    step_id: str
    text: str
    options: list[str]
    menu_text: str
    allowed_handles: list[str]
    menu_entries: list[dict[str, str]]  # handle, action_text


# ---------------------------------------------------------------------------------
# Model calls (claude -p, isolated exactly as the round-4 bridge)
# ---------------------------------------------------------------------------------


class Claude:
    """Round 4-7: `claude -p` called directly with the bridge's flags. Round 8: when
    `base_url` is set, every call goes through the same OpenAI-compatible bridge process the
    PM-Bench baselines use (claude_bridge.py or codex_bridge.py), so no arm has an
    invocation path of its own."""

    def __init__(self, model: str, prompt_log, max_tokens: int = 700, base_url: str | None = None):
        self.model = model
        self.prompt_log = prompt_log
        self.max_tokens = max_tokens
        self.base_url = base_url.rstrip("/") if base_url else None
        self.cwd = os.path.join(tempfile.gettempdir(), "muninn-bridge-cwd")
        os.makedirs(self.cwd, exist_ok=True)
        self.calls = 0
        self.est_input_tokens = 0

    def _via_bridge(self, messages: list[dict[str, str]]) -> str:
        body = json.dumps({"model": self.model, "messages": messages, "max_tokens": self.max_tokens,
                           "temperature": 0}).encode()
        req = urllib.request.Request(self.base_url + "/chat/completions", data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=320) as r:
            v = json.loads(r.read().decode())
        return (v.get("choices") or [{}])[0].get("message", {}).get("content", "") or ""

    def call_json(self, system: str, user: str, tag: str) -> dict[str, Any] | None:
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        est = PM_BENCH.estimate_input_tokens(messages)
        self.est_input_tokens += est
        self.calls += 1
        if self.base_url:
            text = ""
            for attempt in range(3):
                try:
                    text = self._via_bridge(messages)
                except Exception as exc:  # noqa: BLE001
                    print(f"bridge call error ({tag}): {exc}")
                    text = ""
                if text.strip():
                    break
                time.sleep(1.5 * (attempt + 1))
            if self.prompt_log:
                self.prompt_log.write(f"=== {tag} ===\n")
                self.prompt_log.write(json.dumps(messages, indent=2, ensure_ascii=False))
                self.prompt_log.write(f"\nRESPONSE: {text}\nEST_INPUT_TOKENS: {est}\n\n")
                self.prompt_log.flush()
            return parse_json_object(text)
        args = [
            "claude", "-p", user, "--model", self.model, "--output-format", "json", "--max-turns", "1",
            "--tools", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            "--setting-sources", "",
            "--system-prompt", system + f"\n\nAnswer in at most {self.max_tokens} tokens.",
        ]
        text = ""
        for attempt in range(3):
            try:
                out = subprocess.run(
                    args, capture_output=True, text=True, timeout=300, cwd=self.cwd,
                    env={**os.environ, "CLAUDECODE": ""},
                )
                v = json.loads(out.stdout) if out.stdout.strip() else {}
                text = v.get("result", "") if not v.get("is_error") else ""
            except Exception as exc:  # noqa: BLE001
                print(f"claude call error ({tag}): {exc}")
                text = ""
            if text.strip():
                break
            time.sleep(1.5 * (attempt + 1))
        if self.prompt_log:
            self.prompt_log.write(f"=== {tag} ===\n")
            self.prompt_log.write(json.dumps(messages, indent=2, ensure_ascii=False))
            self.prompt_log.write(f"\nRESPONSE: {text}\nEST_INPUT_TOKENS: {est}\n\n")
            self.prompt_log.flush()
        return parse_json_object(text)


def parse_json_object(text: str) -> dict[str, Any] | None:
    if not text:
        return None
    try:
        v = json.loads(text)
        return v if isinstance(v, dict) else None
    except Exception:  # noqa: BLE001
        pass
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not m:
        return None
    try:
        v = json.loads(m.group(0))
        return v if isinstance(v, dict) else None
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------------------------
# The typed store, persisted in Muninn
# ---------------------------------------------------------------------------------


@dataclass
class Intention:
    iid: str
    text: str                     # the action, imperative ("Send the library email")
    trigger: dict[str, Any]       # {"kind":"time","at":"HH:MM"} | {"kind":"event","cue":str}
                                  # | {"kind":"channel","channel":str,"condition":str}
    day: str | None               # day name this intention applies to; None = the day it was formed
    daily: bool = False           # regular: re-armed every day
    status: str = "pending"       # pending | done | canceled | expired
    created_day: str = ""
    created_step: str = ""
    done_days: list[str] = field(default_factory=list)
    record_id: int | None = None  # current Muninn record (today's copy for daily ones)
    history: list[str] = field(default_factory=list)
    revised_step: str = ""        # the step whose text revised the trigger: not eligible at that step

    def trigger_text(self) -> str:
        t = self.trigger
        k = t.get("kind")
        if k == "time":
            return f"at {t.get('at')}"
        if k == "event":
            return f"when: {t.get('cue')}"
        if k == "channel":
            return f"when channel [{t.get('channel')}] shows: {t.get('condition')}"
        return json.dumps(t)


def fake_ms(day_index: int, minutes: int) -> int:
    return FAKE_EPOCH + day_index * DAY_MS + minutes * 60_000


def channel_key(channel: str) -> str:
    return "ch" + re.sub(r"[^a-z0-9]", "", channel.lower())


class MuninnStore:
    def __init__(self, out_dir: str, day_names: list[str]):
        self.root = tempfile.mkdtemp(prefix="pmbench-muninn-", dir=out_dir)
        os.makedirs(os.path.join(self.root, ".git"), exist_ok=True)
        self._run([MUNINN_BIN, "--cwd", self.root, "init", "--keep-native", "--no-boot-block"])
        self.day_names = day_names
        self.intentions: dict[str, Intention] = {}
        self.by_record: dict[int, str] = {}
        self.next_id = 1
        self.events: list[dict[str, Any]] = []

    # -- plumbing -----------------------------------------------------------------
    def _env(self, now_ms: int | None = None) -> dict[str, str]:
        env = dict(os.environ)
        env["MUNINN_ROOT"] = self.root
        env["MUNINN_NO_PROJECT"] = "1"
        if now_ms is not None:
            env["MUNINN_FAKE_NOW_MS"] = str(now_ms)
        return env

    def _run(self, args: list[str], now_ms: int | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(args, env=self._env(now_ms), capture_output=True, text=True)

    def day_index(self, day: str) -> int:
        return self.day_names.index(day)

    def _cues_for(self, it: Intention, day: str) -> list[dict[str, Any]]:
        d = self.day_index(day)
        t = it.trigger
        if t.get("kind") == "time":
            hh, mm = t["at"].split(":")
            return [{"kind": "after", "key": str(fake_ms(d, int(hh) * 60 + int(mm))), "grp": 0}]
        if t.get("kind") == "channel":
            return [
                {"kind": "after", "key": str(fake_ms(d, 0)), "grp": 0},
                {"kind": "keyword", "key": channel_key(t["channel"]), "grp": 0},
            ]
        return [{"kind": "after", "key": str(fake_ms(d, 0)), "grp": 0}]

    def _import(self, it: Intention, day: str, created_ms: int) -> None:
        row = {
            "kind": "decision",
            "subject": f"intention.{it.iid}",
            "relation": "must",
            "object": f"{it.iid} {it.trigger_text()}",
            "body": json.dumps({"iid": it.iid, "text": it.text, "trigger": it.trigger, "day": day, "daily": it.daily}) + "\n",
            "origin": "user_said",
            "session_id": "pmbench",
            "created_at": created_ms,
            "cues": self._cues_for(it, day),
        }
        p = os.path.join(self.root, "import.jsonl")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        self._run([MUNINN_BIN, "--cwd", self.root, "import", p])
        # map the new record id
        xp = os.path.join(self.root, "export.jsonl")
        self._run([MUNINN_BIN, "--cwd", self.root, "--json", "export", "--out", xp])
        newest = None
        try:
            for line in open(xp, encoding="utf-8"):
                rec = json.loads(line)
                if rec.get("subject") == f"intention.{it.iid}" and not rec.get("invalid"):
                    if newest is None or rec["id"] > newest:
                        newest = rec["id"]
        except OSError:
            pass
        it.record_id = newest
        if newest is not None:
            self.by_record[newest] = it.iid

    def _revoke(self, it: Intention, reason: str) -> None:
        if it.record_id is not None:
            self._run([MUNINN_BIN, "--cwd", self.root, "revoke", str(it.record_id), "--reason", reason])
            self.by_record.pop(it.record_id, None)
            it.record_id = None

    # -- lifecycle (code) -----------------------------------------------------------
    def add(self, text: str, trigger: dict[str, Any], day: str, daily: bool, created_day: str, step_id: str, now_ms: int) -> Intention:
        iid = f"i{self.next_id}"
        self.next_id += 1
        it = Intention(iid=iid, text=text, trigger=trigger, day=None if daily else day, daily=daily,
                       created_day=created_day, created_step=step_id)
        it.history.append(f"add@{step_id}")
        self.intentions[iid] = it
        self._import(it, created_day if daily else day, now_ms)
        return it

    def reschedule(self, iid: str, at: str, day: str, step_id: str, now_ms: int) -> bool:
        it = self.intentions.get(iid)
        if not it or it.status != "pending":
            return False
        self._revoke(it, "reschedule")
        it.trigger = {"kind": "time", "at": at}
        it.history.append(f"reschedule->{at}@{step_id}")
        it.revised_step = step_id
        self._import(it, day if it.daily or it.day is None else it.day, now_ms)
        return True

    def override(self, iid: str, trigger: dict[str, Any], day: str, step_id: str, now_ms: int) -> bool:
        it = self.intentions.get(iid)
        if not it or it.status != "pending":
            return False
        self._revoke(it, "override")
        it.trigger = trigger
        it.history.append(f"override->{it.trigger_text()}@{step_id}")
        it.revised_step = step_id
        self._import(it, day if it.daily or it.day is None else it.day, now_ms)
        return True

    def cancel(self, iid: str, step_id: str) -> bool:
        it = self.intentions.get(iid)
        if not it or it.status != "pending":
            return False
        it.status = "canceled"
        it.history.append(f"cancel@{step_id}")
        self._revoke(it, "canceled")
        return True

    def mark_done(self, iid: str, day: str, step_id: str) -> None:
        it = self.intentions.get(iid)
        if not it:
            return
        it.history.append(f"done@{step_id}")
        it.done_days.append(day)
        self._revoke(it, "done")
        if not it.daily:
            it.status = "done"

    def start_day(self, day: str, now_ms: int) -> None:
        """Re-arm daily intentions for this day; nothing else changes."""
        for it in self.intentions.values():
            if it.daily and it.status == "pending" and it.record_id is None:
                self._import(it, day, now_ms)

    def end_day(self, day: str) -> None:
        """Same-day intentions not done by the end of their day expire; daily ones not done
        today are retired for today and re-armed tomorrow; cross-day ones stay."""
        for it in self.intentions.values():
            if it.status != "pending":
                continue
            if it.daily:
                self._revoke(it, "day_end")
                continue
            if it.day == day or it.day is None:
                it.status = "expired"
                it.history.append(f"expire@{day}")
                self._revoke(it, "expired")

    # -- views ----------------------------------------------------------------------
    def pending(self) -> list[Intention]:
        return [it for it in self.intentions.values() if it.status == "pending"]

    def pending_today(self, day: str) -> list[Intention]:
        return [it for it in self.pending() if (it.daily and day not in it.done_days) or (not it.daily and it.day == day)]

    def watched_channels(self, day: str) -> list[str]:
        chans = []
        for it in self.pending_today(day):
            if it.trigger.get("kind") == "channel":
                c = it.trigger.get("channel")
                if c and c not in chans:
                    chans.append(c)
        return chans

    def has_time_intentions(self, day: str) -> bool:
        return any(it.trigger.get("kind") == "time" for it in self.pending_today(day))

    def board(self, day: str, clock_minutes: int | None, answered_channels: list[str]) -> list[Intention]:
        """Filter: ask the store what fires now. after-cues use the fake clock built from the
        queried time; keyword cues are the channels that answered this step."""
        d = self.day_index(day)
        now_ms = fake_ms(d, clock_minutes if clock_minutes is not None else 0)
        args = [MUNINN_BIN, "--cwd", self.root, "--json", "cues", "--session", f"day{d}", "--event", "step", "--ungated"]
        for c in answered_channels:
            args += ["--keyword", channel_key(c)]
        out = self._run(args, now_ms)
        fired: list[int] = []
        try:
            v = json.loads(out.stdout)
            fired = list(v.get("ids", [])) + list(v.get("gated", []))
        except Exception:  # noqa: BLE001
            fired = []
        board = []
        for rid in fired:
            iid = self.by_record.get(rid)
            it = self.intentions.get(iid) if iid else None
            if it and it.status == "pending" and day not in it.done_days:
                board.append(it)
        return board


class PlainStore(MuninnStore):
    """Round 8 ablation: the identical scaffold with the Muninn binary removed. Records live
    in a Python dict; the three store operations are re-implemented with the semantics the
    engine documents (`muninn-core/src/cue.rs::evaluate`): a record fires when every cue of
    its group matches — `after` when the fake clock has passed its key, `keyword` when the
    key is among this step's answered channels; hits ordered by record id. Nothing else in
    the scaffold changes, so muninn_store − plain_store measures the store implementation and
    nothing else."""

    def __init__(self, out_dir: str, day_names: list[str]):
        self.root = tempfile.mkdtemp(prefix="pmbench-plain-", dir=out_dir)
        self.day_names = day_names
        self.intentions: dict[str, Intention] = {}
        self.by_record: dict[int, str] = {}
        self.next_id = 1
        self.events: list[dict[str, Any]] = []
        self._records: dict[int, list[dict[str, Any]]] = {}   # active record id -> cues
        self._next_record = 1
        self._log = open(os.path.join(self.root, "plain-store.jsonl"), "w", encoding="utf-8", buffering=1)

    def _run(self, args: list[str], now_ms: int | None = None):  # never called
        raise RuntimeError("PlainStore does not run the muninn binary")

    def _import(self, it: Intention, day: str, created_ms: int) -> None:
        rid = self._next_record
        self._next_record += 1
        self._records[rid] = self._cues_for(it, day)
        it.record_id = rid
        self.by_record[rid] = it.iid
        self._log.write(json.dumps({"op": "import", "id": rid, "iid": it.iid, "cues": self._records[rid]}) + "\n")

    def _revoke(self, it: Intention, reason: str) -> None:
        if it.record_id is not None:
            self._records.pop(it.record_id, None)
            self.by_record.pop(it.record_id, None)
            self._log.write(json.dumps({"op": "revoke", "id": it.record_id, "reason": reason}) + "\n")
            it.record_id = None

    def board(self, day: str, clock_minutes: int | None, answered_channels: list[str]) -> list[Intention]:
        d = self.day_index(day)
        now_ms = fake_ms(d, clock_minutes if clock_minutes is not None else 0)
        keys = {channel_key(c) for c in answered_channels}
        fired: list[int] = []
        for rid in sorted(self._records):
            cues = self._records[rid]
            ok = all(
                (c["kind"] == "after" and now_ms >= int(c["key"])) or
                (c["kind"] == "keyword" and c["key"] in keys)
                for c in cues
            )
            if ok:
                fired.append(rid)
        board = []
        for rid in fired:
            iid = self.by_record.get(rid)
            it = self.intentions.get(iid) if iid else None
            if it and it.status == "pending" and day not in it.done_days:
                board.append(it)
        return board


class ShadowMuninnStore(MuninnStore):
    """Round 9: a Muninn store that also keeps, for every active Muninn record, the cues the
    dict store would hold, and at every board computes both answers from the same record ids.
    Decisions use the Muninn board; `last_shadow` records whether the dict rule would have
    fired a different set. A disagreement is a semantic difference between `muninn cues` and
    the documented rule, with no model call involved."""

    def __init__(self, out_dir: str, day_names: list[str]):
        super().__init__(out_dir, day_names)
        self._shadow: dict[int, list[dict[str, Any]]] = {}
        self.last_shadow: dict[str, Any] = {}
        self.disagreements = 0
        self.boards_compared = 0

    def _import(self, it: Intention, day: str, created_ms: int) -> None:
        super()._import(it, day, created_ms)
        if it.record_id is not None:
            self._shadow[it.record_id] = self._cues_for(it, day)

    def _revoke(self, it: Intention, reason: str) -> None:
        if it.record_id is not None:
            self._shadow.pop(it.record_id, None)
        super()._revoke(it, reason)

    def board(self, day: str, clock_minutes: int | None, answered_channels: list[str]) -> list[Intention]:
        got = super().board(day, clock_minutes, answered_channels)
        d = self.day_index(day)
        now_ms = fake_ms(d, clock_minutes if clock_minutes is not None else 0)
        keys = {channel_key(c) for c in answered_channels}
        fired = [rid for rid in sorted(self._shadow) if all(
            (c["kind"] == "after" and now_ms >= int(c["key"])) or (c["kind"] == "keyword" and c["key"] in keys)
            for c in self._shadow[rid])]
        shadow = []
        for rid in fired:
            iid = self.by_record.get(rid)
            it = self.intentions.get(iid) if iid else None
            if it and it.status == "pending" and day not in it.done_days:
                shadow.append(it.iid)
        a, b = sorted(i.iid for i in got), sorted(shadow)
        self.boards_compared += 1
        if a != b:
            self.disagreements += 1
        self.last_shadow = {"muninn": a, "dict": b, "agree": a == b}
        return got


def sha256_file(path: str) -> str:
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()
    except OSError:
        return ""


def write_manifest(path: str, *, model: str, store: str, base_url: str | None, scenario_path: str, out_log: str) -> None:
    """Round 8: everything a reader needs to check that the run used what the
    pre-registration froze."""
    muninn_bin = subprocess.run(["bash", "-lc", f"command -v {MUNINN_BIN}"], capture_output=True, text=True).stdout.strip()
    ver = subprocess.run([MUNINN_BIN, "--version"], capture_output=True, text=True).stdout.strip() if store == "muninn" else ""
    canary = None
    if base_url:
        try:
            with urllib.request.urlopen(base_url.rstrip("/").removesuffix("/v1") + "/canary", timeout=320) as r:
                canary = json.loads(r.read().decode())
        except Exception as exc:  # noqa: BLE001
            canary = {"error": str(exc)}
    sim = PROJECT_ROOT / "sim"
    m = {
        "model": model, "store": store, "base_url": base_url, "host": platform.node(), "python": platform.python_version(),
        "scaffold_sha256": sha256_file(__file__), "scenario": scenario_path, "scenario_sha256": sha256_file(scenario_path),
        "pm_bench_py_sha256": sha256_file(str(sim / "pm_bench.py")), "pmbench_commit": subprocess.run(["git", "-C", str(PROJECT_ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "muninn_bin": muninn_bin, "muninn_bin_sha256": sha256_file(muninn_bin) if muninn_bin else "", "muninn_version": ver,
        # muninn-nonet wraps the real binary in a network namespace; record the binary itself too
        "muninn_real_bin": os.environ.get("MUNINN_REAL_BIN"), "muninn_real_bin_sha256": sha256_file(os.environ.get("MUNINN_REAL_BIN", "")),
        "muninn_commit": subprocess.run(["git", "-C", str(Path(__file__).resolve().parents[3]), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "bridge_canary": canary, "log": out_log,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1)


# ---------------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------------

FORM_SYSTEM = """You maintain a typed store of deferred intentions (prospective memory) for someone living
through a simulated week. You will be shown the intentions already in the store and a piece of new
text (a day plan or a short vignette). Your only job is to translate what the text says about
deferred commitments into typed operations. You do not decide what to do now.

Return exactly one raw JSON object: {"ops": [ ... ]}. Each op is one of:
- {"op":"add","text":"<imperative action, no time/cue in it>","trigger":<TRIGGER>,"day":<DAY>,"daily":<bool>}
- {"op":"reschedule","id":"<existing id>","at":"HH:MM"}
- {"op":"override","id":"<existing id>","trigger":<TRIGGER>}
- {"op":"cancel","id":"<existing id>"}

TRIGGER is one of:
- {"kind":"time","at":"HH:MM"}                      — an exact clock time
- {"kind":"event","cue":"<what will be noticed in the scene>"}   — something seen or happening around the person
- {"kind":"channel","channel":"<one of CHANNELS>","condition":"<what the channel must show>"}
  — cues that are only visible by checking a hidden state channel: email, calendar, portals,
  price tracker, bank balance, shipment/laundry status, library hold, reservation waitlist,
  appointment portal. If the text says the cue arrives through one of these, use kind channel.

DAY is a day name ("Monday".."Sunday") when the text says the intention is for another day
("On Thursday, ..."); otherwise null (it applies to the current day). "daily": true only for
things to do every day (regular medication); otherwise false.

Rules:
- A vignette that describes something happening (an order on the rack, a text arriving, a
  counter opening) is a scene, not an instruction: emit nothing for it. An update is announced
  as such ("instead of", "moves to", "changes", "no longer", "does not need to happen").
- The "cue" is the observable event in a few plain words ("a follow-up text comes in", "the
  kiosk blinks"), never its purpose or content ("...with corrected instructions").
- Add only commitments that are NEW. A sentence that merely recalls an existing intention
  ("you still have to send the email today", "you have a feeling the portal may open a slot")
  is not new: emit nothing for it.
- An update always refers to an existing id: a new time -> reschedule; a new cue to wait for
  instead of the old one -> override; "no longer needs to happen", "does not need to happen
  after all", "you do not need to worry about X" -> cancel.
- "text" is the action itself, imperative, without the time or cue ("Send the library email").
- If the text carries no commitment and no update, return {"ops": []}.
- No explanations, no markdown, no code fences."""

DECIDE_SYSTEM = """You are taking a prospective memory evaluation. Each step shows a short vignette with three
ongoing-task options (A/B/C); pick one to advance. A step action menu lists action handles
(task_N: <action text>); performing an action means returning its handle.

An external store tracks the person's deferred intentions. You are given the ELIGIBLE BOARD:
the intentions whose scope allows them now, each with its id, its action, its trigger and,
where known, the evidence (this step's clock reading and state channel replies). Decide which
board intentions are due AT THIS STEP and map each one to the menu handle whose action text
means the same thing.

Rules:
- Act only on board intentions whose trigger is satisfied by this step's evidence: the vignette
  describes the cue, or a channel reply this step shows the condition, or the item is marked
  DUE NOW BY CLOCK. An item marked DUE NOW BY CLOCK is due: include its handle.
- Do not act early ("it will probably happen soon" is not due) and do not act on an intention
  whose cue was merely mentioned or anticipated.
- The cue must be explicitly present. An activity merely associated with it (rinsing a dish
  is not dinner; thinking about a balance is not a balance alert) is not the cue.
- Board intentions that share the same cue are due together.
- Never return a handle that is not on the menu, and never return a menu item that matches no
  due board intention (the menu contains distractors).
- Each handle at most once.

Return exactly one raw JSON object:
{"choice":"A"|"B"|"C","due":[{"id":"<board id>","handle":"task_N"}, ...]}
No explanations, no markdown, no code fences."""


def format_pending(intentions: list[Intention]) -> str:
    if not intentions:
        return "(store is empty)"
    lines = []
    for it in intentions:
        scope = "every day" if it.daily else (it.day or "today")
        lines.append(f"- {it.iid}: {it.text} — {it.trigger_text()} [{scope}]")
    return "\n".join(lines)


def form_user(day: str, pending: list[Intention], channels: list[str], new_text: str) -> str:
    return (
        f"Current day: {day}\n"
        f"CHANNELS: {', '.join(channels)}\n\n"
        f"Intentions already in the store:\n{format_pending(pending)}\n\n"
        f"NEW TEXT:\n{new_text}"
    )


def decide_user(day: str, clock_text: str | None, view: StepView, replies: dict[str, str],
                board: list[Intention], clock_due: set[str]) -> str:
    parts = [f"Day: {day}"]
    parts.append(f"Clock: {clock_text}" if clock_text else "Clock: unknown")
    parts.append("\nVignette:\n" + view.text + "\n" + "\n".join(view.options))
    if replies:
        parts.append("\nState channel replies this step (channels not listed answered: no updates):")
        for c, r in replies.items():
            parts.append(f"- {r}")
    parts.append("\nELIGIBLE BOARD:")
    if not board:
        parts.append("(nothing eligible now)")
    for it in board:
        flag = "  <-- DUE NOW BY CLOCK" if it.iid in clock_due else ""
        if it.trigger.get("kind") == "channel":
            flag += "  (satisfied only by a state channel reply, never by the vignette)"
        parts.append(f"- {it.iid}: {it.text} — {it.trigger_text()}{flag}")
    parts.append("\n" + view.menu_text.strip())
    return "\n".join(parts)


# ---------------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------------

TIME_RE = re.compile(r"^\d{1,2}:\d{2}$")
_STOP = {"the", "a", "an", "to", "of", "and", "your", "you", "up", "in", "on", "at", "for", "when", "it", "is"}


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in _STOP}


def overlap(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def parse_clock(reply: str) -> int | None:
    m = re.search(r"Time\s+(\d{1,2}):(\d{2})", reply or "")
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def normalize_trigger(t: Any, channels: list[str]) -> dict[str, Any] | None:
    if not isinstance(t, dict):
        return None
    k = str(t.get("kind", "")).lower()
    if k == "time":
        at = str(t.get("at", "")).strip()
        if not TIME_RE.match(at):
            return None
        hh, mm = at.split(":")
        return {"kind": "time", "at": f"{int(hh):02d}:{int(mm):02d}"}
    if k == "event":
        cue = " ".join(str(t.get("cue", "")).split())
        return {"kind": "event", "cue": cue} if cue else None
    if k == "channel":
        ch = str(t.get("channel", "")).strip()
        if ch not in channels:
            # tolerate near names
            cands = [c for c in channels if ch and (ch in c or c in ch)]
            if len(cands) != 1:
                return None
            ch = cands[0]
        cond = " ".join(str(t.get("condition", "")).split())
        return {"kind": "channel", "channel": ch, "condition": cond or "an update"}
    return None


def apply_ops(store: MuninnStore, payload: dict[str, Any] | None, day: str, step_id: str, channels: list[str],
              day_names: list[str], now_ms: int) -> list[dict[str, Any]]:
    applied: list[dict[str, Any]] = []
    ops = payload.get("ops") if isinstance(payload, dict) else None
    if not isinstance(ops, list):
        return applied
    for op in ops[:12]:
        if not isinstance(op, dict):
            continue
        kind = str(op.get("op", "")).lower()
        if kind == "add":
            text = " ".join(str(op.get("text", "")).split()).rstrip(".")
            trig = normalize_trigger(op.get("trigger"), channels)
            if not text or not trig:
                continue
            d = op.get("day")
            d = d if isinstance(d, str) and d in day_names else day
            daily = bool(op.get("daily", False))
            # duplicate guard: same action text and same trigger already pending
            dup = next((it for it in store.pending() if overlap(it.text, text) >= 0.99 and it.trigger == trig), None)
            if dup:
                applied.append({"op": "add", "skipped": "duplicate", "of": dup.iid})
                continue
            it = store.add(text, trig, d, daily, day, step_id, now_ms)
            applied.append({"op": "add", "id": it.iid, "text": text, "trigger": trig, "day": it.day, "daily": daily})
        elif kind == "reschedule":
            at = str(op.get("at", "")).strip()
            if TIME_RE.match(at):
                hh, mm = at.split(":")
                at = f"{int(hh):02d}:{int(mm):02d}"
                if store.reschedule(str(op.get("id")), at, day, step_id, now_ms):
                    applied.append({"op": "reschedule", "id": op.get("id"), "at": at})
        elif kind == "override":
            trig = normalize_trigger(op.get("trigger"), channels)
            if trig and store.override(str(op.get("id")), trig, day, step_id, now_ms):
                applied.append({"op": "override", "id": op.get("id"), "trigger": trig})
        elif kind == "cancel":
            if store.cancel(str(op.get("id")), step_id):
                applied.append({"op": "cancel", "id": op.get("id")})
    return applied


# ---------------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------------


def run(scenario: dict[str, Any], model: str, out_dir: str, log_path: str | None, max_days: int | None = None,
        store_kind: str = "muninn", base_url: str | None = None, scenario_path: str = "") -> str:
    started = PM_BENCH.now_utc_iso()
    t0 = time.perf_counter()
    os.makedirs(out_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{os.getpid()}"
    run_prefix = f"{store_kind}-store-{timestamp}-{PM_BENCH.sanitize_model_label(model)}"
    resolved_log = PM_BENCH.resolve_output_path(log_path, out_dir=out_dir, default_filename=f"{run_prefix}/{run_prefix}.jsonl", required_suffix=".jsonl")
    prompt_log = open(str(Path(resolved_log).with_suffix(".prompt.txt")), "w", encoding="utf-8", buffering=1)
    trace_log = open(str(Path(resolved_log).with_suffix(".trace.jsonl")), "w", encoding="utf-8", buffering=1)

    state_visibility = PM_BENCH.normalize_state_visibility(scenario)
    state_channels = PM_BENCH.normalize_state_channels(scenario)
    allowed_channels = PM_BENCH.list_state_channels(scenario)
    channels_no_clock = [c for c in allowed_channels if c != "clock"]
    day_names = [d["name"] for d in scenario["days"]]

    claude = Claude(model, prompt_log, base_url=base_url)
    store = (PlainStore(out_dir, day_names) if store_kind == "plain"
             else ShadowMuninnStore(out_dir, day_names) if store_kind == "muninn-shadow"
             else MuninnStore(out_dir, day_names))
    write_manifest(str(Path(resolved_log).with_suffix(".manifest.json")), model=model, store=store_kind, base_url=base_url,
                   scenario_path=scenario_path, out_log=str(resolved_log))
    entries: list[dict[str, Any]] = []
    guard_events = 0
    due_items_acted = 0
    updates_by_day = PM_BENCH.build_updates_by_day(scenario)

    # the once-per-week header, as every scaffold gets it
    daily_header = "\n".join(PM_BENCH.DAILY_TASK_HEADER_LINES)

    try:
        for day_index, day in enumerate(scenario["days"]):
            if max_days is not None and day_index >= max_days:
                break
            day_name = day["name"]
            tasks = day["tasks"]
            lure_catalog = PM_BENCH.normalize_lure_catalog(day.get("lures", []))
            # runtime state, only to build menus exactly as the benchmark does (hidden from the model logic)
            day_task_states = {t["id"]: PM_BENCH.init_task_state(t) for t in tasks}
            active_task_ids: set[str] = set()
            for t in tasks:
                enc_type, _ = PM_BENCH.normalize_encoding(t["encoding"])
                if enc_type == "start":
                    active_task_ids.add(t["id"])
                    day_task_states[t["id"]]["active"] = True
            day_updates = updates_by_day.get(day_name, {"pre": [], "by_step": {}})
            for update in day_updates.get("pre", []):
                tid = update.get("task_id")
                if tid in day_task_states:
                    PM_BENCH.apply_task_update(day_task_states[tid], update, task_states=day_task_states)
            id_to_handle, _ = PM_BENCH.build_day_handle_maps(day_task_states, lure_catalog, seed_key=f"{day_name}:handles")
            day_start_minutes = PM_BENCH.build_day_start_minutes(day)  # used only to answer clock queries, as the benchmark does
            last_query_step_by_channel: dict[str, int] = {}
            last_snapshot_item_by_channel: dict[str, dict[str, Any]] = {}
            last_reply_today: dict[str, str] = {}

            day_start_ms = fake_ms(day_index, 0)
            store.start_day(day_name, day_start_ms)

            # Form on the day plan (and the weekly header on the first day)
            header_text = "\n".join([f"=== {day_name} ==="] + day.get("start_instructions", []))
            plan_text = (daily_header + "\n\n" + header_text) if day_index == 0 else header_text
            print(f"\n{plan_text}")
            payload = claude.call_json(FORM_SYSTEM, form_user(day_name, store.pending(), channels_no_clock, plan_text), f"{day_name} plan FORM")
            ops = apply_ops(store, payload, day_name, f"{day_name}:plan", channels_no_clock, day_names, day_start_ms)
            trace_log.write(json.dumps({"day": day_name, "step_id": "plan", "ops": ops}) + "\n")

            for step_idx, step in enumerate(day["steps"]):
                # benchmark bookkeeping (menu construction only)
                for update in day_updates.get("by_step", {}).get(step["id"], []):
                    tid = update.get("task_id")
                    if tid in day_task_states:
                        PM_BENCH.apply_task_update(day_task_states[tid], update, task_states=day_task_states)
                for t in tasks:
                    enc_type, enc_step = PM_BENCH.normalize_encoding(t["encoding"])
                    if enc_type == "step" and enc_step == step["id"]:
                        active_task_ids.add(t["id"])
                        day_task_states[t["id"]]["active"] = True
                menu_entries, step_handle_to_id = PM_BENCH.build_step_action_menu(day_task_states, active_task_ids, lure_catalog, id_to_handle, day_name, step["id"])
                menu_text = PM_BENCH.format_action_menu(menu_entries, header="Step action menu")
                view = StepView(step_id=step["id"], text=step["text"], options=list(step["options"]), menu_text=menu_text,
                                allowed_handles=sorted(step_handle_to_id.keys()),
                                menu_entries=[{"handle": e["handle"], "action_text": e["action_text"]} for e in menu_entries])
                print(f"\n{view.text}")
                for o in view.options:
                    print(o)
                print(menu_text)

                # 1. Form / Revise on the vignette
                pre_ms = fake_ms(day_index, 0)
                payload = claude.call_json(FORM_SYSTEM, form_user(day_name, store.pending(), channels_no_clock, view.text), f"{day_name} {step['id']} FORM")
                ops = apply_ops(store, payload, day_name, step["id"], channels_no_clock, day_names, pre_ms)

                # 2. Observe: clock, then every watched channel (code-issued queries)
                state_query_counts: dict[str, int] = {}
                replies: dict[str, str] = {}
                clock_minutes: int | None = None
                clock_text: str | None = None

                def query(channel: str) -> str:
                    state_query_counts[channel] = state_query_counts.get(channel, 0) + 1
                    items = PM_BENCH.resolve_state_query_items(channel, day["steps"], step_idx, day_name, day_start_minutes,
                                                               state_channels, last_query_step_by_channel, last_snapshot_item_by_channel)
                    response = PM_BENCH.build_state_query_response(channel, items, day_name, step["id"])
                    text = PM_BENCH.format_state_query_display(response["channel"], response["items"])
                    print(f"Model action: query_state {channel}")
                    print(text)
                    return text

                if store.has_time_intentions(day_name):
                    clock_text = query("clock")
                    clock_minutes = parse_clock(clock_text)
                answered: list[str] = []
                if store.watched_channels(day_name):
                    # a pending intention watches some channel: observe every channel, so a
                    # channel mistyped at Form time still reaches the judge. Round 5: a reply is
                    # new information only if it is not empty and differs from the channel's
                    # previous reply today (snapshot channels answer every query with their state)
                    for ch in channels_no_clock:
                        r = query(ch)
                        if "(no updates)" not in r and r != last_reply_today.get(ch):
                            replies[ch] = r
                            answered.append(ch)
                        last_reply_today[ch] = r
                if answered:
                    answered = list(channels_no_clock)

                # 3. Filter: what the store fires now
                board = store.board(day_name, clock_minutes, answered)
                clock_due: set[str] = set()
                board_kept: list[Intention] = []
                for it in board:
                    if it.revised_step == step["id"]:
                        # the text that revised the trigger is the update notice, not the cue
                        continue
                    if it.trigger.get("kind") == "time":
                        hh, mm = it.trigger["at"].split(":")
                        target = int(hh) * 60 + int(mm)
                        if clock_minutes is None:
                            continue
                        if clock_minutes == target:
                            clock_due.add(it.iid)
                            board_kept.append(it)
                        # past target: the due step is gone; acting late is a false alarm in set-F1
                        continue
                    board_kept.append(it)
                board = board_kept

                # 4. Decide
                payload = claude.call_json(DECIDE_SYSTEM, decide_user(day_name, clock_text, view, replies, board, clock_due), f"{day_name} {step['id']} DECIDE")
                choice = "A"
                due_pairs: list[tuple[str, str]] = []
                if isinstance(payload, dict):
                    c = str(payload.get("choice", "A")).strip().upper()
                    choice = c if c in ("A", "B", "C") else "A"
                    for d in payload.get("due", []) if isinstance(payload.get("due"), list) else []:
                        if isinstance(d, dict):
                            due_pairs.append((str(d.get("id", "")), str(d.get("handle", ""))))
                board_ids = {it.iid for it in board}
                task_handles: list[str] = []
                acted_ids: list[str] = []
                for iid, handle in due_pairs:
                    if handle in step_handle_to_id and handle not in task_handles and iid in board_ids:
                        task_handles.append(handle)
                        acted_ids.append(iid)
                # guard: a clock-matched intention the model omitted
                guards: list[dict[str, Any]] = []
                for iid in clock_due:
                    if iid in acted_ids:
                        continue
                    it = store.intentions[iid]
                    best, best_h = 0.0, None
                    for e in view.menu_entries:
                        s = overlap(it.text, e["action_text"])
                        if s > best:
                            best, best_h = s, e["handle"]
                    if best_h and best >= GUARD_OVERLAP and best_h not in task_handles:
                        task_handles.append(best_h)
                        acted_ids.append(iid)
                        guards.append({"id": iid, "handle": best_h, "overlap": round(best, 2)})
                        guard_events += 1
                due_items_acted += len(task_handles)
                for iid in acted_ids:
                    store.mark_done(iid, day_name, step["id"])

                task_ids = [step_handle_to_id[h] for h in task_handles]
                print(f"Model action: choose {choice}" + (f" + task(s) {', '.join(task_ids)}" if task_ids else ""))
                entry = {
                    "day": day_name,
                    "step_id": step["id"],
                    "choice": choice,
                    "task_ids": task_ids,
                    "task_handles": task_handles,
                    "check_time": state_query_counts.get("clock", 0),
                    "state_queries": state_query_counts,
                }
                entries.append(entry)
                trace_log.write(json.dumps({**entry, "ops": ops, "clock": clock_text, "replies": replies,
                                            "board": [{"id": it.iid, "text": it.text, "trigger": it.trigger} for it in board],
                                            "clock_due": sorted(clock_due), "due": due_pairs, "guards": guards,
                                            **({"shadow": store.last_shadow} if isinstance(store, ShadowMuninnStore) else {})}) + "\n")
            store.end_day(day_name)
    finally:
        prompt_log.close()
        trace_log.close()

    metadata = PM_BENCH.make_run_metadata(mode=f"run-{store_kind}-store-agent", started_at_utc=started, finished_at_utc=PM_BENCH.now_utc_iso(),
                                          duration_seconds=time.perf_counter() - t0, entry_count=len(entries), model=model, backend=("bridge:" + base_url) if base_url else "claude-p")
    metadata["model_calls"] = claude.calls
    metadata["est_input_tokens"] = claude.est_input_tokens
    metadata["guard_events"] = guard_events
    if isinstance(store, ShadowMuninnStore):
        metadata["shadow_boards_compared"] = store.boards_compared
        metadata["shadow_disagreements"] = store.disagreements
    metadata["items_acted"] = due_items_acted
    PM_BENCH.write_log(resolved_log, entries, run_metadata=metadata)
    with open(str(Path(resolved_log).with_suffix(".store.json")), "w", encoding="utf-8") as fh:
        json.dump({k: asdict(v) for k, v in store.intentions.items()}, fh, indent=1)
    print(f"\nWrote log: {resolved_log}")
    print(f"model calls: {claude.calls} | est input tokens: {claude.est_input_tokens} | guard events: {guard_events}")
    return resolved_log


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--model", default="claude-sonnet-5")
    ap.add_argument("--out-dir", default="runs")
    ap.add_argument("--log", default=None)
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--max-days", type=int, default=None, help="smoke test: stop after N days (the log is then not scoreable)")
    ap.add_argument("--store", choices=["muninn", "plain", "muninn-shadow"], default="muninn",
                    help="round 8: muninn (the engine) or plain (same scaffold, in-process dict, no muninn binary)")
    ap.add_argument("--base-url", default=None,
                    help="round 8: OpenAI-compatible bridge (e.g. http://127.0.0.1:30002/v1); default calls claude -p directly")
    a = ap.parse_args()
    scenario = PM_BENCH.load_scenario(a.scenario)
    log = run(scenario, a.model, a.out_dir, a.log, a.max_days, store_kind=a.store, base_url=a.base_url, scenario_path=a.scenario)
    if a.score:
        subprocess.run([sys.executable, str(PROJECT_ROOT / "sim" / "pm_bench.py"), "score", "--scenario", a.scenario, "--log", log])


if __name__ == "__main__":
    main()
