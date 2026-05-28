#!/usr/bin/env python3
"""
Report which people in data/people.json are stubs vs full entries.

A "stub" is a person who exists only because they're named as a child of
someone else, but has no full entry of their own in raw_entries.py.
A "full" entry has at minimum birth or death dates.

This is the natural to-do list for continued transcription. Run after
build.py to see what's outstanding.

Usage:
    python3 parser/report_stubs.py
    python3 parser/report_stubs.py --branch 1   # filter to John's line
    python3 parser/report_stubs.py --depth 3    # only codes <= 3 chars long
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def is_stub(p):
    """A stub has no birth, death, marriages, or notes."""
    return not any([p.get("birth"), p.get("death"), p.get("marriages"), p.get("notes"), p.get("burial")])


def primary_code(p):
    return p.get("lineageCodes", ["?"])[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", help="Filter to a sibling root code (1,2,5,6,7,8,A)")
    ap.add_argument("--depth", type=int, help="Only show codes up to N chars long")
    ap.add_argument("--full", action="store_true", help="Show full entries instead of stubs")
    args = ap.parse_args()

    data = json.loads((REPO / "data" / "people.json").read_text())
    people = data["people"]

    target = [p for p in people if (is_stub(p) ^ args.full)]
    if args.branch:
        target = [p for p in target if primary_code(p).startswith(args.branch)]
    if args.depth:
        target = [p for p in target if len(primary_code(p)) <= args.depth]

    # Group by depth
    by_depth = defaultdict(list)
    for p in target:
        by_depth[len(primary_code(p))].append(p)

    total_full = sum(1 for p in people if not is_stub(p))
    total_stub = len(people) - total_full

    print(f"Dataset: {len(people)} total — {total_full} full entries, {total_stub} stubs")
    label = "Full entries" if args.full else "Stubs (need transcription)"
    print(f"\n{label}{' for branch ' + args.branch if args.branch else ''}:\n")

    for d in sorted(by_depth):
        gen = "founder" if d == 1 else f"gen {d - 1}"
        print(f"  -- depth {d} ({gen}) — {len(by_depth[d])} people --")
        for p in sorted(by_depth[d], key=lambda x: primary_code(x)):
            code = primary_code(p)
            name = p.get("name", {}).get("full", "?")
            parents = ", ".join(code_for(people, pid) for pid in p.get("parentIds", []))
            print(f"    {code:8s} {name:35s}  (parent: {parents})")
        print()


def code_for(people, pid):
    for p in people:
        if p["id"] == pid:
            return p.get("lineageCodes", ["?"])[0]
    return "?"


if __name__ == "__main__":
    main()
