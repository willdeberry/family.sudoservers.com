# family.sudoservers.com

Genealogy dataset and website for the descendants of an unnamed Guthrie
patriarch. Source: seven scanned PDF genealogies at
`~/Documents/Family Tree/`. Live site: <https://family.sudoservers.com>.

## Two halves

- **Dataset** (Python). `parser/raw_entries.py` → `parser/build.py` →
  `data/people.json`. See `STATUS.md` for transcription/verification state.
- **Website** (Astro + Tailwind + family-chart) in `web/`. See `web/README.md`
  for the dev/deploy loop.

## Read first

- `STATUS.md` — current coverage, decision log, pickup checklist.
- `README.md` — repo layout and the edit-and-rebuild loop.
- `parser/raw_entries.py` — docstring at the top documents the entry format.

## Workflow

Edit `parser/raw_entries.py`, run `python3 parser/build.py`, commit both.
Never hand-edit `data/people.json` — it's generated.

## Useful commands

```bash
python3 parser/build.py                       # rebuild data/people.json
python3 parser/verify.py --stats              # verification progress
python3 parser/verify.py --pdf <branch>       # next batch of drafts to verify
python3 parser/verify.py --code 13F71         # detail on one entry
python3 parser/draft_from_ocr.py --pdf <branch> --missing-only  # extract more drafts
python3 parser/report_missing.py              # codes in OCR but not in dataset
python3 parser/report_stubs.py                # people referenced but no full entry
```

## Workflow note

The dataset is structurally complete (1351 people, all 7 branches, 7+
generations). The active work is **verification**: most entries are OCR
drafts (`verification.status == "draft"`) that need vision review against
the source PDF. Use `verify.py` to get worklists grouped by PDF page.

## OCR vs vision

`ocr/<branch>.txt` exists for grepping and the coverage report only. It
has digit errors (e.g. "15 Nov" → "14 Nov") that are dangerous for
genealogy. **Always use Claude's vision on the original PDF** in
`~/Documents/Family Tree/` for accurate transcription of an entry. The
OCR just tells you *which* codes exist.

## Key facts about the data

- Lineage codes use 1-9 then A-Z to allow >9 children per family. Each char
  is one generation. `74A` = Alexander's branch, 4th child of 7th sibling,
  10th grandchild on that line.
- The seven sibling roots are: `1` John, `2` William, `5` Stephen,
  `6` Rachel, `7` James, `8` Absalom, `A` Alexander. Codes 3, 4, 9 belong
  to undocumented siblings.
- Code `0` is the inferred common patriarch — not in any PDF, added so all
  branches connect.
- Cross-branch marriages (same person under two codes) go in `SEE_REFS`
  in `raw_entries.py`. The build script merges them while preserving both
  codes in `lineageCodes`.

## PDF reading

PDFs are scanned images — `pdftotext` returns nothing. Use the Read tool
with `pages: "N-M"` (20-page max per call). Vision handles the OCR.
