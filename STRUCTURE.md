# TSE Investigation Hub - Structure

This document explains the structure and purpose of the TSE Investigation Hub workspace.

---

## Directory Structure

```
pod-tse-investigation-hub/
│
├── .cursor/                          # Cursor AI configuration
│   ├── rules/                        # AI behavior rules
│   │   ├── investigation-workflow.mdc    # Step-by-step investigation process
│   │   ├── mandatory-outputs.mdc         # Required sections in notes.md
│   │   ├── customer-communication.mdc    # Brief-first tone, template usage
│   │   ├── escalation-criteria.mdc       # When and how to escalate
│   │   ├── risk-assessment.mdc           # Rollback/risk checklist for config changes
│   │   ├── zoom-transcript.mdc           # Auto-summarisation pipeline
│   │   ├── api-access-constraints.mdc    # Read/write boundaries per service
│   │   ├── tse-context.mdc              # Role context and workspace layout
│   │   └── output-standards.mdc          # File structure and data protection
│   ├── hooks/                        # Session hooks
│   │   ├── check-pending-transcripts.sh  # Flags unsummarised Zoom transcripts
│   │   └── check-pending-escalations.sh  # Flags pending escalation summaries
│   ├── hooks.json                    # Hook configuration
│   ├── skills/                       # Reusable investigation skills
│   │   ├── _shared/                      # Shared utilities
│   │   │   ├── zd-api.sh                    # Zendesk API helper script
│   │   │   └── README.md                    # Shared skills documentation
│   │   └── zendesk-ticket/               # Zendesk ticket skills
│   │       ├── investigator/                # Full ticket investigation workflow
│   │       ├── classifier/                  # Ticket classification and routing
│   │       ├── attachment-downloader/       # Download ticket attachments
│   │       └── pool/                        # Ticket pool management
│   └── mcp.json                      # MCP credentials (gitignored)
│
├── app.py                            # POD Ticket Dashboard (Flask web app)
├── requirements.txt                  # Python dependencies
│
├── cases/                            # Active customer cases (gitignored)
│   ├── .template/                    # Template for new case folders
│   │   └── notes.md                      # Notes scaffold with all mandatory sections
│   └── ZD-XXXXXX/                    # One folder per Zendesk ticket
│       ├── notes.md                      # Investigation notes (dashboard tabs render from this)
│       └── assets/                       # Supporting files
│           ├── screenshots/                 # Screenshots
│           ├── logs/                        # Log files
│           └── recordings/                  # Zoom call audio/transcripts
│
├── archive/                          # Resolved cases by month (gitignored)
│
├── templates/                        # Customer communication & escalation templates
│   ├── customer-communication/
│   │   ├── acknowledgment.md             # Initial ticket acknowledgment
│   │   ├── requesting-info.md            # Requesting info from customer
│   │   ├── solution.md                   # Providing a solution/workaround
│   │   ├── escalation-notice.md          # Notifying customer of escalation
│   │   ├── zoom-call.md                  # Zoom call preparation agenda
│   │   ├── zoom-call-transcript.md       # Transcript summary format
│   │   ├── leadership-summary.md         # Non-technical manager summary
│   │   └── tldr-handover.md              # Technical handover for TSEs
│   └── escalation/
│       └── escalation-template.md        # JIRA escalation ticket template
│
├── docs/                             # Documentation
│   ├── escalation-criteria.md            # When to escalate to Engineering
│   ├── apm/                              # Application Performance Monitoring
│   ├── infrastructure/                   # Infrastructure monitoring, agents
│   ├── logs/                             # Log management
│   ├── rum/                              # Real User Monitoring
│   ├── synthetics/                       # Synthetic monitoring
│   ├── network/                          # Network monitoring
│   ├── security/                         # Security products
│   ├── platform/                         # Billing, API, auth
│   └── common/                           # Cross-product (agent, integrations)
│
├── scripts/                          # CLI tools & utilities
│   ├── jira_client.py                    # JIRA search & escalation creation
│   ├── zendesk_client.py                 # Zendesk CLI tool
│   ├── zendesk_mcp_server.py             # Zendesk MCP server
│   ├── transcribe.py                     # Whisper transcription script
│   ├── start-server.sh                   # Auto-restart wrapper for dashboard
│   └── __init__.py                       # Package init
│
├── reference/                        # Reference materials
│   └── jira-project-codes.md            # JIRA project code lookup
│
├── web/                              # Web dashboard UI
│   ├── templates/                    # Jinja2 HTML templates
│   │   ├── base.html                     # Base layout
│   │   ├── dashboard.html                # Case list / home page
│   │   ├── case_detail.html              # Tabbed case detail view
│   │   ├── archive.html                  # Archived cases list
│   │   ├── archive_detail.html           # Archived case detail
│   │   ├── docs.html                     # Documentation browser
│   │   ├── known_issues.html             # Known issues page
│   │   ├── comms_templates.html          # Communication templates
│   │   └── 404.html                      # Error page
│   └── static/
│       └── style.css                     # Dashboard styles
│
├── .env.example                      # Environment variable template
├── .gitignore                        # Protects credentials and customer data
├── README.md                         # Main documentation
├── SETUP.md                          # Full setup guide
├── QUICK_START.md                    # Quick reference
├── STRUCTURE.md                      # This file
├── GIT_STRATEGY.md                   # What to commit / not commit
└── GITHUB_SETUP.md                   # GitHub repository setup
```

