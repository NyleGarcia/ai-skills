---
name: guided-tour-design
description: Designs, builds, and audits in-app guidance in React — spotlight/coach-mark tours, contextual micro-tours, hotspots, tooltips, "Page help" replays, launchers/resource centers, and first-run walkthroughs — covering which guidance pattern fits, tour length and architecture (micro-tour library + short orientation), when a tour may auto-start (auth/role readiness, natural transition points, public routes) vs self-serve, per-tour completion vs opt-out storage synced to the user's account, fading guidance as users gain skill, route-to-tour resolution, async-anchor waiting and missing-anchor handling, card placement that keeps Next/Finish on screen, focus management, adoption-based telemetry, and the tests and anchor-conformance checks that keep tours in sync with the UI. Use when adding or changing a tour, coach mark, hotspot, onboarding walkthrough or page-help button, when a tour shows on the wrong page/role or over the login screen, when "Skip" or "Finish" doesn't stick or one dismissal kills every tour, when a tour points at nothing or hides off-screen on mobile, when tours have high completion but no adoption, or when auditing tour code.
---

# Guided Tour Design

A tour is a promise: **it appears only when it applies to this user on this page, it points at things that are really there, and once dismissed it stays dismissed — for that tour only.** Most tour bugs break one of those three. Guidance is a mitigation, not a fix: if a flow needs a mandatory tour to be usable, redesign the flow.

## Quick start — tour model

```ts
interface TourStep { anchor: string; title: string; body: string; placement?: Placement; advanceOn?: string }
interface Tour { id: string; version: number; role: "any" | "member" | "admin"; trigger: "auto" | "contextual" | "manual"; steps: TourStep[] }

// Route table: ordered, first match wins; `null` = "this page has no tour" (stops fall-through)
const ROUTE_TOURS: Array<[pattern: string, tours: Partial<Record<Role, Tour>> | null]> = [
  ["/login", null], ["/events/:id/edit", null], ["/events/:id", { admin: eventAdmin, member: eventMember }],
];

const canAutoStart = auth.status === "ready" && !route.isPublic && prefs.loaded
  && prefs.toursEnabled && !prefs.completed.has(tour.id) && !dismissedThisSession.has(tour.id)
  && !userIsBusy && !featureMastered(tour.featureKey);
```

Anchors are `data-tour="events-create"` attributes, never CSS classes or DOM paths. Steps whose anchor never appears are **skipped**, not shown pointing at nothing.

## Workflow

