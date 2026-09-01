"""Builds the docs section of the website: docsrc/**/*.html  ->  html/docs/**/*.html

    PYTHONPATH=. .venv/bin/python docs/website/gen/build.py

Page bodies are hand-authored HTML fragments. This script adds the site chrome (header, sidebar
tree, on-page table of contents, prev/next, footer) and replaces the placeholders below with
tables derived from the pydantic models, so the reference cannot drift from the code:

    <!--fields:command:api-->        the fields of one command (CommandBlock's alias, e.g. "if")
    <!--fields:model:LlmModel-->     the fields of a model in models/systemconfig.py or agentmodels.py
    <!--commands:groups-->           every command, grouped as the editor groups them
    <!--enum:SearchBehavior-->       the members of a StrEnum with the comment on each member

    <x-code lang="jsonc">...</x-code>   a code block; contents are escaped and highlighted here,
                                        so sources can hold the raw text.

Only the standard library is used. Run from the repository root.
"""
from __future__ import annotations

import enum
import html
import json
import inspect
import re
import os
import sys
import types
import typing
from pathlib import Path
from typing import Annotated, Any, Literal, get_args, get_origin

ROOT = Path(__file__).resolve().parents[1]          # this project's root
# The docs are generated FROM the server's own models - the command tables, the config tables
# and the validated examples all come from them - so this reaches into a sibling checkout of
# s2oserver. Sibling rather than a package: the two are separate projects and neither installs
# the other. S2OSERVER overrides it if the checkout lives elsewhere.
SERVER = Path(os.environ.get("S2OSERVER") or ROOT.parent / "s2oserver")
SRC = ROOT / "docsrc"
OUT = ROOT / "html" / "docs"
if not (SERVER / "models").is_dir():
    raise SystemExit(f"s2oserver not found at {SERVER}. The documentation is generated from its "
                     f"models; set S2OSERVER to the checkout.")
sys.path.insert(0, str(SERVER))
sys.path.insert(0, str(ROOT / "gen"))

from toc import TOC  # noqa: E402
import figures  # noqa: E402

from pydantic import BaseModel  # noqa: E402
from pydantic_core import PydanticUndefined  # noqa: E402

from models import agentmodels, systemconfig, schemaobjects, reportmodels  # noqa: E402
from models.agentschema import AgentSchema  # noqa: E402
from base.common import safeNamePattern, AgentName  # noqa: E402


# ----------------------------------------------------------------------------- type rendering

_NAMED_TYPES = {
    "ExprString": "dynamic string",
    "PythonExpr": "Python expression",
    "DynamicDict": "dynamic dict",
    "DynamicValue": "any JSON value",
    "CommandBlock": "command block",
    "CommandListModel": "command block",
    "JsonValue": "JSON value",
    "SafeStr": "string",
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
    "dict": "object",
    "list": "list",
    "NoneType": "null",
    "AskInputModel": "input object",
    "AFunctionCallModel": "call object",
    "FunctionArgModel": "argument object",
    "LogModel": "log object",
}

_AGENT_NAME_PATTERN = None
for _m in get_args(AgentName)[1:]:
    _AGENT_NAME_PATTERN = getattr(_m, "pattern", None) or _AGENT_NAME_PATTERN


def _pattern_of(meta) -> str | None:
    for m in meta:
        p = getattr(m, "pattern", None)
        if p:
            return p
        for c in getattr(m, "metadata", []) or []:
            p = getattr(c, "pattern", None)
            if p:
                return p
    return None


def render_type(t: Any) -> tuple[str, bool]:
    """Human name for an annotation, and whether None is allowed."""
    origin = get_origin(t)
    if origin is Annotated:
        base, *meta = get_args(t)
        pattern = _pattern_of(meta)
        if pattern == safeNamePattern:
            return "name", False
        if pattern == _AGENT_NAME_PATTERN:
            return "agent name", False
        return render_type(base)
    if origin in (types.UnionType, typing.Union):
        parts, nullable = [], False
        for a in get_args(t):
            if a is type(None):
                nullable = True
                continue
            name, n = render_type(a)
            nullable = nullable or n
            if name not in parts:
                parts.append(name)
        return " or ".join(parts), nullable
    if origin is Literal:
        return " | ".join(f'"{v}"' if isinstance(v, str) else str(v) for v in get_args(t)), False
    if origin is list:
        args = get_args(t)
        inner = render_type(args[0])[0] if args else "any"
        return f"list of {inner}", False
    if origin is dict:
        args = get_args(t)
        if len(args) == 2:
            k, v = render_type(args[0])[0], render_type(args[1])[0]
            return f"object of {k} → {v}", False
        return "object", False
    if isinstance(t, typing.TypeAliasType):
        return render_type(t.__value__)
    if isinstance(t, type):
        if issubclass(t, enum.Enum):
            return " | ".join(f'"{m.value}"' for m in t), False
        return _NAMED_TYPES.get(t.__name__, t.__name__), False
    name = getattr(t, "__name__", None) or str(t)
    return _NAMED_TYPES.get(name, name), False


