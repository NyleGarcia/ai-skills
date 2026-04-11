---
name: caveman-review
description: Provide one-line, emoji-coded code reviews with no fluff or greetings.
---
# caveman-review

🪨 One-line reviews. No fluff.

## Instructions

Provide code reviews in Caveman style.

### Rules

1. **Format:** `L<line>: <emoji> <severity>: <issue>. <fix>.`
2. **Emojis:** 🔴 (Bug/Critical), 🟡 (Warning/Perf), 🔵 (Style/Suggestion).
3. **No Greeting:** Start immediately with the first finding.

### Examples

- `L42: 🔴 bug: user null. Add guard.`
- `L120: 🟡 perf: nested loop. Use Map for O(1) lookup.`
- `L15: 🔵 style: var name vague. Rename to 'retryCount'.`
