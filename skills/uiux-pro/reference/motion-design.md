# Motion Design Reference

## Core Rules
- **Purposeful:** Motion must direct attention, show relationship, or provide feedback. Never decorative.
- **Easing:** Never use linear easing.
  - Enter: `ease-out` (decelerates). Fast in, slow out.
  - Exit: `ease-in` (accelerates). Slow in, fast out.
  - Standard: `cubic-bezier(0.4, 0.0, 0.2, 1)`.
- **Duration:** 
  - Micro-interactions (hover): 100ms - 200ms.
  - Structural transitions (page load): 300ms - 500ms.
- **Staggering:** Stagger list item entrances by 50ms-100ms for organic feel.
- **Accessibility:** Respect `prefers-reduced-motion`. Disable translations, fade only.

## Anti-Patterns
- Bounce or elastic easing (outdated).
- Durations > 500ms (feels sluggish).
- Moving multiple uncorrelated objects simultaneously.
