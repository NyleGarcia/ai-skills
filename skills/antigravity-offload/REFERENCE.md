# antigravity-offload — reference

## Where things run

| Piece | Location | Notes |
|---|---|---|
| `antigravity-mcp` | zima, ns `mcp`, Deployment `antigravity-mcp` (zima2) | source `~/git/antigravity-mcp`, image `nylegarcia01/antigravity-mcp:0.1.0` (private Hub repo: bundles Google's `agy`) |
| `agy-bridge` sidecar | same pod, container `agy-bridge`, `:8001/mcp` | `sshahzaiib/agy-bridge` 0.4.2 behind `supergateway` 4.1.0; source `bridge/` in the same repo, tag `bridge-0.1.1` |
| Login | PVC `antigravity-data` → `/data/.gemini/antigravity-cli/antigravity-oauth-token` | shared by both containers; survives restarts, not a PVC delete |
| Gateway routes | `k8s/mcp/gateway/config.yaml` in the zima repo | baked into the gateway image: route change = commit + `./scripts/build-mcp-gateway.sh` + `kubectl -n mcp rollout restart deploy/mcp-gateway` |
| Docs | zima `docs/services.md` (truth), `docs/changelog.md` | |

Memory: ~200 Mi per concurrent agy run on top of each server; `AGY_MAX_CONCURRENCY=2` on the main server, limits 768 Mi per container.

## Deep research internals (antigravity-mcp ≥ 0.2.0)

- **Why async:** a standard run is 5–15 min; `deep_research` starts an `asyncio` task and returns a `job_id`; `research_result` long-polls ≤240 s (gateway `requestTimeout` is 900 s). Jobs live in server memory 24 h — a pod restart loses them.
- **One research run at a time** (`research_slot`), so it never holds both agy slots; `ask`/images still get the other.
- **Permissions:** headless agy auto-denies anything needing a prompt, `read_url` included (the agent could search but never open a page). At startup the server merges `read_url(*)` into `/data/.gemini/antigravity-cli/settings.json` → `permissions.allow`. No shell/write rule: the research prompt forbids those, because **one denied call blanks the entire response** (`response: ""`, `denied_actions` lists it). Verified 2026-10-31: flash-medium, 2 sources, 36 s.
- `read_url(*)` also applies to `ask`, and lets injected pages steer the agent to in-cluster URLs — restrict egress with a NetworkPolicy if that matters. (agy-bridge already runs `--dangerously-skip-permissions` by default, `AGY_SKIP_PERMISSIONS`.)
- **Depth → knobs:** quick = 2–3 sub-questions, 5 sources, effort medium, 0.5× timeout · standard = 4–6, 10, high, 1× (`AGY_RESEARCH_TIMEOUT_SECONDS`, default 1200) · deep = 6–10, 20, max, 2×. Model: `AGY_RESEARCH_MODEL` → `AGY_DEFAULT_MODEL` → agy default; strongest on this login is `gemini-4-argon-high`.
- **Helper:** `agy_call.py research` starts + polls (deadline 1 h, exit 2 if still running). Local fallback runs a compact prompt synchronously; needs `read_url(*)` in the local `~/.gemini/antigravity-cli/settings.json` allow-list. Nothing available → Claude's `WebSearch` (extended) or the `deep-research` skill.

## Protocol the helper speaks

Streamable HTTP, all POST to `.../mcp/` with `Accept: application/json, text/event-stream`:

1. `initialize` → read `Mcp-Session-Id` response header.
2. `notifications/initialized` with that header.
3. `tools/call` with that header; the response is SSE, take `data:` lines, parse JSON, `result.content[]` (`type: text|image`, images base64 in `data`).

The gateway requires `Authorization: Bearer <MCP_GATEWAY_API_KEY>` on every route (401 otherwise).

## New machine (no gateway reach)

- **On LAN/VPN but tools missing in Claude Code:** add the gateway entries (key from the cluster, never typed):
  ```bash
  K=$(kubectl --context admin@zima -n mcp get secret mcp-gateway-auth -o jsonpath='{.data.MCP_GATEWAY_API_KEY}' | base64 -d)
  for s in antigravity agy-bridge; do claude mcp add -s user --transport http $s https://mcp.labs.garcia.systems/servers/$s/mcp/ --header "Authorization: Bearer $K"; done
  ```
- **Off-network, want local agy:** install the pinned CLI (same URL + SHA-512 as the Dockerfile in `~/git/antigravity-mcp`), then sign in once in a real terminal:
  ```bash
  curl -sSL -o /tmp/agy.tgz https://storage.googleapis.com/antigravity-public/antigravity-cli/1.3.2-5813501495738368/linux-x64/cli_linux_x64.tar.gz
  echo "8dc2bb8471cfa6326e29e2896add767ad2d1f3714304b70fbae720d68af011182e7afde43964a7a3f54c604ab72c4fad772c8595608b059cfc582fb6798a25d2  /tmp/agy.tgz" | sha512sum -c
  tar -xzf /tmp/agy.tgz -C /tmp antigravity && install -m 0755 /tmp/antigravity ~/.local/bin/agy
  agy   # interactive OAuth; quit after sign-in
  ```
  The helper then uses `agy -p=... --output-format json` directly (text and images). Local stdio MCP instead: `MCP_TRANSPORT=stdio uv run antigravity-mcp` from the repo.
- **Neither possible:** the skill's step 3 — built-in `WebSearch`/`WebFetch` for lookups, own review, no images (say so).

## Known failure signatures

| Message | Meaning | Do |
|---|---|---|
| `route not found` | gateway lacks the route (old image) | rebuild gateway image, restart |
| `mcp: invalid session ID header` | client session predates a gateway restart | re-init (helper) / restart Claude Code |
| `503 Service Temporarily Unavailable` (nginx) | gateway pod restarting (it has OOMKilled at 1536 Mi) | wait, retry |
| `Please sign in` / `Eligibility check failed` | no token on the volume, or no CA bundle in the image | re-login in a TTY; `ca-certificates` must be installed (`node:slim` lacks it) |
| `429 ... quota` | account quota | wait; bridge fails over models |
| `Research run produced no report (denied tools: …)` | agent called a blocked tool, or `read_url` not allowed | rerun; check `permissions.allow` in agy `settings.json` |
| `Unknown tool: deep_research` | pod still on image < 0.2.0 | bump image tag, rollout |
| `Error executing tool …` with nothing else | agy died before printing its JSON envelope | check pod logs `-c antigravity-mcp` / `-c agy-bridge` |
