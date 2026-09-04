---
name: docs-vault
description: Maintain ~/docs — the Obsidian-compatible reference vault for system Linux things (OS tuning, customization, diagnostics, gaming setup, machine/work env, handoffs, memories); ALL repo-level docs go in that repo's ./docs instead. Covers correct Obsidian frontmatter/linking format for both vaults — generated frontmatter, wikilink policy, basename collisions. Use when writing or updating setup docs, fix writeups, handoffs, when a system fix lands, or when creating/linking any note in either vault.
---

# Docs Vault (~/docs and ./docs)

Immutable-ish reference of **current production state**. Repo WIP lives in that repo's `docs/plans/`; when work ships, truth lands in a vault — `~/docs` for system-level, `./docs` for repo-level.

Distinct from `obsidian-vault` skill (the personal "AI Research" vault on Mac/WSL — pure Obsidian, no GitHub/mkdocs dual-rendering constraint, so its wikilink-everywhere convention is correct *for that vault* and not copied here).

## Scope: ~/docs vs ./docs

- **`~/docs` (system vault):** OS tuning, customization, diagnostics, driver/boot/network fixes, gaming setup, machine setup, work env, cross-project handoffs, notes, memories. Anything that outlives or spans repos.
- **`./docs` (repo vault):** ALL repo-level things — architecture, ADRs (`docs/decisions/`), API docs, AND plans/specs (`docs/plans/{now,next,later,specs}/`). Lives with the repo, NOT in `~/docs`.
- Rule of thumb: would it matter after `rm -rf` of the repo? Yes → `~/docs`. No → `./docs`.
- Per-repo `./docs` may still get a pointer note in `~/docs/projects/<name>/` (handoffs, machine-specific config) — link, don't duplicate.

Both are Obsidian-compatible vaults but diverge on two things: `~/docs` is personal/private and free to use wikilinks in body text; `./docs` renders on GitHub and often mkdocs/a GitHub wiki too, so it follows the stricter linking policy below.

## ~/docs Structure (system vault)

```
~/docs/
  Home.md                 # master index — wikilinks to every note
  system/                 # OS, boot, drivers, network fixes (zedpc/CachyOS)
    cachyos-migration/    # migration scripts + config dumps (assets, not notes)
  work/                   # work env (VDI, distrobox)
  projects/<name>/        # per-project handoffs + machine-config archives
  gaming/<game>/          # game setup notes + config assets
```

- **Filenames:** kebab-case, descriptive, `.md`.
- **Frontmatter:** hand-written YAML with `tags:` (e.g. `[system, nvidia]`). `Home.md` carries `tags: [index]`.
- **Note format:** `# Title (host, context)` then `**Date:**` / `**Symptom:**` header lines, `## Root cause`, `## Fix` (complete commands in fenced blocks), `## Notes`. See `system/networkmanager-connectivity-check-fix.md` as template.
- **Wikilinks:** `[[basename-without-extension]]`, used freely in body text (`## Notes` / a `Related:` line) — this vault has no GitHub-rendering constraint to protect.
- **Assets** (scripts, cfg, tarballs, dirs): live beside their note in the same folder; reference by relative path, plain backticks not wikilinks.
- Legacy notes may lack frontmatter — add it when touching a note, don't mass-migrate.

## ./docs Structure (repo vault)

```
docs/
  Home.md                 # vault-native index — one wikilink per note, grouped by area
  README.md                # plain-markdown index, same notes — GitHub/mkdocs-safe
  changelog.md
  decisions/               # ADR-worthy calls — vault conventions, not a bare ADR-NNN template
  plans/
    README.md               # index for this dir specifically — both link forms (see below)
    now/todo.md              # active sprint
    next/backlog.md          # confirmed backlog
    later/ideas.md           # ice box
    specs/<slug>.md           # implementation specs, status: draft|active|done frontmatter
  <topic>/...               # truth notes, organized by area once the flat list gets big
    audits/                  # one-off dated reports (security, perf, codebase) — never at repo root
    history/                 # origin story, retired one-off changelogs
```

