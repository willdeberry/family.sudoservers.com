# Project status

Last updated: 2026-05-28

## What exists

- 187 people in `data/people.json`, generated from `parser/raw_entries.py`
- All 7 sibling branches present
- 12 cross-branch marriages with dedup working (see SEE_REFS in raw_entries.py)
- Tree depth: 7 generations from inferred founder (code `0`)

## Source PDFs and transcription coverage

PDFs live at `~/Documents/Family Tree/`. They are scanned images — no
embedded text. Earlier sessions used Claude's vision to read pages.

| PDF | Pages | Coverage |
|---|---|---|
| Rachel_Guthrie - One Generation.pdf | 1 | ~80% (5/5 gen-1 children; 2/5 gen-2) |
| William_Guthrie - One Generation.pdf | 3 | ~30% (root + 2/4 children; no gen-3) |
| Absalom_Guthrie - One Generation.pdf | 4 | ~40% (root + most gen-1; spotty gen-2) |
| Stephen_Guthrie - One Generation.pdf | 6 | ~25% (root + headline kids; deep gens thin) |
| Alexander_Guthrie - Five Generations.pdf | 11 | ~30% (root + key gen-1/2; some gen-3/4 chains) |
| James_Guthrie - Seven Generations.pdf | 32 | ~20% (root + key cross-branch nodes; gen 4-7 mostly empty) |
| John_Guthrie - Eight Generations.pdf | 147 | ~10% (root + key gen 2-4 chains; ~600+ people remain) |

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
3. `python3 parser/report_stubs.py` — lists people who exist as references
   but have no full entry yet. That's the surface-level to-do.
4. The deeper to-do is in the PDFs themselves. To know what's missing,
   read a page range of a PDF that's not yet well-covered (see coverage
   table above) and compare codes to what's in raw_entries.py.
5. The PDFs are large; use the Read tool with `pages: "N-M"` (max 20 per
   call). Strategy: take a range, find codes, search `parser/raw_entries.py`
   for each code, transcribe missing ones.
6. After adding entries: `python3 parser/build.py`, then commit both
   `raw_entries.py` and `data/people.json` together.

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
