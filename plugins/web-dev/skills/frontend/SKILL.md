---
name: frontend
description: Frontend development expert for React and Angular using TypeScript and Vanilla CSS. Includes UI/UX patterns from uiux-pro.
---

# Frontend Development Skill

Modern, responsive, and high-performance web applications.

## Core Frameworks
- **React**: Preferred with Vite and TypeScript.
- **Angular**: Use for enterprise-scale applications.
- **Vanilla CSS**: Primary choice for styling. Avoid Tailwind unless requested.

## UI/UX Patterns (`uiux-pro`)
- **Spacing**: 8px base grid.
- **Typography**: Modular scales, system-font stacks or curated pairings.
- **Visuals**: Use Soft UI (subtle shadows) or Glassmorphism where appropriate.
- **Interactions**: Add `cursor-pointer` to clickables. 150-300ms transitions.

## Lessons Learned & Gotchas
- **React 19 StrictMode Singletons**: Beware of split-brain singletons (like an `AudioEngine`) when components are double-invoked in dev mode. Initialize heavy singletons outside the component tree or cache them rigorously with `useRef`.
- **Vite Temp File EPERM**: If a Vite project starts throwing `EPERM` errors during dev/build, check for stuck lock files in `.vite-temp` or `.tmp` and clear them.
- **Prop Preservation**: When replacing raw HTML elements (`<button>`, `<input>`) with UI primitives, always preserve standard attributes (`id`, `data-testid`, `aria-label`) and event handlers. If a primitive lacks support, update its interface (e.g., extend `React.ComponentPropsWithoutRef<'button'>`) rather than dropping the prop.
- **Tailwind Class Merging**: Never use raw string interpolation to combine Tailwind classes on primitives. Always use `clsx` and `tailwind-merge` (typically via a `cn()` utility) to ensure dynamic class overrides resolve correctly without scaling or padding conflicts.

## Verification
- Accessibility (WCAG AA).
- Mobile-first responsiveness.
- Performance (Lighthouse score > 90).
