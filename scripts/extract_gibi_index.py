from __future__ import annotations

import csv
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "02_sources" / "gibi_9_2" / "index_utf16_decoded.txt"
OUT = ROOT / "03_gautier_index" / "gibi_letter_index.csv"


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def main() -> None:
    if not INDEX.exists():
        raise SystemExit(f"Missing GIBI index file: {INDEX}")
    lines = INDEX.read_text(encoding="utf-8", errors="replace").splitlines()
    source = "\n".join(lines[138:208])
    text = strip_tags(source)
    text = text.split("//", 1)[0]
    rows = []
    for match in re.finditer(r"(?<!\d)(\d{1,3})\.\s+(.+?)(?=\s+\d{1,3}\.\s+|$)", text):
        number = int(match.group(1))
        title = match.group(2).strip()
        page_match = re.search(r"\((\d+)\)\.?$", title)
        gibi_page = page_match.group(1) if page_match else ""
        if page_match:
            title = title[: page_match.start()].strip()
        rows.append(
            {
                "gautier_id": f"G{number:03d}",
                "gautier_number": number,
                "gibi_title_bg": title,
                "gibi_page": gibi_page,
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["gautier_id", "gautier_number", "gibi_title_bg", "gibi_page"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
