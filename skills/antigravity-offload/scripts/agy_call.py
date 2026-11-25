#!/usr/bin/env python3
"""Call Antigravity (Gemini) through the zima MCP gateway, falling back to a local `agy`.

    agy_call.py probe
    agy_call.py ask "prompt" [--model SLUG] [--effort low|medium|high|xhigh|max]
    agy_call.py image "prompt" [--aspect 1:1|16:9|9:16|4:3|3:4] [--out FILE]
    agy_call.py research "question" [--context TEXT] [--depth quick|standard|deep] [--model SLUG] [--out FILE]
    agy_call.py tool <server> <tool> '<json args>'      # e.g. tool agy-bridge web_lookup '{"query":"..."}'

Fallback chain: gateway (LAN/VPN, bearer key) -> local agy (signed in) -> exit 3.
Exit codes: 0 ok, 2 the tool itself errored (quota, bad args), 3 nothing available.
Stdlib only. Key comes from $MCP_GATEWAY_API_KEY or ~/.claude.json (mcpServers.<server>.headers).
"""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

GATEWAY = os.environ.get("ANTIGRAVITY_GATEWAY", "https://mcp.labs.garcia.systems/servers")
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
AGY_HOME = Path(os.environ.get("HOME", "/tmp")) / ".gemini" / "antigravity-cli"
IMAGE_EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
RESEARCH_DEADLINE = 3600  # seconds of polling before giving up on a research job
# Local fallback only; the server owns the full research prompt. Needs read_url(*) in the local
# ~/.gemini/antigravity-cli/settings.json permissions.allow, or agy can search but not read pages.
LOCAL_RESEARCH = (
    "Deep research task. Use ONLY web search and reading URLs; never run commands or edit files "
    "(blocked: calling one aborts the answer). Split the question into sub-questions, read "
    "authoritative sources, cross-check key claims across two sources, flag disagreements. Reply "
    "in Markdown: ## Answer, ## Findings (claims cited [n]), ## Disagreements and uncertainty, "
    "## Open questions, ## Sources ([n] Title - URL).\n{context}Question: {question}"
)


# ---------- gateway ----------
def bearer(server: str) -> str | None:
    key = os.environ.get("MCP_GATEWAY_API_KEY")
    if key:
        return f"Bearer {key}"
    try:
        servers = json.load(open(Path.home() / ".claude.json"))["mcpServers"]
    except (OSError, ValueError, KeyError):
        return None
    for name in (server, "antigravity", "agy-bridge"):
        auth = servers.get(name, {}).get("headers", {}).get("Authorization")
        if auth:
            return auth
    return None


def _post(url: str, auth: str, body: dict, session: str | None, timeout: float):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST")
    for k, v in {**HEADERS, "Authorization": auth, **({"Mcp-Session-Id": session} if session else {})}.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.headers.get("Mcp-Session-Id"), resp.read().decode()


def _parse(raw: str) -> dict | None:
    for line in raw.splitlines():
        line = line[5:].strip() if line.startswith("data:") else line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except ValueError:
                continue
    return None


def gateway_call(server: str, tool: str, args: dict, timeout: float = 600) -> dict:
    """Return the MCP `result` dict. Raises OSError-ish on transport/auth failure."""
    auth = bearer(server)
    if not auth:
        raise RuntimeError("no gateway key (set MCP_GATEWAY_API_KEY or add the server to ~/.claude.json)")
    url = f"{GATEWAY.rstrip('/')}/{server}/mcp/"
    init = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "agy_call", "version": "1"}}}
    session, raw = _post(url, auth, init, None, 30)
    if not session:
        raise RuntimeError(f"initialize gave no session: {raw[:200]}")
    _post(url, auth, {"jsonrpc": "2.0", "method": "notifications/initialized"}, session, 30)
    _, raw = _post(url, auth, {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                               "params": {"name": tool, "arguments": args}}, session, timeout)
    msg = _parse(raw) or {}
    if "error" in msg:
        raise RuntimeError(f"rpc error: {msg['error']}")
    return msg.get("result", {})


