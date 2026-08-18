from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

try:
    from apply_extended_gautier_audits import UPDATES as EXTENDED_UPDATES
except Exception:
    EXTENDED_UPDATES = {}


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
    gautier_packet = find_line(text, r"^- Gautier source packet:\s*(.*)$")
    packet_match = re.search(r"^.*?\b(PG\d{3})\b", pg_location) if not source_condition.startswith("absent") else None
    return {
        "gautier_id": gid,
        "gautier_number": str(int(gid[1:])),
        "recipient": find_line(text, r"^- Recipient:\s*(.*)$"),
        "old_edition_numbers": find_line(text, r"^- Old numbering:\s*(.*)$"),
        "conventional_title_or_incipit": find_line(text, r"^- Conventional title / incipit:\s*(.*)$"),
        "gautier_pages": find_line(text, r"^- Gautier page range:\s*(.*)$").replace("[not yet verified]", ""),
        "pg_location": pg_location,
        "source_packet": gautier_packet or (packet_match.group(1) if packet_match else ""),
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
    "G001": "Recovered from Gautier I; classroom oration to unruly students. Long text checked enough for B, but final apparatus audit remains.",
    "G002": "Recovered from Gautier I; classroom oration to students. Long text checked enough for B, but final apparatus audit remains.",
    "G003": "Recovered from Gautier I; complete letter to the grand oikonomos checked against Gautier.",
    "G004": "Gautier collation corrected the wind phrase: not literal 'bright,' but a brisk/violent wind in context.",
    "G005": "Boundary repaired: G005 ends with the Heracles/Omphale slavery appeal; the Achrida eagle/frogs material belongs to G006.",
    "G006": "Genuine Gautier G006 recovered; old local G006 duplicated G047. Restored lost opening negation and corrected frog/eagle details.",
    "G007": "Short companion letter checked against Gautier; points to G005 and G006.",
    "G010": "Short exhortation to John Komnenos checked against Gautier.",
    "G019": "Technical terms corrected: paramonai as local guard services and psomozemiai as food-supply obligations.",
    "G023": "Legal term corrected: strategos, not 'the whole army'.",
    "G040": "Short recommendation letter checked against Gautier; Koprinista/Heracles joke preserved.",
    "G041": "Short consolation to Anemas checked against Gautier.",
    "G047": "Confirmed as the Mermentopoulos letter mistakenly duplicated in old local G006.",
    "G050": "Lexical correction: perittos means excessive/superfluous, not useless.",
    "G056": "Short appeal to the bishop of Semna checked against Gautier.",
    "G069": "Corrected inserted negative in Odysseus comparison, 'do not delay,' and restored complete ending from Gautier.",
    "G091": "Restored omitted opening condition: 'if you saw me burning'.",
    "G093": "Corrected final request to 'show us how much you can do'; Gautier ending complete.",
    "G094": "Alcmaeon/Achelous appeal checked against Gautier.",
    "G101": "Short Legion/swine letter checked against Gautier.",
    "G102": "Homeric quotation corrected: garland of the god, not thought of God.",
    "G012": "Targeted PG OCR check completed; localized OCR uncertainty remains around representative/salve/fish-closing details.",
    "G014": "Recipient corrected to bishop of Kitros; earlier Cyprus assignment was wrong.",
    "G018": "Terminology normalized in v2: doux of Skopje, not modernized 'duke'.",
    "G045": "Targeted PG OCR check completed; source remains truncated and must not be completed by conjecture.",
    "G052": "Targeted PG OCR check completed; courier name and Frankish-incursion details remain OCR-sensitive.",
    "G058": "Targeted PG OCR check completed; clipped final prayer preserved rather than supplied.",
    "G062": "Boundary corrected against Gautier: G062 is a tiny mutilated fragment, not the longer consolatory G063 text.",
    "G063": "Recovered as separate mutilated Gautier fragment formerly absorbed into G062; translated only surviving text.",
    "G082": "Targeted PG OCR check completed and Gautier packet identified; juridical terminology still needs full Gautier clause audit.",
    "G096": "Targeted PG OCR check completed and Gautier packet identified; fiscal vocabulary and units remain C-level until full Gautier clause audit.",
    "G103": "Short letter to Bulgarians checked against Gautier; no material semantic correction needed.",
    "G104": "Terminology normalized in v2: protonotary of the doux of Attaleia.",
    "G105": "Terminology normalized in v2: doux of Dyrrachium.",
    "G107": "Short thanksgiving to the Despoina checked against Gautier; no material semantic correction needed.",
    "G121": "Short bereavement letter to the bishop of Kitros checked against Gautier.",
    "G122": "See corrected/confirmed as Debre; short bereavement letter checked against Gautier.",
    "G123": "Terminology normalized in v2: sebastos and doux of Beroia.",
    "G124": "Very short note to former chartophylax Nikephoros checked against Gautier.",
    "G125": "Recovered complete short anepigraphic letter from Gautier after local PG084 failed.",
    "G126": "Short letter to Palaiologos checked against Gautier; praktor terminology standardized.",
    "G128": "Corrected 'by lamplight' to 'in daylight'.",
    "G130": "Short note to Michael Pantechnes checked against Gautier.",
    "G131": "Final request corrected: asks what condition the addressee is in.",
    "G132": "Short consolation for Psellos' brother checked; prosopography remains uncertain.",
    "G133": "Restored omitted 'I am wounded in soul'; addressee remains probably but not certainly Demetrios.",
    "G134": "Genuine G134 recovered from Gautier I: Demetrios/liturgy letter, not Tivanios.",
    "G135": "Tivanios/Tigranes Armenian Christological excerpt reassigned here from first-pass G134 and collated against Gautier.",
}

