#!/usr/bin/env python3
"""Tests for version_assets.py. Standard library only.

Run from the repo root: python3 -m unittest discover -s scripts

Each test builds a tiny site/ in a temp folder, copies the script next to it,
and runs it as a subprocess. The real site/ is only read, never written.
"""
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "version_assets.py"

CSS = b"body { color: red; }\n"
JS = b"console.log('hi');\n"


def h(data):
    return hashlib.sha256(data).hexdigest()[:8]


def page(css_ref, js_ref):
    return f'<link rel="stylesheet" href="{css_ref}">\n<script src="{js_ref}"></script>\n'


class TempSite:
    def __init__(self, html):
        self.dir = tempfile.TemporaryDirectory()
        root = Path(self.dir.name)
        (root / "scripts").mkdir()
        shutil.copy(SCRIPT, root / "scripts" / SCRIPT.name)
        (root / "site" / "css").mkdir(parents=True)
        (root / "site" / "js").mkdir()
        (root / "site" / "css" / "styles.css").write_bytes(CSS)
        (root / "site" / "js" / "app.js").write_bytes(JS)
        self.index = root / "site" / "index.html"
        self.index.write_text(html, encoding="utf-8")
        self.script = root / "scripts" / SCRIPT.name

    def run(self, *args):
        p = subprocess.run([sys.executable, "-I", str(self.script), *args], capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr

    def close(self):
        self.dir.cleanup()


class VersionAssetsTests(unittest.TestCase):
    def site(self, html):
        s = TempSite(html)
        self.addCleanup(s.close)
        return s

    def test_check_passes_when_tags_match(self):
        s = self.site(page(f"css/styles.css?v={h(CSS)}", f"js/app.js?v={h(JS)}"))
        code, out = s.run("--check")
        self.assertEqual(code, 0, out)

    def test_check_fails_on_stale_tag(self):
        s = self.site(page("css/styles.css?v=2026-11-12", f"js/app.js?v={h(JS)}"))
        code, out = s.run("--check")
        self.assertEqual(code, 1, out)
        self.assertIn("css/styles.css: tag is 2026-11-12", out)
        self.assertIn("run `python3 scripts/version_assets.py`", out)

    def test_check_fails_on_missing_tag(self):
        s = self.site(page(f"css/styles.css?v={h(CSS)}", "js/app.js"))
        code, out = s.run("--check")
        self.assertEqual(code, 1, out)
        self.assertIn("js/app.js: tag is missing", out)

    def test_check_does_not_write(self):
        html = page("css/styles.css?v=old", "js/app.js?v=old")
        s = self.site(html)
        s.run("--check")
        self.assertEqual(s.index.read_text(encoding="utf-8"), html)

    def test_rewrite_fixes_tags_and_then_check_passes(self):
        s = self.site(page("css/styles.css?v=old", "js/app.js"))
        code, out = s.run()
        self.assertEqual(code, 0, out)
        self.assertEqual(s.index.read_text(encoding="utf-8"),
                         page(f"css/styles.css?v={h(CSS)}", f"js/app.js?v={h(JS)}"))
        code, out = s.run("--check")
        self.assertEqual(code, 0, out)

    def test_rewrite_is_a_no_op_when_current(self):
        html = page(f"css/styles.css?v={h(CSS)}", f"js/app.js?v={h(JS)}")
        s = self.site(html)
        code, out = s.run()
        self.assertEqual(code, 0, out)
        self.assertIn("already match", out)
        self.assertEqual(s.index.read_text(encoding="utf-8"), html)

    def test_missing_reference_is_an_error(self):
        s = self.site('<link rel="stylesheet" href="css/styles.css">\n')
        code, out = s.run("--check")
        self.assertEqual(code, 1, out)
        self.assertIn("expected exactly one reference to js/app.js", out)

    def test_real_site_tags_match(self):
        # Read-only check on the real site. Fails if someone changed app.js or
        # styles.css without running the script; that's deliberate.
        p = subprocess.run([sys.executable, "-I", str(SCRIPT), "--check"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main()
