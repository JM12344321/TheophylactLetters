from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OCR = ROOT / "02_sources" / "pg126" / "PG126_text.txt"
OUT = ROOT / "02_sources" / "pg126" / "letter_extractions"
MANIFEST = OUT / "pg_letter_extractions.csv"


# Greek majuscule numerals used in the PG headings. Kept as escapes so the
# extractor survives Windows console/codepage round trips.
GREEK_NUMERAL_VALUES = {
    "\u0391": 1,
    "\u0392": 2,
    "\u0393": 3,
    "\u0394": 4,
    "\u0395": 5,
    "\u03da": 6,
    "\u03db": 6,
    "\u03a3\u03a4": 6,
    "\u0396": 7,
    "\u0397": 8,
    "\u0398": 9,
    "\u0399": 10,
    "\u039a": 20,
    "\u039b": 30,
    "\u039c": 40,
    "\u039d": 50,
    "\u039e": 60,
    "\u039f": 70,
    "\u03a0": 80,
    "\u03de": 90,
    "\u03df": 90,
    "\u03a1": 100,
}

CAPS = "\u0391-\u03a9\u03da\u03db\u03de\u03df"
EPIST = "\u0395\u03a0\u0399\u03a3\u03a4"
KEPIST = "\u039a\u0395\u03a0\u0399\u03a3\u03a4"
EPISTOLE_PROTE = "\u0395\u03a0\u0399\u03a3\u03a4\u039f\u039b\u0397 \u03a0\u03a1\u03a9\u03a4\u0397"
DATIVE_TO = "\u03a4[\u1ff7\u1ff6\u1ff3\u1fb7\u1fc6]"  # Twi/Twoi/Toi/Tai/Tei
BARE_DATIVE = "[\u1ff7\u1ff6\u1ff3\u1fb7\u1fc6]"


def clean_num(raw: str) -> str:
    raw = raw.upper()
    raw = raw.replace("\u02b9", "").replace("'", "").replace(".", "")
    raw = raw.replace("-", "").replace("\u00b7", "").strip()
    raw = raw.replace("\u03f9", "\u03a3").replace("C", "\u03a3")
    raw = re.sub(fr"[^{CAPS}]", "", raw)
    return raw


def greek_num_to_int(raw: str) -> int | None:
    raw = clean_num(raw)
    if not raw:
        return None
    if raw == "\u03a3\u03a4":
        return 6
    total = 0
    i = 0
    while i < len(raw):
        if raw[i : i + 2] == "\u03a3\u03a4":
            total += 6
            i += 2
            continue
        total += GREEK_NUMERAL_VALUES.get(raw[i], 0)
        i += 1
    return total or None