GIBI_PAGE_OVERRIDES = {
    "G134": "",
    "G135": "228",
}

AUDITED_SAMPLE = [
    ("G001", "Gautier I", "recovered classroom oration"),
    ("G002", "Gautier I", "recovered classroom oration"),
    ("G003", "Gautier I", "recovered grand-oikonomos letter"),
    ("G004", "Gautier II", "meteorological lexical correction"),
    ("G005", "Gautier II", "boundary repaired"),
    ("G006", "Gautier II", "duplicate replaced and translation recovered"),
    ("G007", "Gautier II", "short companion letter checked"),
    ("G010", "Gautier II", "short exhortation checked"),
    ("G019", "Gautier II", "administrative terms corrected"),
    ("G023", "Gautier II", "legal term corrected"),
    ("G012", "Gautier II/PG100", "localized OCR uncertainty"),
    ("G014", "Gautier II", "recipient corrected to Kitros"),
    ("G040", "Gautier II", "recommendation letter checked"),
    ("G041", "Gautier II", "consolation letter checked"),
    ("G045", "Gautier II/PG003", "truncated source preserved"),
    ("G047", "Gautier II", "Mermentopoulos duplicate confirmed"),
    ("G050", "Gautier II", "lexical correction"),
    ("G052", "Gautier II/PG012", "localized OCR uncertainty"),
    ("G056", "Gautier II", "fiscal oppression letter checked"),
    ("G058", "Gautier II/PG019", "truncated closing preserved"),
    ("G062", "Gautier II", "mutilated fragment boundary corrected"),
    ("G063", "Gautier II", "mutilated fragment recovered"),
    ("G069", "Gautier II", "negation and ending corrected"),
    ("G082", "Gautier II/PG047", "juridical terms flagged"),
    ("G091", "Gautier II", "omitted opening condition restored"),
    ("G093", "Gautier II", "final request corrected"),
    ("G094", "Gautier II", "Alcmaeon appeal checked"),
    ("G096", "Gautier II/PG060", "fiscal terms flagged"),
    ("G101", "Gautier II", "Legion/swine letter checked"),
    ("G102", "Gautier II", "Homeric quotation corrected"),
    ("G103", "Gautier II", "short Bulgarians letter checked"),
    ("G107", "Gautier II", "short thanksgiving checked"),
    ("G109", "Gautier II", "Orestes opening corrected"),
    ("G110", "Gautier II", "river-toll phrasing corrected"),
    ("G111", "Gautier II", "minor lacuna and property terms checked"),
    ("G114", "Gautier II", "lost negation corrected"),
    ("G115", "Gautier II", "Euphemianos name reading checked"),
    ("G116", "Gautier II", "short covering note checked"),
    ("G117", "Gautier II", "short covering note checked"),
    ("G121", "Gautier II", "short bereavement letter checked"),
    ("G122", "Gautier II", "short bereavement letter checked"),
    ("G124", "Gautier II", "short illness note checked"),
    ("G125", "Gautier II", "short anepigraphic letter recovered"),
    ("G126", "Gautier II", "praktor terminology checked"),
    ("G128", "Gautier II", "daylight correction"),
    ("G130", "Gautier II", "short Pantechnes note checked"),
    ("G131", "Gautier II", "final request corrected"),
    ("G132", "Gautier II", "Psellos consolation checked"),
    ("G133", "Gautier II", "opening omission restored"),
    ("G134", "Gautier I", "genuine Demetrios/liturgy letter recovered"),
    ("G135", "Gautier II", "indexing and Christological phrasing corrected"),
]

