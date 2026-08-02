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

In CI, add a shared cache backend: `docker buildx build --cache-to type=gha,mode=max --cache-from type=gha .`

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

```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-slim AS build
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build && npm prune --omit=dev

FROM node:22-slim
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

Distroless runtime variant: `FROM gcr.io/distroless/nodejs22-debian12` and `CMD ["dist/index.js"]`.

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
