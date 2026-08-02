# 21st.dev Registry CLI Reference

Full command reference for `@21st-dev/registry` (team/private registry workflows). Read this when publishing non-interactively, managing teams/registries, or authoring `21st.json`.

## Authentication

```bash
npx @21st-dev/registry login
```

Reads the API key from the `API_KEY_21ST` environment variable or previously stored credentials. Get a key from your 21st.dev account settings.

## Publishing

Interactive (prompts for metadata):

```bash
npx @21st-dev/registry ./Button.tsx --description "Animated primary button"
```

Non-interactive (CI or scripted publishing):

```bash
npx @21st-dev/registry ./component.tsx \
  --name "Component Name" \
  --description "What it is and when to use it" \
  --registry ui \
  --tags "buttons,animation" \
  --demo ./demos/default.tsx \
  --preview ./preview.png \
  --to registry-slug \
  --private
```

Visibility flags: `--unlisted` (default), `--public`, `--private`.

The CLI rewrites relative demo imports to the `@/components/ui/{slug}` alias automatically — author demos with relative imports and let it rewrite them.

## Component metadata: `21st.json`

Place a `21st.json` next to the component to make publishes repeatable:

```json
{
  "name": "Fancy Button",
  "description": "Animated primary button with loading state",
  "registry": "ui",
  "tags": ["buttons", "animation"],
  "visibility": "private",
  "component": "./fancy-button.tsx",
  "demos": [{ "name": "default", "path": "./demos/default.tsx" }]
}
```

## Installing & searching

```bash
npx @21st-dev/registry add @{team}/{component-slug}   # install into project
npx @21st-dev/registry search "query terms"           # search accessible registries
```

`add` writes the component source into the project (per `components.json` aliases) and runs the package manager to install any new dependencies.

## Team & registry management

```bash
npx @21st-dev/registry team list
npx @21st-dev/registry team create "Team Name"
npx @21st-dev/registry team invite dev@company.com --team acme
npx @21st-dev/registry registry list --team acme
npx @21st-dev/registry registry create "Registry Name" --team acme
```

## Agent skill bootstrap

The package bundles its own SKILL.md for agents; installing it globally is optional if this skill is present:

```bash
npx @21st-dev/registry install-skill --global
```
