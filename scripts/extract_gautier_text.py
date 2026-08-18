from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
GAUTIER = ROOT / "02_sources" / "gautier"

PDFS = {
    "16_1": GAUTIER / "CFHB_16_1_Theophylacti_Achridensis_Opera_Gautier_1980.pdf",
    "16_2": GAUTIER / "CFHB_16_2_Theophylacti_Achridensis_Epistulae_Gautier_1986.pdf",
}


def printable(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Keep page extraction honest but reduce noisy trailing spaces.
    return "\n".join(line.rstrip() for line in text.splitlines()).strip() + "\n"


def greek_count(text: str) -> int:
    return sum(1 for c in text if "\u0370" <= c <= "\u03ff" or "\u1f00" <= c <= "\u1fff")


def printed_page_guess(text: str) -> str:
    for line in text.splitlines()[:6]:
        m = re.search(r"\b(\d{1,3})\b", line)
        if m:
            return m.group(1)
    return ""


def extract_volume(key: str, pdf: Path) -> None:
    outdir = GAUTIER / f"{key}_pages"
    outdir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(pdf))
    meta = []
    for idx, page in enumerate(reader.pages, start=1):
        text = printable(page.extract_text() or "")
        out = outdir / f"page_{idx:03d}.txt"
        out.write_text(text, encoding="utf-8")
        meta.append(
            {
                "pdf_page": idx,
                "printed_page_guess": printed_page_guess(text),
                "chars": len(text),
                "greek_chars": greek_count(text),
            }
        )
    (outdir / "page_manifest.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    for key, pdf in PDFS.items():
        extract_volume(key, pdf)


if __name__ == "__main__":
    main()
