# Project status

Last updated: 2026-06-07 (John PDF pages 1-10 vision-verified)

## What exists

- 1503 people in `data/people.json`, generated from `parser/raw_entries.py`
- All 7 sibling branches present, structure largely complete
- 12 cross-branch marriages with dedup working (see SEE_REFS in raw_entries.py)
- Tree depth: 7+ generations from inferred founder (code `0`)
- Verification status: 181 verified (125 manual + 56 vision), 1322 draft

## Verification pass currently in progress

Working through John PDF (147 pages) from the top to fix bulk-import
errors and add missing entries. Found multiple bugs from the regex-based
OCR drafter — cross-contaminated dates and spouses where one person's
data leaked onto a different code. Removing dirty OCR drafts as we go;
parent's children list provides clean basic data.

- John pages 1-5: done (founder, gen 1, gen 2, start of gen 3)
- John pages 6-10: done (rest of gen 3 + start of gen 4 stubs)
- John pages 11-147: pending

Per-branch descendant counts: John 417 · Alexander 64 · James 77 ·
Stephen 31 · Absalom 22 · William 19 · Rachel 7. The lighter branches are
that thin in the source PDFs themselves, not from missing transcription.

## Source PDFs and transcription coverage

PDFs live at `~/Documents/Family Tree/`. They are scanned images.
We OCR'd them with `ocrmypdf --deskew --clean --oversample 600` and
checked them into `ocr/<branch>.txt`. The OCR is too noisy for source
data (digit errors in dates) but good enough as an *index* — see
`parser/report_missing.py` for the auto-generated coverage report.

Live counts (run `python3 parser/report_missing.py` for current numbers):

| PDF | Pages | Codes in OCR | In dataset | Missing |
|---|---:|---:|---:|---:|
| rachel.txt | 1 | 4 | 2 | 2 |
| william.txt | 3 | 22 | 1 | 21 |
| absalom.txt | 4 | 15 | 6 | 9 |
| stephen.txt | 6 | 29 | 7 | 22 |
| alexander.txt | 11 | 95 | 10 | 85 |
| james.txt | 32 | 115 | 11 | 104 |
| john.txt | 147 | ~1100 | 56 | ~1050 |
| **Total** | **204** | **~1390** | **~77 unique** | **~1315** |

(About 5% of the "missing" codes are OCR artifacts — single letters, weird
short tokens — not real entries. Spot-check before transcribing.)

## Decision log

- **Founder code `0`**: The 7 documented PDFs are children of a single
  unnamed Guthrie patriarch. No PDF documents him directly; we created code
  `0` as a placeholder so all branches connect to a single root. Codes 3, 4,
  9 are unaccounted-for siblings.
- **Lineage codes use 1-9 then A-Z**: Original PDF convention for families
  larger than 9. ASCII order conveniently sorts correctly.
- **Stable IDs vs lineage codes**: People get `p_NNNNNN` IDs that never
  change. Lineage codes are a separate field; one person can have multiple
  codes (cross-branch dedup).
- **Source-of-truth is `raw_entries.py`**: JSON is generated. Never hand-edit
  `data/people.json` — it gets overwritten.
- **Same-person merges go in SEE_REFS**: When a person appears under two
  codes (e.g., children of a cross-branch marriage), add to SEE_REFS.
- **Parser is permissive**: We don't currently validate against the schema
  on build. Schema is documentation. (Future: add schema validation.)

## Known SEE_REFS clusters (declared in raw_entries.py)

| Cluster | Codes | Status |
|---|---|---|
| Ray Guthrie | 74A = 172A | active |
| Ward Barnes Guthrie | 11331 = 7151 | active |
| Stella/Charles Moyers kids | 7471-4 = 16221-4 | all 4 active |
| Lydia/Christian Nicola kids | 13E1-9 = 1741-9 | 4 of 9 active (3,6,7,8,9 pending) |

## Pickup checklist for a new session

### Verification workflow (primary work)

The dataset is structurally complete but mostly draft. Verification is the
ongoing work.

1. `python3 parser/verify.py --stats` — see overall progress.
2. `python3 parser/verify.py --pdf <branch> --batch 10` — get a worklist
   of 10 drafts grouped by PDF and page.
3. Read the relevant pages of the source PDF (`~/Documents/Family Tree/`)
   with the Read tool, using `pages: "N-M"`. Compare the visible entries
   to the drafts.
4. In `parser/raw_entries.py`, find each draft entry (search by code),
   correct any errors, and update its verification block to:
   `{"status": "verified", "source": "vision", "lastChecked": "<today>"}`.
5. `python3 parser/build.py`, commit both files.

### Adding entirely new people

1. `python3 parser/report_missing.py --pdf <branch>` — codes in OCR but
   not yet in raw_entries.py (should be near zero now since the bulk
   import).
2. If anything's missing, look it up in the PDF via vision and add to
   raw_entries.py with `verification = {"status": "verified", "source":
   "vision", ...}`.

## Next priorities

In rough order of value-per-effort:

1. **Build the website.** 187 people is plenty to design a tree viewer
   and person-detail page. Build UX in parallel with data backfill.
2. **Claude API ingest script.** A Python script that sends each PDF page
   to Claude and gets back `raw_entries.py`-format dicts. Best way to bulk
   ingest the remaining ~1300 people. Use prompt caching to cut cost.
3. **Manual transcription chunks.** Pick a PDF and a page range, transcribe
   linearly. Roughly 100-200 entries fit in one session before context
   pressure forces a break.
4. **Schema validation in `build.py`.** Optional. Use jsonschema package
   to validate the generated JSON against `schema/person.schema.json`.
