#!/usr/bin/env python3
"""Tests for validate_traits.py. Standard library only.

Run from the repo root: python3 -m unittest discover -s scripts

Each test writes a small traits.json into a temporary copy of the repo
layout (scripts/ + site/), runs the real validator on it, and checks the
exit code and output. The real site/data/traits.json is never touched.
"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parent / "validate_traits.py"

GOOD = {
    "updated": "2026-11-12",
    "collections": ["Akashi Collection", "Nash"],
    "traits": [
        {
            "id": "sharp-drive",
            "name": "Sharp Drive",
            "category": "Handling",
            "tags": ["Ankle Break"],
            "effect": "Increases Ankle Breaker Chance.",
            "effectSource": "Tier II",
            "trainingCamp": "",
            "tiers": {
                "II": {"value": "+1.2%", "icon": "images/icons/sharp-drive-ii.webp", "seenOn": ""},
                "III": {"value": "", "icon": None, "seenOn": ""},
            },
            "collections": [{"name": "Akashi Collection"}, {"name": "Nash"}],
        }
    ],
}


def run(data):
    """Run the validator on `data` in a temp repo; return (exit code, output)."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "scripts").mkdir()
        shutil.copy(VALIDATOR, root / "scripts" / VALIDATOR.name)
        icons = root / "site" / "images" / "icons"
        icons.mkdir(parents=True)
        (icons / "sharp-drive-ii.webp").write_bytes(b"")
        (root / "site" / "data").mkdir()
        (root / "site" / "data" / "traits.json").write_text(
            data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
        p = subprocess.run([sys.executable, "-I", str(root / "scripts" / VALIDATOR.name)],
                           capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr


def bad(fn):
    """A copy of GOOD with `fn` applied to it."""
    d = copy.deepcopy(GOOD)
    fn(d)
    return d


class ValidatorTests(unittest.TestCase):
    def assertFails(self, data, message):
        code, out = run(data)
        self.assertEqual(code, 1, out)
        self.assertIn(message, out)
        self.assertNotIn("Traceback", out)

    def test_good_data_passes(self):
        code, out = run(GOOD)
        self.assertEqual(code, 0, out)
        self.assertIn("OK: 1 traits, 2 collections", out)

    def test_real_data_passes(self):
        # Read-only run on the real repo data and icons. Fails if the real data
        # is invalid; that's deliberate.
        p = subprocess.run([sys.executable, "-I", str(VALIDATOR)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_invalid_json(self):
        self.assertFails("{not json", "not valid JSON")

    def test_bad_updated_date(self):
        self.assertFails(bad(lambda d: d.update(updated="Nov 12")), '"updated" must be a YYYY-MM-DD date')

    def test_collections_out_of_order(self):
        self.assertFails(bad(lambda d: d.update(collections=["Nash", "Akashi Collection"])),
                         "not in alphabetical order")

    def test_basketball_suffix(self):
        def f(d):
            d["collections"] = ["Akashi Collection", "Nash Basketball"]
            d["traits"][0]["collections"][1]["name"] = "Nash Basketball"
        self.assertFails(bad(f), 'should drop the implied "Basketball"')

    def test_missing_trait_key(self):
        self.assertFails(bad(lambda d: d["traits"][0].pop("tags")), "missing keys ['tags']")

    def test_bad_id(self):
        self.assertFails(bad(lambda d: d["traits"][0].update(id="Sharp_Drive")), "lowercase and hyphenated")

    def test_unknown_tag(self):
        self.assertFails(bad(lambda d: d["traits"][0].update(tags=["Pass"])), "unknown tags ['Pass']")

    def test_unknown_tier(self):
        self.assertFails(
            bad(lambda d: d["traits"][0]["tiers"].update(I={"value": "", "icon": None, "seenOn": ""})),
            "unknown tier 'I'")

    def test_icon_wrong_name(self):
        self.assertFails(bad(lambda d: d["traits"][0]["tiers"]["II"].update(icon="images/icons/sd.webp")),
                         "icon should be images/icons/sharp-drive-ii.webp")

    def test_icon_missing_file(self):
        self.assertFails(
            bad(lambda d: d["traits"][0]["tiers"]["III"].update(icon="images/icons/sharp-drive-iii.webp")),
            "does not exist")

    def test_collection_not_listed(self):
        self.assertFails(bad(lambda d: d["traits"][0]["collections"].append({"name": "Wave Rider"})),
                         "'Wave Rider' is not in the collections list")

    def test_collection_listed_twice(self):
        self.assertFails(bad(lambda d: d["traits"][0]["collections"].append({"name": "Nash"})), "listed twice")

    def test_collection_tiers_rejected(self):
        self.assertFails(bad(lambda d: d["traits"][0]["collections"][0].update(tiers="II")),
                         "unknown key(s) ['tiers']; it should only have a name")

    def test_pickup_and_aliases_pass(self):
        def f(d):
            d["traits"][0]["collections"][0]["pickup"] = True
            d["traits"][0]["aliases"] = ["Quick Drive"]
        code, out = run(bad(f))
        self.assertEqual(code, 0, out)

    def test_pickup_must_be_true(self):
        for value in (False, 1, "true", None):
            with self.subTest(pickup=value):
                self.assertFails(bad(lambda d: d["traits"][0]["collections"][0].update(pickup=value)),
                                 "pickup must be true, or left out")

    def test_bad_aliases(self):
        for value in ("Quick Drive", [], [" "], [None], None):
            with self.subTest(aliases=value):
                self.assertFails(bad(lambda d: d["traits"][0].update(aliases=value)),
                                 "aliases must be a non-empty list of non-empty strings")

    def test_alias_listed_twice(self):
        self.assertFails(bad(lambda d: d["traits"][0].update(aliases=["Quick Drive", " quick  drive"])),
                         "'quick drive' is used more than once (sharp-drive)")

    def test_alias_repeats_name(self):
        self.assertFails(bad(lambda d: d["traits"][0].update(aliases=["sharp drive"])),
                         "'sharp drive' is used more than once")

    def test_alias_matches_another_trait(self):
        def f(d):
            other = copy.deepcopy(d["traits"][0])
            other.update(id="quick-drive", name="Quick Drive")
            d["traits"].append(other)
            d["traits"][0]["aliases"] = ["Quick Drive"]
        self.assertFails(bad(f), "'quick drive' is used more than once (sharp-drive, quick-drive)")

    def test_bare_string_collection(self):
        self.assertFails(bad(lambda d: d["traits"][0]["collections"].append("Nash")),
                         "must be an object with a string name")

    def test_non_string_name(self):
        self.assertFails(bad(lambda d: d["traits"][0]["collections"].append({"name": ["x"]})),
                         "must be an object with a string name")

    def test_collections_not_a_list(self):
        self.assertFails(bad(lambda d: d["traits"][0].update(collections="Nash")), "collections must be a list")

    def test_duplicate_collection(self):
        self.assertFails(bad(lambda d: d.update(collections=["Akashi Collection", "Nash", "Nash"])),
                         "duplicate collections: ['Nash']")

    def test_wrong_shapes_fail_cleanly(self):
        # Each of these used to crash the validator with a traceback.
        cases = [
            ("[]", "must be an object with updated, collections and traits"),
            (bad(lambda d: d.update(traits={"x": 1})), "traits must be a list"),
            (bad(lambda d: d.update(collections=[1])), "collections must be a list of names"),
            (bad(lambda d: d["traits"].append("oops")), "trait #2 must be an object, got str"),
            (bad(lambda d: d["traits"][0].update(id=5)), "trait #1: id must be lowercase and hyphenated"),
            (bad(lambda d: d["traits"][0].update(id=["x"])), "trait #1: id must be lowercase and hyphenated"),
            (bad(lambda d: d["traits"][0].update(category=[])), "unknown category []"),
            (bad(lambda d: d["traits"][0]["tiers"]["II"].update(icon=5)), "II: icon must be a string or null"),
            (bad(lambda d: d["traits"][0].update(tags="3PT")), "tags must be a list of tag names"),
            (bad(lambda d: d["traits"][0].update(tiers=[])), "tiers must be an object"),
            (bad(lambda d: d["traits"][0]["tiers"].update(III="none")), "III: must be an object"),
        ]
        for data, message in cases:
            with self.subTest(message=message):
                self.assertFails(data, message)

    def test_duplicate_id(self):
        self.assertFails(bad(lambda d: d["traits"].append(copy.deepcopy(d["traits"][0]))), "duplicate id")

    def test_unknown_category(self):
        self.assertFails(bad(lambda d: d["traits"][0].update(category="Passing")), "unknown category 'Passing'")

    def test_tier_missing_key(self):
        self.assertFails(bad(lambda d: d["traits"][0]["tiers"]["II"].pop("seenOn")), "II: missing keys ['seenOn']")

    def test_unused_collection_warns(self):
        code, out = run(bad(lambda d: d["traits"][0].update(collections=[{"name": "Nash"}])))
        self.assertEqual(code, 0, out)
        self.assertIn("'Akashi Collection' isn't used by any trait", out)

    def test_unreferenced_icon_warns(self):
        code, out = run(bad(lambda d: d["traits"][0]["tiers"]["II"].update(icon=None)))
        self.assertEqual(code, 0, out)
        self.assertIn("images/icons/sharp-drive-ii.webp isn't referenced by any trait", out)


if __name__ == "__main__":
    unittest.main()
