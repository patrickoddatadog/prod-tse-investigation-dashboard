#!/usr/bin/env python3
"""
Ticket Dash — Local Web App

Run with: python app.py
Then open: http://localhost:5001
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

from flask import Flask, render_template, abort, request, redirect, url_for
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

BASE_DIR = Path(__file__).parent.resolve()
CASES_DIR = BASE_DIR / "cases"
ARCHIVE_DIR = BASE_DIR / "archive"
SOLUTIONS_DIR = BASE_DIR / "solutions"
TEMPLATES_DIR = BASE_DIR / "templates"
DOCS_DIR = BASE_DIR / "docs"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "web" / "templates"),
    static_folder=str(BASE_DIR / "web" / "static"),
)

MD_EXTENSIONS = [
    TableExtension(),
    FencedCodeExtension(),
    CodeHiliteExtension(css_class="codehilite", guess_lang=False),
    "nl2br",
]


def render_md(text: str) -> str:
    return markdown.markdown(text, extensions=MD_EXTENSIONS)


def parse_quick_info(readme_text: str) -> dict:
    """Extract Quick Info table fields from a case README.md."""
    info = {}
    table_pattern = re.compile(
        r"\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|"
    )
    for match in table_pattern.finditer(readme_text):
        key = match.group(1).strip()
        value = match.group(2).strip()
        if value and value != "Value":
            info[key] = value
    return info


_RESPONSE_HEADING_RE = re.compile(
    r"^##\s+(?:Draft|Proposed)\s+(?:Customer\s+)?(?:Response|Follow[- ]?Up\s+Message)",
    re.IGNORECASE,
)

_NEXT_STEPS_HEADING_RE = re.compile(
    r"^##\s+(?:Recommended\s+)?Next\s+Steps",
    re.IGNORECASE,
)

_LEADERSHIP_HEADING_RE = re.compile(
    r"^##\s+(?:TLDR\s+Handover|Leadership\s+Summary|Executive\s+Summary)",
    re.IGNORECASE,
)

_ZOOM_CALL_HEADING_RE = re.compile(
    r"^##\s+(?:(?:Proposed\s+)?Zoom\s+Call\s+Agenda|Zoom\s+Call|Call\s+Preparation)",
    re.IGNORECASE,
)



def _extract_section(text: str, heading_re) -> str:
    """Extract a markdown section matching heading_re, up to next ## or ---."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if heading_re.match(line.strip()):
            start = i
            break
    if start is None:
        return ""
    body_lines = []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("## ") or stripped == "---":
            break
        body_lines.append(line)
    return "\n".join(body_lines).strip()


def extract_proposed_response(notes_raw: str) -> str:
    return _extract_section(notes_raw, _RESPONSE_HEADING_RE)


def extract_issue_summary(readme_raw: str) -> str:
    """Pull the Issue Summary section from README.md."""
    return _extract_section(
        readme_raw,
        re.compile(r"^##\s+Issue\s+Summary", re.IGNORECASE),
    )


def extract_next_steps(notes_raw: str) -> str:
    """Pull the Next Steps / Recommended Next Steps section from notes.md."""
    return _extract_section(notes_raw, _NEXT_STEPS_HEADING_RE)


def extract_leadership_summary(notes_raw: str) -> str:
    result = _extract_section(
        notes_raw,
        re.compile(r"^##\s+Leadership\s+Summary", re.IGNORECASE),
    )
    if not result:
        result = _extract_section(notes_raw, _LEADERSHIP_HEADING_RE)
    return result


def extract_zoom_call(notes_raw: str) -> str:
    return _extract_section(notes_raw, _ZOOM_CALL_HEADING_RE)




