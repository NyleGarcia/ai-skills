# Wizard Flow Design — Reference

Patterns and bugs harvested from SC-ORG-BOT's EventWizard, FleetWizard and LootHubWizard (2026-09 → 2026-10). Each bug states the rule it taught.

## Patterns

### Fit + sizing
- **Wizard vs alternatives:** <3 steps → single form + progressive disclosure (expanders, "Advanced"); 3–8 → wizard; >8 → compact, or split into distinct tasks joined by an intermission screen (no inputs, reorients: "Fleet created. Next: invite crew"). High-frequency/bulk entry → inline table/form; a wizard there is pure interaction cost.
- **Wizard-of-Oz before branch logic:** clickable prototype, a researcher plays the system. Closed (fixed reply list: consistent, misses edge cases) / open (improvised: flexible, hard to compare) / hybrid (list + improvise when stuck — default). Use it to find which branches users actually need before coding them.
- **Persona routing:** one early "What are you setting up?" question can prune whole branches; ask it only if it removes ≥1 step for most users.

### Linear vs state-machine
- **Linear array** (create/setup flows): `Step[]` built in one memo, index state, per-step `errors`.
- **State machine with history** (decision trees, e.g. join-a-fleet): `step` + `history: Step[]`; Back pops, chip-jump truncates. **Auto-skip** a step with exactly one valid answer (single group, single role) — but still record the choice.
- **Statechart library (XState)** when branches multiply (≳3 conditional steps or steps that loop): states finite, transitions only via events, guards hold the "is step N valid" rule — so "step 4 without step 3 valid" is unrepresentable and branching lives in the machine, not JSX. Keep the machine in its own module with a unit test per guard; the visual inspector doubles as flow documentation. Don't adopt it for a plain linear 4-step create flow.
- **Chips/rail navigation:** a later chip is enabled only when all earlier steps are valid. Labels are step names, states current / done / upcoming (`aria-current="step"` on current). Free-clickable tabs over unvalidated steps are a disguised form, not a wizard.

### Placement
- **Modal only when self-contained.** If any step needs info visible on the underlying page (a table row, a balance), render as a route or side panel, or echo that info into the step. A modal over the data the user needs blindfolds them.
- **Review jump-to-edit:** each Review group has "Edit" → `goTo(stepKey, { returnTo: "review" })`; that step's primary button reads "Back to review" while `returnTo` is set. Never force sequential Back through every step.

### Expert paths
- Fast paths for repeat users: "Duplicate last/existing", import (CSV/JSON), one-page "all fields" form behind a link, skip-to-review when every required field has a valid default, keyboard (Enter = Next in non-textarea inputs only if tested; `Alt+←/→` optional).
- Persist disclosure state per user (`advancedOpen`), so the expanded view becomes their default.

### Mode swaps
- Whole-flow alternate (e.g. "roulette" vs normal): swap the step list, own validation, own terminal submit; reset `stepIndex` to 0 on switch; offer the toggle only when its handler exists and not while editing.
- Shape-dependent body (fleet / roster / RSVP): swap step body, title, and the "required" rule together — a required field that a shape can't satisfy makes Confirm unreachable.
- Domain vocabulary from one helper (`termFor(shape, ...)`), never `if (game === ...)` in JSX.
- Immutable choices on edit (shape, game) render disabled with the reason.

### State hook
- Flat per-field state + separate actions object; collection edits via immutable updaters (`setRows(prev => ...)`) — StrictMode double-invokes updaters.
- `touched` flags for every seeded field; a seeding effect must not overwrite a deliberate "none".
- Template-apply precedence: user context > explicit pick > template > org default. `null` = "use default", `[]` = "none".
- Every entry point (create, copy, edit, resume, reset) resets edit identity and template-derived state explicitly.

### Close guard + drafts
- One `requestClose` for X / Escape / backdrop; `hasEnteredData` excludes fields with non-empty defaults.
- Modal primitive provides focus trap, Escape, scroll lock; confirm dialog stacks above via overlay-stack z-index, never `z-[n]`.
- Autosave skips empty drafts; unreadable drafts are caught and logged.

### Feedback
- Always-visible validation summary ("Finish this step" / "Cannot schedule yet").
- Funnel telemetry: one action per Next (`step, stepKey, totalSteps, mode`), terminal submit outcome; network outcome reported by the request owner.
- Per-target outcome rows merged one per target, with human reasons ("no events channel set").

### Accessibility (WCAG 2.2)
| Rule | Implementation | SC |
|---|---|---|
| Announce progress | `document.title = \`Step ${n} of ${total}: ${title} – App\`` on each step change (SPA: no reload) | 2.4.2 |
| Focus | after step change focus `<h2 tabIndex={-1} ref>` of new step (or first invalid field after failed Next); never behind sticky footer/overlay | 2.4.3, 2.4.11 |
| Grouping | radio/checkbox sets in `<fieldset><legend>` | 1.3.1 |
| Progress | `<progress>`/rail never animates indefinitely (style out OS shimmer) | 2.2.2 |
| Targets/contrast | ≥44px (min 24px SC), text/errors 4.5:1, input borders 3:1 | 2.5.8, 1.4.3, 1.4.11 |
| Errors | per-step validation; error text tied via `aria-describedby`; summary `role="alert"` | 3.3.1 |

