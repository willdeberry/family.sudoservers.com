#!/usr/bin/env python3
"""
Compare lineage codes found in OCR text files against codes in raw_entries.py.

OCR quality on these scans is too poor to trust for source data, but it's
good enough to act as an *index* — telling us which codes appear in each
PDF. This script extracts code-like tokens from ocr/<branch>.txt files and
reports which are missing from parser/raw_entries.py.

Usage:
    python3 parser/report_missing.py
    python3 parser/report_missing.py --branch 1   # filter to John's line
    python3 parser/report_missing.py --pdf john   # filter by ocr filename
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "parser"))

from raw_entries import ENTRIES, SEE_REFS  # noqa: E402


# Lineage codes use 1-9 then A-Z at each position (never 0). Length 1-8.
# Each line in the source PDFs typically looks like:
#     74A   Ray Guthrie, b. 17 Dec 1895
# or:
#     74A *Ray Guthrie, b. 17 Dec 1895
# Excluding 0 eliminates the biggest source of OCR noise: day-of-month
# numbers (01, 02, ..., 31) bleeding in from date strings.
CODE_LINE_RE = re.compile(
    r"^\s*([1-9A-F][1-9A-F]{0,7})\s+\*?[A-Z][A-Za-z\(]"
)
# Codes that look like 2-digit numbers 10-31 are almost always dates, not
# real lineage codes. Drop them unless they appear with strong context.
DATE_LIKE_RE = re.compile(r"^[12][0-9]$|^3[01]$")


def extract_codes_from_ocr(text):
    """Return the set of code-like tokens found at line starts."""
    found = set()
    for line in text.splitlines():
        m = CODE_LINE_RE.match(line)
        if not m:
            continue
        code = m.group(1)
        if DATE_LIKE_RE.match(code):
            continue
        found.add(code)
    return found


def known_codes():
    """Codes referenced anywhere in raw_entries.py — full entries, inline
    children, or SEE_REFS."""
    known = set()
    for entry in ENTRIES:
        known.add(entry["code"])
        for child in entry.get("children", []):
            known.add(child["code"])
    for ref in SEE_REFS:
        known.update(ref["codes"])
    return known


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", help="Filter to codes starting with this prefix")
    ap.add_argument("--pdf", help="Filter to one ocr/<pdf>.txt file (basename, no ext)")
    ap.add_argument("--show-all", action="store_true", help="Also list codes already covered")
    args = ap.parse_args()

    ocr_dir = REPO / "ocr"
    if not ocr_dir.exists():
        print("No ocr/ directory. Run the OCR pipeline first.", file=sys.stderr)
        sys.exit(1)

    known = known_codes()
    by_pdf = defaultdict(set)

    for txt_path in sorted(ocr_dir.glob("*.txt")):
        if args.pdf and txt_path.stem != args.pdf:
            continue
        codes = extract_codes_from_ocr(txt_path.read_text(errors="replace"))
        by_pdf[txt_path.stem] = codes

    total_seen = set()
    total_missing = set()

    for pdf, codes in by_pdf.items():
        if args.branch:
            codes = {c for c in codes if c.startswith(args.branch)}
        missing = codes - known
        covered = codes & known
        total_seen |= codes
        total_missing |= missing

        print(f"\n== {pdf}.txt ==")
        print(f"  codes in OCR: {len(codes)}")
        print(f"  already in raw_entries.py: {len(covered)}")
        print(f"  missing: {len(missing)}")
        if missing:
            sorted_missing = sorted(missing, key=lambda c: (len(c), c))
            # Show grouped by depth
            depth_groups = defaultdict(list)
            for c in sorted_missing:
                depth_groups[len(c)].append(c)
            for depth in sorted(depth_groups):
                gen = "founder" if depth == 1 else f"gen {depth - 1}"
                print(f"    -- depth {depth} ({gen}) -- {len(depth_groups[depth])} codes")
                # Wrap to 6 per line for readability
                for i in range(0, len(depth_groups[depth]), 8):
                    chunk = depth_groups[depth][i:i + 8]
                    print(f"      {' '.join(c.ljust(7) for c in chunk)}")
        if args.show_all and covered:
            print(f"  covered codes: {sorted(covered, key=lambda c: (len(c), c))}")

    print(f"\nTOTAL: {len(total_seen)} codes seen across all OCR, {len(total_missing)} missing")
    print("Note: OCR is noisy; a few of the 'missing' codes may be OCR artifacts.")
    print("Spot-check ambiguous codes against the PDF before transcribing.")


if __name__ == "__main__":
    main()
