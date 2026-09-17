# Docker Optimize — Reference

Detailed techniques and per-language multi-stage templates. Load only when rewriting a Dockerfile.

## Technique catalog

### Base image selection

| Choice | Typical size | Trade-off |
|---|---|---|
| `ubuntu` / full `node`, `python` | 400 MB–1 GB+ | Everything works; huge. Build stages only |
| `*-slim` (Debian slim) | 60–250 MB | glibc, apt available; **the default choice** |
| `*-alpine` | 5–80 MB | musl libc — native deps compile from source; slow builds, subtle breakage |
| `gcr.io/distroless/*` | 2–100 MB | No shell/package manager but includes CA root certs; runtime-only, most secure |
| `scratch` | 0 MB | Literally empty — static binaries only, bring your own certs |

- **Slim beats Alpine.** Alpine's musl libc means many native dependencies (Python wheels, C-based Node modules) have no prebuilt binaries and must compile during the build — a heavy time tax plus glibc-compat crash risk, all to save a few tens of MB. Reach for Alpine only when everything in the image is verified musl-clean.
- **Distroless beats scratch** for most runtime stages: same no-shell security profile and near-zero weight, but it ships runtime basics like root certificates so TLS works out of the box.

### Pin digests, not tags

Tags — even specific ones like `node:22-slim`, let alone `latest` — are mutable: the maintainer can repoint them at a different build tomorrow and silently break your pipeline.

```dockerfile
FROM node:22-slim@sha256:1a83c9d3f1c5...   # immutable; keep the tag for readability
```

Get the digest with `docker buildx imagetools inspect node:22-slim` (or `docker pull` + `docker image inspect --format '{{index .RepoDigests 0}}'`). Tools like Renovate/Dependabot can bump pinned digests automatically.

### Layer caching

Docker caches per instruction; the first changed instruction invalidates all subsequent layers.

```dockerfile
# BAD: any source change re-installs all dependencies
COPY . .
RUN npm ci

# GOOD: dependency layer survives source changes
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

Same pattern everywhere: `requirements.txt`/`uv.lock` → `pip install` → `COPY . .`; `go.mod go.sum` → `go mod download` → `COPY . .`; `pom.xml` → `mvn dependency:go-offline` → `COPY src`.

### RUN hygiene — clean in the same layer

Layers are additive: deleting files in a *later* layer hides them but doesn't shrink the image.

```dockerfile
# BAD: cache still baked into the earlier layer
RUN apt-get update && apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# GOOD: install + clean in one layer
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
```

- pip: `pip install --no-cache-dir ...`
- apk: `apk add --no-cache ...`
- npm: `npm ci` then `npm cache clean --force` (or rely on cache mounts instead)

### BuildKit cache mounts

Persist package-manager caches across builds without baking them into layers:

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=cache,target=/root/.npm npm ci
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=cache,target=/go/pkg/mod --mount=type=cache,target=/root/.cache/go-build go build ./...
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y gcc
```

### CI / remote build caching

CI runners are usually ephemeral — without an exported cache, every CI build is a cold build. BuildKit can push the layer cache somewhere persistent and pull it back next run:

```bash
# GitHub Actions cache backend
docker buildx build --cache-to type=gha,mode=max --cache-from type=gha .

# Registry cache (works on any CI) — cache lives next to the image
docker buildx build \
  --cache-to type=registry,ref=ghcr.io/org/app:buildcache,mode=max \
  --cache-from type=registry,ref=ghcr.io/org/app:buildcache \
  --push -t ghcr.io/org/app:$SHA .
```

- `mode=max` caches intermediate (build-stage) layers too, not just the final image's — essential for multi-stage builds.
- Simplest fallback: `--cache-from` the previously pushed image tag with inline cache (`--cache-to type=inline`), at the cost of only caching final-stage layers.

### Modern BuildKit instructions

- **`COPY --link`**: makes the copied layer independent of preceding layers, so a base-image bump doesn't invalidate it. Ideal for `COPY --from=build --link /app/dist ./dist`.
- **Bind mounts instead of COPY in build stages**: `RUN --mount=type=bind,source=.,target=/src go build -o /bin/app /src` — the context is mounted, not baked into a layer; nothing to clean up.
- **Heredocs** for readable multi-line RUN blocks:

  ```dockerfile
  RUN <<EOF
  set -e
  apt-get update
  apt-get install -y --no-install-recommends curl
  rm -rf /var/lib/apt/lists/*
  EOF
  ```

### Multi-platform builds

Apple Silicon dev machines + amd64 production (or Graviton runners) make single-arch images a recurring "works on my machine" source. Build both at once:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/org/app:$SHA --push .
```

In cross-compiling stages, split build vs target platform: `FROM --platform=$BUILDPLATFORM golang:1.24 AS build` with `GOARCH=$TARGETARCH` — compiles natively on the runner instead of under slow QEMU emulation.

### Build-time secrets

Never `ARG TOKEN` or `COPY .npmrc` — both persist in image history.

```dockerfile
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
# build: docker build --secret id=npmrc,src=$HOME/.npmrc .
```

### .dockerignore (starter)

`COPY . .` is a perfectly good pattern — *if* `.dockerignore` is maintained like `.gitignore`. That beats long lists of narrowly-scoped `COPY` commands, which bloat the Dockerfile and rot as the project grows. A missing or thin `.dockerignore` also ships the whole context (including `.git` and `node_modules`) to the Docker daemon on every build.

```
.git
.gitignore
node_modules
dist
build
__pycache__
*.pyc
.venv
.env*
*.md
Dockerfile*
docker-compose*
.github
coverage
*.log
```

### Security hardening

```dockerfile
RUN useradd --system --uid 1001 appuser     # (alpine: adduser -S)
USER appuser
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:8080/health || exit 1
```

- `COPY --chown=appuser:appuser` when the app must write to its files.
- Scan the result: `docker scout cves app:after` or `trivy image app:after`.

### Signals, PID 1, and graceful shutdown

A container that ignores SIGTERM gets SIGKILLed after the grace period — dropped requests and corrupted state on every deploy.

```dockerfile
# BAD: shell form — /bin/sh is PID 1, your app never sees SIGTERM
CMD node dist/index.js

