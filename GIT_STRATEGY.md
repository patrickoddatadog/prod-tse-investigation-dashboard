# Git Strategy for Prod TSE Investigation Dashboard

This document outlines what should and shouldn't be committed to git for team sharing.

---

## Repository

- **Public repo:** [github.com/patrickoddatadog/prod-tse-investigation-dashboard](https://github.com/patrickoddatadog/prod-tse-investigation-dashboard)
- **Branch:** `main`

---

## COMMIT TO GIT (Share with Team)

### Core Documentation
```
README.md                         # Main documentation
SETUP.md                          # Full setup instructions
QUICK_START.md                    # Quick reference
STRUCTURE.md                      # Architecture explanation
GIT_STRATEGY.md                   # This file
GITHUB_SETUP.md                   # GitHub setup guide
```

### Configuration & AI Rules
```
.env.example                      # Credential template (NO real tokens)
.gitignore                        # Protect sensitive data
.cursor/rules/*.mdc               # AI behavior rules (investigation, comms, escalation, risk)
.cursor/hooks.json                # Hook configuration
.cursor/hooks/*.sh                # Session hooks (transcript & escalation checks)
.cursor/skills/                   # Reusable investigation skills
```

### Application & Scripts
```
app.py                            # POD Ticket Dashboard (Flask web app)
requirements.txt                  # Python dependencies
scripts/jira_client.py            # JIRA CLI tool
scripts/zendesk_client.py         # Zendesk CLI tool
scripts/zendesk_mcp_server.py     # Zendesk MCP server
scripts/transcribe.py             # Whisper transcription script
scripts/start-server.sh           # Auto-restart wrapper for dashboard
scripts/__init__.py               # Package init
```

### Web Dashboard
```
web/templates/*.html              # Jinja2 HTML templates
web/static/style.css              # Dashboard CSS
```

### Templates (Generic, No Customer Data)
```
cases/.template/                  # Case investigation template
  cases/.template/notes.md        # Notes scaffold with all mandatory sections

templates/customer-communication/
  acknowledgment.md
  requesting-info.md
  solution.md
  escalation-notice.md
  zoom-call.md
  zoom-call-transcript.md
  leadership-summary.md
  tldr-handover.md

templates/escalation/
  escalation-template.md
```

### Documentation & Reference
```
docs/escalation-criteria.md       # When to escalate
reference/jira-project-codes.md   # JIRA project lookup
```

---

## DO NOT COMMIT (Keep Local)

### Credentials & Secrets
```
.env                              # Real API tokens (Zendesk, Atlassian, GitHub, OpenAI)
.cursor/mcp.json                  # MCP credentials
Any file with passwords/tokens
```

### Customer Data (CRITICAL)
```
cases/ZD-*                        # All actual case folders
archive/*                         # All archived tickets
Any customer logs, configs, screenshots
Any PII (names, emails, IPs)
```

### Personal/Local Files
```
.DS_Store                         # macOS metadata
.vscode/                          # Personal editor settings
.idea/                            # Personal IDE settings
*.swp, *.swo                     # Vim swap files
__pycache__/                      # Python cache
*.pyc, *.pyo                     # Python compiled files
*.log                             # Log files
ticketdash.log                    # Dashboard log
.venv/                            # Virtual environment
```

---

## MAYBE COMMIT (Case-by-Case)

### Anonymized Documentation
```
docs/[product]/troubleshooting/   # Troubleshooting guides
  - YES IF: Customer data is anonymized
  - YES IF: It helps the team
  - NO IF: Contains any customer identifiers
```

### Sanitized Examples
```
docs/[product]/examples/          # Example configs
  - YES IF: Completely generic/sanitized
  - NO IF: Based on real customer setup
```

---

## .gitignore (Current)

```gitignore
# Environment & Credentials
.env
.cursor/mcp.json

# Case folders (may contain customer data)
cases/*
!cases/.template/

# Archive (may contain customer data)
archive/*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Editors
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
ticketdash.log

.venv/
```

---

## File-by-File Analysis

| File/Folder | Commit? | Reason |
|-------------|---------|--------|
| `README.md` | YES | Team documentation |
| `SETUP.md` | YES | Setup instructions |
| `QUICK_START.md` | YES | Quick reference |
| `STRUCTURE.md` | YES | Architecture docs |
| `GIT_STRATEGY.md` | YES | This file |
| `GITHUB_SETUP.md` | YES | GitHub setup guide |
| `app.py` | YES | Web dashboard (no secrets) |
| `requirements.txt` | YES | Python dependencies |
| `.gitignore` | YES | Protection config |
| `.env.example` | YES | Template only |
| `.env` | NO | Real credentials |
| `.cursor/mcp.json` | NO | Real credentials |
| `.cursor/rules/` | YES | AI behavior rules (no secrets) |
| `.cursor/hooks/` | YES | Session hooks (no secrets) |
| `.cursor/skills/` | YES | Investigation skills (no secrets) |
| `scripts/*.py` | YES | Tools for everyone |
| `scripts/*.sh` | YES | Shell scripts |
| `web/` | YES | Dashboard templates & CSS |
| `cases/.template/` | YES | Template structure |
| `cases/ZD-*` | NO | Customer data |
| `archive/*` | NO | Customer data |
| `templates/**/*.md` | YES | Communication templates |
| `docs/` | YES | Team guidelines |
| `reference/` | YES | Shared references |

---

## Team Collaboration Workflow

### For Team Members Cloning the Repo

```bash
# 1. Clone
git clone https://github.com/patrickoddatadog/prod-tse-investigation-dashboard.git
cd prod-tse-investigation-dashboard

# 2. Set up credentials (NOT in git)
cp .env.example .env
# Edit .env with your tokens

# 3. Install dependencies
pip install -r requirements.txt

# 4. Open in Cursor and restart (Cmd+Q, reopen)
# Atlassian and Glean will prompt SSO on first use
```

### Sharing Knowledge Updates

**DO share:**
```bash
# Improve a template
git add templates/customer-communication/solution.md
git commit -m "Add rollback section to solution template"
git push

# Add a troubleshooting doc
git add docs/apm/troubleshooting/trace-sampling.md
git commit -m "Add APM trace sampling troubleshooting guide"
git push

# Update a rule
git add .cursor/rules/investigation-workflow.mdc
git commit -m "Add step for checking recent deployments"
git push
```

**DON'T share:**
```bash
git add cases/ZD-12345/   # NO — customer data
git add .env               # NO — real credentials
git add .cursor/mcp.json   # NO — real credentials
git add archive/            # NO — customer data
```

---

## Security Checklist

Before pushing to git, verify:

- [ ] No `.env` file committed
- [ ] No `.cursor/mcp.json` committed
- [ ] No `cases/ZD-*` folders committed
- [ ] No `archive/` contents committed
- [ ] No customer names in commit messages
- [ ] No API tokens in any files
- [ ] No customer logs, configs, or PII
- [ ] `.gitignore` is properly configured

---

## Common Mistakes to Avoid

### Mistake 1: Committing Real Credentials
```bash
# Wrong:
git add .env
git add .cursor/mcp.json

# Right: These are gitignored — never force-add them
```

### Mistake 2: Committing Customer Cases
```bash
# Wrong:
git add cases/ZD-12345/

# Right: Only cases/.template/ should be in git
```

### Mistake 3: Customer Data in Docs
```bash
# Wrong:
echo "Customer Acme Corp had this issue..." > docs/apm/example.md

# Right:
echo "A customer experienced this issue..." > docs/apm/example.md
```

### Mistake 4: Force Adding Ignored Files
```bash
# Wrong:
git add -f .env   # Force adds ignored file!

# Right: Never use -f to add files that are gitignored for security
```

---

## Audit Commands

### Check what's staged before committing
```bash
git status
git diff --cached
```

### Check for accidentally committed secrets
```bash
git log -p | grep -i "token\|password\|secret\|api_key"
```

### Remove accidentally committed file
```bash
# If you committed but haven't pushed:
git rm --cached .env
git commit --amend

# If you already pushed:
# 1. IMMEDIATELY rotate all exposed credentials
# 2. Contact your team lead
# 3. May need git-filter-repo or BFG Repo-Cleaner
```

---

## Summary

### Safe to Share (Commit)
- Documentation, templates, scripts, web dashboard
- AI rules, hooks, skills
- Configuration templates (`.example` files)
- Anonymized troubleshooting guides

### Never Share (Local Only)
- Real credentials (`.env`, `mcp.json`)
- Customer cases (`cases/ZD-*`)
- Archived tickets (`archive/*`)
- Any customer data or PII
- Personal editor settings

### Goal
Create a **shared knowledge base and tooling** for the TSE team while **protecting customer data and credentials**.
