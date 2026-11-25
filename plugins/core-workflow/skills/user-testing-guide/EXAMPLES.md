# Examples

## Good — release retest note (from a real beta release)

```md
**v1.0.0-beta.297 is live on dev.** Ctrl+R in Discord and hard-refresh the web app first.

On a server with Star Comms linked:

### 1. Wizard order
1. **Events → Create** and step through.
**Expect:** **Roster & Signups** has no voice dropdowns. **Voice Comms** comes after it, with Meet Up (Discord channel and/or net) and one row per team.
**Fail if:** voice pickers still show on Roster, or Meet Up can't be set to a net.

### 2. New nets are created
1. In Voice Comms pick **Create a new net** for a team. 2. Save.
**Expect:** net appears in the Star Comms admin within a few seconds; the post shows the real net name.
**Fail if:** net missing from Star Comms (the original critical bug).

### 5. Double post
**Expect:** one "operation open" notice per op. **Fail if:** two.

Ops created before this release get nets the next time they're saved or launched.
Known follow-ups: #1475 (low-severity edge cases) — no need to report those.
```

Why it works: numbered to match the tester's report, prerequisite refresh stated, the critical bug's symptom is the Fail if, old-data behaviour and known follow-ups called out.

## Good — In-review ticket comment

```md
Ready to check on dev (beta.290+).
Setup: admin on a test server; flag `rbac_advanced_mode` Force ON in Admin → Feature Flags.
1. Server Settings → Permissions → Access Mode → **Advanced** → confirm.
   Expect: matrix pre-seeded, "Unranked members" row pinned.
2. Without reloading, switch back to **Basic**, then Advanced again.
   Expect: your edits kept (no re-seed). Fail if: grants reset.
```

## Bad

```md
- Test the new wizard and make sure everything works.
- Check Star Comms integration.
- Verify the bug is fixed.
```

No setup, no actions, no observable result, nothing a tester can fail against.