---

## TSE Workflow

```
1. Customer opens Zendesk ticket
2. TSE investigates using Cursor AI + Glean/JIRA/Confluence/GitHub
3. Cursor creates case folder, fetches context, searches for similar cases
4. TSE troubleshoots, documents findings in notes.md
5. notes.md populates all dashboard tabs (overview, Zoom prep, leadership summary, etc.)
6. If stuck → TSE escalates to Engineering (generates JIRA summary, creates ticket)
7. TSE keeps customer updated using communication templates
8. When resolved → TSE archives the case
```

---

## Key Components

### POD Ticket Dashboard (`app.py`)

Local Flask web app at **http://localhost:8501** that renders `notes.md` into a tabbed UI:

| Tab | Source Section | Purpose |
|-----|---------------|---------|
| Overview | `## Draft Customer Response` | Issue summary and proposed response |
| Investigation Notes | Full `notes.md` | Complete investigation documentation |
| Zoom Call | `## Zoom Call Preparation` | Call preparation agenda |
| Zoom Call Transcript | `## Zoom Call Transcript` | Upload audio, transcribe, summarise |
| Leadership Summary | `## Leadership Summary` | Non-technical summary for managers |
| TLDR Handover | `## TLDR Handover` | Technical handover for TSEs |
| Escalation | `## Escalation Summary` | Generate JIRA-ready escalation |

### Cursor Rules (`.cursor/rules/`)

AI behavior rules that shape how Cursor assists investigations. Always applied — no manual activation needed.

### Cursor Skills (`.cursor/skills/`)

Reusable investigation workflows:
- **investigator** — Full end-to-end ticket investigation
- **classifier** — Ticket classification and routing
- **attachment-downloader** — Download Zendesk ticket attachments
- **pool** — Manage a pool of tickets

### Session Hooks (`.cursor/hooks/`)

Run automatically on session start/stop to flag pending work (unsummarised transcripts, incomplete escalations).

---

## MCP Integrations

| Service | Purpose | Auth |
|---------|---------|------|
| **Glean** | Search Zendesk, Slack, internal docs | SSO |
| **Atlassian** | JIRA search, escalation creation, Confluence docs | SSO |
| **GitHub** | Code research in Datadog repos | PAT (optional) |

---

## Data Protection

| Path | Gitignored | Contains |
|------|-----------|----------|
| `cases/ZD-*` | Yes | Customer case data, logs, screenshots |
| `archive/*` | Yes | Resolved customer cases |
| `.env` | Yes | API tokens and credentials |
| `.cursor/mcp.json` | Yes | MCP credentials |

Only templates, rules, scripts, documentation, and the web dashboard are version-controlled. Customer data never leaves your machine.

---

**Summary:** The TSE Investigation Hub is an AI-powered workspace for Technical Support Engineers at Datadog. It combines Cursor rules, skills, and MCP integrations with a local web dashboard to streamline ticket investigation, customer communication, and engineering escalation.
