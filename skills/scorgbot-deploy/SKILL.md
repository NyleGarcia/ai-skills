---
name: scorgbot-deploy
description: Deploy, operate, and debug the SC-ORG-BOT Kubernetes stack (Helm + ArgoCD in voidput/sc-org-bot-deploy). Use for any work in that repo or when the user mentions deploying SC-ORG-BOT, ArgoCD apps, image updater tags, K8s secrets for the bot, Celery Flower, or dev/prod environment issues for the org bot. Complements bootstrap-scorgbot (which scaffolds new monorepos — this skill is for running the existing deployment).
---

# SC-ORG-BOT Deployment Operations

Operating manual for `voidput/sc-org-bot-deploy`: Helm chart + ArgoCD manifests for SC-ORG-BOT's four services — API (FastAPI), Discord Bot, Celery Worker, React Frontend — backed by in-cluster Bitnami PostgreSQL and Redis/Valkey (ArgoCD-managed, on DO block storage — not managed DO Postgres, despite what the stale README implies).

**Trust the manifests, not the prose.** `README.md`'s setup section and `GEMINI.md` describe an older single-env flow and a tag regex that no longer exists in any live Application. When docs and `argocd/*.yaml` disagree, the YAML wins — verify claims against it.

## Repo map (`argocd/` is more than two apps)

- `argocd/dev-app.yaml`, `prod-app.yaml` — the app Applications (namespaces `sc-org-bot-dev`/`-prod`).
- `argocd/databases-dev.yaml`, `databases-prod.yaml` — Bitnami Postgres + Redis Applications the app depends on.
- `argocd/dev-image-updater.yaml` — ImageUpdater CR for dev; `cluster-issuer.yaml` (cert-manager `letsencrypt-prod`); `argocd-notifications-cm.yaml` + Discord webhooks; `observability-faro.yaml`.
- `argocd/appproject.yaml` — restricted AppProject, **not yet in effect**: both apps deliberately sit on `project: default` (see its header). Don't flip them to `project: sc-org-bot` as a side quest; that's a planned migration with its own rollout order (project applied and confirmed first).
- `argocd/application.yaml` — **deprecated, never apply.** Collides with prod on the `starorg.tools` ingress host, targets an older chart schema, pins `tag: latest` with automated sync. If a stray `sc-org-bot` Application exists in-cluster, delete it deliberately — removing the file doesn't.
- `charts/sc-org-bot/` — the chart; `values.yaml` is shared base, env differences go in `values-dev.yaml`/`values-prod.yaml`.

## Fresh-environment deploy checklist (order matters)

1. **Platform prereqs in cluster:** ArgoCD, argocd-image-updater controller, ingress-nginx, cert-manager; then `kubectl apply -f argocd/cluster-issuer.yaml`.
2. **Secrets:** `./scripts/create-secrets.sh dev` (reads `.env.dev`; `prod` reads `.env.prod`). Creates the namespaces plus `[namespace]-secret`, `databases-{env}-secret` (the Bitnami charts depend on it), `ocr-hauler-{env}-secret`, `regcred`, `argocd-notifications-secret`, and — only if `ca-certificate.crt` is present — `scbot-ca-cert` (skipped with just a warning otherwise; check the output).
3. **`dockerhub-creds` in the `argocd` namespace — manual, no script creates it.** All image-updater configs reference `pullsecret:argocd/dockerhub-creds`; without it the updater can't poll Docker Hub and nothing ever rolls out.
4. **Databases before the app:** `kubectl apply -f argocd/databases-dev.yaml` (or `-prod`). Skipping this leaves every backend CrashLooping on DB connections.
5. **The app:** `kubectl apply -f argocd/dev-app.yaml` (or `prod-app.yaml`).
6. **Fresh DB only:** apply `initial_schema.sql`, then `scripts/seed-db.sh`.

## Releases & image updates — read the actual regexes

Rollouts are driven by ArgoCD Image Updater with git write-back (expect `build: automatic update of sc-org-bot-dev` commits; don't fight them, and don't edit image tags by hand). Write-back lands in `charts/sc-org-bot/.argocd-source-sc-org-bot-dev.yaml` — **that file, not `values-dev.yaml`, is the live dev tag.** The `tag:` in the values files is only the initial/base value and goes stale (both still say `1.0.0-beta.45` while dev runs far past that). To answer "what's deployed in dev?", read the `.argocd-source` file or the latest updater commit. Prod has no `.argocd-source` file because it has never auto-updated. The per-env allow-tags differ and neither has an optional beta group:

- **Dev** (`dev-app.yaml` annotations): `regexp:^v?1\.\d+\.\d+-beta\.\d+$` — `-beta.N` **required**; stable tags never flow to dev.
- **Prod** (`prod-app.yaml` annotations): `regexp:^v?1\.\d+\.\d+$` — stable only; no prerelease suffix matches.
- A tag matching neither (e.g. `1.4.0-rc.1`) is silently ignored everywhere — "my release isn't rolling out" almost always means the tag fails the env's regex. Retag as `1.4.0-beta.N` (dev) or `1.4.0` (prod).
- `dev-image-updater.yaml` (the CR) carries a beta-*optional* regex that disagrees with the dev app annotations — check which mechanism is actually reconciling before "fixing" either.
- **Do not restore an optional-beta group to prod.** `prod-app.yaml`'s header documents that exact regex as the historic bug; prod is still pinned at `1.0.0-beta.45` and has never auto-updated, so the first stable rollout is a large, deliberate event — not routine.

## Conventions that bite

- `CORS_ORIGINS` in `values-*.yaml` is a **comma-separated string**, not a YAML list.
- `DISCORD_REDIRECT_URI` must exactly match the Discord Dev Portal entry (usually `https://[host]/auth/callback`) — mismatch breaks OAuth silently.
- API runs uvicorn with `--proxy-headers --forwarded-allow-ips='*'` for ingress compatibility; keep these when touching deployment args.
- SQLAlchemy uses `postgresql+asyncpg` — plain `postgresql://` connection strings break the async engine.
- Prometheus scrapes backend pods via `prometheus.io/scrape` annotations; telemetry at `/metrics`.

## Ops & debugging

- **Celery Flower is deliberately not on the ingress** (no auth; can revoke tasks and kill workers). Access only via `kubectl port-forward -n sc-org-bot-prod svc/celery-flower 5555:5555`. Never "fix" access by adding it to the ingress.
- **DB maintenance:** `scripts/seed-db.sh`, `scripts/manual_optimize.py`, `scripts/apply_indexes.py`, `scripts/check_connections.py`.
- **Registry hygiene:** `scripts/cleanup_docker_tags_v3.py` is current (v1/v2 superseded).

## Guardrails

- Both apps use `syncPolicy.automated` + `selfHeal`: manual `kubectl` edits to chart-managed resources revert on sync. Change git instead.
- Test chart changes with `helm template charts/sc-org-bot -f charts/sc-org-bot/values-dev.yaml` before pushing — automated sync means a bad render deploys itself.
- Never hardcode credentials in values files; they live in git.
