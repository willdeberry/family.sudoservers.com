#!/usr/bin/env python3
"""
Build people.json from raw_entries.py.

raw_entries.py holds genealogical entries as Python dicts — one per lineage code
from the source PDFs. This script:
  1. Loads ENTRIES and SEE_REFS
  2. Assigns stable person IDs
  3. Merges entries that the SEE_REFS table marks as the same person
  4. Resolves parent/child relationships from lineage codes
  5. Materializes spouses as full Person records when they have enough data
  6. Emits data/people.json

Re-run after editing raw_entries.py.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "parser"))

from raw_entries import ENTRIES, SEE_REFS, FOUNDER_NOTE, SOURCE_FILES  # noqa: E402

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}


def parse_date(raw):
    """Parse a date string. Returns (iso_or_none, raw_string_or_none)."""
    if not raw:
        return None, None
    raw = raw.strip()
    if not raw:
        return None, None

    # Strict "DD Mon YYYY"
    m = re.fullmatch(r"(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})", raw)
    if m:
        d, mon, y = int(m.group(1)), m.group(2).lower()[:4], int(m.group(3))
        mon_key = mon if mon in MONTHS else mon[:3]
        if mon_key in MONTHS:
            try:
                return date(y, MONTHS[mon_key], d).isoformat(), raw
            except ValueError:
                return None, raw

    # "Mon YYYY"
    m = re.fullmatch(r"([A-Za-z]+)\.?\s+(\d{4})", raw)
    if m:
        return None, raw  # month-precision: keep raw only

    # Year only
    if re.fullmatch(r"\d{4}", raw):
        return None, raw

    # Anything else (about/before/circa/etc.) — preserve raw
    return None, raw


def parent_code(code):
    """Return the parent's lineage code, or None for the absolute root.

    Single-character sibling codes (1-9, A-Z) all share founder code '0'.
    """
    if code == "0":
        return None
    if len(code) == 1:
        return "0"
    return code[:-1]


def make_lifeevent(raw_date, place=None):
    if not raw_date and not place:
        return None
    iso, raw = parse_date(raw_date) if raw_date else (None, None)
    out = {}
    if iso:
        out["date"] = iso
    if raw:
        out["dateRaw"] = raw
    if place:
        out["place"] = place
    return out or None


def split_name(full):
    """Split 'First Middle Last' into components. Best-effort."""
    if not full:
        return {"full": full, "first": None, "middle": None, "last": None}
    parts = full.split()
    if len(parts) == 1:
        return {"full": full, "first": parts[0], "middle": None, "last": None}
    if len(parts) == 2:
        return {"full": full, "first": parts[0], "middle": None, "last": parts[1]}
    return {
        "full": full,
        "first": parts[0],
        "middle": " ".join(parts[1:-1]) or None,
        "last": parts[-1],
    }


def build():
    # Map lineage code → entry index
    code_to_entry = {}
    for entry in ENTRIES:
        code = entry["code"]
        if code in code_to_entry:
            raise ValueError(f"Duplicate code in ENTRIES: {code}")
        code_to_entry[code] = entry

    # Resolve SEE_REFS: which codes refer to the same person
    # `canonical_code[code]` returns the chosen canonical code for that person.
    canonical_code = {c: c for c in code_to_entry}
    for ref in SEE_REFS:
        a, b = ref["codes"]
        # Prefer a code that has a full entry. If both or neither do, take the
        # lexicographically smaller one. This guarantees the canonical pid
        # actually receives the person's data.
        a_has = a in code_to_entry
        b_has = b in code_to_entry
        if a_has and not b_has:
            canonical, other = a, b
        elif b_has and not a_has:
            canonical, other = b, a
        else:
            canonical, other = min(a, b), max(a, b)
        canonical_code[other] = canonical
        canonical_code[canonical] = canonical

    # Assign person IDs to canonical codes only
    canonical_codes = sorted(set(canonical_code.values()))
    code_to_pid = {}
    for i, code in enumerate(canonical_codes, start=1):
        code_to_pid[code] = f"p_{i:06d}"
    # Non-canonical codes get the same pid as their canonical
    for code, can in canonical_code.items():
        code_to_pid[code] = code_to_pid[can]

    # Build people dict keyed by pid
    people = {}

    def ensure_person(pid, code=None):
        if pid not in people:
            people[pid] = {
                "id": pid,
                "lineageCodes": [],
                "name": None,
                "sex": None,
                "birth": None,
                "death": None,
                "burial": None,
                "parentIds": [],
                "marriages": [],
                "childIds": [],
                "residences": [],
                "occupation": None,
                "notes": None,
                "sources": [],
                "flags": {},
                "verification": {
                    "status": "draft",
                    "source": "manual",
                    "lastChecked": None,
                    "notes": "Auto-created from a relationship link; no source data yet.",
                },
            }
        if code and code not in people[pid]["lineageCodes"]:
            people[pid]["lineageCodes"].append(code)
        return people[pid]

    # First pass: populate from each entry
    for code, entry in code_to_entry.items():
        pid = code_to_pid[code]
        p = ensure_person(pid, code)

        if not p["name"]:
            p["name"] = split_name(entry["name"])

        if "sex" in entry and not p["sex"]:
            p["sex"] = entry["sex"]

        if "born" in entry and not p["birth"]:
            p["birth"] = make_lifeevent(entry.get("born"), entry.get("born_place"))
            if entry.get("born_alt"):
                # Stash alternative date in dateRaw for transparency
                if p["birth"] is None:
                    p["birth"] = {}
                p["birth"]["dateRaw"] = (p["birth"].get("dateRaw") or entry["born"]) + f" (alt: {entry['born_alt']})"

        if "died" in entry and not p["death"]:
            p["death"] = make_lifeevent(entry.get("died"), entry.get("died_place"))

        if entry.get("buried") and not p["burial"]:
            p["burial"] = {"place": entry["buried"]}

        if entry.get("notes") and not p["notes"]:
            p["notes"] = entry["notes"]

        if entry.get("residences"):
            for r in entry["residences"]:
                if r not in p["residences"]:
                    p["residences"].append(r)

        if entry.get("occupation") and not p["occupation"]:
            p["occupation"] = entry["occupation"]

        if entry.get("flags"):
            p["flags"].update(entry["flags"])

        # Verification status. A full entry in raw_entries.py is treated as
        # verified/manual unless it explicitly says otherwise (the drafter
        # sets status=draft, source=ocr for entries it produced).
        v = entry.get("verification") or {
            "status": "verified",
            "source": "manual",
            "lastChecked": None,
            "notes": None,
        }
        p["verification"] = v

        # Sources
        src = entry.get("source", {})
        if src:
            src_record = {"pdf": src.get("pdf"), "entryCode": code, "page": src.get("page")}
            if src_record not in p["sources"]:
                p["sources"].append(src_record)

        # Spouses → marriages
        for sp in entry.get("spouses", []):
            marriage = {
                "spouseId": None,  # filled in pass 2 if spouse exists in dataset
                "spouseName": sp.get("name"),
                "spouseDetails": sp.get("details"),
                "date": None,
                "dateRaw": None,
                "place": sp.get("married_place"),
                "marriageOrder": sp.get("order"),
                "notes": sp.get("notes"),
                "_spouseBirth": sp.get("born"),
                "_spouseDeath": sp.get("died"),
                "_spouseBuried": sp.get("buried"),
                "_spouseFather": sp.get("father"),
                "_spouseMother": sp.get("mother"),
            }
            iso, raw = parse_date(sp.get("married")) if sp.get("married") else (None, None)
            marriage["date"] = iso
            marriage["dateRaw"] = raw
            p["marriages"].append(marriage)

    # Post-pass: ensure SEE_REF codes both land in lineageCodes (even if only
    # one side had a full entry — the SEE_REF itself is the assertion).
    for ref in SEE_REFS:
        for code in ref["codes"]:
            pid = code_to_pid.get(code)
            if pid and pid in people:
                if code not in people[pid]["lineageCodes"]:
                    people[pid]["lineageCodes"].append(code)

    # Second pass: parent/child relationships from EVERY known lineage code,
    # not just ones that have full entries. This catches SEE_REF codes too —
    # e.g., 172A inherits parent 172 even when only 74A has a full entry.
    all_codes = set(code_to_pid.keys())
    for code in all_codes:
        pcode = parent_code(code)
        if not pcode or pcode not in code_to_pid:
            continue
        child_pid = code_to_pid[code]
        parent_pid = code_to_pid[pcode]
        if child_pid == parent_pid:
            continue  # safety: avoid self-parenting
        if child_pid not in people:
            ensure_person(child_pid, code)
        if parent_pid not in people:
            ensure_person(parent_pid, pcode)
        if parent_pid not in people[child_pid]["parentIds"]:
            people[child_pid]["parentIds"].append(parent_pid)
        if child_pid not in people[parent_pid]["childIds"]:
            people[parent_pid]["childIds"].append(child_pid)

    # Also process declared children (entries that list children inline but don't have
    # their own full entry yet — we create stub people for them)
    for code, entry in code_to_entry.items():
        if "children" not in entry:
            continue
        parent_pid = code_to_pid[code]
        for child in entry["children"]:
            ccode = child["code"]
            if ccode in code_to_pid:
                # Already has a full entry OR is a SEE_REF cross-code.
                # If the person exists but has no name yet (SEE_REF cross-code
                # where neither side had a full entry), populate from this
                # children-list entry.
                existing_pid = code_to_pid[ccode]
                if existing_pid in people and not people[existing_pid].get("name"):
                    p = people[existing_pid]
                    p["name"] = split_name(child["name"])
                    if child.get("born"):
                        p["birth"] = make_lifeevent(child.get("born"))
                    if child.get("died"):
                        p["death"] = make_lifeevent(child.get("died"))
                    if child.get("flags"):
                        p["flags"].update(child["flags"])
                    p["sources"].append({
                        "pdf": entry.get("source", {}).get("pdf"),
                        "entryCode": ccode,
                        "page": entry.get("source", {}).get("page"),
                    })
                    # Cross-coded SEE_REF child where neither side has a
                    # full entry — still a draft until its own line is read.
                    p["verification"] = {
                        "status": "draft",
                        "source": "manual",
                        "lastChecked": None,
                        "notes": "Stub from parent's children list (SEE_REF cross-code). PDF's own line for this person not yet transcribed.",
                    }
                continue
            # Create a stub person
            canonical_code[ccode] = ccode
            canonical_codes_set = set(code_to_pid.values())
            new_pid = f"p_{len(canonical_codes_set) + 1:06d}"
            code_to_pid[ccode] = new_pid
            stub = ensure_person(new_pid, ccode)
            stub["name"] = split_name(child["name"])
            if child.get("born"):
                stub["birth"] = make_lifeevent(child.get("born"))
            if child.get("died"):
                stub["death"] = make_lifeevent(child.get("died"))
            if child.get("flags"):
                stub["flags"].update(child["flags"])
            stub["parentIds"].append(parent_pid)
            people[parent_pid]["childIds"].append(new_pid)
            stub["sources"].append({
                "pdf": entry.get("source", {}).get("pdf"),
                "entryCode": ccode,
                "page": entry.get("source", {}).get("page"),
            })
            # Stubs from a parent's children list have NOT been directly
            # verified — we've only seen this person's name+date listed
            # under their parent's entry. Their own line in the PDF (with
            # marriage, residence, children, death detail) has not been
            # transcribed. They stay draft until someone reads their entry.
            stub["verification"] = {
                "status": "draft",
                "source": "manual",
                "lastChecked": None,
                "notes": "Stub from parent's children list. PDF's own line for this person not yet transcribed — may contain marriage/death/children data not captured here.",
            }

    # Sort child IDs by their lineage code so birth order is preserved
    pid_to_code = {pid: code for code, pid in code_to_pid.items()
                   if canonical_code.get(code) == code}
    # For sorting, use the canonical code
    def code_sort_key(pid):
        # Find the canonical code for this pid
        for code, p in code_to_pid.items():
            if p == pid and canonical_code.get(code) == code:
                return code
        return ""
    for p in people.values():
        p["childIds"].sort(key=code_sort_key)

    # Auto-link spouses: when a marriage's spouseName matches another person's
    # full name (case-insensitive), populate spouseId. Best-effort heuristic;
    # ambiguous matches (same name, multiple people) are left unlinked.
    name_index = {}
    for pid, p in people.items():
        full = (p.get("name") or {}).get("full")
        if full:
            name_index.setdefault(full.lower().strip(), []).append(pid)

    for pid, p in people.items():
        for m in p.get("marriages", []):
            if m.get("spouseId") or not m.get("spouseName"):
                continue
            key = m["spouseName"].lower().strip()
            matches = name_index.get(key, [])
            # Require exactly one match AND it shouldn't be self
            matches = [x for x in matches if x != pid]
            if len(matches) == 1:
                m["spouseId"] = matches[0]

    # Clean: remove None-valued fields for compactness
    output_people = []
    for pid in sorted(people.keys()):
        p = people[pid]
        # Drop ephemeral _spouse* fields
        cleaned_marriages = []
        for m in p["marriages"]:
            cm = {k: v for k, v in m.items() if not k.startswith("_") and v is not None}
            cleaned_marriages.append(cm)
        cleaned = {k: v for k, v in p.items() if v not in (None, [], {}, "")}
        cleaned["marriages"] = cleaned_marriages
        if not cleaned_marriages:
            cleaned.pop("marriages", None)
        output_people.append(cleaned)

    dataset = {
        "version": "1.0",
        "metadata": {
            "lastUpdated": date.today().isoformat(),
            "sourceFiles": SOURCE_FILES,
            "founderNote": FOUNDER_NOTE,
        },
        "people": output_people,
    }

    out_path = REPO / "data" / "people.json"
    out_path.write_text(json.dumps(dataset, indent=2, ensure_ascii=False))
    print(f"Wrote {len(output_people)} people → {out_path}")
    return dataset


if __name__ == "__main__":
    build()
