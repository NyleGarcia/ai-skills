---
name: security-qa
description: Security auditing, vulnerability scanning (Snyk, Trivy, Bandit), and quality assurance procedures for Python applications and infrastructure.
---

# Security & QA Skill

This skill provides checklists and tools for security auditing and QA testing.

## Security Best Practices
- **Secrets Management**: Use Vault, AWS Secrets Manager, or Doppler.
- **Dependency Scanning**: Use `snyk test` or `trivy fs .`.
- **Static Analysis (SAST)**:
  - **Bandit**: `bandit -r src/` (Python specific).
  - **Semgrep**: `semgrep --config auto`.

## Infrastructure Security
- **Container Security**: Scan images with `trivy image <name>`.
- **K8s Security**: Use `kubesec scan manifest.yaml`.
- **IAM Policies**: Principle of least privilege.

## Quality Assurance (QA)
- **Unit Testing**: Focus on logic with `pytest`.
- **Integration Testing**: Test with real external services (or mocks).
- **End-to-End (E2E)**: Use `Playwright` for web apps.
- **Performance Testing**: `Locust` for load testing Python apps.

## QA Checklist
- [ ] Code Coverage: Minimum 80%.
- [ ] Linting & Formatting passes.
- [ ] No high/critical vulnerabilities found in dependency scan.
- [ ] Documentation up-to-date with API changes.
- [ ] Performance benchmarks meet SLIs.
