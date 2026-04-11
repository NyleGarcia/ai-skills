---
name: caveman-compress
description: Compress prose in memory files to save tokens while preserving all technical data, headings, and code blocks.
---
# caveman-compress

🪨 Compress memory files. Claude read less.

## Instructions

When asked to compress a file (e.g., `CLAUDE.md`), rewrite its prose into Caveman style while preserving all technical data (code, URLs, paths, commands).

### Workflow

1. Read target file.
2. Create backup: `filename.original.md`.
3. Rewrite target file:
   - Keep headings, lists, and code blocks.
   - Compress all prose using Caveman principles.
   - Keep technical identifiers exactly as-is.
4. Report token savings.

### Example

**Original:** "The project uses a microservices architecture where the authentication service is responsible for issuing JWT tokens."
**Compressed:** "Project use microservices. Auth service issue JWT."
