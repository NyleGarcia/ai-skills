# Guided Tour Design — Reference

Patterns and bugs harvested from SC-ORG-BOT's tour system (`TourContext`, `TourTooltip`, `GlobalTourManager`, `config/tours.ts`) and its 2026-10-31 audit. Each bug states the rule it taught.

## Patterns

### Guidance typology
| Pattern | Use for | Friction / notes |
|---|---|---|
| Tooltip | one control, on hover/focus; point-of-need, persists | lowest; must also work on focus + touch (not hover-only) |
| Hotspot | optional discovery of one feature | medium; pulse ≤5 s then static; few per page, only where drop-off is measured |
| Micro-tour (2–4 steps) | one workflow, fired on first visit to that feature | interruptive; cap 5 steps |
| Orientation tour (≤3 steps) | first login: where things live | most interruptive; once, skippable, then never auto again |
| Launcher / resource center | on-demand: checklist, replay tours, docs | user-controlled; best engagement — always ship one |
| Command palette / help search (Cmd+K) | power users who search rather than follow | zero friction once learned; index tours + docs here too |

### Tour architecture
- **Single whole-product tour — anti-pattern:** forces a linear path through non-linear software; users after feature 9 skip 1–8, then abandon; nothing is retained by the end.
- **Branched tour — situational:** only when the audience splits into 2–3 very distinct segments; costly to maintain.
- **Micro-tour library — default:** small tours per feature, triggered contextually where friction happens.
- **Hybrid — recommended:** ≤3-step orientation on first login + micro-tour library + launcher for replay.
- **Persona routing:** a 1–2-question welcome survey (role / goal) stored on the account selects which micro-tours are eligible; unknown → generic set.

### Triggers
- **Self-serve first.** Launcher/Page help/replay outperform blanket auto-start ~2–3× on engagement.
- **Auto** only for critical-path activation; **contextual** = first arrival at the feature's route/panel.
- **Never mid-task.** `userIsBusy` = any dirty form, focused text input, drag in progress, open overlay, or input in the last ~2 s. Defer to the next natural transition (route change to a hub, task submit), don't queue a pile of tours — at most one auto-tour per session.
- **Learn by doing:** step with `advanceOn: "event-created"` waits for the real action (anchor clickable, backdrop passes clicks to it) instead of "Next"; offer "Skip step".

### Fading (expertise reversal)
- Per-feature counter `featureUse[featureKey] = { unaided: n }`, incremented on the feature's outcome event when no tour/hint was open. At `n >= RETIRE_AFTER` (default 3) mark mastered on the account → no auto-tour, hotspot, or intro tooltip for that feature; manual replay still works.
- Users with tenure or prior activity in the feature skip orientation and contextual auto-tours.

### Architecture
- **Registry + manager + renderer.** Tours defined in one config module (never inline in components); a headless manager decides *whether* to start; a portal renderer draws backdrop, spotlight, and card. Keep the "should start?" decision a pure function (`resolveTour(path, role, prefs, auth)`) so it is unit-testable.
- **Two entry points, one path.** Auto-start (first visit) and manual replay ("Page help & tour" button) call the same `startTour(tour, {trigger})`. Manual ignores completion but still respects readiness; when no tour resolves it says so ("No tour for this page yet") instead of doing nothing.
- **Pause, don't fight.** Tour joins the overlay stack: a modal opened mid-tour takes Escape first; the tour never auto-starts while any overlay/wizard is open, and ends with `outcome: interrupted` on route change.

### Route → tour resolution
- **Ordered list, first match wins.** Object-key order and "most specific" heuristics drift; an array is explicit. Put specific routes (`/events/:id/edit`) before general (`/events/:id`, `/events/*`).
- **Explicit no-tour entries.** `[pattern, null]` stops fall-through so a prefix pattern doesn't fire a parent's tour on a child page that lacks its anchors.
- **Aliases share a tour object**, never copies (`/cargo` and `/guilds/:id/cargo` → same `cargoTour`).
- **Role comes from the page.** Each entry (or page component) names the gate it uses (`requires: "manage_events"`); the manager evaluates *that* capability. A generic `is_admin || is_officer` flag gave officers the admin tour on pages where only admins see the controls.
- **Public routes opt in.** `public: true` on the entry; everything else waits for an authenticated user. Login, OAuth callback, error and 404 routes are always `null`.

