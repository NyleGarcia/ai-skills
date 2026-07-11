---
name: cicd-k8s-docker
description: Standardized workflows for Docker containerization, Kubernetes orchestration (Helm, manifests), and CI/CD pipelines (GitHub Actions, GitLab CI).
---

# CI/CD, K8s, & Docker Skill

This skill provides templates and workflows for modern DevOps practices.

## Docker Containerization
- **Dockerfile Best Practices**: Multi-stage builds, non-root users, .dockerignore.
- **Python Example (Multi-stage)**:
```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder
COPY . /app
WORKDIR /app
RUN uv sync --frozen --no-dev

FROM python:3.12-alpine
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY src/ /app/src/
USER nobody
CMD ["python", "src/main.py"]
```

## Kubernetes Orchestration
- **Helm Charts**: Standardize deployments across environments.
- **Manifests**: Use `Deployment`, `Service`, `Ingress`, and `NetworkPolicy`.
- **Probes**: Always include `livenessProbe` and `readinessProbe`.

## CI/CD Pipelines
- **GitHub Actions**: Automated testing, linting, and building.
- **Example GHA (CI)**:
```yaml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Run Tests
        run: uv run pytest
```

## Deployment Strategy
- **Blue/Green & Canary**: Manage traffic with Ingress or Service Mesh.
- **GitOps**: Consider tools like ArgoCD or Flux for state synchronization.
