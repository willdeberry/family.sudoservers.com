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

from raw_entries import (  # noqa: E402
    ENTRIES,
    SEE_REFS,
    FOUNDER_NOTE,
    SOURCE_FILES,
)
try:
    from raw_entries import EXTERNAL_ENTRIES  # noqa: E402
except ImportError:
    EXTERNAL_ENTRIES = []

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
                "_spouseBirthPlace": sp.get("born_place"),
                "_spouseDeath": sp.get("died"),
                "_spouseDeathPlace": sp.get("died_place"),
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

    def birth_year(person):
        b = (person.get("birth") or {}).get("dateRaw") or ""
        m = re.search(r"\b(1[6-9]\d{2}|20\d{2})\b", b)
        return int(m.group(1)) if m else None

    for pid, p in people.items():
        for m in p.get("marriages", []):
            if m.get("spouseId") or not m.get("spouseName"):
                continue
            key = m["spouseName"].lower().strip()
            matches = name_index.get(key, [])
            # Exclude self AND anyone who's already a parent or child of this
            # person — same-name father/son or mother/daughter pairs are common
            # and otherwise the auto-linker happily makes Ross Jr his own dad.
            forbidden = {pid}
            forbidden.update(p.get("parentIds", []))
            forbidden.update(p.get("childIds", []))
            matches = [x for x in matches if x not in forbidden]

            # If we have a spouse birth year from the marriage record, prefer
            # candidates whose own birth year matches (within a year tolerance).
            spouse_birth = m.get("_spouseBirth") or ""
            spouse_year_m = re.search(r"\b(1[6-9]\d{2}|20\d{2})\b", spouse_birth)
            if spouse_year_m and len(matches) > 0:
                target_year = int(spouse_year_m.group(1))
                year_matches = [
                    x for x in matches
                    if birth_year(people[x]) is not None
                    and abs(birth_year(people[x]) - target_year) <= 1
                ]
                if year_matches:
                    matches = year_matches

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
            if m.get("_spouseBirth") or m.get("_spouseBirthPlace"):
                sp_person["birth"] = make_lifeevent(
                    m.get("_spouseBirth"), m.get("_spouseBirthPlace")
                )
            if m.get("_spouseDeath") or m.get("_spouseDeathPlace"):
                sp_person["death"] = make_lifeevent(
                    m.get("_spouseDeath"), m.get("_spouseDeathPlace")
                )
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

            # Materialize the spouse's own parents when the spouse dict
            # carried `father`/`mother`. Plain-string form ("Ralph Edward
            # Hughs") creates a name-only stub; dict form
            # ({"name":..., "born":..., "died":...}) carries through life
            # events too. Either way the resulting person is linked as a
            # parent of the spouse so the suggestion/edit flow can surface
            # them as grandparents in the tree.
            for role, key_name in (
                ("father", "_spouseFather"),
                ("mother", "_spouseMother"),
            ):
                raw_parent = m.get(key_name)
                if not raw_parent:
                    continue
                parent_info = (
                    {"name": raw_parent} if isinstance(raw_parent, str) else dict(raw_parent)
                )
                if not parent_info.get("name"):
                    continue
                spouse_counter += 1
                parent_pid = f"sp_{spouse_counter:06d}"
                ensure_person(parent_pid, None)
                parent_p = people[parent_pid]
                parent_p["name"] = split_name(parent_info["name"])
                parent_p["sex"] = "M" if role == "father" else "F"
                if parent_info.get("born") or parent_info.get("born_place"):
                    parent_p["birth"] = make_lifeevent(
                        parent_info.get("born"), parent_info.get("born_place")
                    )
                if parent_info.get("died") or parent_info.get("died_place"):
                    parent_p["death"] = make_lifeevent(
                        parent_info.get("died"), parent_info.get("died_place")
                    )
                parent_p["verification"] = {
                    "status": "verified",
                    "source": "vision",
                    "lastChecked": p.get("verification", {}).get("lastChecked"),
                    "notes": (
                        f"Materialized as {role} of {spouse_name} (spouse of {primary_code})."
                    ),
                }
                if parent_pid not in sp_person["parentIds"]:
                    sp_person["parentIds"].append(parent_pid)
                if sp_pid not in parent_p["childIds"]:
                    parent_p["childIds"].append(sp_pid)

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
            # Defensive: never make a person their own parent. Same-name
            # father/son pairs (e.g. Ross Carlton Miller Sr/Jr) used to slip
            # through here when the auto-linker mis-linked the parent to
            # the child as a spouse.
            if primary_sp_id == child_id:
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

    # ── External entries (codeless people whose bio parents we declare by
    # reference rather than via the Guthrie lineage-code mechanism). Used for
    # step-children whose other biological parent isn't a Guthrie descendant:
    # we want the accurate parentage on the record, but they have no place in
    # the sibling-order code system.
    if EXTERNAL_ENTRIES:
        # Build a name → [pid] index of every person we already have, so
        # parent refs can match against materialized spouses too.
        ext_name_index = {}
        for pid_, p_ in people.items():
            full = (p_.get("name") or {}).get("full")
            if full:
                ext_name_index.setdefault(full.lower().strip(), []).append(pid_)

        def find_existing(ref):
            name = (ref.get("name") or "").lower().strip()
            if not name:
                return None
            matches = ext_name_index.get(name, [])
            if len(matches) == 1:
                return matches[0]
            if len(matches) > 1 and ref.get("born"):
                ref_year = re.search(r"\b(1[6-9]\d{2}|20\d{2})\b", ref["born"])
                if ref_year:
                    target = int(ref_year.group(1))
                    for cand_pid in matches:
                        cb = (people[cand_pid].get("birth") or {}).get("dateRaw") or \
                             (people[cand_pid].get("birth") or {}).get("date") or ""
                        m = re.search(r"\b(1[6-9]\d{2}|20\d{2})\b", cb)
                        if m and abs(int(m.group(1)) - target) <= 1:
                            return cand_pid
            return None

        # Allocate pids for the external entries themselves. Continue the
        # p_NNNNNN sequence so existing ids don't shift around.
        used_nums = [
            int(pid_[2:]) for pid_ in people.keys()
            if pid_.startswith("p_") and pid_[2:].isdigit()
        ]
        next_p_num = (max(used_nums) + 1) if used_nums else 1

        for entry in EXTERNAL_ENTRIES:
            ext_pid = f"p_{next_p_num:06d}"
            next_p_num += 1
            ensure_person(ext_pid, None)
            p_ = people[ext_pid]
            p_["name"] = split_name(entry["name"])
            if entry.get("sex"):
                p_["sex"] = entry["sex"]
            if entry.get("born") or entry.get("born_place"):
                p_["birth"] = make_lifeevent(entry.get("born"), entry.get("born_place"))
            if entry.get("died") or entry.get("died_place"):
                p_["death"] = make_lifeevent(entry.get("died"), entry.get("died_place"))
            if entry.get("buried"):
                p_["burial"] = {"place": entry["buried"]}
            if entry.get("notes"):
                p_["notes"] = entry["notes"]
            if entry.get("occupation"):
                p_["occupation"] = entry["occupation"]
            if entry.get("residences"):
                p_["residences"] = list(entry["residences"])
            if entry.get("source"):
                src = entry["source"]
                p_["sources"].append({
                    "pdf": src.get("pdf"),
                    "entryCode": None,
                    "page": src.get("page"),
                })
            p_["verification"] = entry.get("verification") or {
                "status": "verified",
                "source": "user-submission",
                "lastChecked": None,
                "notes": None,
            }
            # Resolve / materialize parents
            for ref in entry.get("parent_refs", []):
                parent_pid = find_existing(ref)
                if parent_pid is None:
                    # Materialize a new "loose" person record (sp_ namespace,
                    # since they have no children's-list lineage of their own).
                    spouse_counter += 1
                    parent_pid = f"sp_{spouse_counter:06d}"
                    ensure_person(parent_pid, None)
                    parent_p = people[parent_pid]
                    parent_p["name"] = split_name(ref["name"])
                    if ref.get("sex"):
                        parent_p["sex"] = ref["sex"]
                    if ref.get("born") or ref.get("born_place"):
                        parent_p["birth"] = make_lifeevent(
                            ref.get("born"), ref.get("born_place")
                        )
                    if ref.get("died") or ref.get("died_place"):
                        parent_p["death"] = make_lifeevent(
                            ref.get("died"), ref.get("died_place")
                        )
                    parent_p["verification"] = {
                        "status": "verified",
                        "source": "user-submission",
                        "lastChecked": None,
                        "notes": (
                            f"Materialized as biological parent of "
                            f"{(p_.get('name') or {}).get('full')} via external entry."
                        ),
                    }
                    # Index the new parent for any subsequent external entries
                    # that might reference them.
                    ext_name_index.setdefault(ref["name"].lower().strip(), []).append(parent_pid)
                if parent_pid not in p_["parentIds"]:
                    p_["parentIds"].append(parent_pid)
                if ext_pid not in people[parent_pid]["childIds"]:
                    people[parent_pid]["childIds"].append(ext_pid)

    # Integrity sweep: family-chart will infinite-loop on self-references or
    # bidirectional parent/child links. Drop any that slipped past the guards
    # above (most commonly from auto-link mis-matches we couldn't catch).
    self_refs_removed = 0
    cycles_removed = 0
    for pid, p in people.items():
        if pid in p.get("parentIds", []):
            p["parentIds"] = [x for x in p["parentIds"] if x != pid]
            self_refs_removed += 1
        if pid in p.get("childIds", []):
            p["childIds"] = [x for x in p["childIds"] if x != pid]
            self_refs_removed += 1
    # Bidirectional A↔B parent/child: keep only one direction, decided by
    # who has the lower-numbered (older) pid. Father is usually p_NN < child's pid.
    for pid, p in people.items():
        for child_id in list(p.get("childIds", [])):
            child = people.get(child_id)
            if not child:
                continue
            if pid in child.get("childIds", []):
                # Pick the parent: the one with the smaller pid wins
                parent_pid = min(pid, child_id)
                child_pid = max(pid, child_id)
                people[parent_pid]["childIds"] = [
                    x for x in people[parent_pid]["childIds"] if x != parent_pid
                ]
                # Remove the wrong-way edge: parent_pid as child of child_pid
                if parent_pid in people[child_pid].get("childIds", []):
                    people[child_pid]["childIds"].remove(parent_pid)
                if child_pid in people[parent_pid].get("parentIds", []):
                    people[parent_pid]["parentIds"].remove(child_pid)
                cycles_removed += 1
    if self_refs_removed or cycles_removed:
        print(f"Integrity sweep: removed {self_refs_removed} self-refs, {cycles_removed} cycles")

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
