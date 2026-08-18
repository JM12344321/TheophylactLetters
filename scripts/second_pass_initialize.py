#!/usr/bin/env python3
"""Create the second-pass revision layer without overwriting first-pass files.

This script is deliberately conservative. It copies first-pass English into a
versioned layer as an auditable baseline, records source identity, and marks
each letter's confidence according to the evidence actually present. It does
not upgrade a letter merely because a translation file exists.
"""

from __future__ import annotations

import csv
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LETTERS = ROOT / "04_letters"
REV = ROOT / "revised_second_pass"
TODAY = date(2026, 8, 18).isoformat()

PINAKES_GAUTIER_URL = "https://pinakes.irht.cnrs.fr/notices/bibliographie/3BQNCNMD/"
MULLETT_URL = "https://dokumen.pub/theophylact-of-ochrid-reading-the-letters-of-a-byzantine-archbishop-9780860785491-9781138260528.html"


@dataclass
class LetterRecord:
    gid: str
    gnum: int
    v1_status: str
    recipient: str
    old_numbering: str
    source: str
    date_or_range: str
    english: str
    translator_notes: str
    unresolved: str
    source_packet: str
    pg_marker: str
    pg_chars: str
    gibi_title_bg: str
    gibi_page: str
    source_condition: str
    translation_status: str
    confidence: str
    identification_confidence: str
    gautier_pages: str
    pg_location: str
    notes: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1).strip() if match else ""


def metadata_value(text: str, key: str) -> str:
    match = re.search(rf"^- {re.escape(key)}:\s*(.*)$", text, re.M)
    return match.group(1).strip() if match else ""


def status_value(text: str) -> str:
    match = re.search(r"^Status:\s*(.*)$", text, re.M)
    return match.group(1).strip() if match else ""


def load_gibi_index() -> dict[str, dict[str, str]]:
    path = ROOT / "03_gautier_index" / "gibi_letter_index.csv"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as f:
        return {row["gautier_id"]: row for row in csv.DictReader(f)}


def load_pg_index() -> dict[str, dict[str, str]]:
    path = ROOT / "02_sources" / "pg126" / "letter_extractions" / "pg_letter_extractions.csv"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        return {row["pg_unit"]: row for row in csv.DictReader(f)}


def packet_from_source(source: str) -> str:
    explicit = re.search(r"\bpacket\s+(PG\d{3})\b", source, re.I)
    if explicit:
        return explicit.group(1)
    for match in re.finditer(r"\b(PG\d{3})\b", source):
        packet = match.group(1)
        if packet != "PG126":
            return packet
    return ""


def source_condition_from_status(status: str, source: str) -> str:
    lowered = f"{status} {source}".lower()
    if "source_text_not_recovered" in lowered or "no greek" in lowered or "no recoverable" in lowered:
        return "absent_or_not_recovered"
    if "truncated" in lowered:
        return "truncated_ocr"
    if "damaged" in lowered or "corrupt" in lowered:
        return "damaged_or_corrupt_ocr"
    if "merged" in lowered or "continuation" in lowered:
        return "merged_or_continuation_packet"
    if "gibi" in lowered and "pg" not in lowered:
        return "gibi_parallel_text_only"
    if "ocr" in lowered or "pg" in lowered:
        return "pg_ocr_not_collated"
    return "unclassified"


