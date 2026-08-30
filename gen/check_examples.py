"""Validates every jsonc example in the docs sources against the agent models.

    PYTHONPATH=. .venv/bin/python docs/website/gen/check_examples.py

A block that contains "functions" is validated as a whole agent; any other block is treated as
the inside of a function's commands object. Blocks marked <x-code lang="jsonc" nocheck> are skipped
(deliberately partial snippets).
"""
from __future__ import annotations

import json
import re
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# The examples are validated against the server's own models, in a sibling checkout. See the
# same reasoning at the top of build.py.
SERVER = Path(os.environ.get("S2OSERVER") or ROOT.parent / "s2oserver")
sys.path.insert(0, str(SERVER))

from pydantic import ValidationError  # noqa: E402
from models.agentmodels import AgentModel, CommandBlock  # noqa: E402

_XCODE = re.compile(r'<x-code lang="jsonc"([^>]*)>\n?(.*?)</x-code>', re.S)
_COMMENT = re.compile(r'("(?:[^"\\]|\\.)*")|//[^\n]*|/\*.*?\*/', re.S)


def strip_jsonc(text: str) -> str:
    return _COMMENT.sub(lambda m: m.group(1) or "", text)


def main() -> int:
    bad = 0
    total = 0
    for src in sorted((ROOT / "docsrc").rglob("*.html")):
        for m in _XCODE.finditer(src.read_text()):
            attrs, code = m.group(1), m.group(2)
            if "nocheck" in attrs:
                continue
            total += 1
            text = strip_jsonc(code).strip().rstrip(",")
            try:
                if '"functions"' in text:
                    obj = json.loads(text if text.startswith("{") else "{" + text + "}")
                    AgentModel.model_validate(obj)
                elif '"commands"' in text:
                    obj = json.loads("{" + text + "}")
                    obj.setdefault("main", {"commands": {}})
                    AgentModel.model_validate({"functions": obj})
                else:
                    obj = json.loads("{" + text + "}")
                    CommandBlock.model_validate(obj)
            except (json.JSONDecodeError, ValidationError) as e:
                bad += 1
                print(f"{src.relative_to(ROOT)}: {str(e)[:400]}\n")
    print(f"{total} examples checked, {bad} invalid")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