# ---------- local agy ----------
def local_agy() -> str | None:
    exe = shutil.which(os.environ.get("AGY_BIN", "agy"))
    if exe and (AGY_HOME / "antigravity-oauth-token").exists():
        return exe
    return None


def local_call(prompt: str, model: str | None, want_image: bool, timeout: float = 600) -> dict:
    exe = local_agy()
    if not exe:
        raise RuntimeError("no local agy")
    cmd = [exe, f"-p={prompt}", "--output-format", "json", "--print-timeout", f"{int(timeout)}s"]
    if model:
        cmd += ["--model", model]
    with tempfile.TemporaryDirectory(prefix="agy-call-") as ws:
        out = subprocess.run(cmd, cwd=ws, capture_output=True, text=True, timeout=timeout + 30, stdin=subprocess.DEVNULL)
    env = None
    for line in reversed(out.stdout.splitlines()):
        if line.startswith("{"):
            try:
                env = json.loads(line)
                break
            except ValueError:
                pass
    if env is None:
        raise RuntimeError(f"agy gave no JSON envelope (rc={out.returncode}): {(out.stderr or out.stdout)[-400:]}")
    content = [{"type": "text", "text": env.get("response", "")}]
    if want_image and env.get("conversation_id"):
        conv = AGY_HOME / "brain" / env["conversation_id"]
        for p in sorted(conv.rglob("*")):
            if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
                content.append({"type": "image", "mimeType": mime, "data": base64.b64encode(p.read_bytes()).decode()})
    return {"content": content, "isError": env.get("status") not in (None, "ok", "success", "completed")}


# ---------- front ----------
def emit(result: dict, out: str | None) -> int:
    saved = []
    for i, c in enumerate(result.get("content", [])):
        if c.get("type") == "image":
            ext = IMAGE_EXT.get(c.get("mimeType", ""), "bin")
            path = Path(out if out and i == 0 else (f"{Path(out).stem}-{i}.{ext}" if out else f"agy-image-{i}.{ext}"))
            path.write_bytes(base64.b64decode(c["data"]))
            saved.append(str(path))
        elif c.get("type") == "text" and c.get("text"):
            print(c["text"])
    for s in saved:
        print(f"[image saved] {s}")
    return 2 if result.get("isError") else 0


def run(server: str, tool: str, args: dict, prompt: str | None, model: str | None, want_image: bool, out: str | None) -> int:
    try:
        return emit(gateway_call(server, tool, args), out)
    except http.client.HTTPException as e:
        # reachable, but the stream died mid-call (agy crashed on bad args, pod restarted...)
        print(f"[gateway call broke mid-stream: {e!r}; check args / pod logs]", file=sys.stderr)
        return 2
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, TimeoutError, OSError) as e:
        print(f"[gateway unavailable: {e}]", file=sys.stderr)
    if prompt is not None:
        try:
            print("[falling back to local agy]", file=sys.stderr)
            return emit(local_call(prompt, model, want_image), out)
        except (RuntimeError, subprocess.TimeoutExpired) as e:
            print(f"[local agy unavailable: {e}]", file=sys.stderr)
    print("[nothing available: use WebSearch/WebFetch for lookups, review yourself, no images]", file=sys.stderr)
    return 3


def _text(result: dict) -> str:
    return "\n".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")