def extract_records() -> list[LetterRecord]:
    gibi = load_gibi_index()
    pg_index = load_pg_index()
    rows: list[LetterRecord] = []

    for n in range(1, 136):
        gid = f"G{n:03d}"
        path = LETTERS / gid / "translation.md"
        text = read_text(path) if path.exists() else ""
        v1_status = status_value(text)
        recipient = metadata_value(text, "Recipient")
        old_numbering = metadata_value(text, "Old numbering")
        source = metadata_value(text, "Source")
        date_or_range = metadata_value(text, "Date")
        english = section(text, "English Translation")
        translator_notes = section(text, "Translator's Notes")
        unresolved = section(text, "Unresolved Questions")
        source_packet = packet_from_source(source)

        # Correct the known G134/G135 mis-assignment in the revision layer only.
        if gid == "G134":
            v1_status = "v1_misindexed_as_tivanios; corrected_in_second_pass"
            recipient = "Demetrios Hephaistos"
            old_numbering = "[not recovered locally; verify in Gautier]"
            source = (
                "Genuine Gautier G134 not recovered in local project sources. "
                "Mullett identifies it as a letter to Demetrios on the liturgy; "
                "Pinakes distinguishes manuscript witnesses for Ep. 134."
            )
            english = (
                "No defensible English translation is supplied in this second-pass layer, "
                "because the Greek text of genuine Gautier G134 has not been recovered in "
                "the local source set. The first-pass text formerly filed as G134 is the "
                "Tivanios/Tigranes Armenian Christological fragment and has been reassigned "
                "to G135 here."
            )
            translator_notes = (
                "- Corrected corpus identity: genuine G134 is the Demetrios/liturgy item, "
                "not the Tivanios Armenian fragment.\n"
                f"- Evidence: Pinakes distinguishes Ep. 134 witnesses from Ep. 135; Mullett "
                "identifies G134 as addressed to Demetrios and concerning liturgical embraces."
            )
            unresolved = (
                "- [ ] Obtain Gautier's printed Greek for G134, cited by Mullett as I, 335-343.\n"
                "- [ ] Collate against the Athens EBE 1431 and/or Sinai gr. 1117 witnesses if possible."
            )
            source_packet = ""

        elif gid == "G135":
            old_g134 = read_text(LETTERS / "G134" / "translation.md")
            v1_status = "reassigned_from_first_pass_G134_pending_clause_audit"
            recipient = "Tivanios/Tigranes the Armenian"
            old_numbering = "Finetti XX; previously misfiled locally as G134"
            source = (
                "PG126 OCR packet PG022 and GIBI 9.2 pp. 228-229; identified by Mullett as "
                "G135, Gautier II 595-597, a fragment from a letter to Tibanios the Armenian."
            )
            english = section(old_g134, "English Translation")
            translator_notes = (
                "- Corrected corpus identity: the Tivanios/Tigranes Armenian Christological "
                "fragment is G135, not G134.\n"
                "- Subject: natures and wills of Christ; iron/fire analogy.\n"
                f"- Evidence: Mullett identifies G135 as the fragment to Tibanios/Tigranes; "
                "Pinakes distinguishes Ep. 135 as an excerpt in Vat. Reg. gr. 057."
            )
            unresolved = (
                "- [ ] Collate the PG/GIBI text against Gautier II, 595-597.\n"
                "- [ ] Verify whether Tibanios should be identified with Tigranes in final prosopography."
            )
            source_packet = "PG022"

        pg = pg_index.get(source_packet, {})
        source_condition = source_condition_from_status(v1_status, source)
        translation_status = "baseline_first_pass_copied_pending_clause_audit"
        confidence = "C"
        identification_confidence = "medium"
        notes = ""
        gautier_pages = ""

        if source_condition == "absent_or_not_recovered":
            translation_status = "incomplete_source_missing_no_translation"
            confidence = "D"
            identification_confidence = "low"
        elif gid in {"G004", "G014", "G103", "G107"}:
            notes = "Priority sample/spot-check target from prior audit notes."

        if gid == "G001":
            notes = "Known source gap: early Gautier letter not recovered locally; do not confuse with duplicate PG001/G008."
        elif gid == "G002":
            notes = "Known source gap: early Gautier letter not recovered locally; do not confuse with duplicate PG002/G044."
        elif gid == "G003":
            notes = "Known source gap: early Gautier letter not recovered locally; do not confuse with duplicate PG003/G045."
        elif gid == "G063":
            notes = "Known source gap: GIBI row is '?' on p. 152; local extraction has no secure complete text."
            gautier_pages = "II 357-359 (from prior local note; verify)"
        elif gid == "G125":
            notes = "Known source gap: local PG084 contains only corrupt heading/no continuous body."
        elif gid == "G134":
            translation_status = "incomplete_genuine_g134_missing; old_local_g134_reassigned_to_g135"
            confidence = "D"
            identification_confidence = "high_for_identity_low_for_text"
            source_condition = "absent_or_not_recovered"
            gautier_pages = "I 335-343 (Mullett citation; verify in Gautier)"
            notes = "Corrected indexing: genuine G134 is Demetrios/liturgy, not Tivanios."
        elif gid == "G135":
            translation_status = "reassigned_from_old_local_G134_pending_clause_audit"
            confidence = "C"
            identification_confidence = "high"
            source_condition = "pg_ocr_and_gibi_fragment_not_collated"
            gautier_pages = "II 595-597 (Mullett citation; verify in Gautier)"
            notes = "Corrected indexing: Tivanios/Tigranes Armenian fragment belongs here."

        pg_marker = pg.get("pg_page_marker_start", "")
        pg_chars = pg.get("chars", "")
        pg_location = ""
        if source_packet:
            pg_location = source_packet
            if pg_marker:
                pg_location += f" (PG marker {pg_marker})"

        gr = gibi.get(gid, {})
        rows.append(
            LetterRecord(
                gid=gid,
                gnum=n,
                v1_status=v1_status,
                recipient=recipient,
                old_numbering=old_numbering,
                source=source,
                date_or_range=date_or_range,
                english=english,
                translator_notes=translator_notes,
                unresolved=unresolved,
                source_packet=source_packet,
                pg_marker=pg_marker,
                pg_chars=pg_chars,
                gibi_title_bg=gr.get("gibi_title_bg", ""),
                gibi_page=gr.get("gibi_page", ""),
                source_condition=source_condition,
                translation_status=translation_status,
                confidence=confidence,
                identification_confidence=identification_confidence,
                gautier_pages=gautier_pages,
                pg_location=pg_location,
                notes=notes,
            )
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_translation_v2(row: LetterRecord) -> None:
    out_dir = REV / "letters" / row.gid
    out_dir.mkdir(parents=True, exist_ok=True)
    original = f"04_letters/{row.gid}/translation.md"
    if row.gid == "G135":
        original = "04_letters/G134/translation.md"
    changes = "No substantive translation change yet; first-pass English preserved pending direct clause audit."
    if row.gid == "G134":
        changes = "Removed the misindexed Tivanios translation from this slot in the second-pass layer; marked genuine G134 incomplete."
    elif row.gid == "G135":
        changes = "Reassigned the Tivanios/Tigranes Armenian fragment from old local G134 to Gautier G135."

    unresolved = row.unresolved.strip() or "- [ ] Direct clause-by-clause audit against Greek still required."
    notes = row.translator_notes.strip() or "- No first-pass translator notes."
    english = row.english.strip() or "[No source-backed English translation available.]"

    content = f"""# {row.gid} Translation V2

Second-pass status: {row.translation_status}
Confidence category: {row.confidence}

## Corpus Identity

- Gautier ID: {row.gid}
- Recipient: {row.recipient or '[not recorded]'}
- Old numbering: {row.old_numbering or '[not recorded]'}
- Conventional title / incipit: {row.gibi_title_bg or '[not recorded in local index]'}
- Gautier page range: {row.gautier_pages or '[not yet verified]'}
- PG / source location: {row.pg_location or row.source or '[not recovered]'}
- Source condition: {row.source_condition}
- Identification confidence: {row.identification_confidence}
- Original first-pass file: {original}

## Revised English Translation

{english}

## Consequential Changes From First Pass

- {changes}

## Source And Revision Notes

{notes}

## Unresolved Issues

{unresolved}

## Audit Trail

- {TODAY}: Second-pass layer initialized. Original first-pass translation preserved unchanged.
"""
    (out_dir / "translation_v2.md").write_text(content, encoding="utf-8")

    audit = f"""# {row.gid} Source Identification And Audit

- Clause-by-clause Greek audit status: not_started
- First-pass status: {row.v1_status or '[not recorded]'}
- Source packet used in first pass: {row.source_packet or '[none]'}
- PG marker / packet size: {row.pg_marker or '[unknown]'} / {row.pg_chars or '[unknown]'} chars
- GIBI page: {row.gibi_page or '[not present]'}
- Confidence category: {row.confidence}
- Current exception status: {'yes' if row.confidence in {'C', 'D'} else 'no'}

## Evidence Notes

{row.notes or 'No special evidence note recorded at initialization.'}

## Direct Greek Audit Notes

- Pending.
"""
    (out_dir / "audit.md").write_text(audit, encoding="utf-8")


def write_readme(rows: list[LetterRecord]) -> None:
    counts = Counter(row.confidence for row in rows)
    readme = f"""# Revised Second Pass

Created: {TODAY}

This directory is a preservation layer for a philological second pass over the
first complete working translation in `04_letters/`. The original first-pass
files are not overwritten. Each `translation_v2.md` states whether it is merely
a baseline copy awaiting direct Greek audit or a corrected/revised item.

## Current Status

- A: {counts.get('A', 0)}
- B: {counts.get('B', 0)}
- C: {counts.get('C', 0)}
- D: {counts.get('D', 0)}

At initialization, most complete first-pass translations remain C because they
have not yet been rechecked clause by clause against Greek in this layer. That
is intentional: the revision layer distinguishes existence from verification.

## Key Correction Already Applied

The local first-pass corpus filed the Tivanios/Tigranes Armenian Christological
fragment as G134 and left G135 empty. The second-pass corpus map corrects this:

- G134: genuine Demetrios/liturgy letter; Greek not recovered locally; D.
- G135: Tivanios/Tigranes Armenian Christological fragment; reassigned from old
  local G134; C pending direct Gautier collation.

Evidence recorded in `revision_log.csv` cites Pinakes and Mullett.
"""
    (REV / "README.md").write_text(readme, encoding="utf-8")


def write_authority_list() -> None:
    text = f"""# Authority List And Editorial Policy

Created: {TODAY}

This is a living second-pass authority list. It gives default spellings and
translation policies to prevent drift across the corpus.

## Names And Places

| Greek / form | English policy | Note |
|---|---|---|
| Θεοφύλακτος Ἀχρίδος | Theophylact of Ohrid | Use in project framing. |
| Ἀχρίς / Ἀχρίδα | Achrida in translated text; Ohrid in modern framing | Keeps Theophylact's Byzantine toponym visible. |
| Δημήτριος Ἡφαιστός | Demetrios Hephaistos | Theophylact's brother; keep stable. |
| Τιβάνιος / Τιγράνης | Tivanios/Tigranes | Use Tivanios in the heading when following the lemma; note possible identification with Tigranes. |
| Ἰωάννης Κομνηνός | John Komnenos | Do not flatten family titles into modern offices. |
| Μιχαὴλ Παντέχνης | Michael Pantechnes | Keep the learned name in transliteration. |

## Offices And Technical Terms

| Term | English policy | Note |
|---|---|---|
| σεβαστός | sebastos | Transliterate; explain in notes when needed. |
| σεβαστοκράτωρ | sebastokrator | Transliterate; do not render as generic "prince." |
| χαρτοφύλαξ | chartophylax | Transliterate; ecclesiastical office. |
| οἰκονόμος | oikonomos | Transliterate when an office; translate "steward" only in nontechnical contexts. |
| πρωτονοτάριος | protonotarios | Transliterate. |
| πρωτασηκρῆτις / πρωτοασηκρῆτις | protasekretis / protoasekretis | Prefer protasekretis if Gautier confirms; record variant. |
| πραίτωρ | praetor | Byzantine administrative title; avoid "judge" unless context requires. |
| δοὺξ | doux | Transliterate; do not modernize to "duke" in technical contexts. |
| κανόνικον | kanonikon | Fiscal/ecclesiastical due; preserve term and explain. |
| σταυροπήγιον | stauropegion | Ecclesiastical jurisdiction term; preserve term. |
| σιγίλλιον | sigillion | Preserve as document term. |
| κομμέρκιον | kommerkion | Fiscal/customs term; preserve and note. |
| πρακτορες | praktors | Fiscal agents/collectors; transliterate where office matters. |
| σεκρετικά | sekretika | Fiscal/administrative bureaus; transliterate in rhetorical passages. |

## Biblical And Classical Allusions

Translate Theophylact's Greek wording rather than substituting a modern Bible
translation. Add references in notes only when the allusion is secure. Use
"probably alludes to" where the identification is plausible but not certain.
"""
    (REV / "authority_list.md").write_text(text, encoding="utf-8")


def write_revision_log() -> None:
    rows = [
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
            "evidence": "Pinakes lists distinct Ep. 134 and Ep. 135 witnesses; Mullett identifies G135 as the fragment to Tibanios/Tigranes and G134 as to Demetrios on liturgy/liturgical embraces.",
            "source_urls": f"{PINAKES_GAUTIER_URL}; {MULLETT_URL}",
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
            "evidence": "Local PG084 extraction length 40 characters plus first-pass source note.",
            "source_urls": "",
        },
    ]
    write_csv(
        REV / "revision_log.csv",
        rows,
        ["date", "gautier_id", "category", "summary", "evidence", "source_urls"],
    )


