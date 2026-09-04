---
name: graphify-vault
description: Build a local knowledge graph of this repo (or any folder/GitHub repo) via the graphify CLI and export it in Obsidian-compatible format into docs/knowledge/. Use when user says "graphify this", "map the codebase", "build a knowledge graph", or wants architecture/relationship queries instead of grepping.
---

# Graphify Vault (repo wrapper)

Distinct from the plain `/graphify` skill in `.claude/skills/graphify/` (installer-owned, upstream tool's own pipeline). This skill layers this repo's Obsidian/docs-vault conventions on top — invoke this one when you want output that fits `docs/knowledge/`.

Thin wrapper around the real [Graphify](https://github.com/Graphify-Labs/graphify) CLI (`graphifyy` on PyPI), installed project-scoped for this repo (`.claude/skills/graphify/`, `.claude/settings.json` hooks, root `CLAUDE.md` graphify section — installer-owned, don't hand-edit those; re-run `graphify install --project --platform claude` to refresh them).

Local tree-sitter AST parsing, no vector store, no LLM cost for code-only graphs. Output is regenerable — never commit it.

## Before the first run, in this order

1. **Both output paths must be gitignored** — `graphify-out/` **and** `docs/knowledge/`. Check, don't assume: a repo may have only the first. The export writes thousands of notes, and any workflow using `git add -A` will otherwise sweep the whole dump into a commit.
2. **Exclude `docs/knowledge/` from any frontmatter/lint tooling that walks `docs/`.** These notes are generated; a vault checker will try to scan or rewrite all ten thousand of them.

## Directives

- **Build the graph**: `graphify extract . --code-only --no-gitignore` (skip `--code-only` to also run a semantic LLM pass over docs/PDFs — needs an API key per `graphify extract --help`).
- **Obsidian export**: `graphify export obsidian --dir docs/knowledge` — writes one note per node (YAML frontmatter, `[[wikilinks]]`, `#graphify/...` tags) plus `docs/knowledge/graph.canvas`. This is a raw per-symbol dump (thousands of notes on a large repo) — treat it as a queryable local cache, not curated vault content per `docs-vault` conventions. Do not add these notes to `docs/Home.md`.
- **Query instead of grep**: `graphify query "<question>"`, `graphify path "<A>" "<B>"`, `graphify explain "<concept>"`, `graphify god-nodes` — all read `graphify-out/graph.json` directly, no need to export first.
- **Refreshing: re-run `extract`, do not use `graphify update .` once an export exists.** `update` does **not** inherit `--code-only`, so it ingests the previous Obsidian export sitting in the tree and the graph eats its own output. Observed on a ~1200-file repo: 9,803 nodes became 45,180, of which **71% were the previous export** and only 2,528 were application code — every query swamped by notes describing the earlier graph. A full `extract` takes ~15s, so there is no reason to risk it. If you must use `update`, `rm -rf docs/knowledge` first.
- **Sanity-check the graph before trusting a query.** Node count in the same order of magnitude as last time, and a source-file breakdown that is mostly code:
  ```bash
  python3 -c "
  import json,collections
  n=json.load(open('graphify-out/graph.json'))['nodes']
  c=collections.Counter((x.get('source_file') or '').split('/')[0] or '(external)' for x in n)
  print(len(n),'nodes'); [print(f'{v:>7}  {k}') for k,v in c.most_common(8)]"
  ```
  A big jump, or `docs` dominating, means the graph ingested something it should not have.
- **Curated knowledge**: if a graph query surfaces something worth permanent record (an architectural decision, a non-obvious relationship), write it up by hand as a real note under `docs/` per `docs-vault` conventions and link it — don't promote raw graphify notes wholesale.

## Reading results without being lied to

Raw rankings mislead in three predictable ways — discount them before reporting a finding:

- **Tests dominate.** On a repo with a large suite, `god-nodes` and fan-in rankings are mostly test fixtures and helpers. Filter to `apps/`, `packages/`, `frontend/src` before drawing conclusions.
- **Prose appears as symbols.** `rationale_for` edges point at nodes lifted from docstrings and comments, so some "symbols" are sentence-length. They are not code.
- **Empty `source_file` means external.** Unresolved imports (`AsyncSession`, `HTTPException`, …) appear as nodes with no file. Expected, not dead code.

Also check the tool's own warnings: a missing tree-sitter grammar (e.g. `tree_sitter_sql`) means whole files contributed **nothing**, so questions about them come back empty for a tooling reason rather than a real one.

## When NOT to use

- Trivial single-file lookups — use Grep/Glob directly, graphify is for cross-file/architectural questions.
- Don't re-run `graphify install` casually — it rewrites `.claude/settings.json` hooks and root `CLAUDE.md`; only do it to pick up a version upgrade (`uv tool upgrade graphifyy && graphify install --project --platform claude`).