### Readiness gate
```ts
const ready = auth.status !== "loading" && (!auth.user || role.status === "ready") && prefs.status !== "loading";
useEffect(() => {
  if (!ready || activeTour || overlayOpen) return;
  const tour = resolveTour(pathname, role, { isPublic: !auth.user });
  if (!tour || !shouldAutoStart(tour.id)) return;
  closeTransientUi();                                   // drawers, menus, popovers
  const raf = requestAnimationFrame(() => startTour(tour, { trigger: "auto" }));
  return () => cancelAnimationFrame(raf);
}, [ready, pathname, roleKey, activeTour?.id, overlayOpen]); // primitives only
```

### Preference storage
- **Shape:** `{ toursEnabled: boolean; completed: Record<tourId, version> }` on the user record (API `GET/PATCH /me/preferences`). `completed[id] >= tour.version` = done; bump `version` after a redesign to re-show.
- **Opt-out ≠ completion.** "Don't show tours" sets `toursEnabled=false`; it never writes completion ids, and finishing one tour never touches `toursEnabled`. Settings exposes both: the toggle and "Replay all tours" (clears `completed`).
- **Reset is per id** and actually re-shows: `resetTour(id)` removes that id from account + cache + session set.
- **Cache + fallback:** read account prefs when logged in; mirror to `localStorage` under a namespaced key (`app.tours.v1`); logged-out pages use localStorage only. On first authenticated load, merge local ids into the account once (union), then mark migrated (`app.tours.migrated=<userId>`).
- **Safe storage wrapper:** every `getItem/setItem/removeItem` in try/catch (Safari private mode, blocked cookies, quota). Dismissal also goes into an in-memory `Set` checked by `shouldAutoStart`, so a failed write never re-opens the tour on the next render.
- **Optimistic writes:** update local state immediately, PATCH in background, keep local on failure; never block Skip/Finish on the network.

### Step resolution + positioning
- Resolve anchors by `[data-tour="id"]` only. Treat as missing: not in DOM, zero size, `display:none`/`visibility:hidden`, or horizontally off-canvas (closed drawer). Vertical overflow is fine — `scrollIntoView({ block: "center", behavior: reduced ? "auto" : "smooth" })`.
- **Missing anchor → skip** forward (or backward when going Back) and log `skipped_missing`; if every remaining step is missing, end the tour (`outcome: no_anchors`) — or show one centered card for anchorless intro steps declared with `placement: "center"`.
- **Async anchors:** SPA components mount after data loads, so "not in DOM yet" ≠ missing. Wait with a `MutationObserver` on the route container, resolve on first match, give up after a timeout, always `disconnect()` in effect cleanup:
  ```ts
  function waitForAnchor(id: string, root: Element, ms = 3000): Promise<Element | null> {
    const sel = `[data-tour="${id}"]`;
    const hit = root.querySelector(sel);
    if (hit) return Promise.resolve(hit);
    return new Promise(resolve => {
      const obs = new MutationObserver(() => { const el = root.querySelector(sel); if (el) done(el); });
      const timer = setTimeout(() => done(null), ms);
      function done(el: Element | null) { obs.disconnect(); clearTimeout(timer); resolve(el); }
      obs.observe(root, { childList: true, subtree: true });
    });
  }
  ```
  Abort (disconnect) on route change / tour end; a timed-out anchor follows the missing-anchor rule.
- Watch with `ResizeObserver` on anchor + card and `resize`/`scroll` listeners (passive), not a 300 ms poll.
- **Card placement:** measure card via ref after render; try preferred side, flip to opposite if it overflows, then try remaining sides; clamp to viewport with 16px gutter; `max-height: calc(100dvh - 32px)` and `overflow-y: auto` on the body so the footer never leaves the screen. Below ~480px width consider a bottom-sheet card instead of anchored placement.
- Spotlight cut-out sized from the same measured rect; click on backdrop = skip (or ignore — pick one, document it); the anchor itself is not clickable during the tour unless the step says "try it".
- z-index from the shared layer scale (tour band), never literals.

### Content
- Copy lives in the i18n catalogue (`tours.events.create.title`), not in the config as literals; allow 30–40% expansion — card width fixed, height measured.
- Name controls exactly as their on-screen labels; when a label changes, the tour copy changes in the same PR.
- Step counter "2 of 5"; Back from step 2+; Skip always present; final button says "Done"/"Finish".
- No tour step that requires data the user may not have (empty table, no events) — anchor the empty state or the create button instead.
- Teach one thing per step; don't explain the last feature of a long tour — working memory won't hold it. Put it in its own micro-tour.

