---
name: technical-writing
description: Technical documentation and knowledge management. Merges skill-seekers and tapestry. Auto-generates agent skills and knowledge graphs from raw docs/PDFs.
---

# Technical Writing & Knowledge Engine

Transform raw information into agent-ready intelligence.

## 1. Skill Generation (`skill-seekers`)
Convert any documentation, PDF, or repo into structured AI skills instantly.
- **Workflow**: Ingest -> Identify Workflows -> Map Resources -> Generate `SKILL.md`.

## 2. Knowledge Graphs (`tapestry`)
Turn technical docs and PDFs into navigable Obsidian-compatible graphs via the `graphify-vault` skill: `graphify extract` -> `graphify export obsidian --dir docs/knowledge`.
- `docs/knowledge/` is a regenerable per-symbol cache (gitignored, not committed, not linked from `docs/Home.md`) — query it with `graphify query`/`path`/`explain` instead of grepping.
- If a query surfaces something worth permanent record, hand-write it as a real note under `docs/` per `docs-vault` conventions (kebab-case, YAML `tags:`, `[[wikilinks]]`) and link it from `docs/Home.md` — don't promote raw graphify notes wholesale. See `graphify-vault` skill for full directives.

## Directives
- Prefer concise, modular documentation.
- Use `progressive disclosure`: summary first, deep dive in links.
- Keep `docs/` as the single source of truth.
