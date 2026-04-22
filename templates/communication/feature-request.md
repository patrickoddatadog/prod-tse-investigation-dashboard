# Feature Request

Use this template for the `## Feature Request` section in `notes.md`. It is written for **internal engineering / product review** (same audience as a JIRA Feature Request or FR triage), not as a verbatim customer email.

If the dashboard exposes a **Feature Request** tab, this section is the source for that view.

---

## Audience

**Engineering and product** evaluating feasibility, priority, and fit. Technical detail is welcome: product areas, versions, identifiers, and exact customer wording where it clarifies the ask.

---

## Required sub-sections (exactly 4)

Use these headings **in order** under `## Feature Request`:

### Description

- What they want, in plain language.
- **Context:** product(s) involved, language/runtime, platform, versions if known.
- **Facts only** for what exists today; separate wish from current behavior.

### User story (who, what, why)

- Prefer: **As a** [role], **I want** [capability], **so that** [outcome].
- One tight paragraph is enough if the classic triple is redundant.

### Pain point and business impact

- Why it matters: time lost, risk, scale (teams, hosts, revenue), or strategic gap.
- State **None / low** explicitly if the ask is quality-of-life only.

### Workaround

- What they do today, step-by-step if useful.
- Use **`None`** (or **None identified**) if there is no workaround.

---

## Example

```markdown
## Feature Request

### Description

The customer wants to **correlate APM traces with DBM** data (query metrics and explain plans) for the same database workload.

**Application:** Python 3.11  
**Database:** PostgreSQL 15.11  

They can use both products today but cannot jump from a trace span to the matching DBM view in one action.

### User story (who, what, why)

**As a** backend engineer responsible for database performance, **I want** to open DBM from an APM database span (or see a linked explain plan / query metrics for that span), **so that** I can tie application behavior to database execution without manual cross-searching.

### Pain point and business impact

Medium efficiency impact: engineers spend time manually matching resource/statement names between APM and DBM. Not a blocker for adoption of either product; improves depth of diagnosis and perceived integration.

### Workaround

Manually search DBM for the resource name (statement) associated with database spans from the tracer to see explain plans or query metrics for that query.
```
