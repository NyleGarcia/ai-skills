---
name: wizard-flow-design
description: Designs, builds, and reviews multi-step user-flow and guidance wizards (create/setup/onboarding flows, steppers, guided checklists) in React — whether a wizard fits at all, step count and branching, step model, conditional steps per user config, validation gating, drafts and close guards, template seeding, review with jump-to-edit, per-target outcome reporting, expert fast paths, accessibility (title, focus, fieldsets), funnel telemetry, mobile layout, and the tests that pin them. Use when adding or changing a wizard or multi-step form, splitting a long form into steps, adding a step that only some users/orgs should see, auditing a flow testers found confusing or that users abandon, or when a wizard setting "saves but does nothing".
---

# Wizard Flow Design

A wizard is a promise: **every step the user sees applies to them, every value they enter is saved and used, and nothing they did is lost.** Most wizard bugs break one of those three. Its job is cutting *intrinsic* load (one decision at a time) without adding *extraneous* load (clutter, recall, jargon) — see [REFERENCE.md](REFERENCE.md#research-basis).

## Quick start — step model

```tsx
interface Step { key: string; title: string; body: ReactNode; errors: string[] } // [] = Next allowed

const steps = useMemo(() => {
  const basics = {...}, schedule = {...}, roster = {...}, voice = {...}, review = {...};
  return linked ? [basics, schedule, roster, voice, review]   // conditional step
                : [basics, schedule, roster, review];         // unlinked: byte-identical to before
}, [/* explicit primitive deps */]);
const i = Math.min(stepIndex, steps.length - 1);              // clamp when list shrinks
```

Next is disabled and a no-op while `steps[i].errors.length`. Final submit gates on **whole-form** validity, not the last step.

## Workflow

0. **Is a wizard right?** Fits complex, infrequent, order-dependent tasks. **3–8 steps**: <3 → one form with progressive disclosure; >8 → merge steps or split into separate tasks with a no-input intermission screen. Frequent/bulk entry → inline form or table, not a wizard. Unsure of branching → Wizard-of-Oz test a prototype first.
1. **Map the flow before code.** List every field, who it applies to (role, plan, integration, game/shape), and what it changes downstream. Order steps by the user's mental model (what → when → who → how they'll talk → who gets told → review), not by DB table. Branches **prune** steps so each user gets the shortest path.
2. **One concern, one step.** If a setting moves to a conditional step, remove it from the old one (`hideX` prop), keep form fields and payload unchanged. No two steps with near-identical names. Each step is **self-sufficient**: never make users recall an earlier answer (echo it) or leave to look something up.
3. **Gate by config, not by mode.** Steps/fields that don't apply to this user are absent, not disabled. Unaffected users get the exact old flow — pin it with a test. Exception: existing records already using a now-disabled option still show it so it can be switched off.
4. **Never hide "who gets told / where" behind Advanced.** Basic vs Advanced changes depth, not which steps exist. Toggles visible at every width. Remember the user's Advanced choice for next time.
5. **Seeded vs touched.** Prefills from defaults/templates show the seed but send `null` while untouched so the server applies its own ladder; a touched empty value (`[]`) is a real answer. Effects that seed return `prev` when unchanged. Smart defaults = the common case, never a surprising one.
6. **Templates:** user's own context (timezone, explicit picks) beats template; conflicting template is refused inline, never silently applied. Template-derived rows are flagged (`fromTemplate`), shown locked, rebuilt from the template on restore, and dropped when the template is deselected — by any path.
7. **Never lose work.** All dismissals route through one `requestClose`; confirm only if real data entered (ignore default-valued fields). Close keeps the draft ("Resume draft" / "Discard"); success clears it. Drafts load with `??` defaults per field so old drafts survive new fields; never restore edit identity (`editingId`) from a draft.
8. **Show where they are.** Persistent progress rail with **descriptive labels** ("Schedule", not "Step 2"), states current / done / upcoming; later steps not clickable until earlier ones are valid (clickable free-order tabs ≠ wizard). Don't trap the wizard in a modal when users must read the page behind it — use a page or side panel.
9. **Explain every block.** Validate per step, not only at the end. Always-visible validation summary near the footer (no hover-only popovers). Server rejection joins it and clears when the offending field changes. Failing step: inline `role="alert"` + "Try again"; optional dependencies never hard-block ("Continue anyway").
10. **Review + outcomes.** Review step renders a live preview from the same form state as the real output, grouped by step, each group with **Edit** that jumps to that step and returns to Review. Fan-out actions (post to N targets) show excluded targets with reasons *before* submit and per-target outcome rows *after*.
11. **Accessible by construction.** On step change: `document.title = "Step 2 of 5: Schedule – App"`, focus the step `<h2 tabIndex={-1}>` (or first invalid field). Radio/checkbox groups in `<fieldset>`+`<legend>`. Contrast 4.5:1 text, 3:1 borders; progress never animates forever.
12. **Don't trap experts.** Repeat users get a fast path: "Duplicate last", import, a single-page "all fields" form, or skip-to-review when defaults suffice.
13. **Round-trip every field.** Each wizard field must exist in frontend type, request schema, model column, and the reader. Back it with one shared field list + a coverage test — validators that drop unknown fields fail silently.
14. **Instrument.** Per-step view/next/back/exit with time-on-step; terminal submit outcome; the downstream **outcome event** (record actually used) is the real success metric, not completion.
15. **Test + layout check** — see [REFERENCE.md](REFERENCE.md#tests). Layout at 375px and 1440px; 44px targets; nothing needed is `hidden sm:`.

## Review checklist

- [ ] Wizard justified: 3–8 steps, infrequent task; branches prune to shortest path
- [ ] Each step applies to every user who sees it; gated-off users see old flow (tested)
- [ ] No setting configurable in two places; no step needs recall of an earlier one
- [ ] Every field saves, reloads, and changes behaviour (round-trip test)
- [ ] Seeded values send `null` until touched; `[]`/"none" are real answers
- [ ] Template rows locked, rebuilt on restore, cleared on deselect
- [ ] Close/Escape/backdrop keep draft; draft never restores edit identity
- [ ] Labelled progress rail; future steps locked until earlier valid
- [ ] Disabled Next/Submit always says why, visibly, on touch; per-step validation
- [ ] Review groups have Edit → step → back to Review; preview uses real renderer; fan-out shows per-target outcomes
- [ ] Title updates + focus moves to step heading; fieldset/legend on groups
- [ ] Expert fast path exists for repeat users
- [ ] Step list shrink clamps index; mode switch resets to step 0
- [ ] Funnel telemetry per step (incl. time-on-step) + submit + downstream outcome
- [ ] 375/1440 layout clean; stacked dialogs above wizard (overlay stack, no z literals)

Patterns, bug catalogue, research basis, and test recipes: [REFERENCE.md](REFERENCE.md). Teaching the open UI (not collecting input) belongs to `guided-tour-design`; tester guide afterwards via `user-testing-guide`.
