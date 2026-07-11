# Interaction Design Reference

## Core Rules
- **Feedback:** Every action must have an immediate visual reaction.
  - Hover states: Adjust opacity, translation, or box-shadow.
  - Active states: Compress the element (e.g., `transform: scale(0.98)`).
- **Focus States:** Clearly visible focus rings for keyboard navigation. Never `outline: none` without a custom focus style. Use `:focus-visible`.
- **Loading:** Use skeleton loaders instead of spinners for content. Match the skeleton to the expected content shape.
- **Forms:** 
  - Labels always visible (don't rely solely on placeholders).
  - Clear validation states (icons + color + text message).
  - Group related fields visually.

## Anti-Patterns
- Missing hover states.
- Relying on tooltips for essential information.
- Modals that don't trap focus.
- Destructive actions without confirmation or undo.
