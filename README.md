# family.sudoservers.com

Family tree dataset and (eventually) website for the descendants of an unnamed
Guthrie patriarch, compiled from seven scanned PDF genealogies in
`~/Documents/Family Tree/`.

## Layout

```
schema/         JSON Schema for the dataset.
parser/         Build pipeline.
  raw_entries.py   Hand-curated source of truth. Edit this to add/change people.
  build.py         Reads raw_entries.py, resolves relationships, writes people.json.
data/           Generated output.
  people.json   Final dataset consumed by the website.
```

## Adding or editing a person

1. Open `parser/raw_entries.py`.
2. Append (or modify) a dict in `ENTRIES` using the format documented at the
   top of that file.
3. Run `python3 parser/build.py`.
4. Commit both `raw_entries.py` and `data/people.json` together so the source
   and output stay in sync.

## Cross-references (same person, two lineage codes)

When the same person appears in two source PDFs under different codes (e.g.
Ray Guthrie is both `74A` in James's branch and `172A` in John's branch),
add an entry to `SEE_REFS` in `raw_entries.py`. The build script merges the
two codes into one person record while preserving both codes in
`lineageCodes`.

## The numbering scheme

Each character of a lineage code is one generation. Single character =
founder's children (1 = John, 2 = William, 5 = Stephen, 6 = Rachel, 7 =
James, 8 = Absalom, A = Alexander). Two characters = grandchildren, etc.
Children are numbered 1-9 then A-Z to allow families larger than nine.

The build script treats single-character codes as children of code `0`
(the inferred but unnamed common patriarch).
