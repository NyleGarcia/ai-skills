---
name: obsidian-vault
description: Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian.
---

# Obsidian Vault

## Vault location

- **Darwin (Mac)**: `~/Documents/Obsidian Vault/AI Research/` (Verify if exists)
- **Windows (WSL)**: `/mnt/d/Obsidian Vault/AI Research/`
- **Default**: Search for `AI Research` folder if not found.

Mostly flat at root level.

## Naming conventions

- **Index notes**: aggregate related topics (e.g., `Ralph Wiggum Index.md`, `Skills Index.md`, `RAG Index.md`)
- **Title case** for all note names
- No folders for organization - use links and index notes instead

## Linking

- Use Obsidian `[[wikilinks]]` syntax: `[[Note Title]]`
- Notes link to dependencies/related notes at the bottom
- Index notes are just lists of `[[wikilinks]]`

## Obsidian MCP (preferred when available)

If `obsidian` MCP server connected, check `obsidian_list_vaults` for registered vault ids and use MCP tools instead of raw file ops (paths vault-relative):

- **Search:** `obsidian_search_vault` — content + filename, replaces find/grep below.
- **Read/create/edit:** `obsidian_read_note`, `obsidian_create_note`, `obsidian_edit_note` (read first, pass etag on edit — guards concurrent Obsidian edits).
- **Move/rename/tags:** `obsidian_move_note`, `obsidian_add_tags`, `obsidian_manage_tags`.
- Destructive ops journaled under `.obsidian-mcp/`.

**Fallback:** `mcp__obsidian__*` tools not present (server not installed/connected), this vault (`AI Research`) not registered, or tool call errors → use filesystem workflows below directly (Read/Write/Grep on vault path), no asking, no retry loop. On Linux boxes, `~/docs` + repo `./docs` vaults belong to `docs-vault` skill, not this one.

## Workflows (filesystem fallback)

### Search for notes

```bash
# Search by filename
find "/mnt/d/Obsidian Vault/AI Research/" -name "*.md" | grep -i "keyword"

# Search by content
grep -rl "keyword" "/mnt/d/Obsidian Vault/AI Research/" --include="*.md"
```

Or use Grep/Glob tools directly on the vault path.

### Create a new note

1. Use **Title Case** for filename
2. Write content as a unit of learning (per vault rules)
3. Add `[[wikilinks]]` to related notes at the bottom
4. If part of a numbered sequence, use the hierarchical numbering scheme

### Find related notes

Search for `[[Note Title]]` across the vault to find backlinks:

```bash
grep -rl "\\[\\[Note Title\\]\\]" "/mnt/d/Obsidian Vault/AI Research/"
```

### Find index notes

```bash
find "/mnt/d/Obsidian Vault/AI Research/" -name "*Index*"
```
