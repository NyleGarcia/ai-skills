# Color and Contrast Reference

## Core Rules
- **OKLCH:** Prefer OKLCH for consistent perceived lightness.
- **Tinted Neutrals:** Never use pure #000000 or pure gray. Tint grays with the primary brand hue (e.g., `oklch(20% 0.02 250)`).
- **Hierarchy:** 
  - 60% Background (Neutral/Tinted White)
  - 30% Secondary (Cards, Surfaces)
  - 10% Accent (CTA, primary brand)
- **Contrast:** Strictly WCAG AA minimum.
  - Text: Minimum 4.5:1 against background.
  - UI Elements: Minimum 3:1 against background.
- **Dark Mode:** Don't just invert colors. Lighten backgrounds slightly, desaturate accents to reduce eye strain.
- **Semantic Colors:** Ensure red/green/yellow have distinct lightness/saturation values for colorblindness.

## Anti-Patterns
- Pure black on pure white (causes eye strain).
- Default LLM purple/blue gradients.
- Gray text on colored backgrounds (use dark/light variants of the background hue instead).
