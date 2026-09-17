---
name: subagent-orchestration
description: Manages the safe lifecycle, monitoring, and termination of subagents. Use when spinning up teams, orchestrating parallel work, or cleaning up background tasks to prevent zombie agent bloat and CPU/RAM exhaustion.
---

# Subagent Orchestration & Hygiene

## Core Directives

1. **The Recursive Ban:**
   Explicitly forbids deep recursive orchestrator patterns (i.e. subagents that spawn subagents that spawn subagents) unless strictly necessary and bounded by explicit numerical limits.

2. **Sequential Default:**
   Sequential execution is the default mode. Only opt into parallel subagent execution for heavily isolated, I/O-bound tasks, or when explicitly requested by the user. If you spawn subagents, strictly limit concurrency to a small number (e.g., 2-3 workers).

3. **Anti-Hallucination Cleanup Rule:**
   Agents MUST use the `manage_subagents` tool with `Action: list` to confirm the actual state of their subagents. 
   Agents MUST use the `manage_subagents` tool with `Action: kill` to terminate specific subagents or their entire tree. 
   *Never generate text claiming you have killed or shut down agents without actually calling the tool.*

4. **Tree Pruning Lifecycle:**
   Killing a parent subagent automatically cascades down to kill all of its descendants. Use this nuclear option when a subagent tree has become unresponsive, has leaked nested zombie subagents, or is overwhelming system resources (CPU/RAM).
