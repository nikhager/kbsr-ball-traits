#!/usr/bin/env python3
"""Check site/data/traits.json against the rules in CLAUDE.md.

Run from the repo root: python3 scripts/validate_traits.py
Exits 1 and lists every problem if any check fails. No dependencies.
"""
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = SITE / "data" / "traits.json"

CATEGORIES = {"Offense", "Handling", "Defense", "Hybrid", "Rebounding", "Energy"}
TAGS = {"3PT", "Mid-Range", "Close-Range", "Layup", "Dunk", "Steal", "Block",
        "Contest", "Rebound", "Drive", "Ankle Break", "Control", "Speed", "Energy"}
TIERS = ("II", "III")
TRAIT_KEYS = {"id", "name", "category", "tags", "effect", "effectSource",
              "trainingCamp", "tiers", "collections"}
TIER_KEYS = {"value", "icon", "seenOn"}
# Optional keys: "aliases" on a trait, "pickup" on a collection entry.
COLLECTION_KEYS = {"name", "pickup"}

errors, warnings = [], []


def norm(s):
    return " ".join(s.split()).casefold() if isinstance(s, str) else repr(s)


def err(msg):
    errors.append(msg)


def main():
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: traits.json is not valid JSON: {e}")
        return 1

    # Last updated date
    updated = data.get("updated", "")
    try:
        date.fromisoformat(updated)
    except (TypeError, ValueError):
        err(f'"updated" must be a YYYY-MM-DD date, got {updated!r}')

    # Collections list
    cols = data.get("collections", [])
    if cols != sorted(cols, key=str.lower):
        err("collections are not in alphabetical order (case-insensitive)")
    dupes = {c for c in cols if cols.count(c) > 1}
    if dupes:
        err(f"duplicate collections: {sorted(dupes)}")
    for c in cols:
        if re.search(r"\(?Basketball\)?$", c):
            err(f'collection "{c}" should drop the implied "Basketball"')

    # Traits
    seen_ids, used_cols, used_icons = set(), set(), set()
    names_of = defaultdict(list)  # normalized trait name or alias -> trait labels using it
    for i, t in enumerate(data.get("traits", [])):
        label = t.get("id") or f"trait #{i + 1}"
        missing = TRAIT_KEYS - t.keys()
        if missing:
            err(f"{label}: missing keys {sorted(missing)}")
            continue
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", t["id"]):
            err(f"{label}: id must be lowercase and hyphenated")
        if t["id"] in seen_ids:
            err(f"{label}: duplicate id")
        seen_ids.add(t["id"])
        if t["category"] not in CATEGORIES:
            err(f"{label}: unknown category {t['category']!r}")
        bad_tags = set(t["tags"]) - TAGS
        if bad_tags:
            err(f"{label}: unknown tags {sorted(bad_tags)}")
        # Names and aliases share one namespace (case- and space-insensitive),
        # so an alias search can't match two traits.
        names_of[norm(t["name"])].append(label)
        if "aliases" in t:
            aliases = t["aliases"]
            if not isinstance(aliases, list) or not aliases \
                    or not all(isinstance(a, str) and a.strip() for a in aliases):
                err(f"{label}: aliases must be a non-empty list of non-empty strings (leave the key out if none)")
            else:
                for a in aliases:
                    names_of[norm(a)].append(label)

        for tier, v in t["tiers"].items():
            if tier not in TIERS:
                err(f"{label}: unknown tier {tier!r}")
                continue
            if TIER_KEYS - v.keys():
                err(f"{label} {tier}: missing keys {sorted(TIER_KEYS - v.keys())}")
                continue
            icon = v["icon"]
            if icon is None:
                continue
            expected = f"images/icons/{t['id']}-{tier.lower()}.webp"
            if icon != expected:
                err(f"{label} {tier}: icon should be {expected}, got {icon}")
            if not (SITE / icon).is_file():
                err(f"{label} {tier}: icon file {icon} does not exist")
            used_icons.add(icon)

        entries = []
        if not isinstance(t["collections"], list):
            err(f"{label}: collections must be a list")
        else:
            for c in t["collections"]:
                if isinstance(c, dict) and isinstance(c.get("name"), str):
                    entries.append(c)
                else:
                    err(f"{label}: collection entry {c!r} must be an object with a string name")
        names = [c.get("name") for c in entries]
        for n in {n for n in names if names.count(n) > 1}:
            err(f"{label}: collection {n!r} listed twice")
        for c in entries:
            if c.get("name") not in cols:
                err(f"{label}: collection {c.get('name')!r} is not in the collections list")
            extra = set(c) - COLLECTION_KEYS
            if extra:
                err(f"{label}: collection {c.get('name')!r} has unknown key(s) {sorted(extra)}; it should only have a name"
                    " and optional pickup (any trait can roll II or III on a gold ball)")
            if "pickup" in c and c["pickup"] is not True:
                err(f"{label}: collection {c.get('name')!r} pickup must be true, or left out")
            used_cols.add(c.get("name"))

    for n, labels in sorted(names_of.items()):
        if len(labels) > 1:
            where = ", ".join(dict.fromkeys(labels))  # each trait once, in file order
            err(f"name or alias {n!r} is used more than once ({where})")

    for c in sorted(set(cols) - used_cols):
        warnings.append(f"collection {c!r} isn't used by any trait")
    on_disk = {f"images/icons/{p.name}" for p in (SITE / "images" / "icons").glob("*.webp")}
    for icon in sorted(on_disk - used_icons):
        warnings.append(f"{icon} isn't referenced by any trait")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    if errors:
        print(f"FAIL: {len(errors)} problem(s) in traits.json")
        return 1
    print(f"OK: {len(seen_ids)} traits, {len(cols)} collections")
    return 0


if __name__ == "__main__":
    sys.exit(main())
