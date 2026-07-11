# Original User Request

## Initial Request — 2026-07-05T10:38:23-05:00

Cleanup and consolidate Antigravity skills and plugins in global config. Integrate learnings, new skills, and rules from `/Users/nylegarcia/git/SC-ORG-BOT` and `/Users/nylegarcia/git/dumpers_repo`.

Working directory: /Users/nylegarcia/.gemini/config
Integrity mode: development

## Requirements

### R1. Deduplicate and Categorize
Analyze the global config skills and plugins. Deduplicate any overlapping skills and categorize them logically into plugins.

### R2. Standardize Formatting
Standardize all `SKILL.md` files across the global config to ensure they have valid YAML frontmatter (name, description) and consistent markdown formatting.

### R3. Integrate Learnings
Analyze skills and rules in `/Users/nylegarcia/git/SC-ORG-BOT` and `/Users/nylegarcia/git/dumpers_repo`. Integrate useful learnings, patterns, or entirely new skills into the global config. The agent team should decide the best approach (merge vs. new) based on overlap.

### R4. Antigravity Conformity
Ensure all changes strictly conform to the official Antigravity documentation for skills, rules/workflows, and plugins:
- https://antigravity.google/docs/skills
- https://antigravity.google/docs/rules-workflows
- https://antigravity.google/docs/plugins

## Acceptance Criteria

### Formatting & Structure
- [ ] A script or manual check verifies that every `SKILL.md` in the config contains valid YAML frontmatter (`name` and `description`).
- [ ] No identically purposed skills exist in the global config (deduplication is complete).
- [ ] Folder structures and file formats match exactly what is specified in the Antigravity documentation URLs provided.

### Integration
- [ ] The global config contains identifiable concepts, rules, or skills extracted from `SC-ORG-BOT` and `dumpers_repo`.

## Follow-up — 2026-07-05T15:45:07Z

New user requirement added mid-flight: Ensure that `install.sh` is updated at the end to make sure everything is installed fine.

## Follow-up — 2026-07-05T15:51:50Z

New user requirements added mid-flight:
1. Ensure that the `ralph-loop` plugin/skill uses `teamwork-preview` and vice versa (integrate them).
2. Look into how to make sure the skills are secure and scanned to make sure they don't have any prompt poisoning or issues.
