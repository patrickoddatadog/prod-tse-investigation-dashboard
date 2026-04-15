# GitHub Setup for TSE Investigation Hub

This repo is already live at [github.com/patrickoddatadog/pod-tse-investigation-hub](https://github.com/patrickoddatadog/pod-tse-investigation-hub). This guide covers how to clone, contribute, and manage the repository.

---

## For New Team Members: Clone and Set Up

```bash
# 1. Clone the repo
git clone https://github.com/patrickoddatadog/pod-tse-investigation-hub.git
cd pod-tse-investigation-hub

# 2. Set up credentials (NOT in git)
cp .env.example .env
# Edit .env with your Zendesk, Atlassian, GitHub, and OpenAI tokens

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Open in Cursor
cursor .

# 5. Restart Cursor (Cmd+Q, reopen)
# Atlassian and Glean will prompt SSO on first use

# 6. Test — ask Cursor:
# "Search JIRA for open SCRS tickets"
```

**Full setup guide:** See [SETUP.md](SETUP.md)

---

## Repository Structure on GitHub

```
pod-tse-investigation-hub/
├── .cursor/
│   ├── rules/                    # AI behavior rules
│   │   ├── investigation-workflow.mdc
│   │   ├── mandatory-outputs.mdc
│   │   ├── customer-communication.mdc
│   │   ├── escalation-criteria.mdc
│   │   ├── risk-assessment.mdc
│   │   ├── zoom-transcript.mdc
│   │   ├── api-access-constraints.mdc
│   │   ├── tse-context.mdc
│   │   └── output-standards.mdc
│   ├── hooks/                    # Session hooks
│   │   ├── check-pending-escalations.sh
│   │   └── check-pending-transcripts.sh
│   ├── hooks.json                # Hook configuration
│   └── skills/                   # Reusable investigation skills
│       ├── _shared/
│       └── zendesk-ticket/
├── app.py                        # POD Ticket Dashboard (Flask)
├── requirements.txt              # Python dependencies
├── cases/
│   └── .template/                # Template only (cases/* gitignored)
├── docs/                         # Escalation criteria
├── reference/                    # JIRA project codes
├── scripts/                      # CLI tools & utilities
├── templates/                    # Customer communication & escalation templates
├── web/                          # Dashboard HTML templates & CSS
├── .env.example                  # Credential template (safe)
├── .gitignore                    # Protects secrets & customer data
├── README.md
├── SETUP.md
├── QUICK_START.md
├── STRUCTURE.md
├── GIT_STRATEGY.md
└── GITHUB_SETUP.md               # This file
```

**Not on GitHub (by design):**
- `.env` — real credentials (gitignored)
- `.cursor/mcp.json` — MCP credentials (gitignored)
- `cases/ZD-*` — customer case data (gitignored)
- `archive/*` — archived cases (gitignored)

---

## Remotes

The repo has three remotes configured:

| Remote | URL | Purpose |
|--------|-----|---------|
| `personal` | `github.com/patrickoddatadog/pod-tse-investigation-hub` | Public repo (primary) |
| `origin` | `github.com/patrick-odonovan_ddog/tse-investigation-hub` | Work account fork |
| `upstream` | `github.com/eoghanm2013/tse-investigation-hub` | Original repo |

To push changes:
```bash
# Push to the public repo
git push personal main

# Note: If you get auth errors, the macOS keychain may serve credentials
# for the wrong account. Use gh to authenticate:
gh auth switch --user patrickoddatadog
TOKEN=$(gh auth token --user patrickoddatadog) && \
  git -c credential.helper= \
  -c "http.https://github.com/.extraheader=Authorization: basic $(echo -n "patrickoddatadog:${TOKEN}" | base64)" \
  push personal main
```

---

## Contributing

### Making Changes

```bash
# 1. Pull latest
git pull personal main

# 2. Make your changes
# Edit templates, rules, scripts, docs, etc.

# 3. Commit
git add <files>
git commit -m "Description of change"

# 4. Push
git push personal main
```

### What to Commit

- Updated templates and rules
- New troubleshooting docs (anonymized)
- Script improvements
- Dashboard enhancements
- Documentation updates

### What NOT to Commit

- Customer data (`cases/ZD-*`, `archive/*`)
- Real credentials (`.env`, `.cursor/mcp.json`)
- Personal editor settings
- Customer names, logs, screenshots, or PII

See [GIT_STRATEGY.md](GIT_STRATEGY.md) for the full breakdown.

---

## Repository Settings (Optional)

### Branch Protection

If using this as a team repo, consider adding branch protection on `main`:

1. Go to **Settings > Branches > Add rule** for `main`
2. Recommended:
   - Require pull request reviews before merging
   - Require status checks to pass
   - Restrict who can push

### Team Access

1. Go to **Settings > Collaborators and teams**
2. Add team members:
   - **Write** — for active contributors
   - **Read** — for reference only

### Repository Topics

Add topics for discoverability:
- `tse`, `support-engineering`, `investigation`, `cursor-ai`, `datadog`

---

## Share with Team

```
Hey team,

I've set up the TSE Investigation Hub — an AI-powered workspace for
investigating customer cases in Cursor.

Repo: https://github.com/patrickoddatadog/pod-tse-investigation-hub

Features:
- AI-assisted Zendesk ticket investigation via Glean, JIRA, Confluence
- POD Ticket Dashboard (local web UI) at localhost:8501
- Zoom call transcription and summarisation (Whisper + OpenAI)
- Auto-generated customer responses, leadership summaries, handovers
- One-click escalation summary generation for JIRA

Getting started:
1. Clone the repo
2. Follow SETUP.md (5 min)
3. Ask Cursor: "Investigate Zendesk ticket [ID]"

Questions? Check QUICK_START.md or ask in #support-team
```

---

## Troubleshooting

### Permission Denied
```
ERROR: Permission to patrickoddatadog/pod-tse-investigation-hub.git denied
```
1. Verify you have access to the repo
2. Check SSH key: `ssh -T git@github.com`
3. Or switch `gh` auth: `gh auth switch --user patrickoddatadog`

### Repository Not Found
```
ERROR: Repository not found
```
1. Check the remote URL: `git remote -v`
2. Ensure you're authenticated as the correct GitHub user
3. Update if wrong: `git remote set-url personal https://github.com/patrickoddatadog/pod-tse-investigation-hub.git`

### Accidentally Pushed Secrets

1. **IMMEDIATELY** rotate the exposed credentials (Zendesk, Atlassian, GitHub, OpenAI tokens)
2. Remove from history — contact team lead, may need `git-filter-repo` or BFG Repo-Cleaner
3. Prevention: always check `git status` and `git diff --cached` before committing; never use `git add -f` on ignored files

---

## Security Checklist

Before every push:

- [ ] No real credentials in files
- [ ] No customer names or data
- [ ] No Zendesk ticket IDs in commit messages
- [ ] `.gitignore` is protecting sensitive files
- [ ] Only sharing templates, rules, scripts, and docs — not actual cases