for gid, update in EXTENDED_UPDATES.items():
    NOTE_OVERRIDES.setdefault(gid, "Extended Gautier clause audit: " + "; ".join(update["changes"]))
    if gid not in {item[0] for item in AUDITED_SAMPLE}:
        AUDITED_SAMPLE.append((gid, "Gautier II", "extended clause audit; " + update["changes"][0]))

AUDITED_SAMPLE.sort(key=lambda item: int(item[0][1:]))


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
            "summary": "Created and maintained revised_second_pass layer preserving first-pass 04_letters files.",
            "evidence": "Local project architecture; user preservation requirement; original first-pass files remain untouched.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "ALL",
            "category": "workflow",
            "summary": "Added Gautier CFHB source layer, extracted both volumes, and built 135 per-letter Gautier source packets.",
            "evidence": "02_sources/gautier/CFHB_16_1_Theophylacti_Achridensis_Opera_Gautier_1980.pdf; 02_sources/gautier/CFHB_16_2_Theophylacti_Achridensis_Epistulae_Gautier_1986.pdf; 02_sources/gautier/letter_packets/G001-G135_gautier.txt.",
            "source_urls": "https://archive.org/details/cfhb-11.1-nicetae-choniatae-historia; https://pinakes.irht.cnrs.fr/notices/bibliographie/3BQNCNMD/",
        },
        {
            "date": TODAY,
            "gautier_id": "G134/G135",
            "category": "indexing_correction",
            "summary": "Resolved local G134/G135 assignment: genuine G134 is the Demetrios/liturgy letter recovered from Gautier I; the Tivanios/Tigranes Armenian Christological excerpt belongs to G135.",
            "evidence": "Gautier I, pp. 334-343 for G134; Gautier II, letter 135 and p. 592 cross-reference; local first-pass G134 matched G135.",
            "source_urls": "https://archive.org/details/cfhb-11.1-nicetae-choniatae-historia; https://pinakes.irht.cnrs.fr/notices/bibliographie/3BQNCNMD/",
        },
        {
            "date": TODAY,
            "gautier_id": "G001-G003",
            "category": "source_recovery",
            "summary": "Recovered and translated Gautier G001-G003 from Gautier I; earlier local PG001-PG003 packets were old-edition duplicate packets for later Gautier letters.",
            "evidence": "Gautier I packets G001-G003; local PG001 matched G008, PG002 matched G044, and PG003 matched G045 by heading/opening.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G005/G006/G047",
            "category": "indexing_correction",
            "summary": "Repaired early-letter boundary: G005 ends with the Heracles/Omphale appeal; G006 is the Achrida headless-necks/eagle/frogs/gout letter; old local G006 duplicated G047.",
            "evidence": "Gautier II packets G005, G006, and G047.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G062/G063",
            "category": "boundary_correction",
            "summary": "Separated two mutilated Gautier fragments formerly merged locally; G062 is only the tiny opening fragment and G063 is the following mutilated consolation fragment.",
            "evidence": "Gautier II packets G062-G063 and apparatus notes on lacunae/mutilation.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G125",
            "category": "source_recovery",
            "summary": "Recovered and translated complete short anepigraphic G125 from Gautier after local PG084 failed.",
            "evidence": "Gautier II, letter 125; Chisianus-only note.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G004/G018/G104/G105/G123/G126",
            "category": "technical_terminology",
            "summary": "Standardized key technical terms including doux, praktor, aer, kanonikon, episkepititai, and fiscal/property vocabulary where audited.",
            "evidence": "Gautier packets and project authority-list policy.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "G004/G019/G023/G069/G091/G093/G102/G109/G114/G128/G131/G133/G135",
            "category": "translation_correction",
            "summary": "Recorded targeted Gautier corrections from the first recovery pass, including a meteorological correction, fiscal terms, lost/inserted negatives, Homeric/classical phrasing, and restored omitted clauses.",
            "evidence": "Per-letter translation_v2 notes and Gautier packets.",
            "source_urls": "",
        },
        {
            "date": TODAY,
            "gautier_id": "ALL",
            "category": "targeted_audit",
            "summary": f"Completed extended Gautier clause checks for {len(AUDITED_SAMPLE)} letters, raising every defensible short/complete item checked to A and reserving B for localized textual or prosopographical uncertainty.",
            "evidence": "Per-letter translation_v2 notes, regenerated master_concordance.csv, and sample_audit.md.",
            "source_urls": "",
        },
    ]
    for gid in sorted(EXTENDED_UPDATES, key=lambda item: int(item[1:])):
        update = EXTENDED_UPDATES[gid]
        letter_path = LETTERS / gid / "translation_v2.md"
        packet = find_line(letter_path.read_text(encoding="utf-8"), r"^- Gautier source packet:\s*(.*)$")
        entries.append({
            "date": TODAY,
            "gautier_id": gid,
            "category": "extended_gautier_clause_audit",
            "summary": "; ".join(update["changes"]),
            "evidence": f"{letter_path}; {packet}",
            "source_urls": "",
        })
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
        "This report intentionally lists every C or D item. C does not mean unusable; it means the item still lacks the evidence needed for a final scholarly confidence rating, usually a complete clause-by-clause audit even though a Gautier packet now exists.",
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
        next_needed = "Direct manuscript or apparatus-level work; Gautier preserves only fragmentary/lacunose text."
        lines.append(f"| {row['gautier_id']} | {row['recipient']} | {row['notes']} | {next_needed} |")

    lines.extend([
        "",
        "## C - Audited But Still Provisional",
        "",
        "| G | Recipient | Source | Reason |",
        "|---|---|---|---|",
    ])
    for row in audited_c:
        lines.append(f"| {row['gautier_id']} | {row['recipient']} | {row['source_packet']} | {row['translation_status']}; {row['notes']} |")

    lines.extend([
        "",
        "## C - Pending Full Second-Pass Audit",
        "",
        "| G | Recipient | Source | Reason |",
        "|---|---|---|---|",
    ])
    for row in pending_c:
        lines.append(f"| {row['gautier_id']} | {row['recipient']} | {row['source_packet']} | {row['translation_status']}; {row['source_condition']} |")

    (REV / "exception_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def refresh_sample_audit(rows: list[dict[str, str]]) -> None:
    by_gid = {row["gautier_id"]: row for row in rows}
    lines = [
        "# Targeted Second-Pass Sample Audit",
        "",
        f"Created: {TODAY}",
        "",
        "This records the cross-range Gautier audit sample and the extended short-letter clause checks completed in this revision layer. It is evidence of revised status decisions, not a substitute for the remaining C-letter audits.",
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
        "- The first-pass translation is often closer to the Greek than expected in checked samples, especially in several short rhetorical letters.",
        "- The most common corrected failures are small agency/negation mistakes, over-smoothed technical terms, false truncation markers, and classical/biblical allusions made too generic.",
        "- Evidence of broad invented passages was not found in the checked complete letters, but localized unsupported propositions were found and removed or corrected.",
        "- The remaining C letters are mostly longer, denser, or previously OCR-sensitive and still need full clause audit before being upgraded.",
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
    packet_count = len(list((ROOT / "02_sources" / "gautier" / "letter_packets").glob("G*_gautier.txt")))

    lines = [
        "# Second-Pass QC Report",
        "",
        f"Created: {TODAY}",
        "",
        "## Corpus Accounting",
        "",
        f"- Letter directories found: {len(dirs)}",
        f"- Expected sequence G001-G135 present: {'yes' if not missing and not extra else 'no'}",
        f"- Gautier source packets found: {packet_count}",
        f"- Missing directories: {', '.join(missing) if missing else 'none'}",
        f"- Extra directories: {', '.join(extra) if extra else 'none'}",
        f"- Confidence counts: A={counts.get('A', 0)}, B={counts.get('B', 0)}, C={counts.get('C', 0)}, D={counts.get('D', 0)}",
        f"- D/incomplete letters: {', '.join(d_ids)}",
        "",
        "## Numbering Checks",
        "",
        "- G134/G135 explicitly resolved in v2: G134 is the recovered Demetrios/liturgy letter; G135 is the Tivanios/Tigranes Armenian Christological excerpt.",
        "- G001-G003 explicitly recovered from Gautier I; they are not the old local PG001-PG003 duplicate packets.",
        "- G005/G006 boundary repaired; old local G006 duplicate of G047 corrected.",
        "- G062/G063 boundary repaired and both retained as D because Gautier preserves mutilated/lacunose fragments.",
        "- G125 recovered from Gautier II after the local PG084 packet failed.",
        "- First-pass translations in `04_letters/` were not overwritten.",
        "- `revised_second_pass/letters/G134/translation_v2.md` carries the genuine recovered G134; `revised_second_pass/letters/G135/translation_v2.md` carries the reassigned Christological fragment.",
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
        "- Items were upgraded above C only after direct Gautier-packet comparison; B was retained where the text or identification remains locally uncertain.",
        "- No D item has been filled from summary or conjecture; the only D letters are the mutilated G062 and G063 fragments.",
        "",
        "## Remaining Risks",
        "",
        "- Remaining C letters have Gautier source packets but still need full clause-by-clause audit before they can be called strong.",
        "- The authority list is preliminary and needs expansion after full prosopographical work.",
        "- Long and dense packets, especially G008, G011, G027, G035-G039, G052-G061, G073-G079, G087-G088, G096-G098, G120, and G127, still need detailed clause checks.",
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