### Metrics
- **Primary: subsequent feature adoption** — share of toured users who fire the feature's *outcome event* (report generated, not report menu opened) within N days, vs a holdout/untoured cohort.
- Completion rate is a vanity metric: 90% completion + flat adoption = extraneous load. Steps with median dwell < ~1 s = click-through dismissal; shorten or cut.
- Drop-off by step index; a cliff at step 4+ says the tour is too long.
- Feedback prompts (NPS, "Was this helpful?") only after the outcome event, never on tooltip dismiss.
- Treat each tour as a hypothesis: ship with an owner + success threshold; retire tours that don't move adoption.

## Bug catalogue → rule

| Symptom | Cause | Rule |
|---|---|---|
| New user saw the member tour, then admin controls appeared under it; tour drawn over the login page | manager ran on first render before auth/guild loaded; no public-route concept | gate auto-start on auth + role + prefs ready; public routes explicit; login/callback always no-tour |
| Finishing the first tour suppressed every other tour forever | completion also wrote one global `tour_completed=true` that `hasCompleted` checked first | completion keyed per tour id; global flag only for explicit opt-out |
| "Reset tour" did nothing | reset removed the per-id key but the global key still short-circuited | reset per id re-shows that tour; test it |
| Opt-out and completion indistinguishable | same key used for both | separate `toursEnabled` and `completed` |
| Tour fired on edit/sub-pages with none of its anchors | prefix/parent patterns matched child routes; object-key order decided | ordered first-match list + explicit `null` entries |
| Steps spotlit empty space / card pointed at nothing | step shown even when anchor missing | skip missing-anchor steps; end if none left |
| Skip/Finish re-opened the tour in a loop (private mode) | storage write failed silently; next render saw "not completed" | try/catch wrapper + in-memory dismissed set |
| Crash on load with storage blocked | unguarded `localStorage.getItem` at module/render time | every storage access guarded; read lazily |
| Mobile: target hidden behind open drawer; card pointed into closed drawer | started immediately with nav drawer open / anchor off-canvas | close transient UI, start next frame, treat off-canvas as missing |
| Next/Finish below the fold at 375px | card clamped using hard-coded 200px height; real card taller | measure card, flip, max-height + scroll backstop |
| Keyboard users trapped behind backdrop / lost focus | dialog without `aria-modal`, no focus move, no trap, no restore | aria-modal, focus trap, Escape = skip, restore to opener |
| Officers got the admin tour on admin-only pages | role from `is_admin \|\| is_officer` instead of the page's real gate | page declares the capability its tour assumes |
| No idea whether tours help | no events | start/step/end(outcome) telemetry |
| Tour came back on every new device / after clearing data | preference only in localStorage | per-user account prefs, local as cache, one-time migration |
| Steps silently broke after a redesign | anchor ids renamed/removed with no check | anchor conformance test per tour |
| Hover-only "Skip" tooltip on icon button | label only in tooltip | visible text Skip button + aria-label on icon |

### Generic anti-patterns (research)
| Anti-pattern | Rule |
|---|---|
| 10-step "Next, Next, Next" product tour on first login (~16% completion past 5 steps) | micro-tours ≤5 steps; ≤3-step orientation |
| Pulsing dot on every button → users ignore all help ("dot blindness") | hotspots only on measured drop-off; pulse ≤5 s |
| Mandatory tour to explain a confusing screen | fix the screen; tours accelerate clear flows only |
| One big tour on day 1, no help on day 21 | contextual micro-tours + launcher replay |
| Tour pops while user is typing/mid-task | defer to natural transition; `userIsBusy` gate |
| Expert keeps getting intro tooltips | retire per feature after N unaided completions |
| Step "opens" before async content renders → fails | MutationObserver wait + timeout, then skip |
| Success reported as completion % | measure downstream feature adoption |

## Research basis

Cognitive Load Theory: working memory ≈ 4 chunks; tours add **extraneous** load unless they build a mental model (**germane**) at the point of need. **Expertise reversal effect:** step-by-step guidance that helps novices actively hurts experts (redundant info, broken flow) — hence fading, self-serve defaults, and command palettes. Dreyfus model (novice → expert) as the lens for who sees what. Sources: Chameleon "In-App Guidance: Types, Examples, Best Practices"; AdoptKit "Onboarding for SPAs"; Userpilot "How to Measure New Feature Success"; NN/G "8 Design Guidelines for Complex Applications". Distilled from a 2026-10-31 research brief "UI/UX Architectures for Web Applications: Wizards, Guided Tours, and Cognitive Load".

