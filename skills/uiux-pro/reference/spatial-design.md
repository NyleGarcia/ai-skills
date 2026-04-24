# Spatial Design Reference

## Core Rules
- **Grid System:** 8px base grid. 4px for micro-adjustments.
  - Margins/Padding: 4px, 8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px.
- **Proximity:** Group related items close together. Space between groups must be larger than space within groups.
- **Visual Hierarchy:** 
  - Dominance: One clear focal point per screen.
  - Depth: Use subtle, multi-layered shadows for elevation. Avoid flat 1px borders everywhere.
- **Containment:** Use whitespace instead of borders and cards where possible.

## Anti-Patterns
- Nesting cards inside cards inside cards.
- Arbitrary spacing values (e.g., 13px, 27px).
- Edge-to-edge text without container max-widths.
- Insufficient whitespace around CTAs.
