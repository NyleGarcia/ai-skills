---
name: graphify-docs-gaps
description: Scan the graphify knowledge graph to find god-nodes, communities, and architecturally significant code that has no corresponding docs/ coverage, then produce a ranked gap list for new-doc generation. Use when user says "find missing docs", "what's undocumented", "docs coverage gaps", "what should we document next", or wants a prioritized list handed off to graphify-docs-upgrade for drafting.
---

# Graphify Docs Gaps

Gap-finder that feeds `graphify-docs-upgrade`'s Convert mode. This skill only detects and ranks — it does not draft notes itself. Distinct from `graphify-docs-upgrade` Mode 2 (drift on *existing* notes): this is about concepts with **zero** docs/ coverage.

## Prerequisites

- Current `graphify-out/graph.json` — run `graphify-vault` first if missing or stale, same sanity-check (node count, source-file breakdown) before trusting it. `graphify hook install` (see `graphify-vault`) keeps it fresh automatically after every commit — worth having if this skill runs regularly.
- `docs/knowledge/` (the raw Obsidian export) does **not** count as coverage — it's the regenerable per-symbol cache. Only hand-written `docs/` notes (per `docs-vault` conventions) close a gap.
- Prefer `graphify-out/wiki/index.md` (`graphify export wiki`, see `graphify-vault`) over `GRAPH_REPORT.md` when it exists — one curated article per community, matches root `CLAUDE.md`'s own navigation preference and is a cleaner diff source than raw report snippets.

## Workflow

1. **Inventory existing coverage.** Scan `docs/` (excluding `docs/knowledge/`) for note titles, `[[wikilinks]]`, and symbol/file names mentioned in body text — `grep -rli` across `docs/*.md` and any subfolders that aren't the raw export.
2. **Inventory graph-significant concepts.** Pull from `graphify-out/wiki/index.md` if it exists (community articles), otherwise `GRAPH_REPORT.md` / `graphify god-nodes`: god-nodes, community labels, and any node in "Surprising Connections" or "Suggested Questions." A community only counts if it has enough members to be a real subsystem, not a stray cluster.
3. **Diff.** For each graph-significant concept, first fuzzy-match against the coverage inventory (filename slug, class/module name substring, wikilink target). For any concept that still looks uncovered, confirm with a live check before calling it a gap: run the vocab-expansion step from the installer-owned `/graphify` skill's `references/query.md`, then `graphify query "<concept>"` or `graphify explain "<concept>"` using expanded vocabulary — the raw matcher is literal substring with no stemming or synonyms, so a bare miss on your first-pass wording is not proof the concept is undocumented, only that the words didn't match.
4. **Discount false positives** per `graphify-vault`'s "Reading results without being lied to": test fixtures/helpers dominating fan-in, prose lifted into node-shaped "symbols," empty `source_file` (external/unresolved import — not undocumented code). Also skip trivial single-file utilities with no cross-file significance — same bar `graphify`'s "When NOT to use" applies.
5. **Rank.** God-nodes first, then large/cohesive communities, then surprising-connection bridge nodes, then everything else. For each gap, one line: concept name, why it matters (e.g. "god-node, N incoming edges" / "community of M nodes, no note"), suggested doc shape (architecture note, reference, ADR-style decision record).
6. **Report, don't draft.** Present the ranked list to the user. Do not create any `docs/` notes from this skill directly — hand off selected gaps to `graphify-docs-upgrade` Mode 1 (Convert) once the user picks which ones to fill. Drafting a dozen notes unprompted is worse than a short list they can triage.

## Guardrails

- Never count `docs/knowledge/*.md` toward coverage — that inverts curated vs. regenerable, same mistake `graphify-docs-upgrade` guards against.
- Never call something a gap off a single raw-substring miss — run vocab expansion first (Step 3). A wording mismatch is not the same as missing documentation.
- Stop and say so, don't report gaps, if the graph looks broken (implausible node count, `GRAPH HEALTH WARNING`, missing tree-sitter grammar) — a gap list from a corrupt graph is worse than none.
- If `docs/` doesn't exist yet, that's not a bug — the whole god-node list is the gap list; say so plainly instead of grepping an empty directory repeatedly.