# GOOD: exec form — the app is PID 1 and receives signals
CMD ["node", "dist/index.js"]
```

- If the app spawns child processes, PID 1 must also reap zombies: use `docker run --init`, or bake in tini (`ENTRYPOINT ["tini", "--"]`).
- `STOPSIGNAL SIGQUIT` when the app's graceful-shutdown signal isn't SIGTERM (e.g. Nginx).
- The app itself must handle the signal — verify with `docker stop` and watch shutdown logs.

### Supply chain: labels, SBOM, provenance, signing

Standard OCI labels make images traceable back to source:

```dockerfile
LABEL org.opencontainers.image.source="https://github.com/org/app" \
      org.opencontainers.image.revision="${GIT_SHA}" \
      org.opencontainers.image.licenses="MIT"
```

Attach attestations at build time and sign in CI:

```bash
docker buildx build --sbom=true --provenance=mode=max -t ghcr.io/org/app:$SHA --push .
cosign sign --yes ghcr.io/org/app@$DIGEST
```

`--provenance` produces SLSA provenance (what built the image, from what source); `--sbom` embeds a software bill of materials that scanners and auditors can consume without pulling the image apart.

### Lint with droast

[droast](https://github.com/immanuwell/dockerfile-roast) is a fast, opinionated Rust Dockerfile linter (~85 rules): flags `npm install` instead of `npm ci`, missing `.dockerignore`, `apt-get install` without `--no-install-recommends`, unpinned base images, uncleaned caches, missing healthchecks, and other anti-patterns.

```bash
brew install droast          # or grab a release binary
droast Dockerfile            # single file
droast .                     # recurse the repo
droast --format sarif .      # CI-friendly output; a GitHub Action also exists
```

Run it before and after a rewrite; treat remaining warnings as a to-do list.

### One process per container — a guideline, not a law

The ideal is one process per container, but strict adherence can cost more complexity than it saves. If the app genuinely needs a sidecar-ish companion (e.g. an Nginx proxy directly in front of it) and you aren't on an orchestrator that gives you sidecars for free, running both under a lightweight supervisor like `supervisord` in one container is a legitimate choice:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends supervisor nginx \
    && rm -rf /var/lib/apt/lists/*
COPY supervisord.conf /etc/supervisor/conf.d/app.conf
CMD ["supervisord", "-n"]
```

On Kubernetes, prefer real sidecar containers instead.

## Language templates

### Node.js

Prerequisite: a maintained `.dockerignore` (see above) — it's what makes `COPY . .` safe.

```dockerfile
# syntax=docker/dockerfile:1

# Builder: slim (not alpine), pinned by digest. Replace the digest with the
# current one: docker buildx imagetools inspect node:22-slim
FROM node:22-slim@sha256:<digest> AS build
WORKDIR /app
# Onion caching: manifests first, so the dependency layer survives code edits
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
# Safe because .dockerignore excludes node_modules, .git, logs, env files
COPY . .
RUN npm run build && npm prune --omit=dev

# Runtime: distroless — no shell, no package manager, but CA certs included.
# Runs as nonroot by default; exec-form CMD so the app receives SIGTERM.
FROM gcr.io/distroless/nodejs22-debian12:nonroot@sha256:<digest>
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build --link /app/node_modules ./node_modules
COPY --from=build --link /app/dist ./dist
COPY --from=build --link /app/package.json ./
EXPOSE 3000
CMD ["dist/index.js"]
```

Slim runtime variant (when you need a shell for debugging): `FROM node:22-slim@sha256:<digest>`, add `USER node`, and `CMD ["node", "dist/index.js"]`.

### Python (uv)

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-slim AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

FROM python:3.13-slim
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=build /app /app
RUN useradd --system --uid 1001 appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

pip variant: `COPY requirements.txt ./` → `RUN --mount=type=cache,target=/root/.cache/pip pip install --prefix=/install -r requirements.txt`, then `COPY --from=build /install /usr/local` in the runtime stage.

### Go

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.24 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod go mod download
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -ldflags="-s -w" -o /bin/app .

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /bin/app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
```

`scratch` also works for pure-static binaries; add `COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/` if the app makes TLS calls.

### Java (Maven + JRE)

```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jdk AS build
WORKDIR /app
COPY pom.xml mvnw ./
COPY .mvn .mvn
RUN --mount=type=cache,target=/root/.m2 ./mvnw dependency:go-offline
COPY src src
RUN --mount=type=cache,target=/root/.m2 ./mvnw package -DskipTests

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN useradd --system --uid 1001 appuser
USER appuser
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Go further with `jlink` (custom minimal JRE) or `jdeps` to trim modules.

## Diagnosing a fat image

```bash
docker history app:tag --format "{{.Size}}\t{{.CreatedBy}}" --no-trunc | sort -hr | head -15
dive app:tag                # interactive layer browser, shows wasted space
docker sbom app:tag         # what's actually inside
```

Common culprits: dev dependencies in the final stage, `.git` in the build context, package-manager caches, `COPY . .` into the runtime stage, build toolchains (gcc, JDK, full node) shipped to production.
