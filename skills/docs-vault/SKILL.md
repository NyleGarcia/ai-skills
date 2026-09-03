---
name: docs-vault
description: Maintain ~/docs — the Obsidian-compatible reference vault for system Linux things (OS tuning, customization, diagnostics, gaming setup, machine/work env, handoffs, memories); ALL repo-level docs go in that repo's ./docs instead. Use when writing or updating setup docs, fix writeups, handoffs, or when user says "add to docs", "document this", or a system fix lands.
---

# Docs Vault (~/docs)

Immutable-ish reference of **current production state** on this machine. Repo WIP lives in that repo's `docs/plans/`; when system-level work ships, truth lands here.

Distinct from `obsidian-vault` skill (AI Research vault on Mac/WSL). This vault is local `~/docs` on Linux boxes.

## Scope: ~/docs vs ./docs

- **`~/docs` (this vault):** system Linux things — OS tuning, customization, diagnostics, driver/boot/network fixes, gaming setup, machine setup, work env, cross-project handoffs, notes, memories. Anything that outlives or spans repos.
- **`./docs` (inside a git repo):** ALL repo-level things — application architecture, ADRs, API docs, AND plans/specs (`docs/plans/{now,next,later,specs}/`). Lives with the repo, NOT in this vault.
- **`./docs` is itself an Obsidian-compatible mini-vault:** same conventions as `~/docs` — kebab-case `.md` filenames, YAML frontmatter with `tags:`, wikilinks `[[note-name]]`, assets beside notes, and a `docs/Home.md` master index updated on every add/move/rename.
- Rule of thumb: would it matter after `rm -rf` of the repo? Yes → `~/docs`. No → `./docs`.
- Per-repo `./docs` may still get a pointer note in `~/docs/projects/<name>/` (handoffs, machine-specific config) — link, don't duplicate.

## Structure

```
~/docs/
  Home.md                 # master index — wikilinks to every note
  system/                 # OS, boot, drivers, network fixes (zedpc/CachyOS)
    cachyos-migration/    # migration scripts + config dumps (assets, not notes)
  work/                   # work env (VDI, distrobox)
  projects/<name>/        # per-project handoffs + machine-config archives
  gaming/<game>/          # game setup notes + config assets
```

## Conventions

- **Filenames:** kebab-case, descriptive, `.md` (terminal-friendly; Obsidian resolves wikilinks by basename regardless of folder).
- **Frontmatter:** YAML with `tags:` (e.g. `[system, nvidia]`). `Home.md` carries `tags: [index]`.
- **Note format:** `# Title (host, context)` then `**Date:**` / `**Symptom:**` header lines, `## Root cause`, `## Fix` (complete commands in fenced blocks), `## Notes`. See `system/networkmanager-connectivity-check-fix.md` as template.
- **Wikilinks:** `[[basename-without-extension]]`. Cross-link related notes in `## Notes` or a `Related:` line at bottom.
- **Assets** (scripts, cfg, tarballs, dirs): live beside their note in the same folder; reference by relative path in the note, plain backticks not wikilinks.
- Legacy notes may lack frontmatter — add it when touching a note, don't mass-migrate.

## Workflows

### Add a new doc

1. Pick folder by domain (`system/`, `work/`, `projects/<name>/`, `gaming/<game>/`). Create subfolder if new project/game.
2. Write note per conventions above. Date in `YYYY-MM-DD`.
3. Add wikilinks to related notes; update those notes' `Related:` lines if strongly coupled.
4. **Always add a line to `Home.md`** under the matching section: `- [[note-name]] — one-line hook`.

### Update existing doc

1. Search first: `grep -rli "keyword" ~/docs --include='*.md'` — extend existing note over creating near-duplicate.
2. Append dated findings ("Happened in practice: ..."), don't rewrite history.
3. If moved/renamed, fix `Home.md` and inbound wikilinks: `grep -rl '\[\[old-name\]\]' ~/docs`.

### Obsidian integration

Vault ships with `claude-code-skills` plugin (v1.0.5, github.com/p3nguln5/obsidian-claude-code-skills) preinstalled in `.obsidian/plugins/` — highlight text → right-click → invoke Claude Code skill, streamed to sidebar. Requires `claude` CLI on PATH; desktop only. First open: "Open folder as vault" on `~/docs`, turn off restricted mode.

### Versioning & backup

- Vault is a git repo → `github.com/NyleGarcia/docs` (private). **Commit + push after any note change** — plain messages like `docs: <what>`.
- `.gitignore` excludes bulky assets (`*.tar.gz`, `*.zip`, `gaming/star-citizen/user/`, `.obsidian/workspace*`, `.tmp/`, `scratch/`). Those survive only via Drive sync — reference them in notes anyway.
- Backup: one-way hourly rclone sync `~/docs` → `gdrive:linux/` (systemd user timer `gdrive-sync.timer`; local is source of truth, remote deletions trashed 30 days). See [[google-drive-rclone-setup]].

### Sync with agent memory

Facts worth cross-session recall get BOTH: full writeup here, compressed pointer in Claude memory (`~/.claude/projects/-home-zedwil/memory/`). Memory links doc via path; doc stands alone.
