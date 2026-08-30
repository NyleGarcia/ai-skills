#!/usr/bin/env python3
"""Claude Code statusline.

Renders: <elapsed> | <model> | <effort> | Ctx:<pct> | $<cost> ($<rate>/hr) | <branch> | <project>

Wire up in ~/.claude/settings.json:
    "statusLine": {"type": "command", "command": "/home/Zedwil/git/ai-skills/scripts/statusline.py"}
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

DEBUG_DUMP = os.environ.get("CLAUDE_STATUSLINE_DEBUG")

# ---- palette (256-color, dark bg) -----------------------------------------
SEP = "\033[38;5;240m│\033[0m"
DIM = "\033[38;5;245m"
MODEL = "\033[38;5;110m"
EFFORT = "\033[38;5;140m"
COST = "\033[38;5;108m"
BRANCH = "\033[38;5;180m"
PROJ = "\033[38;5;74m"
OK, WARN, HOT = "\033[38;5;108m", "\033[38;5;179m", "\033[38;5;174m"
R = "\033[0m"

BRANCH_MAX = 20


def dig(d, *path, default=None):
    for k in path:
        if not isinstance(d, dict):
            return default
        d = d.get(k)
    return d if d is not None else default


def fmt_elapsed(ms):
    if not ms or ms < 0:
        return None
    s = int(ms / 1000)
    h, m, s = s // 3600, (s % 3600) // 60, s % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    if m:
        return f"{m}m{s:02d}s"
    return f"{s}s"


def transcript_stats(path):
    """Return (context_tokens, session_ms) scraped from the transcript."""
    ctx, first, last = 0, None, None
    if not path or not os.path.exists(path):
        return ctx, None
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line or '"timestamp"' not in line:
                    continue
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = ev.get("timestamp")
                if ts:
                    first = first or ts
                    last = ts
                if ev.get("type") != "assistant" or ev.get("isSidechain"):
                    continue
                u = dig(ev, "message", "usage", default={})
                total = sum(
                    u.get(k) or 0
                    for k in (
                        "input_tokens",
                        "cache_read_input_tokens",
                        "cache_creation_input_tokens",
                        "output_tokens",
                    )
                )
                if total:
                    ctx = total
    except OSError:
        return ctx, None
    span = None
    if first and last:
        try:
            t0 = datetime.fromisoformat(first.replace("Z", "+00:00"))
            span = (datetime.now(timezone.utc) - t0).total_seconds() * 1000
        except ValueError:
            span = None
    return ctx, span


def git_branch(cwd):
    try:
        out = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=1,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    name = out.stdout.strip()
    if out.returncode != 0 or not name:
        return None
    if name == "HEAD":  # detached
        sha = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=1,
        ).stdout.strip()
        name = f"@{sha}" if sha else "detached"
    if len(name) > BRANCH_MAX:
        name = name[: BRANCH_MAX - 2] + ".."
    return name


def context_pct(data, transcript_tokens):
    """Prefer the harness-reported usage; fall back to transcript math."""
    pct = dig(data, "context_window", "used_percentage")
    if isinstance(pct, (int, float)):
        return round(pct)
    if not transcript_tokens:
        return None
    limit = dig(data, "context_window", "context_window_size")
    if not isinstance(limit, int) or limit <= 0:
        hay = f'{dig(data, "model", "id", default="")} {dig(data, "model", "display_name", default="")}'.lower()
        limit = 1_000_000 if ("[1m]" in hay or "1m context" in hay) else 200_000
    return round(100 * transcript_tokens / limit)


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        data = {}

    if DEBUG_DUMP:
        try:
            with open(DEBUG_DUMP, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2)
        except OSError:
            pass

    cwd = data.get("cwd") or dig(data, "workspace", "current_dir") or os.getcwd()
    project = dig(data, "workspace", "project_dir") or cwd
    model_id = dig(data, "model", "id", default="")
    display = dig(data, "model", "display_name", default="") or model_id or "claude"
    if "1m" in model_id.lower() and "1m" not in display.lower():
        display += " (1M context)"

    ctx_tokens, span_ms = (0, None)
    if dig(data, "context_window", "used_percentage") is None:
        ctx_tokens, span_ms = transcript_stats(data.get("transcript_path"))
    dur_ms = dig(data, "cost", "total_duration_ms") or span_ms
    cost = dig(data, "cost", "total_cost_usd", default=0.0) or 0.0

    parts = []

    elapsed = fmt_elapsed(dur_ms)
    if elapsed:
        parts.append(f"{DIM}{elapsed}{R}")

    parts.append(f"{MODEL}{display}{R}")

    effort = dig(data, "effort", "level") or data.get("reasoning_effort")
    if effort:
        parts.append(f"{EFFORT}{effort}{R}")

    pct = context_pct(data, ctx_tokens)
    if pct is not None:
        tone = OK if pct < 50 else WARN if pct < 80 else HOT
        parts.append(f"{tone}Ctx:{pct}%{R}")

    if cost:
        hours = (dur_ms or 0) / 3_600_000
        rate = f" (${cost / hours:.2f}/hr)" if hours > 0.02 else ""
        parts.append(f"{COST}${cost:.2f}{rate}{R}")

    branch = git_branch(cwd)
    if branch:
        parts.append(f"{BRANCH}{branch}{R}")

    parts.append(f"{PROJ}{os.path.basename(project.rstrip('/')) or project}{R}")

    sys.stdout.write(f" {SEP} ".join(parts))


if __name__ == "__main__":
    main()
