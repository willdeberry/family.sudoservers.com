# Project status

Last updated: 2026-05-28 (post-OCR)

## What exists

- 187 people in `data/people.json`, generated from `parser/raw_entries.py`
- All 7 sibling branches present
- 12 cross-branch marriages with dedup working (see SEE_REFS in raw_entries.py)
- Tree depth: 7 generations from inferred founder (code `0`)

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

1. `cd /Users/will/code/family.sudoservers.com && git log --oneline` —
   see what's been done.
2. Read this file (STATUS.md), `README.md`, and the docstring at the top
   of `parser/raw_entries.py`.
3. `python3 parser/report_missing.py --pdf <branch>` — lists exactly which
   codes from that PDF's OCR are missing from raw_entries.py. Pick one,
   look up the surrounding page in the PDF.
4. For accurate transcription of a missing entry, **use Claude's vision on
   the PDF** — not the OCR text. OCR is the index; the PDF is ground truth.
   Use the Read tool with `pages: "N-M"` (max 20 per call) on the original
   PDF in `~/Documents/Family Tree/`.
5. Append entries to `parser/raw_entries.py`, run `python3 parser/build.py`,
   commit both `raw_entries.py` and `data/people.json` together.

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