def research(question: str, context: str | None, depth: str, model: str | None, out: str | None) -> int:
    """Start a deep_research job on the gateway and poll research_result until it finishes."""
    args = {"question": question, "depth": depth, **({"context": context} if context else {}),
            **({"model": model} if model else {})}
    try:
        started = gateway_call("antigravity", "deep_research", args, timeout=120)
        if started.get("isError"):
            return emit(started, None)
        job = _text(started).splitlines()[0].removeprefix("job_id: ").strip()
        print(f"[research job {job} ({depth}) started; polling]", file=sys.stderr)
        deadline = time.time() + RESEARCH_DEADLINE
        while time.time() < deadline:
            result = gateway_call("antigravity", "research_result", {"job_id": job, "wait_seconds": 240}, timeout=300)
            text = _text(result)
            if result.get("isError") or not text.startswith(f"job_id: {job}\nstatus: running"):
                if out and not result.get("isError"):
                    Path(out).write_text(text + "\n")
                    print(f"[report saved] {out}")
                    return 0
                return emit(result, None)
            print(f"[{text.splitlines()[-1].removeprefix('status: ')}]", file=sys.stderr)
        print(f"[research job {job} still running after {RESEARCH_DEADLINE}s; poll research_result later]", file=sys.stderr)
        return 2
    except http.client.HTTPException as e:
        print(f"[gateway call broke mid-stream: {e!r}; check pod logs]", file=sys.stderr)
        return 2
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, TimeoutError, OSError) as e:
        print(f"[gateway unavailable: {e}]", file=sys.stderr)
    prompt = LOCAL_RESEARCH.format(context=f"Background: {context}\n" if context else "", question=question)
    try:
        print("[falling back to local agy research (needs read_url(*) allowed locally)]", file=sys.stderr)
        return emit(local_call(prompt, model, False, timeout=1800), out)
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        print(f"[local agy unavailable: {e}]", file=sys.stderr)
    print("[nothing available: use WebSearch (extended) / the deep-research skill instead]", file=sys.stderr)
    return 3


def probe() -> int:
    status = {"gateway": None, "local_agy": None}
    try:
        r = gateway_call("antigravity", "list_models", {}, timeout=120)
        status["gateway"] = "ok" if not r.get("isError") else f"tool error: {r}"
    except Exception as e:  # noqa: BLE001 - report everything
        status["gateway"] = f"unreachable ({e})"
    status["local_agy"] = local_agy() or "absent or not signed in"
    verdict = "gateway" if status["gateway"] == "ok" else ("local" if local_agy() else "none")
    print(json.dumps({"verdict": verdict, **status}, indent=2))
    return 0 if verdict != "none" else 3


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe")
    a = sub.add_parser("ask"); a.add_argument("prompt"); a.add_argument("--model"); a.add_argument("--effort")
    i = sub.add_parser("image"); i.add_argument("prompt"); i.add_argument("--aspect", default="1:1"); i.add_argument("--out")
    r = sub.add_parser("research"); r.add_argument("question"); r.add_argument("--context"); r.add_argument("--model"); r.add_argument("--out")
    r.add_argument("--depth", default="standard", choices=["quick", "standard", "deep"])
    t = sub.add_parser("tool"); t.add_argument("server"); t.add_argument("tool"); t.add_argument("args", nargs="?", default="{}"); t.add_argument("--out")
    ns = ap.parse_args()
    if ns.cmd == "probe":
        return probe()
    if ns.cmd == "ask":
        args = {"prompt": ns.prompt, **({"model": ns.model} if ns.model else {}), **({"effort": ns.effort} if ns.effort else {})}
        return run("antigravity", "ask", args, ns.prompt, ns.model, False, None)
    if ns.cmd == "research":
        return research(ns.question, ns.context, ns.depth, ns.model, ns.out)
    if ns.cmd == "image":
        return run("antigravity", "generate_image", {"prompt": ns.prompt, "aspect_ratio": ns.aspect},
                   f"Generate one image, aspect ratio {ns.aspect}: {ns.prompt}", None, True, ns.out)
    args = json.loads(ns.args)
    prompt = args.get("prompt") or args.get("query") or args.get("question") or args.get("content")
    return run(ns.server, ns.tool, args, prompt, args.get("model"), False, ns.out)


if __name__ == "__main__":
    sys.exit(main())
