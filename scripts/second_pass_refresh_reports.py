from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REV = ROOT / "revised_second_pass"
LETTERS = REV / "letters"
TODAY = "2026-08-18"

FIELDS = [
    "gautier_id",
    "gautier_number",
    "recipient",
    "old_edition_numbers",
    "conventional_title_or_incipit",
    "gautier_pages",
    "pg_location",
    "gibi_page",
    "source_packet",
    "source_condition",
    "translation_status",
    "confidence",
    "identification_confidence",
    "notes",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_line(text: str, pattern: str, default: str = "") -> str:
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else default


def parse_translation(path: Path) -> dict[str, str]:
    text = read_text(path)
    gid = find_line(text, r"^# (G\d{3}) Translation V2$")
    if not gid:
        gid = path.parent.name
    pg_location = find_line(text, r"^- PG / source location:\s*(.*)$")
    source_condition = find_line(text, r"^- Source condition:\s*(.*)$")
    packet_match = re.search(r"^.*?\b(PG\d{3})\b", pg_location) if not source_condition.startswith("absent") else None
    return {
        "gautier_id": gid,
        "gautier_number": str(int(gid[1:])),
        "recipient": find_line(text, r"^- Recipient:\s*(.*)$"),
        "old_edition_numbers": find_line(text, r"^- Old numbering:\s*(.*)$"),
        "conventional_title_or_incipit": find_line(text, r"^- Conventional title / incipit:\s*(.*)$"),
        "gautier_pages": find_line(text, r"^- Gautier page range:\s*(.*)$").replace("[not yet verified]", ""),
        "pg_location": pg_location,
        "source_packet": packet_match.group(1) if packet_match else "",
        "source_condition": source_condition,
        "translation_status": find_line(text, r"^Second-pass status:\s*(.*)$"),
        "confidence": find_line(text, r"^Confidence category:\s*(.*)$"),
        "identification_confidence": find_line(text, r"^- Identification confidence:\s*(.*)$"),
        "notes": "",
    }


def load_existing_master() -> dict[str, dict[str, str]]:
    path = REV / "master_concordance.csv"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as f:
        return {row["gautier_id"]: row for row in csv.DictReader(f)}


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


NOTE_OVERRIDES = {
    "G001": "Known source gap: early Gautier letter not recovered locally; do not confuse with duplicate PG001/G008.",
    "G002": "Known source gap: early Gautier letter not recovered locally; do not confuse with duplicate PG002/G044.",
    "G003": "Known source gap: early Gautier letter not recovered locally; do not confuse with duplicate PG003/G045.",
    "G004": "Targeted correction: meteorological phrase revised from 'bright wind' to 'that squall'; PG OCR still uncollated.",
    "G006": "Targeted PG OCR check completed; no material semantic correction made.",
    "G012": "Targeted PG OCR check completed; localized OCR uncertainty remains around representative/salve/fish-closing details.",
    "G014": "Recipient metadata revised to bishop of Cyprus per GIBI; Gautier confirmation still required.",
    "G018": "Terminology normalized in v2: doux of Skopje, not modernized 'duke'.",
    "G045": "Targeted PG OCR check completed; source remains truncated and must not be completed by conjecture.",
    "G052": "Targeted PG OCR check completed; courier name and Frankish-incursion details remain OCR-sensitive.",
    "G058": "Targeted PG OCR check completed; clipped final prayer preserved rather than supplied.",
    "G063": "Known source gap: GIBI row is '?' on p. 152; local extraction has no secure complete text.",
    "G082": "Targeted PG OCR check completed; juridical terminology still needs Gautier collation.",
    "G096": "Targeted PG OCR check completed; fiscal vocabulary and units remain C-level until Gautier collation.",
    "G103": "Targeted PG OCR check completed; no material semantic correction made in G103 unit within merged PG066.",
    "G104": "Terminology normalized in v2: protonotary of the doux of Attaleia.",
    "G105": "Terminology normalized in v2: doux of Dyrrachium.",
    "G107": "Targeted PG OCR check completed; no material semantic correction made.",
    "G121": "Short-letter PG OCR check completed; closing body/stream metaphor remains OCR-sensitive.",
    "G122": "Short-letter PG OCR check completed; no material semantic correction made; see-name needs Gautier.",
    "G123": "Terminology normalized in v2: sebastos and doux of Beroia.",
    "G125": "Known source gap: local PG084 contains only corrupt heading/no continuous body.",
    "G126": "Short-letter PG OCR check completed; boundary with G127 in merged PG088 confirmed.",
    "G134": "Corrected indexing: genuine G134 is Demetrios/liturgy, not Tivanios; no local Greek recovered.",
    "G135": "Corrected indexing: Tivanios/Tigranes Armenian Christological fragment reassigned here from first-pass G134; two doctrinal/lexical corrections made.",
}

GIBI_PAGE_OVERRIDES = {
    "G134": "",
    "G135": "228",
}

AUDITED_SAMPLE = [
    ("G004", "PG093", "meteorological lexical correction"),
    ("G006", "PG006", "no material semantic correction"),
    ("G012", "PG100", "localized OCR uncertainty"),
    ("G014", "PG035", "recipient metadata revised; no English correction"),
    ("G045", "PG003", "truncated source preserved"),
    ("G052", "PG012", "localized OCR uncertainty"),
    ("G058", "PG019", "truncated closing preserved"),
    ("G082", "PG047", "juridical terms flagged"),
    ("G096", "PG060", "fiscal terms flagged"),
    ("G103", "PG066", "merged packet unit checked"),
    ("G107", "PG069", "no material semantic correction"),
    ("G121", "PG083", "short bereavement letter checked"),
    ("G122", "PG085", "short bereavement letter checked"),
    ("G126", "PG088", "boundary with G127 confirmed"),
    ("G135", "PG022", "indexing and Christological phrasing corrected"),
]


def refresh_master() -> list[dict[str, str]]:
    existing = load_existing_master()
    rows: list[dict[str, str]] = []
    for n in range(1, 136):
        gid = f"G{n:03d}"
        path = LETTERS / gid / "translation_v2.md"
        parsed = parse_translation(path)
        old = existing.get(gid, {})
        row = {field: "" for field in FIELDS}
        row.update(old)
        row.update(parsed)
        row["gibi_page"] = GIBI_PAGE_OVERRIDES.get(gid, old.get("gibi_page", row.get("gibi_page", "")))
        row["notes"] = NOTE_OVERRIDES.get(gid, old.get("notes", ""))
        rows.append(row)
    write_csv(REV / "master_concordance.csv", rows, FIELDS)
    return rows


def refresh_revision_log() -> None:
    entries = [
        {
            "date": TODAY,
            "gautier_id": "ALL",
            "category": "workflow",
            "summary": "Created revised_second_pass layer preserving first-pass 04_letters files.",
            "evidence": "Local project architecture; user preservation requirement.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G134/G135",
            "category": "indexing_correction",
            "summary": "Corrected local G134/G135 assignment: Tivanios/Tigranes Armenian fragment belongs to G135; genuine G134 is Demetrios/liturgy and is missing locally.",
            "evidence": "Pinakes lists distinct Ep. 134 and Ep. 135 witnesses; Mullett identifies G135 as the Tibanios/Tigranes fragment and G134 as Demetrios/liturgy.",
            "source_urls": "https://pinakes.irht.cnrs.fr/notices/bibliographie/3BQNCNMD/; https://dokumen.pub/theophylact-of-ochrid-reading-the-letters-of-a-byzantine-archbishop-9780860785491-9781138260528.html",
        },
        {
            "date": TODAY,
            "gautier_id": "G001-G003",
            "category": "source_gap",
            "summary": "Confirmed local PG001-PG003 packets are old-edition duplicate packets for later Gautier letters, not recovered Gautier G001-G003.",
            "evidence": "PG001 matches G008; PG002 matches G044; PG003 matches G045 by heading and opening text.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G063",
            "category": "source_gap",
            "summary": "Preserved G063 as incomplete; local GIBI row is '?' and no secure Greek body is present.",
            "evidence": "Local GIBI index p. 152 and first-pass source note.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G125",
            "category": "source_gap",
            "summary": "Preserved G125 as incomplete; local PG084 packet contains only a corrupt heading/no continuous Greek body.",
            "evidence": "Local PG084 extraction length is too small to support a translation.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G004",
            "category": "lexical_correction",
            "summary": "Revised meteorological phrase from 'that bright wind' to 'that squall'.",
            "evidence": "PG093 context concerns violent wind/storm vocabulary, not brightness.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G018/G104/G105/G123",
            "category": "technical_terminology",
            "summary": "Standardized Byzantine administrative title as doux rather than modern 'duke'.",
            "evidence": "Project authority-list policy for doux; local headings and contexts use Byzantine office terminology.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G135",
            "category": "translation_correction",
            "summary": "Revised two Christological-fragment phrases: iron analogy now 'elongated and blade-like'; confused-union phrase now 'not one rather than the other'.",
            "evidence": "PG004 wording and comparison against the local first-pass translation.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G006/G012/G014/G045/G052/G058/G082/G096/G103/G107/G121/G122/G126/G135",
            "category": "targeted_audit",
            "summary": "Completed a 15-letter targeted second-pass sample across early, middle, late, short, long, administrative, damaged, and theological material.",
            "evidence": "Per-letter audit.md files and sample_audit.md.",
            "source_urls": "",
        },
    ]
    write_csv(REV / "revision_log.csv", entries, ["date", "gautier_id", "category", "summary", "evidence", "source_urls"])


def refresh_exception_report(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["confidence"] for row in rows)
    audited = {gid for gid, _, _ in AUDITED_SAMPLE}
    d_rows = [row for row in rows if row["confidence"] == "D"]
    c_rows = [row for row in rows if row["confidence"] == "C"]
    audited_c = [row for row in c_rows if row["gautier_id"] in audited]
    pending_c = [row for row in c_rows if row["gautier_id"] not in audited]

    lines = [
        "# Exception Report",
        "",
        f"Created: {TODAY}",
        "",
        "This report intentionally lists every C or D item. C does not mean unusable; it means the item still lacks the evidence needed for a final scholarly confidence rating, usually Gautier collation or full clause audit.",
        "",
        "## Counts",
        "",
        f"- A: {counts.get('A', 0)}",
        f"- B: {counts.get('B', 0)}",
        f"- C: {counts.get('C', 0)}",
        f"- D: {counts.get('D', 0)}",
        "",
        "## D - Incomplete / Source Missing",
        "",
        "| G | Recipient | Reason | Next evidence needed |",
        "|---|---|---|---|",
    ]
    for row in d_rows:
        next_needed = "Recover Greek from Gautier/manuscript/page image."
        if row["gautier_id"] == "G125":
            next_needed = "Recover readable Greek for corrupt PG084 slot."
        if row["gautier_id"] == "G134":
            next_needed = "Obtain Gautier I, 335-343 or a verified witness for the Demetrios/liturgy letter."
        lines.append(f"| {row['gautier_id']} | {row['recipient']} | {row['notes']} | {next_needed} |")

    lines.extend([
        "",
        "## C - Audited But Still Provisional",
        "",
        "| G | Recipient | Source | Reason |",
        "|---|---|---|---|",
    ])
    for row in audited_c:
        lines.append(f"| {row['gautier_id']} | {row['recipient']} | {row['pg_location']} | {row['translation_status']}; {row['notes']} |")

    lines.extend([
        "",
        "## C - Pending Full Second-Pass Audit",
        "",
        "| G | Recipient | Source | Reason |",
        "|---|---|---|---|",
    ])
    for row in pending_c:
        lines.append(f"| {row['gautier_id']} | {row['recipient']} | {row['pg_location']} | {row['translation_status']}; {row['source_condition']} |")

    (REV / "exception_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def refresh_sample_audit(rows: list[dict[str, str]]) -> None:
    by_gid = {row["gautier_id"]: row for row in rows}
    lines = [
        "# Targeted Second-Pass Sample Audit",
        "",
        f"Created: {TODAY}",
        "",
        "This is not a final corpus-wide clause audit. It records the 15 source-backed checks completed in this revision layer and keeps their remaining uncertainty visible.",
        "",
        "| G | Source | Result | Confidence |",
        "|---|---|---|---|",
    ]
    for gid, source, result in AUDITED_SAMPLE:
        row = by_gid[gid]
        lines.append(f"| {gid} | {source} | {result}; status `{row['translation_status']}` | {row['confidence']} |")
    lines.extend([
        "",
        "## Systematic Findings",
        "",
        "- The first-pass translation is often closer to the Greek than expected in checked samples.",
        "- The most common unresolved risk is OCR corruption around proper names, fiscal terminology, and page breaks.",
        "- Clear hallucination was not found in the checked sample; the larger risk is overconfident smoothing of damaged or compressed Greek.",
        "- G127 remains a high-priority long-letter audit because it shares PG088 with G126 and contains dense comic/classical material.",
    ])
    (REV / "sample_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def refresh_qc_report(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["confidence"] for row in rows)
    dirs = sorted(p.name for p in LETTERS.iterdir() if p.is_dir() and re.fullmatch(r"G\d{3}", p.name))
    expected = [f"G{n:03d}" for n in range(1, 136)]
    missing = [gid for gid in expected if gid not in dirs]
    extra = [gid for gid in dirs if gid not in expected]

    packet_to_gids: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        if row["source_packet"]:
            packet_to_gids[row["source_packet"]].append(row["gautier_id"])
    duplicated_packets = {k: v for k, v in packet_to_gids.items() if len(v) > 1}

    status_counts = Counter(row["translation_status"] for row in rows)
    audited = {gid for gid, _, _ in AUDITED_SAMPLE}
    d_ids = [row["gautier_id"] for row in rows if row["confidence"] == "D"]

    lines = [
        "# Second-Pass QC Report",
        "",
        f"Created: {TODAY}",
        "",
        "## Corpus Accounting",
        "",
        f"- Letter directories found: {len(dirs)}",
        f"- Expected sequence G001-G135 present: {'yes' if not missing and not extra else 'no'}",
        f"- Missing directories: {', '.join(missing) if missing else 'none'}",
        f"- Extra directories: {', '.join(extra) if extra else 'none'}",
        f"- Confidence counts: A={counts.get('A', 0)}, B={counts.get('B', 0)}, C={counts.get('C', 0)}, D={counts.get('D', 0)}",
        f"- D/incomplete letters: {', '.join(d_ids)}",
        "",
        "## Numbering Checks",
        "",
        "- G134/G135 explicitly resolved in v2: G134 is Demetrios/liturgy and remains D; G135 is the Tivanios/Tigranes Armenian Christological fragment.",
        "- First-pass translations in `04_letters/` were not overwritten.",
        "- `revised_second_pass/letters/G135/translation_v2.md` carries the reassigned fragment; `revised_second_pass/letters/G134/translation_v2.md` intentionally contains no fabricated translation.",
        "",
        "## Duplicate Source Packets",
        "",
    ]
    if duplicated_packets:
        for packet, gids in sorted(duplicated_packets.items()):
            lines.append(f"- {packet}: {', '.join(gids)}")
    else:
        lines.append("- none detected")

    lines.extend([
        "",
        "## Status Counts",
        "",
    ])
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")

    lines.extend([
        "",
        "## Targeted Audits Completed",
        "",
        f"- {len(AUDITED_SAMPLE)} letters checked against local Greek extractions: {', '.join(gid for gid, _, _ in AUDITED_SAMPLE)}",
        "- No item has been raised above C because Gautier collation has not been completed.",
        "- No D item has been filled from summary or conjecture.",
        "",
        "## Remaining Risks",
        "",
        "- Most translations remain copied first-pass texts pending direct clause audit.",
        "- Gautier page ranges are still largely unfilled in the local concordance.",
        "- The authority list is preliminary and needs expansion after full prosopographical work.",
        "- Long merged packets, especially G127, still need detailed boundary and clause checks.",
    ])
    (REV / "qc_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = refresh_master()
    refresh_revision_log()
    refresh_exception_report(rows)
    refresh_sample_audit(rows)
    refresh_qc_report(rows)


if __name__ == "__main__":
    main()
