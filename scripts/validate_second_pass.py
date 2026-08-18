from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REV = ROOT / "revised_second_pass"
LETTERS = REV / "letters"
PACKETS = ROOT / "02_sources" / "gautier" / "letter_packets"

EXPECTED = [f"G{n:03d}" for n in range(1, 136)]
STALE_BODY_PHRASES = [
    "bishop of Cyprus",
    "that squall",
    "the canons are asleep",
    "holy antidote",
    "by lamplight",
    "thought of God",
    "Athenian things",
    "do not worry",
    "source_missing_no_translation",
    "[not yet verified]",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_line(text: str, pattern: str) -> str:
    match = re.search(pattern, text, re.M)
    return match.group(1).strip() if match else ""


def body(text: str) -> str:
    match = re.search(r"## Revised English Translation\n\n(.*?)(?:\n## |\Z)", text, re.S)
    return match.group(1).strip() if match else ""


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION FAILED: {message}")


def main() -> None:
    dirs = sorted(p.name for p in LETTERS.iterdir() if p.is_dir() and re.fullmatch(r"G\d{3}", p.name))
    if dirs != EXPECTED:
        fail("letter directory sequence is not exactly G001-G135")

    packet_ids = sorted(p.stem.replace("_gautier", "") for p in PACKETS.glob("G*_gautier.txt"))
    if packet_ids != EXPECTED:
        fail("Gautier packet sequence is not exactly G001-G135")

    rows = list(csv.DictReader((REV / "master_concordance.csv").open(encoding="utf-8")))
    if [row["gautier_id"] for row in rows] != EXPECTED:
        fail("master concordance sequence is not exactly G001-G135")

    counts = Counter()
    seen_bodies: dict[str, str] = {}
    duplicate_bodies: list[tuple[str, str]] = []
    stale_hits: list[tuple[str, str]] = []

    for gid in EXPECTED:
        translation = LETTERS / gid / "translation_v2.md"
        audit = LETTERS / gid / "audit.md"
        if not translation.exists():
            fail(f"{gid} missing translation_v2.md")
        if not audit.exists():
            fail(f"{gid} missing audit.md")

        text = read(translation)
        confidence = find_line(text, r"^Confidence category:\s*(.*)$")
        counts[confidence] += 1

        b = body(text)
        normalized = re.sub(r"\s+", " ", b)
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        if digest in seen_bodies:
            duplicate_bodies.append((seen_bodies[digest], gid))
        seen_bodies[digest] = gid

        for phrase in STALE_BODY_PHRASES:
            if phrase in b:
                stale_hits.append((gid, phrase))

    if duplicate_bodies:
        fail(f"duplicate translation bodies detected: {duplicate_bodies}")
    if stale_hits:
        fail(f"stale phrase(s) in live translation bodies: {stale_hits}")
    if [row["gautier_id"] for row in rows if row["confidence"] == "D"] != ["G062", "G063"]:
        fail("D letters are not exactly G062 and G063")

    row_by_id = {row["gautier_id"]: row for row in rows}
    if row_by_id["G134"]["recipient"] != "his brother Demetrios":
        fail("G134 recipient is not Demetrios")
    if "Tivanios" not in row_by_id["G135"]["recipient"]:
        fail("G135 recipient is not Tivanios/Tigranes")

    print(f"Second-pass validation passed. Counts: A={counts['A']}, B={counts['B']}, C={counts['C']}, D={counts['D']}.")


if __name__ == "__main__":
    main()
