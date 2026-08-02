---
name: docker-optimize
description: Optimize Docker images for size, build speed, and security via multi-stage builds, layer-cache ordering, minimal base images, BuildKit cache mounts, and .dockerignore. Use when a Docker image is too large or slow to build, when reviewing or writing a Dockerfile, or when user mentions "optimize docker", "shrink image", "docker build slow", or "reduce image size".
---

# Docker Optimize

Audit and rewrite Dockerfiles so images are small, builds are fast (cache-friendly), and containers run securely. Always **measure before and after** so the improvement is provable.

## Workflow

### 1. Measure the baseline

```bash
docker build -t app:before .
docker image ls app:before                    # total size
docker history app:before --no-trunc          # size per layer — find the fat ones
```

If `dive` is available, use `dive app:before` to inspect wasted bytes per layer.

### 2. Audit the Dockerfile

Check, in order of impact:

- [ ] **Base image**: full-fat image (`node`, `python`, `ubuntu`) where `-slim`, `-alpine`, or distroless would do? Tag pinned (never bare `latest`)?
- [ ] **Multi-stage build**: are build tools (compilers, dev dependencies, SDKs) present in the final image? They shouldn't be.
- [ ] **Layer order**: are dependency manifests (`package.json`, `requirements.txt`, `go.mod`) copied and installed *before* `COPY . .`? Least-changing instructions first.
- [ ] **`.dockerignore`**: exists and excludes `.git`, `node_modules`, build output, tests, docs, secrets/env files?
- [ ] **RUN hygiene**: package-manager caches cleaned *in the same layer* (`apt-get clean`, `--no-cache-dir`, `rm -rf /var/lib/apt/lists/*`)? A later `rm` in its own layer removes nothing from image size.
- [ ] **BuildKit cache mounts**: `RUN --mount=type=cache,...` for package-manager caches so rebuilds don't redownload?
- [ ] **Security**: runs as non-root `USER`? No secrets in `COPY`/`ENV`/build args? `HEALTHCHECK` where relevant?

### 3. Rewrite

Apply the canonical shape — build stage with all tooling, minimal runtime stage that copies only artifacts:

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
USER node
CMD ["node", "dist/index.js"]
```

Language-specific templates (Node, Python, Go, Java) and advanced techniques: see [REFERENCE.md](REFERENCE.md).

### 4. Verify

```bash
docker build -t app:after .
docker image ls app:before app:after          # compare sizes
docker run --rm app:after                     # smoke test — it must still run
docker build -t app:after . && touch src/x && docker build -t app:after .
                                              # 2nd build: deps layers must be CACHED
```

Report the before/after size and build-time delta. If the app has tests, run them against the new image.

## Rules of thumb

- Order instructions least-changing → most-changing; a changed layer invalidates every layer after it.
- One logical concern per `RUN`; chain with `&&` and clean up in the same layer.
- `COPY` only what's needed (`COPY src/ src/`), not the whole context, in the runtime stage.
- Prefer distroless or `-slim` over `alpine` when native deps have musl issues.
- Never bake secrets into layers — use `RUN --mount=type=secret` for build-time credentials.
