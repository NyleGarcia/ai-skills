---
name: graphify-docs-upgrade
description: Convert graphify's raw output (graphify-out/graph.json, GRAPH_REPORT.md, or the docs/knowledge Obsidian export) into curated docs/ vault notes, and detect + fix drift in existing docs/ notes against the current graph. Use when user says "convert graphify output to docs", "upgrade our docs from the graph", "turn the graph export into real docs", "sync docs with the codebase", or wants graphify findings promoted into docs/ instead of left as raw dump.
---

# Graphify Docs Upgrade

Promotion step between `graphify-vault` (builds/exports the graph) and `docs-vault` (this repo's `./docs` conventions). The raw `graphify-out/` and `docs/knowledge/` export are a regenerable per-symbol dump — thousands of notes, never committed. This skill is how select findings graduate into hand-written, permanent `docs/` content.

## Prerequisites

- Graph must exist and be current: `graphify-out/graph.json`. If missing or you suspect it's stale, run `graphify-vault` first (`graphify extract . --code-only --no-gitignore`; add `--obsidian` if you want the `docs/knowledge/` export too). `graphify hook install` (see `graphify-vault`) keeps this current automatically after every commit.
- Sanity-check per `graphify-vault`'s node-count / source-file-breakdown check before trusting the graph as source material — don't document a broken or self-eaten graph as fact.
- Follow `docs-vault` conventions for every note you write or touch: kebab-case filename, YAML frontmatter (`tags:`), `[[wikilinks]]`, a `docs/Home.md` line.
- Before treating any `graphify query`/`explain` result as "nothing here," run the vocab-expansion step from the installer-owned `/graphify` skill's `references/query.md`. The matcher is literal case-folded substring — no stemming, no synonyms — so a wording mismatch between your phrasing and the graph's own node labels looks identical to "genuinely not in the graph." Both modes below depend on this.

## Mode 1 — Convert (new docs from graph findings)

Use when `docs/` is thin or missing coverage the graph surfaces. Feed this from `graphify-docs-gaps`'s ranked output when available, or run ad hoc.

1. Pull scoped material, never the raw dump: `graphify explain "<concept>"`, `graphify query "<question>"`, `graphify path "<A>" "<B>"`, `graphify-out/wiki/index.md` (`graphify export wiki` per `graphify-vault`, if generated), or the God Nodes / Surprising Connections sections of `GRAPH_REPORT.md`.
2. Discount known noise before writing anything down (see `graphify-vault`'s "Reading results without being lied to"): test fixtures dominating fan-in rankings, prose lifted into node-shaped "symbols," empty `source_file` meaning an external/unresolved import, not dead code.
3. For each finding worth a permanent record (architecture, an implicit ADR, a cross-module relationship nobody had written down), draft one hand-written `docs/` note. Cite `source_location` from the graph, but write real prose — do not paste node/edge JSON or copy a `docs/knowledge/` note verbatim.
4. Wikilink related notes, add a `docs/Home.md` line. If a note cites a specific `docs/knowledge/` node for a reader who wants the raw detail, link it as a plain reference — don't move that file into `docs/`.

## Mode 2 — Upgrade (refresh existing docs against drift)

Use when code has changed and `docs/` notes may no longer match it.

1. Refresh the graph first: `graphify extract .` (or `--update` per `graphify-vault`'s refresh rules — never `graphify update .` once a `docs/knowledge/` export exists, it self-ingests).
2. For each `docs/` note describing a module, file, or concept, run `graphify explain "<that concept>"` (with vocab expansion per Prerequisites) and compare its current relationships/community/location against what the note claims.
3. Flag mismatches — renamed/moved files, a described relationship no longer present, a god-node that dropped out, a community split or merged. List drifted notes; don't silently rewrite. A miss on `explain` alone is not proof of drift until vocab-expanded — confirm before flagging.
4. Fix flagged notes per `docs-vault`'s update convention: append a dated finding rather than erasing history, unless the note is purely descriptive scaffolding with no history worth keeping (rewrite those directly).
5. If a note's whole subject no longer exists in the graph (file/module deleted), don't delete the note unprompted — surface it and ask.

## Guardrails

- Never bulk-copy or bulk-link `docs/knowledge/*.md` into `docs/` — that inverts the vault (curated vs. regenerable cache) and is exactly the mistake `graphify-vault` warns against.
- Every note this skill creates or edits gets a `docs/Home.md` line — no orphans.
- Stop and tell the user if the graph itself looks broken (implausible node count, `GRAPH HEALTH WARNING`, missing tree-sitter grammar) before drafting or upgrading anything from it.
- This skill never edits `graphify-out/` or `docs/knowledge/` — those stay regenerable, gitignored, hands-off.
