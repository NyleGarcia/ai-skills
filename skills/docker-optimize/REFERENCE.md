# Docker Optimize — Reference

Detailed techniques and per-language multi-stage templates. Load only when rewriting a Dockerfile.

## Technique catalog

### Base image selection

| Choice | Typical size | Trade-off |
|---|---|---|
| `ubuntu` / full `node`, `python` | 400 MB–1 GB+ | Everything works; huge |
| `*-slim` (Debian slim) | 60–250 MB | glibc, apt available; good default |
| `*-alpine` | 5–80 MB | musl libc — native modules / wheels can break |
| `gcr.io/distroless/*` | 2–100 MB | No shell/package manager; runtime-only, most secure |
| `scratch` | 0 MB | Static binaries only (Go, Rust) |

- Pin a specific tag (`node:22-slim`), ideally with digest for reproducible CI builds.
- Prefer slim/distroless over alpine for Python (many wheels don't ship musl builds → slow source compiles).

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
