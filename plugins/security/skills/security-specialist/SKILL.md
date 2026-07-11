---
name: security-specialist
description: End-to-end security skill. Includes security-qa for static analysis/checklists and security-fuzzer for active vulnerability analysis/endpoint discovery.
---

# Security Specialist

Comprehensive security auditing and active defense.

## 1. Static Analysis & QA (`security-qa`)
Checklists and tools for codebase hardening.
- **Checklist**: Secrets mgmt, dependency scanning (`snyk`, `trivy`), SAST (`bandit`, `semgrep`).
- **QA**: Unit/Integration tests, E2E (`playwright`), Perf (`locust`).
- **K8s/Docker**: Scan manifests (`kubesec`) and images (`trivy`).

## 2. Active Fuzzing (`security-fuzzer`)
Vulnerability analysis and endpoint discovery.
- **Workflow**: Define scope -> Select wordlists (SecLists) -> Execute (`ffuf`, `gobuster`) -> Filter/Analyze.
- **Targets**: Exposed `.git`, `.env`, hidden API versions, parameter injections.

## Directives
- ONLY test authorized targets.
- Rate limit to prevent DoS.
- Principle of least privilege for IAM.