def write_concordance(rows: list[LetterRecord]) -> None:
    fields = [
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
    data = [
        {
            "gautier_id": row.gid,
            "gautier_number": str(row.gnum),
            "recipient": row.recipient,
            "old_edition_numbers": row.old_numbering,
            "conventional_title_or_incipit": row.gibi_title_bg,
            "gautier_pages": row.gautier_pages,
            "pg_location": row.pg_location,
            "gibi_page": row.gibi_page,
            "source_packet": row.source_packet,
            "source_condition": row.source_condition,
            "translation_status": row.translation_status,
            "confidence": row.confidence,
            "identification_confidence": row.identification_confidence,
            "notes": row.notes,
        }
        for row in rows
    ]
    write_csv(REV / "master_concordance.csv", data, fields)


def write_exception_report(rows: list[LetterRecord]) -> None:
    counts = Counter(row.confidence for row in rows)
    lines = [
        "# Exception Report",
        "",
        f"Created: {TODAY}",
        "",
        "This report intentionally lists every C or D item. At initialization, C means a source-backed first-pass translation exists but has not yet received a direct second-pass clause audit in this layer.",
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
    for row in rows:
        if row.confidence == "D":
            next_needed = "Recover Greek from Gautier/manuscript/page image."
            if row.gid == "G134":
                next_needed = "Obtain Gautier I, 335-343 or Athens/Sinai witness."
            elif row.gid == "G125":
                next_needed = "Recover readable Greek for corrupt PG084 slot."
            lines.append(f"| {row.gid} | {row.recipient} | {row.notes or row.source_condition} | {next_needed} |")

    lines.extend(
        [
            "",
            "## C - Provisional / Pending Direct Clause Audit",
            "",
            "| G | Recipient | Source | Reason |",
            "|---|---|---|---|",
        ]
    )
    for row in rows:
        if row.confidence == "C":
            lines.append(
                f"| {row.gid} | {row.recipient} | {row.pg_location or row.source or '[source not listed]'} | {row.translation_status}; {row.source_condition} |"
            )
    (REV / "exception_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_qc_report(rows: list[LetterRecord]) -> None:
    ids = [row.gid for row in rows]
    duplicates = defaultdict(list)
    for row in rows:
        if row.source_packet:
            duplicates[row.source_packet].append(row.gid)
    dup_lines = [
        f"- {packet}: {', '.join(gids)}"
        for packet, gids in sorted(duplicates.items())
        if len(gids) > 1
    ]
    counts = Counter(row.confidence for row in rows)
    missing_ids = [f"G{n:03d}" for n in range(1, 136) if f"G{n:03d}" not in ids]
    text = f"""# Second-Pass QC Report

Created: {TODAY}

## Inventory

- Letter records generated: {len(rows)}
- Expected range: G001-G135
- Missing IDs: {', '.join(missing_ids) if missing_ids else 'none'}
- Translation V2 files expected: 135

## Confidence Counts

- A: {counts.get('A', 0)}
- B: {counts.get('B', 0)}
- C: {counts.get('C', 0)}
- D: {counts.get('D', 0)}

## Known Numbering And Source Issues

- G134/G135: corrected in second-pass layer. Old local G134 text is G135; genuine G134 remains missing.
- G001-G003: not recovered locally. Local PG001-PG003 extraction packets are duplicate old-edition witnesses for later Gautier letters, not the missing early Gautier letters.
- G063: local source missing/incomplete.
- G125: local PG084 source corrupt/no continuous body.

## Duplicate Source Packets In Concordance

{chr(10).join(dup_lines) if dup_lines else '- None detected by source-packet metadata.'}

## Final Audit Status

The final 15-letter random clause audit has not yet been completed in this layer.
No A or B ratings are assigned until direct Greek comparison has been performed
and recorded.
"""
    (REV / "qc_report.md").write_text(text, encoding="utf-8")


def write_all() -> None:
    if REV.exists():
        shutil.rmtree(REV)
    REV.mkdir(parents=True)
    rows = extract_records()
    for row in rows:
        write_translation_v2(row)
    write_readme(rows)
    write_authority_list()
    write_revision_log()
    write_concordance(rows)
    write_exception_report(rows)
    write_qc_report(rows)


if __name__ == "__main__":
    write_all()
    print(f"Initialized {REV} with 135 letter records.")
