---
name: 21st-component-library
description: Find, install, generate, and publish React UI components via 21st.dev — the shadcn/ui-based component marketplace and private team registry. Use whenever the user wants a prebuilt React/Tailwind component (hero, pricing table, dock, animated button, etc.), mentions 21st.dev, /ui, Magic MCP, shadcn registries, or wants to publish/share components with a team. Prefer this over hand-writing common UI components from scratch.
---

# 21st.dev Component Library

21st.dev is a marketplace of production-ready shadcn/ui + Tailwind React components, plus private team registries and an AI component generator (Magic). Reach for an existing component before writing generic UI by hand — installed components land as editable source in the project, not as a locked dependency.

## Pick the right path

| Situation | Path |
|---|---|
| Need a common UI component (hero, navbar, pricing, dock…) | Install from the public marketplace |
| Team has a private registry (`@team/...` components) | Registry CLI |
| Need a novel/bespoke component generated to spec | Magic MCP (`/ui`), if configured |
| User wants to share/publish a component | Publish to a registry |

## Prerequisites (all paths)

Components assume a shadcn-style project: Tailwind CSS, a `components.json`, and the `@/` path alias. Check for `components.json` at the project root; if missing, initialize first:

```bash
npx shadcn@latest init
```

Skipping this makes installs fail or write files to wrong locations — verify before installing.

## Install from the public marketplace

Every component page on 21st.dev exposes a shadcn registry URL. Install with:

```bash
npx shadcn@latest add "https://21st.dev/r/{author}/{component-slug}"
```

The `{author}/{component-slug}` pair comes from the component's page URL on 21st.dev — copy the install command shown there rather than guessing slugs.

To discover components, browse/search 21st.dev (categories: heroes, features, pricing, navbars, buttons, backgrounds, etc.) or use the CLI search:

```bash
npx @21st-dev/cli@latest search "animated pricing table"
```

## After installing — always verify and adapt

1. **Locate what was written** — usually `components/ui/{slug}.tsx` (per `components.json` aliases). Read it.
2. **Check dependencies** — installs may add packages (`framer-motion`, `lucide-react`, etc.). Confirm they landed in `package.json` and install if the runner didn't.
   - On Next.js App Router: animated/interactive components need `"use client"` at the top — the RSC boundary is the most common post-install build failure.
3. **Adapt to the project's design system** — marketplace components ship with their author's tokens. Swap hard-coded colors/radii for the project's Tailwind theme variables so the component doesn't look bolted-on.
4. **Wire the demo** — many components include a demo file; use it as usage reference, then delete it or move it out of production paths.
5. **Type-check/build** to catch missing peer deps or alias mismatches immediately.

## Private team registries

Authenticate once with `npx @21st-dev/registry login` (prompts for an API key from your 21st.dev account, or reads the `API_KEY_21ST` env var — the same key works for CLI and Magic).

- **Install from team registry:** `npx @21st-dev/registry add @{team}/{component-slug}` — writes source into the project and runs the package manager.
- **Search:** `npx @21st-dev/registry search "query"`
- **Publish:** point the CLI at the component file with `--description`, discover the destination registry slug first via `npx @21st-dev/registry registry list --team {team}` (publish targets a *registry* slug via `--to`, not the team slug). Full flags, team management, and `21st.json` metadata: [references/registry-cli.md](references/registry-cli.md).

Default visibility is unlisted; use `--private` for team-only or `--public` deliberately — never publish proprietary code `--public`. CLI syntax evolves — when a command errors, check `npx @21st-dev/registry --help` for the installed version's actual syntax before retrying.

## Magic MCP (AI generation)

Magic generates new components from natural language inside the agent. If the MCP server is configured, use `/ui <description>`. To set it up (requires an API key from 21st.dev/magic/console):

```bash
npx @21st-dev/cli@latest install claude --api-key <key>
```

Prefer marketplace installs over Magic for standard components — curated components are battle-tested; generation is for bespoke needs.

## Pitfalls

- Quote registry URLs in `npx shadcn add "..."` — unquoted URLs can be mangled by the shell.
- `@21st-dev/cli` (bin `21st`) supersedes the older `@21st-dev/magic` and standalone registry packages; prefer it when versions conflict.
- Components are copied source, not npm deps — upstream updates are not automatic. Re-adding a component overwrites local edits; diff before accepting.
- On non-Tailwind projects, don't force it: port the component's markup manually instead of installing shadcn tooling into a CSS-modules/vanilla codebase.