def normalize_heading(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def is_page_marker(line: str) -> bool:
    return line.startswith("$0=")


def find_page(line: str) -> str:
    match = re.search(r"\$8=(\d+)", line)
    return match.group(1) if match else ""


def is_short_addressee(stripped: str) -> bool:
    if len(stripped) > 120:
        return False
    return re.match(fr"^[\u039a\-]?\s*{DATIVE_TO}\s", stripped) is not None


def is_heading(line: str, ix: int) -> tuple[bool, str, int | None]:
    stripped = line.strip()
    if not stripped:
        return (False, "", None)
    upper = stripped.upper()

    # The PG 126 OCR section from line 7300 to 14180 contains the printed
    # letter material used here. Other sections are commentary/orations.
    if ix < 7300 or ix > 14180:
        return (False, "", None)

    if upper.startswith(EPISTOLE_PROTE):
        return (True, "Meursius", 1)

    if upper.startswith(EPIST) or upper.startswith(KEPIST):
        m = re.search(fr"{EPIST}[\u039f\u039b\u0397\u0387\u02b9'.\s-]*([{CAPS}]{{1,4}})", stripped, re.I)
        if m:
            old = greek_num_to_int(m.group(1))
            bucket = "Lami-Finetti" if ix >= 12455 else "Meursius"
            return (True, bucket, old)
        bucket = "Lami-Finetti" if ix >= 12455 else "Meursius"
        return (True, bucket, None)

    # Earlier excerpts often print as "B'.-To ..." rather than "Epist. B".
    # Require explicit numeral punctuation so body words like Christoi do not
    # become false letter starts.
    m = re.match(fr"^([{CAPS}]{{1,4}})\s*(?:\u02b9|['.\u00b7-])+\s*{DATIVE_TO}\b", stripped, re.I)
    if m and 7300 <= ix < 8875:
        return (True, "Pre-Meursius", greek_num_to_int(m.group(1)))

    if 7631 <= ix < 8875 and re.match(fr"^[\-]?\s*{DATIVE_TO}\s", stripped):
        return (True, "Pre-Meursius", None)

    m = re.match(fr"^([{CAPS}]{{1,4}})\s*(?:\u02b9|['.\u00b7-])+\s*{BARE_DATIVE}\s", stripped, re.I)
    if m and 7631 <= ix < 8875:
        return (True, "Pre-Meursius", greek_num_to_int(m.group(1)))

    if 7631 <= ix < 8875 and re.search(fr"[\u02b9'.\u00b7-]\s*{DATIVE_TO}\s", stripped):
        return (True, "Pre-Meursius", None)

    if 7631 <= ix < 8875 and re.match(r"^[\u0399X\u03a7][A-Z\u0391-\u03c9]*[.\-]\s*", stripped):
        return (True, "Pre-Meursius", None)

    if 7631 <= ix < 8875 and "\u1f18\u03ba \u03c4\u1fc6\u03c2 \u03c0\u03c1\u1f78\u03c2" in stripped:
        return (True, "Pre-Meursius", None)

    if is_short_addressee(stripped):
        if 8875 <= ix < 12455:
            return (True, "Meursius", None)
        if 12455 <= ix < 14180:
            return (True, "Lami-Finetti", None)

    return (False, "", None)


def trim_ocr_noise(lines: list[str]) -> list[str]:
    trimmed: list[str] = []
    for line in lines:
        if is_page_marker(line):
            trimmed.append(line)
            continue
        # Drop all-caps Latin/OCR header fragments while preserving Greek lines.
        if re.fullmatch(r"[A-Z0-9 .,';:()\-]+", line.strip()) and len(line.strip()) > 8:
            continue
        trimmed.append(line.rstrip())
    return trimmed


def main() -> None:
    if not OCR.exists():
        raise SystemExit(f"Missing OCR file: {OCR}")
    OUT.mkdir(parents=True, exist_ok=True)
    lines = OCR.read_text(encoding="utf-8", errors="replace").splitlines()
    candidates = []
    current_page = ""
    for ix, line in enumerate(lines, start=1):
        if is_page_marker(line):
            current_page = find_page(line) or current_page
        ok, bucket, old_no = is_heading(line, ix)
        if ok:
            candidates.append(
                {
                    "file_line": ix,
                    "pg_page_marker": current_page,
                    "bucket": bucket,
                    "old_number": old_no,
                    "heading": normalize_heading(line),
                }
            )

    starts = []
    for c in candidates:
        previous = starts[-1] if starts else None
        if previous and c["file_line"] - previous["file_line"] <= 2:
            prev_is_heading_label = previous["heading"].upper().startswith((EPIST, KEPIST))
            cur_is_addressee = is_short_addressee(c["heading"])
            # Merge EPIST. labels with next-line addressee lemmas.
            if cur_is_addressee and prev_is_heading_label:
                continue
            # Merge numbered early addressee headings with body lines that OCR
            # starts as a separate short dative line.
            if previous["bucket"] == "Pre-Meursius" and cur_is_addressee:
                continue
        if starts and c["file_line"] - starts[-1]["file_line"] <= 2 and c["heading"] == starts[-1]["heading"]:
            continue
        starts.append(c)

    rows = []
    for idx, start in enumerate(starts, start=1):
        end_line = starts[idx]["file_line"] - 1 if idx < len(starts) else 14180
        block = lines[start["file_line"] - 1 : end_line]
        block = trim_ocr_noise(block)
        token = f"PG{idx:03d}"
        out_path = OUT / f"{token}.txt"
        out_path.write_text("\n".join(block).strip() + "\n", encoding="utf-8")
        first_addressee = ""
        if len(block) > 1 and re.match(fr"^[\u039a\-]?\s*{DATIVE_TO}\s", block[1].strip()):
            first_addressee = normalize_heading(block[1])
        rows.append(
            {
                "pg_unit": token,
                "bucket": start["bucket"],
                "old_number": start["old_number"] or "",
                "file_line_start": start["file_line"],
                "file_line_end": end_line,
                "pg_page_marker_start": start["pg_page_marker"],
                "heading": start["heading"],
                "addressee_line": first_addressee,
                "chars": len("\n".join(block)),
                "path": str(out_path.relative_to(ROOT)).replace("\\", "/"),
            }
        )

    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "pg_unit",
                "bucket",
                "old_number",
                "file_line_start",
                "file_line_end",
                "pg_page_marker_start",
                "heading",
                "addressee_line",
                "chars",
                "path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Extracted {len(rows)} PG letter units")
    print(MANIFEST)


if __name__ == "__main__":
    main()
