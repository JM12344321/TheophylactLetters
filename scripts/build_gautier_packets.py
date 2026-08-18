from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAUTIER = ROOT / "02_sources" / "gautier"
PACKETS = GAUTIER / "letter_packets"


# Gautier II contains the letter volume proper, but G001-G003 and G134 are
# printed in Gautier I and only cross-referenced in Gautier II.
VOL1_RANGES: dict[int, tuple[int, int, str]] = {
    1: (64, 71, "Gautier I, pp. 130-143; cross-referenced in Gautier II, p. 184"),
    2: (72, 82, "Gautier I, pp. 146-165; cross-referenced in Gautier II, p. 184"),
    3: (83, 87, "Gautier I, pp. 168-175; cross-referenced in Gautier II, p. 184"),
    134: (166, 171, "Gautier I, pp. 334-343; cross-referenced in Gautier II, p. 592"),
}


# Local PDF text-layer page starts for Gautier II. The printed running heads in
# the OCR are occasionally noisy, so this map is deliberately explicit.
VOL2_STARTS: dict[int, int] = {
    4: 68,
    5: 71,
    6: 73,
    7: 75,
    8: 76,
    9: 78,
    10: 80,
    11: 81,
    12: 83,
    13: 85,
    14: 87,
    15: 89,
    16: 91,
    17: 93,
    18: 95,
    19: 97,
    20: 98,
    21: 99,
    22: 101,
    23: 103,
    24: 104,
    25: 106,
    26: 107,
    27: 109,
    28: 111,
    29: 112,
    30: 114,
    31: 116,
    32: 118,
    33: 120,
    34: 121,
    35: 122,
    36: 124,
    37: 126,
    38: 129,
    39: 131,
    40: 133,
    41: 134,
    42: 135,
    43: 137,
    44: 138,
    45: 140,
    46: 144,
    47: 146,
    48: 147,
    49: 148,
    50: 149,
    51: 150,
    52: 151,
    53: 153,
    54: 156,
    55: 158,
    56: 160,
    57: 161,
    58: 163,
    59: 168,
    60: 171,
    61: 175,
    62: 177,
    63: 178,
    64: 180,
    65: 181,
    66: 182,
    67: 184,
    68: 186,
    69: 188,
    70: 189,
    71: 191,
    72: 193,
    73: 194,
    74: 197,
    75: 199,
    76: 201,
    77: 203,
    78: 207,
    79: 209,
    80: 211,
    81: 213,
    82: 217,
    83: 219,
    84: 220,
    85: 222,
    86: 226,
    87: 228,
    88: 230,
    89: 232,
    90: 234,
    91: 235,
    92: 236,
    93: 238,
    94: 239,
    95: 240,
    96: 241,
    97: 247,
    98: 249,
    99: 253,
    100: 254,
    101: 256,
    102: 257,
    103: 258,
    104: 259,
    105: 260,
    106: 261,
    107: 262,
    108: 263,
    109: 264,
    110: 265,
    111: 267,
    112: 268,
    113: 269,
    114: 270,
    115: 271,
    116: 272,
    117: 273,
    118: 274,
    119: 275,
    120: 276,
    121: 279,
    122: 280,
    123: 282,
    124: 283,
    125: 284,
    126: 285,
    127: 286,
    128: 291,
    129: 292,
    130: 293,
    131: 294,
    132: 295,
    133: 296,
    135: 298,
}


def read_page(vol: str, page: int) -> str:
    return (GAUTIER / f"{vol}_pages" / f"page_{page:03d}.txt").read_text(encoding="utf-8")


def write_packet(gnum: int, vol: str, start: int, end: int, citation: str) -> dict[str, str | int]:
    gid = f"G{gnum:03d}"
    out = PACKETS / f"{gid}_gautier.txt"
    chunks = [
        f"# {gid} Gautier Source Packet",
        "",
        f"Source: {citation}",
        f"Local extraction: 02_sources/gautier/{vol}_pages/page_{start:03d}.txt-page_{end:03d}.txt",
        "",
    ]
    for page in range(start, end + 1):
        chunks.append(f"\n\n===== {vol} page_{page:03d} =====\n")
        chunks.append(read_page(vol, page))
    out.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
    return {
        "gautier_id": gid,
        "volume": vol,
        "start_pdf_page": start,
        "end_pdf_page": end,
        "citation": citation,
        "packet": str(out.relative_to(ROOT)).replace("\\", "/"),
    }


def main() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str | int]] = []

    for gnum, (start, end, citation) in sorted(VOL1_RANGES.items()):
        rows.append(write_packet(gnum, "16_1", start, end, citation))

    starts = sorted(VOL2_STARTS.items())
    for idx, (gnum, start) in enumerate(starts):
        if idx + 1 < len(starts):
            next_gnum, next_start = starts[idx + 1]
            # G134 is a cross-reference in Gautier II, not a separate full text.
            if gnum == 133:
                end = 296
            else:
                end = next_start - 1
        else:
            end = 299
        citation = f"Gautier II, letter {gnum}; local PDF text pages {start:03d}-{end:03d}"
        rows.append(write_packet(gnum, "16_2", start, end, citation))

    manifest = sorted(rows, key=lambda row: int(str(row["gautier_id"])[1:]))
    (PACKETS / "packet_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(manifest)} Gautier packets to {PACKETS}")


if __name__ == "__main__":
    main()