1. **Decide whether to guide at all — and with what.** Tour only non-obvious, high-value surfaces. Never tour self-explanatory UI, legal text, error states, or anything a label/empty state could explain. Pick the lightest pattern: tooltip (one control) < hotspot (optional discovery) < micro-tour (one workflow) < orientation tour (first login only). Plus a launcher ("Page help", resource center/checklist) so help is never one-and-done. See [REFERENCE.md](REFERENCE.md#guidance-typology).
2. **Micro-tours, not marathons.** Library of 2–4-step tours, one per feature, fired when the user first reaches that feature; optional ≤3-step orientation at first login (hybrid). **Hard cap 5 steps** — completion collapses past it. One long whole-product tour is an anti-pattern. Prefer learn-by-doing steps that advance when the user performs the action (`advanceOn`).
3. **Author against stable anchors.** Add `data-tour` ids in the component in the same PR as the step; anchor the control the user acts on, not a wrapper. Copy: title ≤ 4 words, body 1–2 sentences, say *what it's for / what to do*, no "Click here", no jargon, consistent with on-screen labels.
4. **Resolve the tour deterministically.** Ordered route table, first match wins, explicit `null` entries for pages with no tour (edit screens, sub-routes lacking the anchors). The **page declares its tour role** (same check that gates the page's controls) — never infer it from a loosely related flag. Optional welcome-survey answer (role/goal) selects which micro-tours apply.
5. **Gate auto-start on readiness and timing.** Wait for auth + role + preferences to finish loading. Public/logged-out routes are opt-in by an explicit `public: true`; never auto-start over login/callback/error routes. Never interrupt a modal, wizard, another tour, or a user mid-task (typing, dragging, form dirty) — wait for a natural transition (page arrival, task done). Default to self-serve; auto only on the new-user critical path.
6. **Store state per tour, per user.** Two separate concepts: `toursEnabled` (global opt-out, a user setting) and `completedTourIds` (per tour id, + version bump to re-show after redesign). Persist on the user's account; localStorage is a cache and the fallback for logged-out pages; migrate local ids to the account once on first login. All storage access in try/catch with an in-memory "dismissed this session" set so Skip/Finish always ends the tour.
7. **Fade with expertise.** Track feature use; once the user completes the workflow unaided N times (default 3), permanently retire that feature's auto-triggers, hotspots, and intro tooltips. Experienced/returning users skip orientation. Replay stays available via launcher.
8. **Prepare the page before step 1.** Close drawers/sidebars/menus that could cover anchors, then start on the next frame (`requestAnimationFrame`). Anchors behind async data: wait via `MutationObserver` with a timeout (≈3 s), disconnect on cleanup, then skip. Re-measure on resize/scroll; skip steps whose anchor is absent, zero-size, or off-canvas.
9. **Place the card so controls stay reachable.** Measure the rendered card (no hard-coded height), flip to the opposite side when it doesn't fit, clamp to the viewport, `max-height` + internal scroll as backstop — Next/Finish/Skip always visible at 375px.
10. **Make it accessible.** `role="dialog"` + `aria-modal` + `aria-labelledby`, focus moves into the card, focus trap, Escape = skip, focus returns to the opener (Page help button) or the anchor. Step counter announced; honour `prefers-reduced-motion`; hotspot pulse stops within 5 s (WCAG 2.2.2). Hotspots sparse — only on workflows with measured drop-off (dot blindness).
11. **Instrument adoption, not clicks.** `tour_start {id, trigger}`, `tour_step {id, index, skipped_missing, ms}`, `tour_end {id, outcome, at_step}`, plus the feature's **outcome event** afterwards. Success = adoption lift vs untoured users; high completion with flat adoption = the tour is noise. Sub-second steps = click-through dismissal.
12. **Test + conformance + layout** — see [REFERENCE.md](REFERENCE.md#tests). Every step's anchor must exist on its page (test). Layout check at 375px and 1440px.

## Review checklist

- [ ] Lightest pattern chosen; UI not patched with a tour instead of fixed
- [ ] Tours ≤5 steps (micro-tours 2–4); no whole-product marathon; launcher/Page help for replay
- [ ] No auto-start until auth/role/prefs resolve; never on login/public routes unless marked `public`
- [ ] Never auto-starts mid-task or over overlays; self-serve default, auto only on critical path
- [ ] Completion stored per tour id; global opt-out is a separate flag; reset of one tour re-shows only that tour
- [ ] Preference lives on the user account; localStorage only cache/fallback; one-time migration done
- [ ] Skip/Finish end the tour even when storage throws or is blocked (in-memory set)
- [ ] Guidance retired per feature after N unaided completions
- [ ] Route table ordered, first-match, explicit `null` for no-tour pages; tour role declared by page
- [ ] Every anchor is a `data-tour` id; conformance test asserts each exists on its page
- [ ] Async anchors awaited (observer + timeout, disconnected); missing → skipped, never empty spotlight
- [ ] Drawers/menus closed before start; start deferred a frame
- [ ] Card measured, flips, max-height backstop; controls on screen at 375 and 1440
- [ ] `aria-modal`, focus trap, Escape = skip, focus restored; reduced motion; pulses stop ≤5 s
- [ ] Telemetry: start / step(ms) / end + downstream outcome event; judged on adoption

Patterns, bug catalogue, research basis, and test recipes: [REFERENCE.md](REFERENCE.md). Multi-step forms belong to `wizard-flow-design`; tester guide afterwards via `user-testing-guide`.
