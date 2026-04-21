# Case Investigation Dashboard Canvas — Design Spec

**Date:** 2026-04-21
**Status:** Approved
**Approach:** Canvas Skill Only (Approach 1)

---

## Purpose

A Cursor Canvas skill that renders a compact, single-view case investigation dashboard alongside chat. It serves as a quick-glance companion to the existing Flask web dashboard — the TSE scans the canvas for a high-level overview and clicks through to the web dashboard for full detail.

## Trigger Behavior

### Auto-trigger (post-investigation)
After the investigator skill completes all mandatory outputs in `notes.md`, it invokes the canvas skill as a final step. This is a single line addition to the investigator skill's checklist.

### On-demand trigger
Any prompt containing trigger keywords invokes the canvas for the specified case:
- "canvas ZD-XXXXX"
- "case dashboard ZD-XXXXX"
- "case summary ZD-XXXXX"
- "show case canvas ZD-XXXXX"

## Data Source

The canvas reads `cases/ZD-XXXXX/notes.md` directly. No helper scripts, no API calls. All section extraction is done by Cursor interpreting the markdown headings.

## Canvas Layout

The canvas renders as a single-page dashboard with these sections in order:

### Header
- Case ID as the title (e.g. "ZD-2874104 — Case Dashboard")
- Link to web dashboard: `http://localhost:8501/case/ZD-XXXXX`

### Section 1: Ticket Metadata
A compact two-column table extracted from the `## Ticket Summary` table in `notes.md`:
- Customer, Priority, Status, Product Area, Tier, MRR, Complexity, Created date

### Section 2: Investigation Summary
The core problem and initial assessment condensed to 3-5 sentences. Extraction priority:
1. If `## Timeline` exists with a "Problem Summary" subsection, use that
2. Otherwise, use the "Initial Assessment" subsection from `## Timeline`
3. If multiple timeline entries exist, summarise the first entry only — later entries are investigation progress, not the problem statement

### Section 3: Proposed Customer Response
Full text of the draft message from `## Proposed Customer Response`. Shown in full since this is the section the TSE reviews most.

### Section 4: TLDR Handover
All subsections from `## TLDR Handover`:
- Summary of Issue
- Investigation
- Next Steps
- Need from Customer

### Section 5: Leadership Summary
All three subsections from `## Leadership Summary`:
- Leadership Summary (≤45 words)
- Investigation (≤50 words)
- Next Steps (≤50 words)

### Section 6: Zoom Call Prep
Condensed bullet lists from `## Zoom Call Preparation`:
- Agenda items
- Key points to communicate

### Section 7: Important Links
All links from `### Important Links` in TLDR Handover, plus the Zendesk ticket link (`https://datadog.zendesk.com/agent/tickets/XXXXX`).

### Section 8: Escalation Status
- If not escalated: "Not escalated"
- If escalated: JIRA ticket link and brief reason
- Pulled from `## Escalation Summary` or `## Escalation Notes`

### Footer
- Last modified timestamp
- "Open in web dashboard" link

## Missing Section Handling

If a section doesn't exist in `notes.md`, the canvas shows "Not yet populated" for that section. This doubles as a checklist of what still needs to be done.

## Files Changed

| File | Change |
|------|--------|
| `~/.cursor/skills-cursor/canvas/SKILL.md` | Replace empty stub with full canvas skill definition |
| `.cursor/skills/zendesk-ticket/investigator/SKILL.md` | Add one checklist item: invoke canvas skill after completing mandatory outputs |

## What This Does NOT Do

- No custom HTML/CSS — uses Cursor's built-in canvas rendering
- No new Python scripts or dependencies
- No changes to `app.py` or the web dashboard
- No new API endpoints
- Does not replace the web dashboard — complements it

## Success Criteria

1. Running "canvas ZD-2874104" in chat produces a canvas with all 8 sections populated from that case's `notes.md`
2. Missing sections show "Not yet populated" instead of being omitted
3. The investigator skill auto-generates a canvas at the end of an investigation
4. The canvas includes a working link to the web dashboard
