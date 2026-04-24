---
name: debugger
description: Systematic debugging workflows, root-cause analysis (RCA), and error tracing for Python and JavaScript.
---

# Debugger Skill

Systematic approach to finding and fixing bugs.

## 1. Root-Cause Analysis (RCA)
1. **Reproduce**: Minimal script or test case.
2. **Isolate**: Check logs, stack traces, and environment variables.
3. **Trace**: Follow data flow across boundaries (API, DB, Frontend).
4. **Fix**: Surgical patch with regression test.

## 2. Platform Specifics
- **Python**: Use `pdb`, `icecream`, or `logging`. Check `pip list` vs `uv lock`.
- **Node.js/JS**: Browser devtools, `console.trace()`, `node --inspect`.

## Directives
- NEVER suppress errors without handling.
- Always check the "Happy Path" first.
- If a fix fails > 3 times, re-evaluate architectural assumptions.
