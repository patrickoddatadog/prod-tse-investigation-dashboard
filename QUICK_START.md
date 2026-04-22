# Prod TSE Investigation Dashboard - Quick Start

**TL;DR:** This workspace helps TSEs investigate customer cases using AI-assisted workflows, with a local web dashboard for visualization.

---

## What Is This?

A Cursor AI workspace for Technical Support Engineers (TSEs) to:
- Investigate Zendesk tickets with AI-powered search across Glean, JIRA, Confluence, and GitHub
- Document investigations systematically with mandatory outputs (customer response, leadership summary, handover, Zoom prep, feature request section when needed)
- Visualize cases in a local web dashboard (POD Ticket Dashboard)
- Transcribe and summarise Zoom call recordings with Whisper + OpenAI
- Generate **JIRA-ready feature request** copy from case notes (dashboard **Feature Request** tab + OpenAI)
- Escalate to Engineering with properly formatted JIRA tickets
- Communicate clearly with customers using pre-built templates under `templates/communication/`

---

## 5-Minute Setup

```bash
# 1. Clone and open in Cursor
git clone https://github.com/eoghanm2013/tse-investigation-hub.git
cd tse-investigation-hub
cursor .

# 2. Set up credentials
cp .env.example .env
# Edit .env with your API tokens (Zendesk, Atlassian, GitHub, OpenAI)

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Restart Cursor (Cmd+Q, reopen)
```

Atlassian and Glean use SSO — they'll prompt a one-time login on first use. No tokens needed for those.

