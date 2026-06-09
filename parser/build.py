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

        # Spouses → marriages. Dedupe: when SEE_REF merges two entries for the
        # same person, both may carry the same marriage. Skip if we've already
        # added a marriage with the same spouse name (case-insensitive).
        existing_spouse_names = {
            (m.get("spouseName") or "").lower().strip()
            for m in p["marriages"]
        }
        for sp in entry.get("spouses", []):
            sp_name = (sp.get("name") or "").lower().strip()
            if sp_name and sp_name in existing_spouse_names:
                continue
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
            existing_spouse_names.add(sp_name)

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
        # Always ensure both codes are recorded on the person record, even when
        # the person already exists (handles SEE_REF cross-codes both flowing
        # through here at separate iterations).
        ensure_person(child_pid, code)
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
                    if child.get("verified_terminal"):
                        parent_v = entry.get("verification") or {"status": "verified", "source": "manual"}
                        p["verification"] = {
                            "status": "verified",
                            "source": parent_v.get("source", "manual"),
                            "lastChecked": parent_v.get("lastChecked"),
                            "notes": "Terminal stub: confirmed against source PDF — no separate entry for this person; parent's children list is the complete data.",
                        }
                    else:
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
            # verified UNLESS the children-list entry has the explicit flag
            # `verified_terminal=True` — meaning the transcriber has read the
            # source PDF page and confirmed the PDF says no more about this
            # person than what's in the children list (i.e., no own-entry).
            if child.get("verified_terminal"):
                parent_v = entry.get("verification") or {"status": "verified", "source": "manual"}
                stub["verification"] = {
                    "status": "verified",
                    "source": parent_v.get("source", "manual"),
                    "lastChecked": parent_v.get("lastChecked"),
                    "notes": "Terminal stub: confirmed against source PDF — no separate entry for this person; parent's children list is the complete data.",
                }
            else:
                stub["verification"] = {
                    "status": "draft",
                    "source": "manual",
                    "lastChecked": None,
                    "notes": "Stub from parent's children list. PDF's own line for this person not yet transcribed — may contain marriage/death/children data not captured here.",
                }

    # Re-run the parent/child code-prefix linkage now that pass 3 has added
    # children-list stubs to code_to_pid. Without this, a grandchild whose
    # immediate parent is a stub (e.g. 71721 whose parent 7172 only exists as
    # a verified_terminal child of 717) would never get its parent link.
    all_codes = set(code_to_pid.keys())
    for code in all_codes:
        pcode = parent_code(code)
        if not pcode or pcode not in code_to_pid:
            continue
        child_pid = code_to_pid[code]
        parent_pid = code_to_pid[pcode]
        if child_pid == parent_pid:
            continue
        ensure_person(child_pid, code)
        ensure_person(parent_pid, pcode)
        if parent_pid not in people[child_pid]["parentIds"]:
            people[child_pid]["parentIds"].append(parent_pid)
        if child_pid not in people[parent_pid]["childIds"]:
            people[parent_pid]["childIds"].append(child_pid)

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

    # Add reciprocal marriages for any auto-linked spouses where the spouse
    # doesn't have a back-marriage to this person. Without this, the chart
    # would render the relationship only one direction.
    for pid, p in list(people.items()):
        for m in p.get("marriages", []):
            sp_id = m.get("spouseId")
            if not sp_id or sp_id not in people:
                continue
            sp = people[sp_id]
            # Does the spouse already have a marriage back to this person?
            if any(mm.get("spouseId") == pid for mm in sp.get("marriages", [])):
                continue
            # Add a reciprocal marriage
            sp["marriages"].append({
                "spouseId": pid,
                "spouseName": (p.get("name") or {}).get("full"),
                "date": m.get("date"),
                "dateRaw": m.get("dateRaw"),
                "place": m.get("place"),
                "marriageOrder": None,
                "notes": None,
            })

    # Materialize spouses as Person records. Every named spouse that doesn't
    # already correspond to an existing person becomes a synthetic node so the
    # family-chart can render them.
    #
    # Dedup: if a spouse name + birth year matches an already-materialized
    # synthetic spouse, reuse that pid instead of creating a duplicate. This
    # handles the case where one person had two marriages — e.g. Jacob Peter
    # Barnes married Sarah Ann Guthrie then Amanda Jane Harshbarger; both
    # wives reference him and he should be a SINGLE synth record with two
    # marriages, not two synthetic Jacobs.

    def spouse_key(m_dict):
        name = (m_dict.get("spouseName") or "").lower().strip()
        born = (m_dict.get("_spouseBirth") or "").strip()
        return (name, born) if name else None

    materialized_by_key = {}
    spouse_counter = 0
    for pid in list(people.keys()):
        p = people[pid]
        for idx, m in enumerate(p.get("marriages", [])):
            if m.get("spouseId"):
                continue
            spouse_name = m.get("spouseName")
            if not spouse_name:
                continue

            key = spouse_key(m)
            existing_sp_pid = materialized_by_key.get(key) if key else None

            if existing_sp_pid:
                # Reuse the existing synth: just add a marriage on their side
                # pointing back to this person.
                sp_person = people[existing_sp_pid]
                if not any(mm.get("spouseId") == pid for mm in sp_person.get("marriages", [])):
                    sp_person["marriages"].append({
                        "spouseId": pid,
                        "spouseName": (p.get("name") or {}).get("full"),
                        "date": m.get("date"),
                        "dateRaw": m.get("dateRaw"),
                        "place": m.get("place"),
                        "marriageOrder": m.get("marriageOrder"),
                        "notes": m.get("notes"),
                    })
                m["spouseId"] = existing_sp_pid
                continue

            spouse_counter += 1
            sp_pid = f"sp_{spouse_counter:06d}"
            primary_code = (p.get("lineageCodes") or ["?"])[0]
            spouse_code = f"{primary_code}-sp{idx+1}"
            ensure_person(sp_pid, spouse_code)
            sp_person = people[sp_pid]
            sp_person["name"] = split_name(spouse_name)
            if p.get("sex") == "M":
                sp_person["sex"] = "F"
            elif p.get("sex") == "F":
                sp_person["sex"] = "M"
            if m.get("_spouseBirth"):
                sp_person["birth"] = make_lifeevent(m["_spouseBirth"])
            if m.get("_spouseDeath"):
                sp_person["death"] = make_lifeevent(m["_spouseDeath"])
            if m.get("_spouseBuried"):
                sp_person["burial"] = {"place": m["_spouseBuried"]}
            sp_person["sources"] = list(p.get("sources") or [])
            sp_person["verification"] = {
                "status": "verified",
                "source": "vision",
                "lastChecked": p.get("verification", {}).get("lastChecked"),
                "notes": f"Materialized spouse of {primary_code}; data from that entry's spouses array.",
            }
            sp_person["marriages"].append({
                "spouseId": pid,
                "spouseName": (p.get("name") or {}).get("full"),
                "date": m.get("date"),
                "dateRaw": m.get("dateRaw"),
                "place": m.get("place"),
                "marriageOrder": m.get("marriageOrder"),
                "notes": m.get("notes"),
            })
            m["spouseId"] = sp_pid
            if key:
                materialized_by_key[key] = sp_pid

    # Link spouses as co-parents of their partner's children. Without this,
    # children only get a single parent (the lineage-code path), so the chart
    # only renders one parent line. Heuristic: if person A is married to B
    # and A has children, B is also a parent of those children — UNLESS those
    # children already have a different second parent (i.e., from a prior
    # marriage of A) AND the child's birth doesn't fall in this marriage's
    # window. For now we use the simpler rule: take A's marriageOrder=1 spouse
    # as the default co-parent of every A-child who has no second parent.
    for pid, p in list(people.items()):
        if not p.get("marriages"):
            continue
        # Pick the primary spouse: marriageOrder=1, or first marriage if none flagged
        primary_sp_id = None
        ordered = sorted(p["marriages"], key=lambda mm: (mm.get("marriageOrder") or 99))
        for m in ordered:
            if m.get("spouseId"):
                primary_sp_id = m["spouseId"]
                break
        if not primary_sp_id:
            continue
        for child_id in p.get("childIds", []):
            child = people.get(child_id)
            if not child:
                continue
            # Already has 2+ parents — skip
            if len(child.get("parentIds", [])) >= 2:
                continue
            if primary_sp_id in child.get("parentIds", []):
                continue
            child["parentIds"].append(primary_sp_id)
            # Mirror: the spouse gets the child too
            sp = people.get(primary_sp_id)
            if sp and child_id not in sp.get("childIds", []):
                sp["childIds"].append(child_id)

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
