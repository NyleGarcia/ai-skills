---
name: issue-council-report
description: Write high-quality CIG Issue Council (IC) posts for Star Citizen bugs — gathers local build/log/crash-dump evidence, searches IC for duplicates before filing, and follows a verified UI walkthrough with known gotchas. Use when user says "issue council", "IC report", "file SC bug", "write up this crash", or wants to report a Star Citizen bug to CIG.
---

# Issue Council Report Writer

Write high-quality CIG Issue Council (IC) posts for Star Citizen bugs, and search IC before filing.
Triggers: "issue council", "IC report", "file SC bug", "write up this crash".

## Workflow

1. **Gather evidence locally first** (paths per `~/docs/gaming/star-citizen/star-citizen-linux-setup.md`):
   - Build: `.../StarCitizen/<CHANNEL>/build_manifest.id` → `Branch`, `BuildId`, `RequestedP4ChangeNum`.
   - Log: `<CHANNEL>/Game.log` + `logbackups/` — grab the last ~30 lines before crash/quit,
     any `[Error]`/`Fatal`/`SystemQuit cause=` lines, and the entity/location names in them.
   - Crash dump: `drive_c/users/zedwil/AppData/Local/star citizen/crashes/` (note 0-byte dmp = handler wedged).
2. **Search IC for duplicates before writing** — IC is login-walled; use claude-in-chrome with the
   user's session: `issue-council.robertsspaceindustries.com`, search the exact entity/error string
   (e.g. `TransportManager_Orison_Elevator_Instance-Siege`), then location + symptom keywords.
   If a duplicate exists: **contribute + vote** instead of new report (dupes get closed and waste votes).
3. **Draft the report** using the template below. Show the draft to the user before posting.
4. **Post via claude-in-chrome** (user logged in), or hand user the finished markdown to paste.

## Report template

- **Title:** `<Location> - <System> - <Symptom>` — concrete, no "HELP"/"broken!!".
  Ex: `Orison - Siege Instance - Client hangs after transport gateway schedule errors`.
- **One issue per report.** Split unrelated symptoms.
- **Body sections:**
  - *Summary*: 1-2 sentences, what breaks and impact.
  - *Steps to reproduce*: numbered, minimal, from a known state ("1. Spawn at Orison ...").
  - *Expected result* / *Actual result*: one line each.
  - *Reproduction rate*: n/m attempts (IC asks for this — count honestly).
  - *Evidence*: Game.log excerpt (trimmed, in code block), build id/branch, timestamps UTC.
  - *Workaround* if known.
- **Environment quirks (this machine is Linux/Wine):** CIG only supports Windows. Do NOT lead with
  Wine. If the bug is content/server-side (repros regardless of OS — e.g. entity errors in Game.log,
  server instance bugs), file normally; log evidence is OS-neutral. If it could plausibly be
  Wine/driver-specific (rendering, input, crash-on-launch), check LUG Discord/wiki first and only
  file if Windows players report it too — otherwise it gets closed "unsupported platform".

## Quality bar

- Exact strings from logs, never paraphrased error text.
- No speculation about cause in the report body — symptoms + evidence only; theories go in comments.
- Trim log excerpts to the relevant lines (<30); link nothing external that requires login.
- Re-check the IC entry after posting: confirm repro steps render as a numbered list.
- **Voice: write like a gamer, not an AI.** Casual, first person, lowercase-ish ok, contractions,
  no bullet lists or headers in comments — but keep exact log strings/build ids verbatim.
  Ex: "happened to me twice tonight about 20 min apart... had to kill the process. checked
  Game.log and its spamming X right before Y". Never corporate phrasing ("I experienced an issue
  wherein...").

## Contribution flow (browser, verified 2026-09-01)

CONTRIBUTE button → wizard: (1) "Yes, I did" → Next; (2) impact radio (Critical = gamebreaking)
→ Next; (3) setup: device + game version + optional settings → Next; (4) "More info" textarea +
optional evidence upload → SUBMIT. Success = "+1 Thank you for your contribution".

UI gotchas (claude-in-chrome):
- SPA loads slow — RSI splash for 5-10s; `wait` then act, don't trust first empty page text.
- **Escape closes the whole dialog and loses the form** — dismiss autocompletes by clicking
  elsewhere inside the dialog instead.
- Session can expire mid-flow (bounces to sign-in landing) — user must re-login, then redo wizard.
- Device config saves to the account and is reused next time ("Edit" instead of "Add") — filled
  once as cachyos / i9-14900K / 64GB / RTX 5080, System field: "Linux (CachyOS) via Wine 11.16".
- Processor/GPU autocompletes have no modern entries — free text is accepted, ignore suggestions.
- Game version = two dropdowns: environment (LIVE 4.10.0) then build (e.g. 4.10.0-live.12545750,
  marked "Current version") → "THIS IS MY VERSION".
- IC force-labels every contribution "PC Windows" in the feed regardless of device entry — fine,
  the account device record carries the truth.
- **DxDiag upload is a dead end — confirmed content-independent** (tested 2026-09-01, 3 variants):
  `detectSystemConfigurationFromDxDiagFile` gql mutation → 403 Forbidden every time — UTF-8,
  UTF-16LE+BOM, and a minimal file with no `C:\` paths or registry strings. Block is at the
  WAF/endpoint level (IP/session/geo or endpoint dead), not the file. Never retry — use ENTER
  CONFIGURATION MANUALLY; the device saves to the account and is reused for all future
  contributions. Synthetic dxdiag kept at `~/Documents/DxDiag.txt` if ever needed elsewhere.

## Learnings

- 2026-09-01: 4.10 LIVE Orison Siege — `Gateway Schedule Unretrievable` /
  `TransportManager_Orison_Elevator_Instance-Siege` error flood precedes client hang; CIG crash
  handler wedges under Wine (0-byte error.dmp) making crash look like a hard lock.
  Related IC issues user tracked: STARC-219060, STARC-218400. Contributed to STARC-218400
  (2026-09-01, as Zedwil). Community workaround for the 4.10 Vulkan crash family: switch
  in-game renderer to DX11 (multiple reporters confirm zero crashes after).
