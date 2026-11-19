#!/usr/bin/env python3
"""Changes the pip package name or the GitHub organization everywhere on the site in one step.

    scripts/set-names.py --pip tactet-agents
    scripts/set-names.py --github tactet-com

The current values are in gen/names.json. The script replaces the current pip name (in install commands and where the package is named)
and `github.com/<current>/` in the web pages, the docs sources and the docs template, records the new
values, and prints how many places changed. Rebuild the docs afterwards with gen/build.py."""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAMES_FILE = ROOT / "gen" / "names.json"
PATTERNS = {
    "pipPackage": ("pip install {}", 'pip install "{}[', "PyPI as <code>{}</code>", "<code>{}</code> package",
                   "&quot;{}&quot; Python package", '"{}" Python package'),
    "githubOrg": ("github.com/{}/",),
}
FILE_GLOBS = ("html/*.html", "html/legal/*.html", "docsrc/**/*.html", "gen/build.py", "gen/toc.py", "content/legal/*.md")

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--pip", dest="pipPackage", help="new pip package name")
parser.add_argument("--github", dest="githubOrg", help="new GitHub organization")
wanted = {key: value for key, value in vars(parser.parse_args()).items() if value}

names = json.loads(NAMES_FILE.read_text())
changes = {pattern.format(names[key]): pattern.format(value)
           for key, value in wanted.items() if value != names[key] for pattern in PATTERNS[key]}
places = 0
for pattern in FILE_GLOBS:
    for path in ROOT.glob(pattern):
        text = path.read_text()
        updated = text
        for old, new in changes.items():
            places += updated.count(old)
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated)
names.update(wanted)
NAMES_FILE.write_text(json.dumps(names, indent=2) + "\n")
print(f"{places} places changed; names are now {names}")
