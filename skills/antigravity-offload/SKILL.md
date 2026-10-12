---
name: antigravity-offload
description: Offload work to Google's Antigravity agent (Gemini 3.x, Nano Banana images) on the zima MCP gateway — image generation, web lookups with citations, second opinions from another model family, bulk grunt work — with a fallback chain (gateway → local agy → built-ins) when the gateway is unreachable. Use when the user asks for an image, "ask gemini", a second opinion, a doc/web lookup, or to offload a large summarise/extract task; and whenever an `antigravity` or `agy-bridge` MCP tool call fails.
---

# Antigravity offload

Two MCP servers on the zima gateway share one Google-account login (account quota, no API key):

| Server | Tools | Reach for it when |
|---|---|---|
| `antigravity` | `generate_image(prompt, aspect_ratio)`, `ask(prompt, model, effort)`, `list_models` | images; plain text offload |
| `agy-bridge` | `web_lookup(query)`, `adversarial_review(content, focus)`, `delegate(prompt)`, `follow_up(session_id, question)`, `analyze_files`, `deep_search` | lookups with sources; plan/code critique; continue a session |

Every call is a full agent run: 25–60 s, ~12k tokens of agent overhead (~40k for images). Not for trivia.

## Quick start

1. Tools present in this session (`mcp__antigravity__*`, `mcp__agy-bridge__*`)? Call them directly.
2. Not present, or call errors → run the probe and follow its verdict:
   ```bash
   python3 ~/.claude/skills/antigravity-offload/scripts/agy_call.py probe
   ```
3. From scripts/loops use the same helper instead of hand-rolled MCP calls:
   ```bash
   agy_call.py image "isometric homelab rack, flat vector" --aspect 16:9 --out rack.jpg
   agy_call.py ask "Summarise:\n$(cat big.log)"
   agy_call.py tool agy-bridge web_lookup '{"query":"agentgateway latest release, cite URL"}'
   ```

## Fallback chain (always, in this order)

1. **Gateway** `https://mcp.labs.garcia.systems/servers/{antigravity,agy-bridge}/mcp/` — LAN/VPN only; bearer from `~/.claude.json` (`mcpServers.antigravity.headers.Authorization`) or `$MCP_GATEWAY_API_KEY`.
2. **Local `agy`** — if `agy` is on PATH and signed in (`~/.gemini/antigravity-cli/antigravity-oauth-token` exists): `agy -p='<prompt>' --output-format json`. Images land under `~/.gemini/antigravity-cli/brain/<conversation_id>/`. The helper does this automatically.
3. **Degrade** — no agy anywhere: text lookups → `WebSearch`/`WebFetch`; reviews → do it yourself (say so: no second model family); images → tell the user plainly that image generation is unavailable here and what would enable it (see REFERENCE.md "New machine"). Never silently skip, never invent an image.

Helper exit codes: 0 ok · 2 tool error (quota, bad args) · 3 nothing available (fell through to step 3).

## Prompting

- **Images:** subject · style ("flat vector", "isometric", "photo") · setting/lighting · composition; pass `aspect_ratio` (`1:1`, `16:9`, `9:16`, `4:3`, `3:4`). One image per call; the model sometimes returns none → the server retries once, then errors; just call again.
- **Reviews:** `adversarial_review(content=<the plan/diff/text>, focus="correctness|security|design")`. The agent runs on zima: it cannot see local files, so paste what matters into `content`/`prompt`. `cwd`, `files`, `deep_search` only make sense for content you already put in the prompt.
- **Lookups:** ask for a one-line answer plus source URL; `web_lookup` grounds with Google Search.
- **Continuing:** every agy-bridge reply ends with `session: <id>`; pass it to `follow_up`.
- **Models:** `list_models` shows the slugs this login has (gemini-3.8-flash-*, claude-*, gpt-oss). Default is fine; name one only when the task needs it.

## Gotchas

- `invalid session ID` / 503 right after a gateway restart → stale client session: restart Claude Code or just re-init (the helper always does).
- 429 "quota" from agy → account quota, wait; the bridge fails over models on its own.
- Fresh PVC on zima = re-login needed in a real terminal: `kubectl -n mcp exec -it deploy/antigravity-mcp -- agy` (not via `!`, no TTY).
- Route/ops details, memory numbers, new-machine setup: [REFERENCE.md](REFERENCE.md).
