#!/usr/bin/env python3
"""
Verification worklist for draft entries.

Draft entries (OCR-extracted) live in data/people.json with
verification.status="draft". This script picks unverified entries, groups
them by source PDF and page so a Claude session can read a single page
range and verify multiple entries at once, and prints a worklist.

The actual verification is done by Claude using the Read tool on the
source PDFs (vision). This script just produces the work plan.

Usage:
    python3 parser/verify.py                       # show next batch (10 entries)
    python3 parser/verify.py --pdf james           # filter to one PDF
    python3 parser/verify.py --batch 25            # bigger batch
    python3 parser/verify.py --page-range 1-20     # only one page range
    python3 parser/verify.py --stats               # progress only, no list
    python3 parser/verify.py --code 13F71          # show one specific entry

To record verification results, edit raw_entries.py: change the entry's
verification block to status="verified", set source="vision", and
lastChecked to today's ISO date. Re-run parser/build.py.
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def load_people():
    return json.loads((REPO / "data" / "people.json").read_text())["people"]


def primary_code(p):
    return p.get("lineageCodes", ["?"])[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", help="Filter to one source PDF (substring match)")
    ap.add_argument("--batch", type=int, default=10, help="How many entries to show")
    ap.add_argument("--page-range", help="Only show entries on pages in this range, e.g. 20-40")
    ap.add_argument("--stats", action="store_true", help="Show only summary stats, no entry list")
    ap.add_argument("--code", help="Show details for one specific lineage code")
    args = ap.parse_args()

    people = load_people()

    if args.code:
        for p in people:
            if args.code in p.get("lineageCodes", []):
                print_entry_detail(p)
                return
        print(f"No person with lineage code {args.code}", file=sys.stderr)
        sys.exit(1)

    # Tally verification status
    counts = defaultdict(int)
    for p in people:
        v = p.get("verification", {})
        counts[(v.get("status", "?"), v.get("source", "?"))] += 1

    print("Verification status:")
    for (status, source), n in sorted(counts.items()):
        print(f"  {status:14s} via {source:8s}  {n:5d}")
    total = len(people)
    verified = sum(n for (s, _), n in counts.items() if s == "verified")
    print(f"  TOTAL: {total} ({verified} verified, {total - verified} pending — {100 * verified // total}%)")

    if args.stats:
        return

    # Build worklist: drafts only, grouped by (pdf, page) so the reviewer
    # can fetch one PDF page range and resolve multiple entries at once.
    drafts = []
    for p in people:
        if p.get("verification", {}).get("status") == "draft":
            sources = p.get("sources", [])
            src = sources[0] if sources else {"pdf": "?", "page": None}
            if args.pdf and args.pdf.lower() not in (src.get("pdf") or "").lower():
                continue
            page = src.get("page")
            if args.page_range and page is not None:
                lo, hi = map(int, args.page_range.split("-"))
                if not (lo <= page <= hi):
                    continue
            drafts.append((src.get("pdf"), page or 0, p))

    drafts.sort(key=lambda x: (x[0] or "", x[1], primary_code(x[2])))

    print(f"\nDraft entries needing verification: {len(drafts)}")
    if not drafts:
        return

    print(f"Showing next {min(args.batch, len(drafts))} (grouped by PDF and page):\n")

    current_pdf = None
    shown = 0
    for pdf, page, p in drafts:
        if shown >= args.batch:
            remaining = len(drafts) - shown
            print(f"\n... {remaining} more drafts not shown. Re-run with --batch {remaining + args.batch} to see them.")
            break
        if pdf != current_pdf:
            print(f"\n── {pdf} ──")
            current_pdf = pdf
        code = primary_code(p)
        name = p.get("name", {}).get("full", "?")
        born = (p.get("birth") or {}).get("dateRaw") or "?"
        died = (p.get("death") or {}).get("dateRaw") or "?"
        notes = (p.get("verification") or {}).get("notes") or ""
        notes_short = notes[:60] + "…" if len(notes) > 60 else notes
        print(f"  page {page:4} | {code:8s} | {name:35s} | b. {born:18s} d. {died:18s}")
        if notes_short and "OCR" not in notes_short:
            print(f"               note: {notes_short}")
        shown += 1

    print(f"\nNext steps:")
    print(f"  1. Read the relevant PDF page range with the Read tool (pages: \"N-M\").")
    print(f"     PDFs live at ~/Documents/Family Tree/")
    print(f"  2. For each entry above, confirm or correct in parser/raw_entries.py.")
    print(f"  3. Update its verification block:")
    print(f"       'verification': {{'status': 'verified', 'source': 'vision',")
    print(f"                          'lastChecked': '{date.today().isoformat()}', 'notes': None}}")
    print(f"  4. Run python3 parser/build.py and commit.")


def print_entry_detail(p):
    """Detailed view of one entry — useful when reviewing a single draft."""
    print(f"ID: {p['id']}")
    print(f"Lineage codes: {p.get('lineageCodes', [])}")
    print(f"Name: {(p.get('name') or {}).get('full', '?')}")
    if p.get("birth"):
        print(f"Birth: {p['birth']}")
    if p.get("death"):
        print(f"Death: {p['death']}")
    for m in p.get("marriages", []):
        print(f"Marriage: {m}")
    print(f"Parents (IDs): {p.get('parentIds', [])}")
    print(f"Children (IDs): {p.get('childIds', [])}")
    print(f"Sources: {p.get('sources', [])}")
    print(f"Verification: {p.get('verification')}")


if __name__ == "__main__":
    main()