def render_default(field) -> str:
    if field.default_factory is not None:
        try:
            v = field.default_factory()
        except TypeError:
            return ""
        if v in ({}, [], "", None):
            return ""
        return html.escape(repr(v))
    d = field.default
    if d is PydanticUndefined or d is None:
        return ""
    if isinstance(d, enum.Enum):
        d = d.value
    if isinstance(d, BaseModel):
        return ""
    if isinstance(d, bool):
        return "true" if d else "false"
    if isinstance(d, str):
        return html.escape(f'"{d}"') if d else ""
    return html.escape(str(d))


def fields_table(model: type[BaseModel], skip: tuple[str, ...] = ("type",)) -> str:
    rows = []
    for name, field in model.model_fields.items():
        if name in skip:
            continue
        key = field.alias or name
        tname, nullable = render_type(field.annotation)
        req = field.is_required()
        rows.append(
            "<tr>"
            f"<td><code>{html.escape(key)}</code>{'<span class=req>required</span>' if req else ''}</td>"
            f"<td class=ty>{html.escape(tname)}</td>"
            f"<td class=dflt>{render_default(field)}</td>"
            f"<td>{html.escape(field.description or field.title or '')}</td>"
            "</tr>"
        )
    return (
        "<div class=tablewrap><table class=fields>"
        "<thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def scalar_table(field) -> str:
    tname, _ = render_type(field.annotation)
    return (
        "<div class=tablewrap><table class=fields>"
        "<thead><tr><th>Value</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>"
        f"<tbody><tr><td><em>the command's value</em></td><td class=ty>{html.escape(tname)}</td>"
        f"<td class=dflt>{render_default(field)}</td><td>{html.escape(field.description or '')}</td></tr>"
        "</tbody></table></div>"
    )


_COMMAND_FIELDS = {(f.alias or n): (n, f) for n, f in agentmodels.CommandBlock.model_fields.items()}


def command_model(alias: str) -> type[BaseModel] | None:
    _, field = _COMMAND_FIELDS[alias]
    t = field.annotation
    for cand in (t, *get_args(t)):
        if isinstance(cand, type) and issubclass(cand, BaseModel):
            return cand
    return None


def command_fields(alias: str) -> str:
    name, field = _COMMAND_FIELDS[alias]
    model = command_model(alias)
    if alias == "var":
        return ""  # var's keys are the variable names; documented in prose
    if model is None:
        return scalar_table(field)
    return fields_table(model, skip=())


def commands_groups() -> str:
    out = []
    for g in AgentSchema.getSchema().commandGroups:
        out.append(f"<h3>{html.escape(g.title)}</h3><ul class=cmdlist>")
        for c in g.commands:
            alias = c.value
            _, field = _COMMAND_FIELDS[alias]
            out.append(
                f"<li><a href='../commands/{alias}.html'><code>{alias}</code></a>"
                f"<span>{html.escape(field.description or field.title or '')}</span></li>"
            )
        out.append("</ul>")
    return "".join(out)


def enum_table(name: str) -> str:
    e = getattr(systemconfig, name, None) or getattr(schemaobjects, name)
    src = inspect.getsource(e)
    rows = []
    for m in e:
        mt = re.search(rf"^\s*{m.name}\s*=.*?#\s*(.*)$", src, re.M)
        note = mt.group(1).strip() if mt else ""
        rows.append(f"<tr><td><code>{html.escape(m.value)}</code></td><td>{html.escape(note)}</td></tr>")
    return (
        "<div class=tablewrap><table class=fields><thead><tr><th>Value</th><th>Meaning</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def model_by_name(name: str) -> type[BaseModel]:
    for mod in (systemconfig, agentmodels, schemaobjects, reportmodels):
        m = getattr(mod, name, None)
        if isinstance(m, type) and issubclass(m, BaseModel):
            return m
    raise KeyError(name)


_SHOT = re.compile(r"<!--shot:(.*?)-->")
_PLACEHOLDER = re.compile(r"<!--(fields|commands|enum|pages|agent|figure):([a-zA-Z-]+)(?::([\w-]+))?-->")


def section_cards(sslug: str) -> str:
    ps = next(ps for s_, _, ps in TOC if s_ == sslug)
    items = []
    for entry in ps:
        pslug, ptitle = entry[0], entry[1]
        src = SRC / sslug / f"{pslug}.html"
        blurb = first_paragraph(src.read_text()) if src.exists() else ""
        items.append(f"<li><a href='{pslug}.html'><b>{html.escape(ptitle)}</b><small>{html.escape(blurb)}</small></a></li>")
    return f"<ul class=pagecards>{''.join(items)}</ul>"



def shot_block(spec: str) -> str:
    """<!--shot:name|width|alt|caption--> -> a screenshot captured in both GUI themes; docs.css shows the
    one matching the page theme (img/NAME-light.png and img/NAME-dark.png must both exist)."""
    name, width, alt, caption = (x.strip() for x in spec.split("|", 3))
    imgs = "".join(f'<img class="{t}" src="../img/{name}-{t}.png" alt="{html.escape(alt)}" style="--shot-w:{width}px">' for t in ("light", "dark"))
    return f'<figure class="shot">{imgs}<figcaption>{caption}</figcaption></figure>'

def expand_placeholders(body: str, sslug: str | None = None) -> str:
    def sub(m):
        kind, a, b = m.group(1), m.group(2), m.group(3)
        if kind == "pages" and a == "cards":
            return section_cards(sslug)
        if kind == "figure":
            return figures.render(a)
        if kind == "fields" and a == "command":
            return command_fields(b)
        if kind == "fields" and a == "model":
            return fields_table(model_by_name(b))
        if kind == "commands" and a == "groups":
            return commands_groups()
        if kind == "enum":
            return enum_table(a)
        raise ValueError(f"unknown placeholder {m.group(0)}")
    body = _SHOT.sub(lambda m: shot_block(m.group(1)), body)
    return _PLACEHOLDER.sub(sub, body)


# ----------------------------------------------------------------------------- code blocks

_TOKENS = {
    "jsonc": [
        (r"//[^\n]*", "cm"),
        (r"/\*.*?\*/", "cm"),
        (r'"(?:[^"\\]|\\.)*"(?=\s*:)', "key"),
        (r'"(?:[^"\\]|\\.)*"', "str"),
        (r"\b(?:true|false|null)\b", "kw"),
        (r"-?\b\d+(?:\.\d+)?\b", "num"),
    ],
    "bash": [
        (r"#[^\n]*", "cm"),
        (r"^\$ ", "ps1"),
        (r'"(?:[^"\\]|\\.)*"|\'[^\']*\'', "str"),
    ],
    "python": [
        (r"#[^\n]*", "cm"),
        (r'"""[\s\S]*?"""|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', "str"),
        (r"\b(?:def|class|return|import|from|async|await|if|else|elif|for|in|not|and|or|None|True|False|raise|try|except|with|as|pass|lambda)\b", "kw"),
        (r"\b\d+\b", "num"),
    ],
}


def highlight(code: str, lang: str) -> str:
    rules = _TOKENS.get(lang)
    if not rules:
        return html.escape(code)
    pattern = re.compile("|".join(f"(?P<t{i}>{r})" for i, (r, _) in enumerate(rules)), re.S | re.M)
    out, pos = [], 0
    for m in pattern.finditer(code):
        out.append(html.escape(code[pos:m.start()]))
        cls = rules[int(m.lastgroup[1:])][1]
        out.append(f"<span class={cls}>{html.escape(m.group(0))}</span>")
        pos = m.end()
    out.append(html.escape(code[pos:]))
    return "".join(out)


_XCODE = re.compile(r"<x-code(?:\s+lang=\"(\w+)\")?(?:\s+nocheck)?(?:\s+title=\"([^\"]*)\")?>\n?(.*?)</x-code>", re.S)


def expand_code(body: str) -> str:
    def sub(m):
        lang, title, code = m.group(1) or "text", m.group(2), m.group(3).rstrip("\n")
        # strip common indentation so sources can indent the block
        lines = code.split("\n")
        indent = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
        code = "\n".join(l[indent:] for l in lines)
        bar = f"<div class=bar><span>{html.escape(title)}</span></div>" if title else ""
        return f"<figure class=code data-lang={lang}>{bar}<pre><code>{highlight(code, lang)}</code></pre></figure>"
    return _XCODE.sub(sub, body)


# ----------------------------------------------------------------------------- chrome

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


_HEADING = re.compile(r"<h([23])([^>]*)>(.*?)</h\1>", re.S)


def add_heading_ids(body: str) -> tuple[str, list[tuple[int, str, str]]]:
    seen, toc = set(), []

    def sub(m):
        level, attrs, inner = int(m.group(1)), m.group(2), m.group(3)
        idm = re.search(r'id="([^"]+)"', attrs)
        text = re.sub(r"<[^>]+>", "", inner)
        hid = idm.group(1) if idm else slugify(html.unescape(text))
        base, n = hid, 2
        while hid in seen:
            hid, n = f"{base}-{n}", n + 1
        seen.add(hid)
        toc.append((level, hid, text))
        attrs = attrs if idm else f'{attrs} id="{hid}"'
        return f"<h{level}{attrs}>{inner}</h{level}>"
    return _HEADING.sub(sub, body), toc


def flatten():
    pages = []
    for sslug, stitle, ps in TOC:
        pages.append((sslug, None, stitle, stitle))
        for entry in ps:
            pages.append((sslug, entry[0], stitle, entry[1]))
    return pages


def rel(depth: int) -> str:
    return "../" * depth


def href(sslug, pslug, from_depth):
    p = f"{sslug}/index.html" if pslug is None else f"{sslug}/{pslug}.html"
    return rel(from_depth) + p


def sidebar(cur_s, cur_p, depth) -> str:
    out = ["<nav class=sidebar aria-label='Documentation'>"]
    out.append(f"<a class='sb-home{' current' if cur_s is None else ''}' href='{rel(depth)}index.html'>Documentation</a>")
    for sslug, stitle, ps in TOC:
        open_ = sslug == cur_s
        if not ps:   # a section that is one page: a plain link, no chevron and no empty list
            out.append(f"<a class='sb-solo{' current' if open_ else ''}' href='{href(sslug, None, depth)}'"
                       f"{' aria-current=page' if open_ else ''}>{html.escape(stitle)}</a>")
            continue
        out.append(f"<details{' open' if open_ else ''}><summary><a href='{href(sslug, None, depth)}'"
                   f"{' aria-current=page' if open_ and cur_p is None else ''}>{html.escape(stitle)}</a></summary><ul>")
        last_group = None
        for entry in ps:
            pslug, ptitle = entry[0], entry[1]
            group = entry[2] if len(entry) > 2 else None
            if group and group != last_group:
                out.append(f"<li class=sb-group>{html.escape(group)}</li>")
                last_group = group
            cur = open_ and pslug == cur_p
            out.append(f"<li><a href='{href(sslug, pslug, depth)}'{' aria-current=page' if cur else ''}>{html.escape(ptitle)}</a></li>")
        out.append("</ul></details>")
    out.append("</nav>")
    return "".join(out)


def page_toc(toc) -> str:
    if len(toc) < 2:
        return ""
    items = "".join(f"<li class=l{lvl}><a href='#{hid}'>{text}</a></li>" for lvl, hid, text in toc)
    return f"<aside class=pagetoc><div class=label>On this page</div><ul>{items}</ul></aside>"


def header(depth) -> str:
    r = rel(depth) + "../"
    return f"""<header class="site-header">
  <div class="container header-row">
    <a class="brand" href="{r}index.html" aria-label="Search2o home"><img src="{r}logo.png" alt="Search2o" width="560" height="102"></a>
    <nav class="site-nav" aria-label="Main">
      <a class="navlink" href="{r}index.html">Home</a>
      <a class="navlink" href="{r}gettingstarted.html">Getting started</a>
      <a class="navlink" href="{rel(depth)}index.html" aria-current="page">Docs</a>
      <a class="navlink" href="{r}pricing.html">Pricing</a>
      <a class="navlink" href="{r}about.html">About</a>
    </nav>
    <button class="theme-toggle" type="button" aria-label="Switch theme">
      <svg class="sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.6 4.6l1.8 1.8M17.6 17.6l1.8 1.8M19.4 4.6l-1.8 1.8M6.4 17.6l-1.8 1.8"/></svg>
      <svg class="moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
    </button>
    <a class="btn btn-primary btn-sm header-cta" href="{r}gettingstarted.html">Get started</a>
  </div>
</header>"""


def footer(depth) -> str:
    r = rel(depth) + "../"
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-base">
      <span>&copy; <span id="year">2026</span> Search2o &middot; Northern Virginia, USA</span>
      <span><a href="{r}about.html#contact">Contact</a></span>
    </div>
  </div>
</footer>"""


def render_page(sslug, pslug, stitle, ptitle, body, prev, nxt, depth, description) -> str:
    body, toc = add_heading_ids(body)
    r = rel(depth) + "../"
    crumbs = f"<a href='{rel(depth)}index.html'>Docs</a>"
    if pslug is not None:
        crumbs += f" <span>/</span> <a href='{href(sslug, None, depth)}'>{html.escape(stitle)}</a>"
    nav = "<nav class=prevnext>"
    nav += (f"<a class=prev href='{href(prev[0], prev[1], depth)}'><small>Previous</small>{html.escape(prev[3])}</a>" if prev else "<span></span>")
    nav += (f"<a class=next href='{href(nxt[0], nxt[1], depth)}'><small>Next</small>{html.escape(nxt[3])}</a>" if nxt else "<span></span>")
    nav += "</nav>"
    title = f"{ptitle} — Search2o docs" if pslug or sslug else "Search2o documentation"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>try{{var t=localStorage.getItem("s2o-theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" type="image/svg+xml" href="{r}favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}styles.css">
<link rel="stylesheet" href="{rel(depth)}docs.css">
</head>
<body class="docs">
{header(depth)}
<div class="container docs-layout">
  <button class="sb-toggle" type="button" aria-expanded="false" aria-controls="sidebar">Contents</button>
  <div id="sidebar" class="sb-wrap">{sidebar(sslug, pslug, depth)}</div>
  <main class="docs-main">
    <div class="crumbs">{crumbs}</div>
    <article class="docs-article">
      <h1>{html.escape(ptitle)}</h1>
      {body}
    </article>
    {nav}
  </main>
  {page_toc(toc)}
</div>
{footer(depth)}
<script src="{r}site.js"></script>
<script src="{rel(depth)}docs.js"></script>
</body>
</html>
"""


def first_paragraph(body: str) -> str:
    m = re.search(r"<p[^>]*>(.*?)</p>", body, re.S)
    text = re.sub(r"<[^>]+>", "", m.group(1)) if m else ""
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return text[:157] + "…" if len(text) > 160 else text


def build() -> int:
    pages = flatten()
    missing = 0
    OUT.mkdir(parents=True, exist_ok=True)
    home = SRC / "index.html"
    # docs home
    body = expand_code(expand_placeholders(home.read_text()))
    (OUT / "index.html").write_text(render_page(None, None, "Documentation", "Search2o documentation",
                                                body, None, pages[0], 0, first_paragraph(body)))
    written = 1
    for i, (sslug, pslug, stitle, ptitle) in enumerate(pages):
        src = SRC / sslug / ("index.html" if pslug is None else f"{pslug}.html")
        if not src.exists():
            print(f"MISSING {src.relative_to(ROOT)}")
            missing += 1
            continue
        body = expand_code(expand_placeholders(src.read_text(), sslug))
        prev = pages[i - 1] if i > 0 else None
        nxt = pages[i + 1] if i + 1 < len(pages) else None
        out = OUT / sslug / ("index.html" if pslug is None else f"{pslug}.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_page(sslug, pslug, stitle, ptitle, body, prev, nxt, 1, first_paragraph(body)))
        written += 1
    print(f"wrote {written} pages to {OUT.relative_to(ROOT)}; {missing} missing sources")
    return missing


if __name__ == "__main__":
    sys.exit(1 if build() else 0)