### Metrics
- **Drop-off per step:** large exit at step N usually reflects friction accumulated over steps < N too — inspect earlier steps, not just N.
- **Time-on-step spike** → too much intrinsic load or confusing copy → split step, add inline help, or rewrite.
- **Silent failures:** session replay (privacy-masked) for rage clicks / repeated Next — often an invisible validation error.
- **Success = outcome event** (event actually held, fleet actually joined), not wizard completion. Survey/NPS only after the outcome event.

### Setup/onboarding flows
- Checklist computed from a requirement registry, not a stored "done" bool.
- Current step in the URL (`?step=`) so refresh/back work.
- One generic `RequirementField` renders every registry row; PATCH only changed fields.
- Preflight warns, never blocks; permission races after install treated as transient.
- Tours: missing/hidden/off-canvas target → centered card, no spotlight.

## Bug catalogue → rule

| Symptom | Cause | Rule |
|---|---|---|
| Inputs lose focus every keystroke | focus-trap effect depended on inline `onClose` | keep callbacks in a ref; depend on primitives |
| Close X "dead" | confirm dialog z-index under wizard backdrop | overlay stack for z-index |
| "8pm" became 8pm UTC | template stored literal `UTC`, overrode user | user context beats template |
| Half-built event lost on close | no close guard; close reset form | guard + keep draft |
| Most users never saw pings/channel | settings only in Advanced; toggle hidden on mobile | who-gets-told never Advanced-only; toggles at all widths |
| Voice step shown to everyone | step not gated by integration | gate by config; old flow pinned |
| Voice pickers in two steps | moved step, left originals | one concern, one step (`hideX`) |
| Pings silent / overrode game roles | seed always sent | send `null` until touched |
| "Saves but does nothing" (6+ fields) | missing from schema/columns; validator dropped unknown keys | shared field list + round-trip coverage test |
| Save PATCHed wrong record | stale `editingId` survived edit→cancel→copy | reset identity in every entry point |
| Edit wiped organizer | response never serialized field, form sent `null` | form only sends fields it loaded |
| Auto-shared to all trusted orgs | trust treated as subscription | fan-out opt-in; template rows explicit + locked |
| Legacy records lost builder | NULL/NULL read as wrong shape | explicit shape state with documented legacy default |
| Phantom seats for infantry | per-wizard hand-rolled capacity math | one shared capacity helper |
| Link dropdown listed cancelled items | unfiltered source list | filter choice lists by context |
| Can't choose "none" | select had no empty option | optional fields accept and send null |
| Officers-only gate refused organizers | permission check too narrow | gate on the real capability |
| Stepper overwrote keystroke | re-seeded on mount | re-seed only when upstream value changes |
| Legacy poll answers drawn as blank rows | old key format rendered as data | filter/label legacy data, never render blank |

### Generic anti-patterns (research)
| Anti-pattern | Rule |
|---|---|
| 2-field task as 3-step wizard; bulk entry via wizard | wizard only for 3–8-step infrequent tasks |
| Wizard modal hides the data the user must copy from | page/side panel, or echo the data into the step |
| Clickable tabs over unvalidated steps | lock future steps until earlier valid |
| "Step 1 / Step 2" rail | descriptive step names |
| Step needs answer from 3 screens back | echo prior answer; self-sufficient steps |
| Error found only at final submit, user must walk back | validate per step; review Edit jumps straight there |
| Everyone forced through the wizard forever | expert fast path; remember Advanced state |

## Research basis

Cognitive Load Theory (Sweller): working memory ≈ 4 chunks. **Intrinsic** load (task complexity) is managed by splitting into steps; **extraneous** load (noise, recall, jargon, inconsistent controls) is removed; **germane** load (building a mental model) is supported with inline help and immediate feedback. Hick's law → fewer choices per step; Fitts's law → large, predictably placed Next/Back; Gestalt proximity → group related fields. **Expertise reversal:** scaffolding that helps novices slows experts — hence fast paths. Sources: NN/G "Wizards: Definition and Design Recommendations" and "Wizard of Oz Method"; W3C WAI "Multi-page Forms" tutorial; xstate-wizards (GitHub). Distilled from a 2026-10-31 research brief "UI/UX Architectures for Web Applications: Wizards, Guided Tours, and Cognitive Load".

## Tests

- Per-file `makeForm(overrides)` fake with `vi.fn()` setters + `renderWizard(form, props)`; mock auth and API clients.
- `goToStep(n)` clicks `getByRole("button", { name: "Next" })` — **exact** name (date pickers have "Next Month").
- Assert: step header/count (`/Step 4 of 6 · Voice Comms/`), gated-off flow unchanged (step count + where fields live), Next blocked per shape, mode radios toggle pickers and skip fetches, template conflict refused inline, payload shape (UTC conversion, `null` for untouched), dialog: Escape closes when empty, asks when dirty, focus stays in prompt.
- Back preserves data; Enter in a text input doesn't submit; submit disabled with reason when unauthenticated.
- A11y: after Next, `document.title` matches `/^Step 2 of \d+: /` and the step heading has focus; failed Next focuses first invalid field; group has `getByRole("group", { name })` (fieldset/legend).
- Review: clicking a group's Edit lands on that step and its primary button reads "Back to review", which returns to Review with data intact.
- Relabelling copy breaks text selectors — keep stable `data-testid`/titles for things tests key on.
- Layout check at 375 and 1440 on every UI change.