**Alternate clone (fork):** [patrickoddatadog/prod-tse-investigation-dashboard](https://github.com/patrickoddatadog/prod-tse-investigation-dashboard) — after clone, `cd prod-tse-investigation-dashboard`.

**Full setup guide:** See [SETUP.md](SETUP.md)

---

## Using It

### Start an Investigation
Ask Cursor:
> "Investigate Zendesk ticket 2864882"

Cursor will:
1. Fetch the ticket (Zendesk via Chrome or Glean, depending on your setup)
2. Search for similar historical cases (Glean, Confluence, JIRA, local `archive/`)
3. Create a case folder in `cases/ZD-2864882/`
4. Generate `notes.md` with all mandatory sections
5. Draft a customer response, Zoom call prep, leadership summary, TLDR handover, and placeholders for escalation / feature request sections as needed

### During Investigation
- **Ask Cursor** to search Confluence, JIRA, GitHub, Glean, or Slack (via Glean)
- **Drop files** into `cases/ZD-2864882/assets/` (logs, screenshots, recordings)
- **Document findings** in `notes.md` — each `##` section renders as a tab in the dashboard
- **Use templates** from `templates/communication/` for customer responses

### Launch the Web Dashboard
```bash
# Option 1: Direct
python3 app.py

# Option 2: Auto-restart wrapper
./scripts/start-server.sh
```
Then open: **http://localhost:8501**

### Zoom Call Recording
1. Upload audio via the dashboard's **Zoom Call Transcript** tab
2. Whisper auto-transcribes the recording
3. Click **Summarise** to generate a structured summary via OpenAI
4. Summary appears in `notes.md` and the dashboard

### Need to Escalate?
1. Complete your investigation and document findings in `notes.md`
2. Open the **Escalation** tab in the dashboard and click **Generate Escalation Summary**
3. Ask Cursor: `"Create JIRA escalation for ZD-12345"`

### Feature request (internal / product triage)
Use this when the ticket is (or includes) a product gap you want to capture for engineering or FR workflows—not a verbatim customer email.

1. Fill in `cases/ZD-XXXXXX/README.md` and `notes.md` with the ask, customer impact, and technical detail
2. Ensure `OPENAI_API_KEY` is set in `.env` (same as Zoom summary and escalation generation)
3. Open the **Feature Request** tab → **Generate Feature Request Summary** (writes or replaces `## Feature Request` in `notes.md` from `README.md` + notes)
4. Use **Regenerate Feature Request Summary** after you edit the case; polish the markdown before pasting into JIRA or internal FR channels

Template reference for section structure: `templates/communication/feature-request.md`. Cursor rule: `.cursor/rules/feature-request.mdc`.

---

## Folder Guide

| Folder | Purpose |
|--------|---------|
| `cases/` | Active customer investigations (gitignored — never committed) |
| `archive/` | Resolved cases by month (gitignored) |
| `.cursor/rules/` | AI behavior rules (investigation workflow, comms, escalation, risk) |
| `.cursor/hooks/` | Auto-checks for pending transcripts and escalations |
| `.cursor/skills/` | Reusable investigation skills (ticket pool, attachment downloader) |
| `templates/` | `communication/` (customer + handover + feature request), `escalation/`, etc. |
| `docs/` | Escalation criteria, product documentation |
| `scripts/` | CLI tools (JIRA client, Whisper transcription, server launcher) |
| `web/` | Dashboard HTML templates and CSS |
| `reference/` | JIRA project codes, reference materials |

---

## Mandatory Investigation Outputs

Every investigation should include these sections in `notes.md`. The dashboard maps each `##` heading to a tab (where the section exists):

| Section (`notes.md`) | Dashboard tab | Audience | Purpose |
|----------------------|---------------|----------|---------|
| **Proposed Customer Response** | Proposed Customer Response | Customer | Brief-first message body only (review before sending) |
| **Zoom Call Preparation** | Zoom Call Prep | TSE (you) | Agenda, key points, resources |
| **Leadership Summary** | Leadership Summary | Non-technical managers | Plain English, strict word limits |
| **TLDR Handover** | TLDR | TSEs + managers | Technical detail, next steps, important links |
| **Feature Request** | Feature Request | Engineering / product triage | Optional: use **Generate Feature Request Summary** for JIRA-ready draft (`OPENAI_API_KEY`) |
| **Escalation Summary** | Escalation | Engineering | Optional: **Generate Escalation Summary** for JIRA-ready escalation |

Full investigation narrative lives under **Investigation Notes** (same file, `##` sections the app extracts).

---

## Cursor Rules & Hooks

Pre-configured AI rules that shape how Cursor assists you:

| Rule | What It Does |
|------|-------------|
| `investigation-workflow` | Step-by-step process for investigating tickets |
| `mandatory-outputs` | Ensures all required sections exist in `notes.md` |
| `communication` | Brief-first tone, template usage |
| `escalation-criteria` | When and how to escalate to Engineering |
| `risk-assessment` | Rollback/risk checklist for config change recommendations |
| `zoom-transcript` | Auto-summarisation pipeline for call recordings |
| `api-access-constraints` | Read/write boundaries for each external service |
| `feature-request` | Guidance when authoring or generating the `## Feature Request` section |

**Hooks** run automatically on session start to flag unsummarised transcripts and pending escalations.

---

## API Access

| Service | Access | Notes |
|---------|--------|-------|
| **Glean** | Read | Searches Zendesk, Slack, internal docs |
| **Atlassian (JIRA)** | Read; Write for escalations | Confirm before creating tickets |
| **Atlassian (Confluence)** | Read | Internal documentation |
| **GitHub** | Read-only | Code research — never creates branches, PRs, or issues |
| **Slack** | Via Glean search | Never access Slack URLs directly |

---

## Common Prompts

```
"Investigate Zendesk ticket 2864882"
"Search JIRA for open SCRS tickets about APM"
"Search Confluence for agent troubleshooting"
"Search Glean for recent security product updates"
"Draft a customer response for this case"
"Prepare a Zoom call agenda for ZD-12345"
"Create JIRA escalation for ZD-12345"
"Draft a feature request summary for ZD-12345"   # or use the dashboard Feature Request tab
```

---

## Best Practices

**Do:**
- Document as you investigate — easier than doing it later
- Use templates for customer communication — consistent, professional
- Search archive and Glean before starting — someone may have solved this
- Escalate when appropriate — don't spend days on engineering-level issues
- Include risk callouts when recommending config changes

**Don't:**
- Commit customer data to git — it's all gitignored
- Skip the investigation workflow — documentation helps future cases
- Give production config advice without considering rollback plans
- Send customer responses without reviewing the draft first

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| JIRA/Confluence not working | Restart Cursor (Cmd+Q) — SSO will re-prompt |
| GitHub not working | Token expired — regenerate PAT |
| Zendesk 401/403 | Regenerate API token in Zendesk Admin |
| Dashboard won't start | Check `python3 --version` (need 3.9+); check port 8501 |
| Whisper transcription fails | Install ffmpeg: `brew install ffmpeg` |
| OpenAI summarisation fails | Check `OPENAI_API_KEY` in `.env` |
| Feature Request or Escalation generate fails | Same as OpenAI; confirm model env vars if you override defaults |
| MCP not loading | Verify `.cursor/mcp.json` exists; restart Cursor |

---

## Links

- **Full setup guide:** [SETUP.md](SETUP.md)
- **Workspace structure:** [STRUCTURE.md](STRUCTURE.md)
- **Escalation criteria:** [docs/escalation-criteria.md](docs/escalation-criteria.md)
- **Agent vs dashboard flow:** [docs/agent-flow.md](docs/agent-flow.md)
- **Primary repo:** [eoghanm2013/tse-investigation-hub](https://github.com/eoghanm2013/tse-investigation-hub)
- **Fork:** [patrickoddatadog/prod-tse-investigation-dashboard](https://github.com/patrickoddatadog/prod-tse-investigation-dashboard)

---

**Ready to go?** Start with: `"Investigate Zendesk ticket [ID]"`
