---
name: graphify-vault
description: Build a local knowledge graph of this repo (or any folder/GitHub repo) via the graphify CLI and export it in Obsidian-compatible format into docs/knowledge/. Use when user says "graphify this", "map the codebase", "build a knowledge graph", or wants architecture/relationship queries instead of grepping.
---

# Graphify Vault (repo wrapper)

Distinct from the plain `/graphify` skill in `.claude/skills/graphify/` (installer-owned, upstream tool's own pipeline). This skill layers this repo's Obsidian/docs-vault conventions on top — invoke this one when you want output that fits `docs/knowledge/`.

Thin wrapper around the real [Graphify](https://github.com/Graphify-Labs/graphify) CLI (`graphifyy` on PyPI), installed project-scoped for this repo (`.claude/skills/graphify/`, `.claude/settings.json` hooks, root `CLAUDE.md` graphify section — installer-owned, don't hand-edit those; re-run `graphify install --project --platform claude` to refresh them).

Local tree-sitter AST parsing, no vector store, no LLM cost for code-only graphs. Output is regenerable — never commit it (see `.gitignore`: `graphify-out/`, `docs/knowledge/`).

## Directives

- **Build/refresh the graph**: `graphify extract . --code-only --no-gitignore` (skip `--code-only` to also run a semantic LLM pass over docs/PDFs — needs an API key per `graphify extract --help`).
- **Obsidian export**: `graphify export obsidian --dir docs/knowledge` — writes one note per node (YAML frontmatter, `[[wikilinks]]`, `#graphify/...` tags) plus `docs/knowledge/graph.canvas`. This is a raw per-symbol dump (thousands of notes on a large repo) — treat it as a queryable local cache, not curated vault content per `docs-vault` conventions. Do not add these notes to `docs/Home.md`.
- **Query instead of grep**: `graphify query "<question>"`, `graphify path "<A>" "<B>"`, `graphify explain "<concept>"`, `graphify god-nodes` — all read `graphify-out/graph.json` directly, no need to export first.
- **Keep it current**: after code changes, `graphify update .` (AST-only, no LLM cost) before querying again.
- **Curated knowledge**: if a graph query surfaces something worth permanent record (an architectural decision, a non-obvious relationship), write it up by hand as a real note under `docs/` per `docs-vault` conventions and link it — don't promote raw graphify notes wholesale.

## When NOT to use

- Trivial single-file lookups — use Grep/Glob directly, graphify is for cross-file/architectural questions.
- Don't re-run `graphify install` casually — it rewrites `.claude/settings.json` hooks and root `CLAUDE.md`; only do it to pick up a version upgrade (`uv tool upgrade graphifyy && graphify install --project --platform claude`).