def get_case_dirs():
    if not CASES_DIR.exists():
        return []
    return sorted(
        [
            d
            for d in CASES_DIR.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )


def get_archive_dirs():
    if not ARCHIVE_DIR.exists():
        return []
    months = []
    for d in sorted(ARCHIVE_DIR.iterdir(), reverse=True):
        if d.is_dir():
            files = sorted(d.glob("ZD-*.md"))
            months.append({"name": d.name, "path": d, "files": files})
    return months


def load_case(case_id: str) -> Optional[dict]:
    case_dir = CASES_DIR / case_id
    if not case_dir.exists():
        return None

    readme_path = case_dir / "README.md"
    notes_path = case_dir / "notes.md"

    readme_raw = readme_path.read_text() if readme_path.exists() else ""
    notes_raw = notes_path.read_text() if notes_path.exists() else ""

    info = parse_quick_info(readme_raw)

    status = info.get("Status", "Unknown")
    priority = info.get("Priority", "Unknown")

    proposed_raw = extract_proposed_response(notes_raw)
    summary_raw = extract_issue_summary(readme_raw)
    next_steps_raw = extract_next_steps(notes_raw)
    leadership_raw = extract_leadership_summary(notes_raw)
    zoom_raw = extract_zoom_call(notes_raw)

    requester = (
        info.get("Requester", "")
        or info.get("Contact", "")
    )
    if requester:
        requester = re.sub(r"\s*\(.*?\)\s*", "", requester).strip()
        requester = re.sub(r"\s*\S+@\S+\s*", "", requester).strip()
    if not requester:
        customer = info.get("Customer", "")
        paren = re.search(r"\(([^)]+)\)", customer)
        if paren:
            val = paren.group(1)
            if not re.match(r"(?i)(org.?id|visa|inc|ltd|llc|ag)\b", val):
                requester = val

    return {
        "id": case_id,
        "dir": case_dir,
        "info": info,
        "status": status,
        "requester": requester,
        "priority": priority,
        "customer": info.get("Customer", "Unknown"),
        "product_area": info.get("Product Area", "—"),
        "assigned": info.get("Assigned TSE", "—"),
        "started": info.get("Started", "—"),
        "readme_raw": readme_raw,
        "readme_html": render_md(readme_raw),
        "notes_raw": notes_raw,
        "notes_html": render_md(notes_raw),
        "has_notes": bool(notes_raw.strip()),
        "proposed_response_raw": proposed_raw,
        "proposed_response_html": render_md(proposed_raw) if proposed_raw else "",
        "issue_summary_raw": summary_raw,
        "issue_summary_html": render_md(summary_raw) if summary_raw else "",
        "next_steps_raw": next_steps_raw,
        "next_steps_html": render_md(next_steps_raw) if next_steps_raw else "",
        "leadership_raw": leadership_raw,
        "leadership_html": render_md(leadership_raw) if leadership_raw else "",
        "zoom_raw": zoom_raw,
        "zoom_html": render_md(zoom_raw) if zoom_raw else "",
        "last_modified": datetime.fromtimestamp(case_dir.stat().st_mtime),
    }


# ── Routes ──────────────────────────────────────────────────────────────────


@app.route("/")
def dashboard():
    cases = []
    for d in get_case_dirs():
        case = load_case(d.name)
        if case:
            cases.append(case)

    status_filter = request.args.get("status", "").lower()
    priority_filter = request.args.get("priority", "").lower()
    search_query = request.args.get("q", "").lower()

    filtered = cases
    if status_filter:
        filtered = [c for c in filtered if c["status"].lower() == status_filter]
    if priority_filter:
        filtered = [c for c in filtered if c["priority"].lower() == priority_filter]
    if search_query:
        filtered = [
            c
            for c in filtered
            if search_query in c["id"].lower()
            or search_query in c["customer"].lower()
            or search_query in c["product_area"].lower()
            or search_query in c["readme_raw"].lower()
        ]

    statuses = sorted(set(c["status"] for c in cases))
    priorities = sorted(set(c["priority"] for c in cases))

    stats = {
        "total": len(cases),
        "investigating": sum(1 for c in cases if "investigat" in c["status"].lower()),
        "escalated": sum(1 for c in cases if "escalat" in c["status"].lower()),
        "resolved": sum(1 for c in cases if "resolv" in c["status"].lower()),
    }

    return render_template(
        "dashboard.html",
        cases=filtered,
        stats=stats,
        statuses=statuses,
        priorities=priorities,
        current_status=status_filter,
        current_priority=priority_filter,
        current_query=request.args.get("q", ""),
    )


@app.route("/case/<case_id>")
def case_detail(case_id: str):
    case = load_case(case_id)
    if not case:
        abort(404)

    assets = []
    assets_dir = case["dir"] / "assets"
    if assets_dir.exists():
        for f in sorted(assets_dir.rglob("*")):
            if f.is_file():
                assets.append(str(f.relative_to(case["dir"])))

    return render_template("case_detail.html", case=case, assets=assets)


@app.route("/known-issues")
def known_issues():
    ki_path = SOLUTIONS_DIR / "known-issues.md"
    content = ""
    if ki_path.exists():
        content = render_md(ki_path.read_text())
    return render_template("known_issues.html", content=content)


@app.route("/comms-templates")
def comms_templates():
    groups = {}
    if TEMPLATES_DIR.exists():
        for subdir in sorted(TEMPLATES_DIR.iterdir()):
            if subdir.is_dir():
                files = []
                for f in sorted(subdir.glob("*.md")):
                    files.append(
                        {
                            "name": f.stem.replace("-", " ").title(),
                            "filename": f.name,
                            "subdir": subdir.name,
                            "content_html": render_md(f.read_text()),
                            "content_raw": f.read_text(),
                        }
                    )
                if files:
                    groups[subdir.name.replace("-", " ").title()] = files
    return render_template("comms_templates.html", groups=groups)


@app.route("/archive")
def archive():
    months = get_archive_dirs()
    archive_data = []
    for m in months:
        entries = []
        for f in m["files"]:
            raw = f.read_text()
            entries.append(
                {
                    "name": f.stem,
                    "filename": f.name,
                    "month": m["name"],
                    "html": render_md(raw),
                }
            )
        archive_data.append({"name": m["name"], "entries": entries})
    return render_template("archive.html", months=archive_data)


@app.route("/archive/<month>/<filename>")
def archive_detail(month: str, filename: str):
    fpath = ARCHIVE_DIR / month / filename
    if not fpath.exists():
        abort(404)
    raw = fpath.read_text()
    return render_template(
        "archive_detail.html",
        month=month,
        filename=filename,
        content=render_md(raw),
    )


@app.route("/docs")
def docs():
    content_map = {}

    esc_path = DOCS_DIR / "escalation-criteria.md"
    if esc_path.exists():
        content_map["Escalation Criteria"] = render_md(esc_path.read_text())

    if DOCS_DIR.exists():
        for item in sorted(DOCS_DIR.iterdir()):
            if item.is_dir():
                for f in sorted(item.glob("*.md")):
                    label = f"{item.name.title()} / {f.stem.replace('-', ' ').title()}"
                    content_map[label] = render_md(f.read_text())

    return render_template("docs.html", content_map=content_map)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    print("\n  Ticket Dash")
    print("  http://localhost:8501\n")
    app.run(debug=True, port=8501)
