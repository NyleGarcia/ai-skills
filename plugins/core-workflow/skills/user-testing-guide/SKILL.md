---
name: user-testing-guide
description: Writes tester-facing guides for checking new or changed features by hand — retest checklists, release "what to test" notes, In-review ticket comments, and sections of a standing user-testing guide. Use when a feature ships to a beta/dev environment and humans must verify it, when a ticket moves to In review and needs "what to check", when tester feedback must be turned into retest steps, or when the user asks for a test plan, QA checklist, UAT script, or testing doc.
---

# User Testing Guide

A testing doc tells a non-developer **exactly what to do and what they should see**, so a pass or a fail is unambiguous and a fail is reportable. It is not a feature tour, a changelog, or developer docs.

## Quick start

For each change under test, write one block:

```md
### <Feature, in user words>
**Setup:** <role/server/state needed; what must be enabled first>
1. <one action, named exactly as the UI labels it>
2. ...
**Expect:** <observable result: what appears, where, within how long>
**Fail if:** <the specific wrong outcome, esp. the one that was reported>
```

## Workflow

1. **Inventory from the diff, not memory.** List every user-visible change in the release (`git log <prev-tag>..HEAD`, changelog fragments, closed tickets). Each becomes a block. Mark which ones fix a reported bug — those lead.
2. **State preconditions up front** (one Prerequisites block): version/build to confirm, refresh steps (hard-refresh web, Ctrl+R Discord/desktop clients), roles/permissions, integrations that must be linked/enabled, a second account for multi-user flows, seed data.
3. **Write steps** — one action per step, UI labels verbatim in **bold**, the path to reach it (Settings → Permissions → Access Mode). No "verify it works".
4. **Write Expect + Fail if** — observable, specific, timed ("appears in the admin within a few seconds"). Fail if names the original bug symptom so regressions are recognisable.
5. **Add edge checks** that real users will hit — see the checklist below. Pick the ones that apply; don't pad.
6. **Scope boundaries** — say what is *not* changed, what old data won't pick up the change ("ops created before this release update on next save"), and known open follow-ups with ticket links, so testers don't re-report them.
7. **How to report** — what to include in a fail: step number, screenshot, server/guild id, time (UTC), event/record id, browser/client.
8. **Place it** — see Destinations. Keep tester language plain; caveman/terse style never applies to tester docs.

## Edge-check checklist

- [ ] **Gated-off path:** user/server *without* the integration/permission/flag sees the old flow, unchanged (and no dead controls).
- [ ] **Persistence:** save, reload, reopen — value still there. Toggle on+save, then off+save.
- [ ] **No-reload freshness:** change in one place, return without reloading — other view reflects it (or say a refresh is expected).
- [ ] **Multi-user / multi-tenant:** second account, second server, partner/allied server — sees only what it should.
- [ ] **Teardown/undo:** cancel/end/delete removes what was created, keeps what it shouldn't touch.
- [ ] **Duplicates:** action posts/notifies exactly once (watch for double messages after restarts/re-sends).
- [ ] **Legacy data:** records created before the change render sensibly, not blank.
- [ ] **Failure mode:** dependency down/slow → clear message, no spinner forever, nothing half-saved.
- [ ] **Mobile width** for UI changes (phone portrait).

## Destinations

| Need | Where | Shape |
|---|---|---|
| Ticket ready for human check | ticket comment, status **In review**, leave open | blocks for that ticket only |
| Release to testers | release note / chat post | Prerequisites + numbered blocks + "Also in this release" + follow-ups |
| Tester feedback came back | reply to tester | one block per reported item, same numbering as their report |
| Standing coverage | repo user-testing guide (e.g. `docs/internal/meta/USER-TESTING-GUIDE.md`) | section per feature area; update in same PR as the feature |

Examples and anti-patterns: [EXAMPLES.md](EXAMPLES.md).

## Review checklist

- [ ] Every step is one action with exact UI labels; no "check it works"
- [ ] Every block has Expect **and** Fail if
- [ ] Reported-bug fixes listed first, with original symptom in Fail if
- [ ] Prerequisites cover version, refresh, roles, integrations, second account
- [ ] Gated-off / legacy / duplicate checks considered
- [ ] Out-of-scope + known follow-ups stated with links
- [ ] Report instructions present
