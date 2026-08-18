from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LETTERS = ROOT / "revised_second_pass" / "letters"
TODAY = "2026-08-18"


def find_line(text: str, pattern: str, default: str = "") -> str:
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else default


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    return match.group(1).strip() if match else ""


def audit_label(confidence: str) -> str:
    if confidence == "A":
        return "completed_against_gautier_packet"
    if confidence == "B":
        return "completed_against_gautier_packet_with_localized_uncertainty"
    if confidence == "C":
        return "gautier_packet_identified_pending_full_clause_audit"
    if confidence == "D":
        return "incomplete_fragment_or_lacuna_not_completable_by_conjecture"
    return "unknown"


def write_audit(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    gid = path.parent.name
    confidence = find_line(text, r"^Confidence category:\s*(.*)$")
    status = find_line(text, r"^Second-pass status:\s*(.*)$")
    recipient = find_line(text, r"^- Recipient:\s*(.*)$")
    gautier_pages = find_line(text, r"^- Gautier page range:\s*(.*)$")
    packet = find_line(text, r"^- Gautier source packet:\s*(.*)$")
    pg_location = find_line(text, r"^- PG / source location:\s*(.*)$")
    source_condition = find_line(text, r"^- Source condition:\s*(.*)$")
    id_confidence = find_line(text, r"^- Identification confidence:\s*(.*)$")
    original = find_line(text, r"^- Original first-pass file:\s*(.*)$")
    changes = section(text, "Consequential Changes From First Pass") or "- None recorded."
    notes = section(text, "Source And Revision Notes") or "- None recorded."
    unresolved = section(text, "Unresolved Issues") or "- None recorded."

    current_exception = "yes" if confidence in {"C", "D"} else "no"
    lines = [
        f"# {gid} Source Identification And Audit",
        "",
        f"- Recipient: {recipient}",
        f"- Clause-by-clause Greek audit status: {audit_label(confidence)}",
        f"- Second-pass status: {status}",
        f"- Gautier source packet: {packet}",
        f"- Gautier page range: {gautier_pages}",
        f"- PG / earlier source location: {pg_location}",
        f"- Source condition: {source_condition}",
        f"- Identification confidence: {id_confidence}",
        f"- Confidence category: {confidence}",
        f"- Current exception status: {current_exception}",
        f"- Original first-pass file: {original}",
        "",
        "## Evidence Notes",
        "",
        notes,
        "",
        "## Direct Greek Audit Notes",
        "",
        changes,
        "",
        "## Unresolved Issues",
        "",
        unresolved,
        "",
        "## Audit Trail",
        "",
        f"- {TODAY}: Regenerated from current translation_v2 metadata after Gautier packet collation.",
    ]
    (path.parent / "audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    count = 0
    for path in sorted(LETTERS.glob("G*/translation_v2.md")):
        write_audit(path)
        count += 1
    print(f"Refreshed {count} audit files.")


if __name__ == "__main__":
    main()
