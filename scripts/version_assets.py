#!/usr/bin/env python3
"""Keep the ?v= tags in site/index.html in step with the files they load.

Each tag is the first 8 hex characters of the file's SHA-256, so it changes
exactly when the file's contents change and browsers fetch the new copy.

Run from the repo root:
    python3 scripts/version_assets.py          # rewrite the tags
    python3 scripts/version_assets.py --check  # exit 1 if any tag is stale (CI)
No dependencies.
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
INDEX = SITE / "index.html"
ASSETS = ("css/styles.css", "js/app.js")


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def main(argv):
    check = "--check" in argv
    html = INDEX.read_text(encoding="utf-8")
    new_html, problems = html, []
    for asset in ASSETS:
        want = fingerprint(SITE / asset)
        pattern = re.compile(r'(["\'])' + re.escape(asset) + r'(\?v=[^"\']*)?\1')
        found = pattern.findall(new_html)
        if len(found) != 1:
            problems.append(f"expected exactly one reference to {asset} in index.html, found {len(found)}")
            continue
        current = (found[0][1] or "")[3:]
        if current != want:
            problems.append(f"{asset}: tag is {current or 'missing'}, file hash is {want}")
            new_html = pattern.sub(lambda m: f"{m.group(1)}{asset}?v={want}{m.group(1)}", new_html)

    bad_refs = [p for p in problems if p.startswith("expected")]
    if bad_refs:
        for p in bad_refs:
            print(f"error: {p}")
        return 1
    if check:
        if problems:
            for p in problems:
                print(f"error: {p}")
            print("FAIL: run `python3 scripts/version_assets.py` and commit index.html")
            return 1
        print("OK: asset version tags match")
        return 0
    if new_html != html:
        INDEX.write_text(new_html, encoding="utf-8")
        for p in problems:
            print(f"updated: {p}")
    else:
        print("OK: asset version tags already match")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
