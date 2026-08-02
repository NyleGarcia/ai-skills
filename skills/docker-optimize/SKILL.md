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

Run `droast Dockerfile` if available (opinionated Rust linter, catches most of the below). Then check, in order of impact:

- [ ] **Base image**: default to `-slim`, not Alpine. Alpine's musl libc forces native deps (Python wheels, C-based Node modules) to compile from source — slower builds and runtime breakage for a negligible size win. Full-fat images (`node`, `python`, `ubuntu`) only in build stages, if at all.
- [ ] **Pinned by digest**: tags are mutable — `node:22-slim` can point at a different build tomorrow. Pin `FROM node:22-slim@sha256:...` for immutable, reproducible builds.
- [ ] **Multi-stage build**: are build tools (compilers, dev dependencies, SDKs) present in the final image? They shouldn't be.
- [ ] **Layer order**: are dependency manifests (`package.json`, `requirements.txt`, `go.mod`) copied and installed *before* `COPY . .`? Least-changing instructions first — layer order *is* your cache strategy.
- [ ] **`.dockerignore`**: `COPY . .` is a fine pattern *if* `.dockerignore` is thorough. Treat it like `.gitignore`: exclude `.git`, `node_modules`, build output, logs, secrets/env files. Prefer this over sprawling, hard-to-maintain lists of specific `COPY` commands.
- [ ] **RUN hygiene**: package-manager caches cleaned *in the same layer* (`apt-get clean`, `--no-cache-dir`, `rm -rf /var/lib/apt/lists/*`)? A later `rm` in its own layer removes nothing from image size. Lockfile-respecting installs (`npm ci`, not `npm install`)?
- [ ] **BuildKit cache mounts**: `RUN --mount=type=cache,...` for package-manager caches so rebuilds don't redownload?
- [ ] **Signals & PID 1**: `CMD`/`ENTRYPOINT` in exec (JSON array) form so SIGTERM reaches the app, not a wrapping shell? An init (`tini` / `docker run --init`) if the app spawns child processes?
- [ ] **CI caching**: builds in CI export/import cache (`--cache-to`/`--cache-from` with a registry or `gha` backend)? Without it, every CI build is a cold build.
- [ ] **Security**: runs as non-root `USER`? No secrets in `COPY`/`ENV`/build args? `HEALTHCHECK` where relevant?

### 3. Rewrite

Apply the canonical shape — build stage with all tooling, minimal runtime stage that copies only artifacts:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-slim@sha256:<digest> AS build        # slim, digest-pinned
WORKDIR /app
COPY package.json package-lock.json ./            # manifests first: onion caching
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .                                          # safe — .dockerignore is thorough
RUN npm run build && npm prune --omit=dev

FROM gcr.io/distroless/nodejs22-debian12:nonroot@sha256:<digest>
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
CMD ["dist/index.js"]                             # exec form: app gets SIGTERM
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

Re-run `droast Dockerfile` until clean. Report the before/after size and build-time delta. If the app has tests, run them against the new image.

## Rules of thumb

- Order instructions least-changing → most-changing; a changed layer invalidates every layer after it.
- One logical concern per `RUN`; chain with `&&` and clean up in the same layer.
- Build stage: `COPY . .` with a strict `.dockerignore`. Runtime stage: `COPY --from=build` only the artifacts.
- Slim over Alpine (glibc vs musl); distroless over `scratch` for the runtime stage — same tiny/no-shell security profile, but ships runtime basics like CA root certificates.
- Pin base images by digest, never bare `latest` or a mutable tag alone.
- Never bake secrets into layers — use `RUN --mount=type=secret` for build-time credentials.
- One process per container is a guideline, not a law: if the app genuinely needs e.g. an Nginx proxy in front and you're not on Kubernetes, running both under `supervisord` in one container is fine.