## Tests

Harness: `renderWithProviders(ui, { auth, prefs, route })` wrapping Router + Auth + Prefs + Tour providers; mock the prefs API client; `CI=1 npx vitest run`. Mock `requestAnimationFrame` (`vi.useFakeTimers({ toFake: ["requestAnimationFrame"] })`) or `await waitFor`.

```tsx
it("waits for auth before auto-starting", async () => {
  const { rerender } = renderApp("/events", { auth: { status: "loading" } });
  expect(screen.queryByRole("dialog")).toBeNull();
  rerender(appAt("/events", { auth: { status: "ready", user: admin } }));
  expect(await screen.findByRole("dialog", { name: /create an event/i })).toBeVisible();
});

it("never auto-starts on public routes", () => {
  renderApp("/login", { auth: { status: "ready", user: null } });
  expect(screen.queryByRole("dialog")).toBeNull();
});

it("completing one tour does not suppress another", async () => {
  const prefs = mockPrefs({ completed: { events_admin: 1 } });
  renderApp("/fleet", { prefs });
  expect(await screen.findByRole("dialog")).toBeVisible();
});

it("opt-out hides all tours; reset re-shows only that tour", async () => { /* toursEnabled=false → none; resetTour("x") → only x */ });

it("Skip ends the tour when storage throws", async () => {
  vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => { throw new DOMException("blocked"); });
  renderApp("/events");
  await user.click(await screen.findByRole("button", { name: "Skip" }));
  expect(screen.queryByRole("dialog")).toBeNull();
  act(() => rerenderSameRoute());             // no loop
  expect(screen.queryByRole("dialog")).toBeNull();
});

it("skips steps whose anchor is missing", async () => {
  renderTour(tourWith(["a", "missing", "c"]), <><div data-tour="a" /><div data-tour="c" /></>);
  await user.click(screen.getByRole("button", { name: "Next" }));
  expect(screen.getByRole("dialog")).toHaveAccessibleName(/step c/i);
});

it("traps focus, Escape skips, focus returns to opener", async () => {
  const opener = screen.getByRole("button", { name: "Page help & tour" });
  await user.click(opener);
  const dialog = await screen.findByRole("dialog");
  expect(dialog).toHaveAttribute("aria-modal", "true");
  expect(dialog).toContainElement(document.activeElement as HTMLElement);
  for (let i = 0; i < 6; i++) await user.tab();
  expect(dialog).toContainElement(document.activeElement as HTMLElement);
  await user.keyboard("{Escape}");
  expect(opener).toHaveFocus();
});

it("waits for an async anchor, then skips after timeout", async () => { /* anchor mounted at 500 ms → step shown; never mounted → skipped after 3 s; observer disconnected on unmount */ });

it("does not auto-start while a form is dirty", async () => { /* focus text input / dirty form → no dialog; submit → tour may start at transition */ });

it("retires auto-tour after N unaided completions", async () => { /* featureUse.unaided = 3 → no auto-start; Page help still starts it */ });
```

Also pin: hotspot animation ends ≤5 s (fake timers), `advanceOn` step advances on the real event not Next, route resolution table (`resolveTour` unit test over every pattern incl. `null` entries and first-match order), role resolution per page gate, migration (local ids → PATCH once, not twice), telemetry calls with outcome, reduced motion (`matchMedia` mock → `scrollIntoView` called with `behavior: "auto"`).

### Anchor conformance
- **Unit:** for each `[route, tours]`, render the page component with fixtures for that role and assert `document.querySelector('[data-tour="' + step.anchor + '"]')` for every step not marked `optional`. Fail lists `tourId/stepIndex/anchor`.
- **Static (cheap CI gate):** script collects every `anchor` from the registry and greps `data-tour="…"` in `src/`; any anchor with zero hits fails. Catches renames, not conditional rendering — keep both.
- **E2E (Playwright):** per tour, visit route as role, `startTour` via Page help, step through asserting a spotlight + card in viewport each step.

### Layout
Run the layout/overlap checker at **375px and 1440px** with each tour open on its longest step: card fully on screen, footer buttons not clipped, ≥ 44px targets, spotlight aligned to anchor, nothing behind a drawer. Repeat with the longest translated locale if any.