- **Filenames:** kebab-case. Existing non-kebab names get renamed incrementally when touched, not en masse (mass renames churn links across in-flight branches).
- **`docs/plans/specs/<slug>.md` uses `status:` frontmatter (`draft`/`active`/`done`), never a file move or deletion at closeout** — a spec stays where inbound wikilinks expect it, permanently queryable by status. (Real-world note: "delete the spec after merge" sounds tidy but doesn't survive contact with multi-phase features — status frontmatter is the version that actually holds up.)
- **`docs/decisions/` ADRs follow the same vault conventions as everything else** — kebab-case slug, frontmatter, wikilinks, a `Home.md` line — not a separate bare sequential-numbering scheme.
- **Optional three-tier split**, once a repo has real end users, not just engineers/agents reading it: `docs/` (internal, this vault) for engineering truth, `docs/public/` for a polished end-user site (mkdocs, custom domain), `docs/wiki/` for a GitHub wiki mirror. Skip this for a repo with no external audience — one tier is enough.
- **`docs/plans/now/todo.md` item format:** the primary link is to whatever tracks the work (a GitHub issue, if the repo uses `gh`) — not every item needs a spec. Add a spec wikilink only once a spec actually exists for that item: `- [ ] <task> ([#123](issue-url)) — [[specs/<slug>]]` when there's a spec, `- [ ] <task> ([#123](issue-url))` when there isn't. Never invent a spec link for an item that doesn't have one yet.

### Frontmatter: generated, not hand-written

Hand-writing frontmatter drifts (tags forgotten, dates stale). Generate it instead: `skills/docs-vault/scripts/obsidian_frontmatter.py` (stdlib-only, copy into the repo's own `scripts/`) prepends a three-key block to any eligible `docs/**/*.md` that doesn't already have one:

```yaml
---
title: Voice presence (the Redis mirror of Discord voice state)
tags: [docs, internal, architecture]
updated: 2026-09-02
---
```

- `title` — the file's first `# ` heading, verbatim; no heading → the filename, title-cased.
- `tags` — path segments above the file, lowercased: `docs/internal/ui/theming.md` → `[docs, internal, ui]`. Zero manual tagging; `#architecture` in Obsidian pulls every architecture note for free.
- `updated` — `git log -1 --format=%cs -- <file>` (untracked file → its mtime). Written **once** — the script never rewrites an existing block, so this field does not track later edits. Bump it by hand for a substantial rewrite; leave it for typo fixes.

Write the note body first, with no frontmatter — run `uv run python scripts/obsidian_frontmatter.py` (add `--check` as a CI/pre-commit gate, `--verbose` to see every file's outcome). It never touches a body and never touches an existing frontmatter block, so hand-tuned frontmatter (e.g. mkdocs `hide:` keys) survives. Excluded by default: `docs/wiki/**` (GitHub's wiki renderer prints frontmatter as literal page text) and `docs/knowledge/**` (the gitignored `graphify-vault` export — a regenerable cache, never vault content).

### Wikilinks: index-only, always paired with a plain link

Existing relative markdown links (`[api.md](../reference/api.md)`) are **never** rewritten into wikilinks — GitHub, mkdocs, and every agent reading raw markdown depend on them rendering as real links. Wikilinks appear **only in index notes** (`Home.md`, `plans/README.md`, any other note whose whole job is "list of related notes"), and always sit beside a plain link, not instead of one:

```markdown
- [[voice-hubs-lifecycle-spec]] — ([open](plans/specs/voice-hubs-lifecycle-spec.md)) — one-line hook
```

Body prose in every other note stays plain-markdown links only. Writing a bare `[[wikilink]]` inside body prose of a non-index note is the single most common mistake here — it looks fine in Obsidian and renders as literal broken text everywhere else.

**Basename collisions are real** — the same slug can exist under `specs/` and under a topic folder (e.g. `temp-voice-channels.md` in both `plans/specs/` and `internal/architecture/`). A bare `[[temp-voice-channels]]` is ambiguous; Obsidian may resolve it to either file. Before adding any wikilink, check the basename is unique:

```bash
find docs -name '<basename>.md' -not -path 'docs/wiki/*'
```

If it isn't, path-qualify enough of the path to disambiguate: `[[specs/temp-voice-channels]]` vs `[[architecture/temp-voice-channels]]`.

### Dual index

Maintain both, not one:

- **`docs/Home.md`** — vault-native index, wikilink per note, grouped by area. What Obsidian's graph/quick-switcher actually use.
- **`docs/README.md`** — plain-markdown structured index, same notes, one-line hook each. What renders on GitHub's repo landing.

Update both whenever a doc is added, moved, or renamed. `docs/plans/README.md` is the same pattern applied to just the plans dir — an index note with both link forms per entry, per the format above.

### Obsidian vault settings (first open)

1. **Open folder as vault** → repo root (or just `docs/`).
2. Settings → **Files & Links**: *New link format* → **Relative path to file**; turn **Use [[Wikilinks]]** OFF. Ad hoc edits made inside Obsidian then stay GitHub-compatible by default instead of silently inserting wikilinks into body prose.
3. Settings → **Files & Links** → *Excluded files*: add `node_modules`, `frontend`, `.venv` (or repo equivalents) so the graph isn't noise.
4. `.obsidian/` (per-vault config, created on first open) is personal workspace state — gitignore it (`**/.obsidian/`), never commit it.

## Workflows

### Add a new doc

1. **`~/docs`:** pick folder by domain (`system/`, `work/`, `projects/<name>/`, `gaming/<game>/`); create a subfolder if new. Write frontmatter by hand.
   **`./docs`:** pick the right area (or `docs/plans/specs/` for a spec, `docs/decisions/` for an ADR). Write the note with **no** frontmatter — run the generator script after.
2. Write note per the conventions above. Date in `YYYY-MM-DD`.
3. Cross-link related notes with plain links in body prose. If this note is itself an index, add wikilink+plain-link pairs.
4. **Always add a line to `Home.md`** (and, for `./docs`, `README.md`) under the matching section: `- [[note-name]] — one-line hook`.

### Update existing doc

1. Search first: `grep -rli "keyword" <vault-root> --include='*.md'` — extend an existing note over creating a near-duplicate.
2. Append dated findings ("Happened in practice: ..."), don't rewrite history.
3. If moved/renamed, fix `Home.md`/`README.md` and inbound links: `grep -rl '\[\[old-name\]\]\|old-name\.md' <vault-root>`.

### Restructuring the vault itself

When the plans/vault structure changes (a scheme retired, a horizon renamed), leave a dated callout at the top of the affected index note explaining what changed and why, rather than silently altering structure — future readers (and agents) need to know a `[[wikilink]]` pointing at the old scheme isn't stale, it's historical.

### Obsidian MCP (preferred when available)

`obsidian` MCP server registers vaults by id — check with `obsidian_list_vaults` (or `claude mcp list`). Current ids: `home` = `~/docs`; repo `./docs` vaults registered per-repo (e.g. `sc-org-bot`, `openwave`, `tobii-linux`). Paths in tool calls are vault-relative.

- **Search:** `obsidian_search_vault` (content + filename) over `grep -rli`.
- **Read/create/edit:** `obsidian_read_note` → `obsidian_create_note` / `obsidian_edit_note`. Read first, pass etag when editing — guards concurrent Obsidian edits.
- **Move/rename:** `obsidian_move_note` — still fix `Home.md`/`README.md` + inbound links yourself.
- **Tags:** `obsidian_add_tags` / `obsidian_manage_tags` for frontmatter `tags:` instead of hand-editing YAML (`~/docs`; for `./docs`, prefer the generator script over either).
- Destructive ops journaled under `.obsidian-mcp/`.
- **Fallback:** `mcp__obsidian__*` tools not present (server not installed/connected), vault unregistered, or tool call errors → work files directly (Read/Write/Edit/Grep on the path), same conventions, no asking, no retry loop. New repo vault worth registering → add `--vault name=/path/docs` to `obsidian` server args in `~/.claude.json`.

### Obsidian plugin integration

`~/docs` ships with `claude-code-skills` plugin (v1.0.5, github.com/p3nguln5/obsidian-claude-code-skills) preinstalled in `.obsidian/plugins/` — highlight text → right-click → invoke Claude Code skill, streamed to sidebar. Requires `claude` CLI on PATH; desktop only. First open: "Open folder as vault" on `~/docs`, turn off restricted mode.

### Versioning & backup

- `~/docs` is a git repo → `github.com/NyleGarcia/docs` (private). **Commit + push after any note change** — plain messages like `docs: <what>`.
- `.gitignore` excludes bulky assets (`*.tar.gz`, `*.zip`, `gaming/star-citizen/user/`, `.obsidian/workspace*`, `.tmp/`, `scratch/`). Those survive only via Drive sync — reference them in notes anyway.
- Backup: one-way hourly rclone sync `~/docs` → `gdrive:linux/` (systemd user timer `gdrive-sync.timer`; local is source of truth, remote deletions trashed 30 days). See [[google-drive-rclone-setup]].

### Sync with agent memory

Facts worth cross-session recall get BOTH: full writeup here, compressed pointer in Claude memory (`~/.claude/projects/-home-zedwil/memory/`). Memory links doc via path; doc stands alone.
