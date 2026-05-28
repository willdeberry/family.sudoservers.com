#!/usr/bin/env python3
"""
Extract draft genealogical entries from OCR text files.

OCR quality on the source scans is too low to trust for dates and numbers,
but the *structure* (entry-per-code, code at line start, name after) is
usually intact. This script extracts code/name/birth/death/marriage as best
it can and emits raw_entries.py-format Python dicts with
`verification = {status: "draft", source: "ocr"}` so a later verification
pass can confirm or fix each one.

Usage:
    python3 parser/draft_from_ocr.py --pdf john           # to stdout
    python3 parser/draft_from_ocr.py --pdf absalom --missing-only
    python3 parser/draft_from_ocr.py --pdf john > /tmp/drafts.py

Then either review and paste into raw_entries.py, or use --append to
append directly with a .bak file alongside.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "parser"))

from raw_entries import ENTRIES, SEE_REFS  # noqa: E402

# Source PDF filename per OCR text basename
PDF_FOR = {
    "john": "John_Guthrie - Eight Generations.pdf",
    "james": "James_Guthrie - Seven Generations.pdf",
    "alexander": "Alexander_Guthrie - Five Generations.pdf",
    "stephen": "Stephen_Guthrie - One Generation .pdf",
    "absalom": "Absalom_Guthrie - One Generation .pdf",
    "william": "William_Guthrie - One Generation.pdf",
    "rachel": "Rachel_Guthrie - One Generation .pdf",
}

# Lineage code at the start of a line — same regex as report_missing.py
CODE_LINE_RE = re.compile(
    r"^\s*([1-9A-F][1-9A-F]{0,7})\s+\*?([A-Z][A-Za-z\-\.\(\)'].*)?$"
)
DATE_LIKE_RE = re.compile(r"^[12][0-9]$|^3[01]$")

# Dates in the form "DD Mon YYYY" or "Mon YYYY" — OCR may mangle "May" to
# "Mav", "Jul" to "Jul.", etc. We accept anything that fuzzy-matches.
MONTH = r"(?:Jan|Feb|Mar|Apr|May|Mav|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?"
DATE_RE = re.compile(rf"(\d{{1,2}}\s+{MONTH}\s+\d{{4}})", re.IGNORECASE)
DATE_OR_YEAR_RE = re.compile(rf"(\d{{1,2}}\s+{MONTH}\s+\d{{4}}|{MONTH}\s+\d{{4}}|about\s+\d{{4}}|\b\d{{4}}\b)", re.IGNORECASE)


def known_codes():
    known = set()
    for e in ENTRIES:
        known.add(e["code"])
        for c in e.get("children", []):
            known.add(c["code"])
    for ref in SEE_REFS:
        known.update(ref["codes"])
    return known


# Each PDF documents one sibling branch. Codes in that PDF should start
# with that branch's prefix (with a small allowance for cross-references).
BRANCH_PREFIX = {
    "john": "1",
    "william": "2",
    "stephen": "5",
    "rachel": "6",
    "james": "7",
    "absalom": "8",
    "alexander": "A",
}


def page_index(text):
    """Return a list of (line_index, page_num).

    `pdftotext` emits a form-feed (\\f) on a line by itself between pages.
    `vision_ocr.py` emits '=== Page N ===' headers. Support both."""
    idx = [(0, 1)]  # default: line 0 is page 1
    page = 1
    for i, line in enumerate(text.splitlines()):
        m = re.match(r"=== Page (\d+) ===", line)
        if m:
            page = int(m.group(1))
            idx.append((i, page))
            continue
        if "\f" in line:
            page += 1
            idx.append((i + 1, page))
    return idx


def page_for_line(page_idx, line_no):
    """Return the page number a given line falls into."""
    current = None
    for ln, page in page_idx:
        if ln <= line_no:
            current = page
        else:
            break
    return current


def find_entries(text):
    """Yield (code, line_no, block_text) for every code-headed entry block.

    A block runs from one code-headed line until the next."""
    lines = text.splitlines()
    starts = []
    for i, line in enumerate(lines):
        m = CODE_LINE_RE.match(line)
        if not m:
            continue
        code = m.group(1)
        if DATE_LIKE_RE.match(code):
            continue
        # Skip code-only lines with no name
        if not m.group(2):
            continue
        starts.append((i, code))

    for j, (ln, code) in enumerate(starts):
        end = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
        block = "\n".join(lines[ln:end])
        # Normalize whitespace
        block = re.sub(r"\s+", " ", block).strip()
        yield code, ln, block


def clean_name(raw):
    """Best-effort cleanup of an OCR name. Strip trailing punctuation, fix
    obvious uppercase artifacts."""
    if not raw:
        return None
    # Remove leading *
    raw = raw.lstrip("*").strip()
    # Stop at first 'b.' (birth) or comma
    raw = re.split(r"\bb\b\.?|\bd\b\.?|\bm\b\.?|,|;", raw, maxsplit=1)[0]
    # Strip junk
    raw = re.sub(r"[._]+$", "", raw).strip()
    # Collapse repeated punctuation
    raw = re.sub(r"\.+", ".", raw)
    # Common name correction: Mav→May etc
    raw = raw.replace("Mav", "May")
    # Title-case all-caps names (entry headers in the PDFs are uppercase)
    if raw and raw == raw.upper():
        raw = " ".join(
            w.capitalize() if w.isalpha() else w
            for w in raw.split()
        )
    return raw or None


def normalize_date_token(raw):
    """Convert 'Mav' to 'May' etc in a date string."""
    if not raw:
        return raw
    return raw.strip().replace(" Mav ", " May ").replace("Sept ", "Sep ")


def parse_entry(code, block, pdf, page):
    """Parse a single OCR entry block. Return a dict suitable for ENTRIES."""
    # Remove the leading code
    rest = re.sub(rf"^\s*{re.escape(code)}\s+", "", block, count=1)

    # Name: from start until first "b." or first ","
    name_match = re.match(r"\*?([A-Z][A-Za-z'\.\-\(\) ]+?)(?:\s*[,;\.]|\s+\bb\b)", rest)
    name = clean_name(name_match.group(1)) if name_match else None
    if not name:
        return None  # Couldn't parse — skip

    out = {
        "code": code,
        "name": name,
        "source": {"pdf": pdf, "page": page},
        "verification": {
            "status": "draft",
            "source": "ocr",
            "lastChecked": None,
            "notes": "Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.",
        },
    }

    # Find dates. The first one after the name is the birth; second is the
    # death of the subject (typically). Subsequent ones belong to the spouse.
    dates = [normalize_date_token(m.group(1)) for m in DATE_OR_YEAR_RE.finditer(rest)]

    # Heuristic: look for "b." then a date for birth; "d." then a date for death.
    b_match = re.search(rf"\bb\b\.?\s+({DATE_OR_YEAR_RE.pattern})", rest, re.IGNORECASE)
    if b_match:
        out["born"] = normalize_date_token(b_match.group(1))
    d_match = re.search(rf"\bd\b\.?\s+({DATE_OR_YEAR_RE.pattern})", rest, re.IGNORECASE)
    if d_match:
        out["died"] = normalize_date_token(d_match.group(1))

    # Marriage / spouse. Look for "m " or "m. " followed by name.
    m_match = re.search(r"\bm\b\.?\s+([A-Z][A-Za-z'\.\-\(\) ]+?)(?:\s*[,;\.]|\s+\bb\b|$)", rest)
    if m_match:
        spouse_name = clean_name(m_match.group(1))
        if spouse_name and len(spouse_name) >= 3:
            spouse = {"name": spouse_name}
            # Try to find marriage date — but only DD Mon YYYY or Mon YYYY,
            # never a 4-digit year alone (too likely to be a code or birth year).
            after_m = rest[m_match.end():]
            strict_date = re.search(
                rf"(\d{{1,2}}\s+{MONTH}\s+\d{{4}}|{MONTH}\s+\d{{4}})",
                after_m[:120], re.IGNORECASE,
            )
            if strict_date:
                spouse["married"] = normalize_date_token(strict_date.group(1))
            out["spouses"] = [spouse]

    return out


def looks_like_real_entry(entry):
    """Reject entries that are obvious OCR artifacts.

    A real genealogy entry has:
      - a plausible name (alpha chars, reasonable length)
      - the name doesn't look like a street address or random tokens
    """
    name = entry.get("name") or ""
    if len(name) < 4:
        return False
    # Reject names that look like addresses (e.g., '2583 Glen Echo Dave')
    if re.match(r"^\d", name):
        return False
    # Reject names that are mostly lowercase (OCR noise)
    alpha = [c for c in name if c.isalpha()]
    if alpha:
        uppercase_ratio = sum(1 for c in alpha if c.isupper()) / len(alpha)
        # Real names: roughly 1 uppercase per word
        if uppercase_ratio < 0.05:
            return False
    # Reject if name contains too many non-letter chars
    non_letter = sum(1 for c in name if not c.isalpha() and c not in " '-.")
    if non_letter > 3:
        return False
    return True


def format_entry(entry):
    """Format a parsed entry as a Python ENTRIES.append(...) block."""
    lines = ["ENTRIES.append({"]
    for k, v in entry.items():
        if k == "spouses":
            lines.append("    \"spouses\": [")
            for sp in v:
                lines.append("        {")
                for sk, sv in sp.items():
                    lines.append(f"            {sk!r}: {sv!r},")
                lines.append("        },")
            lines.append("    ],")
        elif k == "source":
            lines.append("    \"source\": {")
            for sk, sv in v.items():
                lines.append(f"        {sk!r}: {sv!r},")
            lines.append("    },")
        elif k == "verification":
            lines.append("    \"verification\": {")
            for sk, sv in v.items():
                lines.append(f"        {sk!r}: {sv!r},")
            lines.append("    },")
        else:
            lines.append(f"    {k!r}: {v!r},")
    lines.append("})")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="OCR basename without extension, e.g. 'john'")
    ap.add_argument("--missing-only", action="store_true",
                    help="Skip entries whose code is already in raw_entries.py")
    ap.add_argument("--append", action="store_true",
                    help="Append drafts to parser/raw_entries.py (creates .bak)")
    args = ap.parse_args()

    ocr_path = REPO / "ocr" / f"{args.pdf}.txt"
    if not ocr_path.exists():
        print(f"No such OCR file: {ocr_path}", file=sys.stderr)
        sys.exit(1)
    pdf_filename = PDF_FOR[args.pdf]
    text = ocr_path.read_text(errors="replace")
    pages = page_index(text)
    known = known_codes()

    output_lines = []
    extracted = 0
    skipped_known = 0
    skipped_parse = 0

    skipped_noise = 0
    skipped_wrong_branch = 0
    skipped_dup = 0
    seen_codes = set()
    expected_prefix = BRANCH_PREFIX.get(args.pdf)
    # Pass 1: collect entries, dedupe by code (keep richest version)
    candidates = {}  # code -> entry
    for code, ln, block in find_entries(text):
        if args.missing_only and code in known:
            skipped_known += 1
            continue
        if expected_prefix and not code.startswith(expected_prefix):
            skipped_wrong_branch += 1
            continue
        page = page_for_line(pages, ln)
        entry = parse_entry(code, block, pdf_filename, page)
        if not entry:
            skipped_parse += 1
            continue
        if not looks_like_real_entry(entry):
            skipped_noise += 1
            continue
        existing = candidates.get(code)
        # Score = number of populated data fields (born/died/spouses)
        def score(e):
            return sum(1 for k in ("born", "died", "spouses") if e.get(k))
        if existing is None or score(entry) > score(existing):
            if existing is not None:
                skipped_dup += 1
            candidates[code] = entry
        else:
            skipped_dup += 1

    for code in sorted(candidates):
        output_lines.append(format_entry(candidates[code]))
        output_lines.append("")
        extracted += 1

    sys.stderr.write(
        f"Extracted {extracted} draft entries from {args.pdf}.txt "
        f"({skipped_known} already known, {skipped_parse} failed to parse, "
        f"{skipped_noise} rejected as OCR noise, "
        f"{skipped_wrong_branch} wrong-branch, "
        f"{skipped_dup} duplicate-code merged)\n"
    )

    out_text = "\n".join(output_lines)
    if args.append:
        path = REPO / "parser" / "raw_entries.py"
        backup = path.with_suffix(".py.bak")
        backup.write_text(path.read_text())
        with path.open("a") as f:
            f.write(f"\n# === Drafts extracted from {args.pdf}.txt by draft_from_ocr.py ===\n")
            f.write(out_text)
            f.write("\n")
        sys.stderr.write(f"Appended to {path} (backup at {backup})\n")
    else:
        print(out_text)


if __name__ == "__main__":
    main()
