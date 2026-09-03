"""Illustrations for the docs, emitted as inline SVG so they take the page's light/dark tokens.

A figure is referenced from a page body as <!--figure:NAME-->. Everything is drawn with a
handful of primitives on a fixed-width canvas; colours are CSS variables from styles.css, so
the same SVG is right in both themes and scales with the column.
"""
from __future__ import annotations

import html

W = 720  # canvas width; the page scales it


class Fig:
    def __init__(self, name: str, height: int, title: str, width: int = W):
        self.name, self.w, self.h, self.title = name, width, height, title
        self.parts: list[str] = []

    # ---- primitives -------------------------------------------------------------
    def box(self, x, y, w, h, label="", sub="", kind="card", r=10, size=13.5, mono=False):
        fill = {"card": "var(--card)", "soft": "var(--bg-soft)", "accent": "var(--blue)",
                "dark": "var(--navy)", "ok": "var(--badge-bg)", "none": "none"}[kind]
        stroke = {"card": "var(--line)", "soft": "var(--line)", "accent": "var(--blue)",
                  "dark": "var(--navy)", "ok": "var(--ok)", "none": "var(--line)"}[kind]
        text = "#ffffff" if kind in ("accent", "dark") else "var(--ink)"
        subc = "rgba(255,255,255,.75)" if kind in ("accent", "dark") else "var(--muted)"
        dash = ' stroke-dasharray="5 4"' if kind == "none" else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"{dash}/>')
        if label:
            cy = y + h / 2 + (0 if not sub else -7)
            fam = ' font-family="var(--mono)"' if mono else ""
            self.parts.append(f'<text x="{x + w / 2}" y="{cy}" text-anchor="middle" dominant-baseline="middle" '
                              f'font-size="{size}" font-weight="600" fill="{text}"{fam}>{html.escape(label)}</text>')
        if sub:
            self.parts.append(f'<text x="{x + w / 2}" y="{y + h / 2 + 11}" text-anchor="middle" dominant-baseline="middle" '
                              f'font-size="{10.5 if len(sub) > 16 else 11.5}" fill="{subc}">{html.escape(sub)}</text>')

    def text(self, x, y, s, size=12.5, fill="muted", anchor="start", weight=500, mono=False):
        col = {"muted": "var(--muted)", "ink": "var(--ink)", "faint": "var(--faint)", "blue": "var(--blue-ink)", "white": "#fff"}[fill]
        fam = ' font-family="var(--mono)"' if mono else ""
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" dominant-baseline="middle" font-size="{size}" '
                          f'font-weight="{weight}" fill="{col}"{fam}>{html.escape(s)}</text>')

    def arrow(self, x1, y1, x2, y2, label="", dashed=False, both=False, curve=0):
        d = f'M{x1},{y1} L{x2},{y2}' if not curve else f'M{x1},{y1} Q{(x1 + x2) / 2},{(y1 + y2) / 2 + curve} {x2},{y2}'
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        mk = f' marker-start="url(#{self.name}-arr-r)"' if both else ""
        self.parts.append(f'<path d="{d}" fill="none" stroke="var(--faint)" stroke-width="1.6"{dash} marker-end="url(#{self.name}-arr)"{mk}/>')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + curve / 2
            tw = len(label) * 6.4 + 12
            self.parts.append(f'<rect x="{mx - tw / 2}" y="{my - 9}" width="{tw}" height="18" rx="9" fill="var(--bg)"/>')
            self.text(mx, my, label, size=11, anchor="middle")

    def diamond(self, cx, cy, w, h, label=""):
        pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
        self.parts.append(f'<polygon points="{pts}" fill="var(--bg-soft)" stroke="var(--line)"/>')
        if label:
            self.text(cx, cy, label, size=11, fill="ink", anchor="middle", weight=600)

    def line(self, x1, y1, x2, y2, dashed=False):
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="var(--line)" stroke-width="1.4"{dash}/>')

    def dot(self, x, y, r=4, kind="accent"):
        fill = {"accent": "var(--blue)", "ok": "var(--ok)", "muted": "var(--faint)"}[kind]
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')

    def group(self, x, y, w, h, label, dashed=True):
        self.box(x, y, w, h, kind="none" if dashed else "soft", r=14)
        self.text(x + 14, y + 16, label, size=11.5, weight=700, fill="faint")

    # ---- compound widgets -------------------------------------------------------
    def table(self, x, y, w, cols, rows, rowh=22, widths=None):
        n = len(cols)
        widths = widths or [w / n] * n
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{rowh}" rx="6" fill="var(--bg-soft)"/>')
        cx = x + 10
        for c, cw in zip(cols, widths):
            self.text(cx, y + rowh / 2, c, size=10.5, weight=700, fill="muted")
            cx += cw
        for i, row in enumerate(rows):
            ry = y + rowh * (i + 1)
            self.line(x, ry, x + w, ry)
            cx = x + 10
            for cell, cw in zip(row, widths):
                self.text(cx, ry + rowh / 2, str(cell), size=11.5, fill="ink" if cell and str(cell)[0].isalpha() else "muted")
                cx += cw
        return y + rowh * (len(rows) + 1)

    def sparkline(self, x, y, w, h, values, kind="accent"):
        mx, mn = max(values), min(values)
        pts = []
        for i, v in enumerate(values):
            px = x + i * w / (len(values) - 1)
            py = y + h - (v - mn) / (mx - mn or 1) * h
            pts.append(f"{px:.1f},{py:.1f}")
        col = {"accent": "var(--blue)", "ok": "var(--ok)", "warn": "#d97706"}[kind]
        self.parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>')

    def screen(self, x, y, w, h, rail, header, active=None):
        """A stylized GUI window: dark rail with items, header strip, content area. Returns the content rect."""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="var(--card)" stroke="var(--line)"/>')
        rw = 120
        self.parts.append(f'<path d="M{x + 12},{y} h{rw - 12} v{h} h-{rw - 12} a12,12 0 0 1 -12,-12 v-{h - 24} a12,12 0 0 1 12,-12z" fill="var(--navy)"/>')
        self.text(x + 14, y + 20, "Search2o", size=11, weight=800, fill="white")
        ry = y + 44
        for item in rail:
            if item.startswith("#"):
                self.text(x + 14, ry, item[1:], size=8.5, weight=700, fill="white")
                self.parts[-1] = self.parts[-1].replace('fill="#fff"', 'fill="rgba(255,255,255,.55)"')
            else:
                if item == active:
                    self.parts.append(f'<rect x="{x + 8}" y="{ry - 8}" width="{rw - 16}" height="16" rx="5" fill="var(--teal)" opacity=".85"/>')
                self.text(x + 14, ry, item, size=9.5, weight=500 if item != active else 700, fill="white")
            ry += 17
        self.line(x + rw, y + 30, x + w, y + 30)
        self.text(x + rw + 14, y + 16, header, size=10, weight=600, fill="ink")
        return (x + rw + 14, y + 44, w - rw - 28, h - 56)

    def render(self) -> str:
        defs = (f'<defs><marker id="{self.name}-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="var(--faint)"/></marker>'
                f'<marker id="{self.name}-arr-r" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M10,0 L0,5 L10,10 z" fill="var(--faint)"/></marker></defs>')
        return (f'<figure class="fig"><svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{html.escape(self.title)}" '
                f'xmlns="http://www.w3.org/2000/svg">{defs}{"".join(self.parts)}</svg>'
                f'<figcaption>{html.escape(self.title)}</figcaption></figure>')


# ---------------------------------------------------------------------------- figures
FIGURES: dict[str, callable] = {}


def figure(name):
    def deco(fn):
        FIGURES[name] = fn
        return fn
    return deco


@figure("architecture")
def _architecture():
    f = Fig("architecture", 300, "The three parts, and what talks to what")
    f.group(20, 20, 420, 260, "YOUR ORGANIZATION")
    f.box(40, 60, 120, 60, "Users", "browser", kind="soft")
    f.box(40, 190, 120, 60, "Developers", "browser", kind="soft")
    f.box(210, 100, 210, 110, "Agent server", "stateless · pip install search2o", kind="dark")
    f.text(315, 192, "GUI at /ui · REST at /api", size=11, fill="white", anchor="middle")
    f.parts[-1] = f.parts[-1].replace('fill="#fff"', 'fill="rgba(255,255,255,.75)"')
    f.arrow(160, 90, 210, 125)
    f.arrow(160, 220, 210, 185)
    f.box(480, 60, 220, 190, "Search2o Cloud", "accounts · agents · config", kind="accent")
    f.text(590, 200, "conversation state (encrypted)", size=11, fill="white", anchor="middle")
    f.text(590, 220, "search index · reports", size=11, fill="white", anchor="middle")
    for i in range(-2, 0):
        f.parts[i] = f.parts[i].replace('fill="#fff"', 'fill="rgba(255,255,255,.8)"')
    f.arrow(420, 155, 480, 155, "TLS", both=True)
    f.box(210, 235, 210, 36, "Your APIs · databases · LLMs · MCP", kind="soft", size=11)
    f.arrow(315, 210, 315, 235)
    return f.render()


@figure("request-lifecycle")
def _request_lifecycle():
    f = Fig("request-lifecycle", 210, "From a query to an answer")
    steps = [("1. Query", "user types a request", "soft"), ("2. Match", "cloud picks the agent", "accent"),
             ("3. Run", "agent server executes", "dark"), ("4. Stream", "output as it happens", "soft"),
             ("5. Save", "state stored, encrypted", "accent")]
    x = 20
    for i, (a, b, k) in enumerate(steps):
        f.box(x, 40, 124, 64, a, b, kind=k, size=13)
        if i < 4:
            f.arrow(x + 124, 72, x + 140, 72)
        x += 140
    f.line(642, 104, 642, 140)
    f.line(642, 140, 82, 140)
    f.arrow(82, 140, 82, 104)
    f.text(362, 168, "follow-up: the state is restored and the conversation continues", size=11.5, anchor="middle")
    return f.render()


@figure("build-pipeline")
def _build_pipeline():
    f = Fig("build-pipeline", 230, "From a draft to a searchable agent")
    steps = [("Draft", "private, JSONC", "soft"), ("Validate", "check + run", "accent"), ("Publish", "new version", "dark"),
             ("Describe", "plain English", "soft"), ("Indexed", "found by search", "ok")]
    x = 20
    for i, (a, b, k) in enumerate(steps):
        f.box(x, 40, 124, 64, a, b, kind=k)
        if i < 4:
            f.arrow(x + 124, 72, x + 140, 72)
        x += 140
    f.text(160, 130, "the cloud checks the definition and its expressions;", size=11.5)
    f.text(160, 146, "the agent server runs the validation query with tracing on", size=11.5)
    f.text(520, 130, "cloud indexes the description;", size=11.5)
    f.text(520, 146, "a notification says when it is done", size=11.5)
    f.arrow(300, 104, 300, 120, dashed=True)
    f.arrow(640, 104, 640, 120, dashed=True)
    f.arrow(82, 104, 82, 190, dashed=True)
    f.text(96, 190, "every edit creates a new draft; changes to a published agent go through a draft too", size=11.5)
    return f.render()


@figure("config-sync")
def _config_sync():
    f = Fig("config-sync", 260, "How a configuration change reaches every agent server")
    f.box(20, 40, 150, 56, "GUI", "administrator edits a part", kind="soft")
    f.box(250, 40, 220, 56, "Search2o Cloud", "stores it, stamps the time", kind="accent")
    f.arrow(170, 68, 250, 68, "save")
    f.box(20, 170, 140, 56, "Agent server A", kind="dark")
    f.box(175, 170, 140, 56, "Agent server B", kind="dark")
    f.box(330, 170, 140, 56, "Agent server C", kind="dark")
    for cx in (90, 245, 400):
        f.arrow(cx, 170, min(max(cx, 260), 460), 96, dashed=True)
    f.text(500, 140, "on every agent start:", size=11.5, weight=700, fill="ink")
    f.text(500, 158, "1. tell the cloud a run starts", size=11.5)
    f.text(500, 174, "2. learn the latest change time", size=11.5)
    f.text(500, 190, "3. fetch only the changed parts", size=11.5)
    f.text(500, 206, "4. rebuild the runtime, then run", size=11.5)
    f.text(20, 246, "Every change is live on the next run, on every server; a running agent keeps the runtime it started with.", size=11.5)
    return f.render()


@figure("agent-structure")
def _agent_structure():
    from toc import TOC
    f = Fig("agent-structure", 392, "An agent is a set of functions, main is required, and a function is an ordered dict of commands")
    parts = f.parts
    f.parts = []  # container drawn last, once its height is known
    y = 54
    for name, note, n in [("main", "required · execution starts here", 3), ("functionA", "", 2), ("functionB", "", 2)]:
        h = 30 + n * 20 + 16
        f.box(40, y, 250, h, "", kind="card", r=10)
        f.text(56, y + 16, name, size=12.5, weight=700, fill="ink", mono=True)
        if note:
            f.text(56 + len(name) * 8 + 14, y + 16, note, size=11)
        for i in range(n):
            f.box(56, y + 30 + i * 20, 160, 16, "command", kind="soft", r=4, size=10.5, mono=True)
        f.text(136, y + 30 + n * 20 + 4, "…", size=12, anchor="middle")
        y += h + 10
    left_end = y
    groups: dict[str, list[str]] = {}
    for slug, _, group in next(pages for sec, _, pages in TOC if sec == "commands"):
        groups.setdefault(group, []).append(slug)
    f.text(360, 64, "The commands", size=12.5, weight=700, fill="ink")
    ry = 92
    for group, names in groups.items():
        f.text(360, ry, group, size=10, weight=700)
        cx = 492
        for name in names:
            w = len(name) * 7 + 16
            if cx + w > 700:
                cx, ry = 492, ry + 22
            f.box(cx, ry - 9, w, 18, name, kind="card", r=5, size=10.5, mono=True)
            cx += w + 6
        ry += 26
    bottom = max(left_end, ry - 8)
    body = f.parts
    f.parts = parts
    f.box(20, 20, 680, bottom - 20, kind="soft", r=14)
    f.text(36, 40, "agent", size=13, weight=700, fill="ink", mono=True)
    f.text(92, 40, "a set of functions", size=11)
    f.parts += body
    f.h = bottom + 14
    return f.render()


@figure("variable-scopes")
def _variable_scopes():
    f = Fig("variable-scopes", 230, "Three scopes for variables")
    cols = [("local", "one function, one run", "city, rows, loop variables", "any Python value"),
            ("agent.x", "one agent, whole conversation", "agent.hasInit, agent.cache", "JSON-serializable, saved"),
            ("conv.x", "all agents, whole conversation", "conv.order, conv.customer", "JSON-serializable, saved")]
    x = 20
    for name, scope, ex, kind in cols:
        f.box(x, 30, 220, 130, "", kind="card")
        f.text(x + 16, 52, name, size=13, weight=700, fill="ink", mono=True)
        f.text(x + 16, 78, scope, size=11.5)
        f.text(x + 16, 100, ex, size=11, mono=True)
        f.text(x + 16, 126, kind, size=11.5)
        x += 230
    f.text(20, 186, "read-only:  sys · command · result · exc", size=11.5, weight=600, fill="ink")
    f.text(20, 208, "set with var; seed agent. and conv. values before reading them", size=11.5)
    return f.render()


@figure("flow-control")
def _flow_control():
    f = Fig("flow-control", 300, "Flow control: if, loops, and the commands that leave a loop, a function or the agent")
    # if
    f.text(120, 24, "if", size=12.5, weight=700, fill="ink", anchor="middle", mono=True)
    f.diamond(120, 66, 120, 48, "condition")
    f.arrow(60, 66, 30, 66)
    f.text(45, 54, "true", size=10, anchor="middle")
    f.arrow(180, 66, 210, 66)
    f.text(195, 54, "false", size=10, anchor="middle")
    f.box(20, 104, 80, 40, "then", kind="card", size=12, mono=True)
    f.arrow(30, 66, 30, 104)
    f.box(160, 104, 80, 40, "else", kind="card", size=12, mono=True)
    f.arrow(210, 66, 210, 104)
    f.line(60, 144, 60, 172)
    f.line(200, 144, 200, 172)
    f.line(60, 172, 200, 172)
    f.arrow(120, 172, 120, 192)
    f.box(20, 192, 200, 40, "next command", kind="soft", size=12)
    # loop
    f.text(370, 24, "for / while", size=12.5, weight=700, fill="ink", anchor="middle", mono=True)
    f.diamond(370, 66, 130, 48, "another iteration?")
    f.arrow(370, 90, 370, 118)
    f.text(384, 104, "yes", size=10)
    f.box(300, 118, 140, 96, "", kind="card")
    f.text(370, 134, "body", size=12, weight=700, fill="ink", anchor="middle", mono=True)
    f.box(312, 148, 116, 22, "continue", kind="soft", r=5, size=11, mono=True)
    f.box(312, 178, 116, 22, "break", kind="soft", r=5, size=11, mono=True)
    f.line(370, 214, 370, 232)
    f.line(370, 232, 262, 232)
    f.line(262, 232, 262, 66)
    f.arrow(262, 66, 305, 66)
    f.line(312, 159, 262, 159)
    f.line(435, 66, 484, 66)
    f.text(490, 84, "no", size=10, anchor="middle")
    f.line(484, 66, 484, 277)
    f.arrow(484, 277, 440, 277)
    f.line(428, 189, 484, 189)
    f.box(300, 262, 140, 30, "next command", kind="soft", size=11.5)
    # leaving
    f.text(608, 24, "leaving", size=12.5, weight=700, fill="ink", anchor="middle", mono=True)
    for i, (cmd, target, sub) in enumerate([("return", "function", "a value"), ("end", "agent", "success"), ("fail", "agent", "failure")]):
        y = 48 + i * 74
        f.box(516, y, 76, 40, cmd, kind="card", size=12, mono=True)
        f.arrow(592, y + 20, 626, y + 20)
        f.box(626, y, 74, 40, target, sub, kind="dark" if target == "agent" else "accent", size=11.5)
    return f.render()


@figure("ask-pause")
def _ask_pause():
    f = Fig("ask-pause", 260, "Pausing on ask and resuming with the answers")
    f.box(20, 40, 110, 50, "commands", "run", kind="soft")
    f.box(150, 40, 110, 50, "ask", "pause", kind="accent")
    f.box(280, 40, 200, 50, "position saved", "with the conversation", kind="dark")
    f.arrow(130, 65, 150, 65)
    f.arrow(260, 65, 280, 65)
    f.box(500, 40, 200, 50, "UI shows a form", "user answers later", kind="soft")
    f.arrow(480, 65, 500, 65)
    f.line(600, 90, 600, 122)
    f.line(600, 122, 205, 122)
    f.arrow(205, 122, 205, 160)
    f.text(402, 138, "the answers arrive as the next message", size=11, anchor="middle")
    f.box(150, 160, 110, 50, "ask", "resumes here", kind="accent")
    f.box(280, 160, 200, 50, "result = answers", "keyed by input name", kind="card")
    f.arrow(260, 185, 280, 185)
    f.box(500, 160, 200, 50, "rest of the agent", "variables restored", kind="soft")
    f.arrow(480, 185, 500, 185)
    f.text(20, 240, "Commands before the pause are not re-executed; a function, loop or LLM tool loop in progress continues where it was.", size=11)
    return f.render()


@figure("tool-loop")
def _tool_loop():
    f = Fig("tool-loop", 260, "The llm command's tool loop")
    f.box(20, 40, 150, 56, "prompt", "system + history + query", kind="soft")
    f.box(240, 40, 180, 56, "LLM", kind="accent")
    f.arrow(170, 68, 240, 68)
    f.box(500, 40, 200, 56, "answer", "no tool call · the result", kind="ok")
    f.arrow(420, 68, 500, 68)
    f.arrow(300, 96, 300, 150, "tool call")
    f.box(240, 150, 180, 56, "run the tool", "your function or MCP", kind="dark")
    f.arrow(420, 178, 470, 178)
    f.box(470, 150, 150, 56, "tool results", kind="card")
    f.line(545, 150, 545, 122)
    f.line(545, 122, 390, 122)
    f.arrow(390, 122, 390, 96)
    f.text(360, 232, "Repeats until the LLM answers without a tool call, at most maxToolCallLoops times.", size=11, anchor="middle")
    f.text(360, 248, "A tool error goes back to the LLM with the profile's tool error prompt.", size=11, anchor="middle")
    return f.render()


@figure("deep-agent")
def _deep_agent():
    f = Fig("deep-agent", 250, "A front-door agent: search, then invoke")
    f.box(20, 40, 150, 56, "concierge", "tag: orchestrator", kind="dark")
    f.box(240, 40, 150, 56, "search", "tag: general", kind="accent")
    f.arrow(170, 68, 240, 68)
    f.text(205, 30, "the user's query", size=10.5, anchor="middle")
    f.box(460, 20, 120, 40, "weather", kind="card", size=12, mono=True)
    f.box(460, 70, 120, 40, "hr_policy", kind="card", size=12, mono=True)
    f.box(460, 120, 120, 40, "it_helpdesk", kind="card", size=12, mono=True)
    f.arrow(390, 60, 460, 40)
    f.arrow(390, 68, 460, 90)
    f.arrow(390, 76, 460, 140)
    f.text(600, 40, "0–3 matches,", size=11.5)
    f.text(600, 56, "best first", size=11.5)
    f.box(240, 160, 150, 56, "invoke", "result[0]", kind="accent")
    f.arrow(315, 96, 315, 160, "top match")
    f.arrow(390, 188, 460, 140, curve=30)
    f.text(410, 232, "the chosen agent runs in the same conversation", size=10.5)
    f.arrow(240, 188, 95, 96, "its return value", curve=40)
    return f.render()


@figure("parallel")
def _parallel():
    f = Fig("parallel", 220, "parallel runs functions at once and returns their results keyed by name")
    f.box(20, 80, 150, 56, "parallel", "{A: args, B: args, C: args}", kind="accent", mono=False)
    for i, n in enumerate("ABC"):
        y = 20 + i * 66
        f.box(300, y, 150, 50, f"function {n}", "own locals", kind="dark")
        f.arrow(170, 108, 300, y + 25)
        f.arrow(450, y + 25, 560, 108)
    f.box(560, 80, 140, 56, "result", "{A: rA, B: rB, C: rC}", kind="ok", mono=False)
    return f.render()


@figure("rag")
def _rag():
    f = Fig("rag", 230, "Retrieval-augmented generation")
    f.box(20, 40, 110, 56, "query", "sys.query", kind="soft")
    f.box(220, 40, 140, 56, "retrieve", "db, api or memory", kind="dark")
    f.arrow(130, 68, 220, 68, "terms")
    f.box(400, 40, 130, 56, "passages", "dict by title", kind="card")
    f.arrow(360, 68, 400, 68)
    f.box(580, 40, 120, 56, "prompt", "+ question", kind="soft")
    f.arrow(530, 68, 580, 68)
    f.box(580, 150, 120, 56, "llm", "answer + citations", kind="accent")
    f.arrow(640, 96, 640, 150)
    f.text(20, 180, "The model is told to answer only from the passages and to cite the titles it used.", size=11.5)
    return f.render()


@figure("output-stream")
def _output_stream():
    f = Fig("output-stream", 200, "Output is a stream of parts, appended as commands run")
    xs = 20
    for i, (lbl, k) in enumerate([("text", "soft"), ("html", "soft"), ("image", "soft"), ("llm text", "accent"), ("text", "soft")]):
        f.box(xs, 40, 120, 50, lbl, "part", kind=k, size=12, mono=(k == "soft"))
        if i < 4:
            f.arrow(xs + 120, 65, xs + 136, 65)
        xs += 136
    f.text(20, 130, "each output command appends one or more parts; the browser renders them as they arrive", size=11.5)
    f.text(20, 150, "progress and trace go to separate channels and are not part of the output", size=11.5)
    return f.render()


@figure("conversation-state")
def _conversation_state():
    f = Fig("conversation-state", 270, "What is saved with a conversation")
    f.box(20, 30, 680, 220, "", kind="soft", r=14)
    f.text(36, 50, "conversation state  (encrypted before it leaves the agent server)", size=12, weight=700, fill="ink")
    cols = [("runs", "which agent, inputs, output, where it paused"), ("prompts", "system text + full history per named prompt"),
            ("conv. variables", "shared by every agent"), ("agent variables", "per agent that has run")]
    x = 36
    for a, b in cols:
        f.box(x, 70, 155, 92, "", kind="card")
        f.text(x + 77, 90, a, size=12.5, weight=700, fill="ink", anchor="middle", mono=(a in ("runs", "prompts")))
        cut = b.rfind(" ", 0, 26)
        if cut < 0:
            cut = len(b)
        f.text(x + 77, 118, b[:cut], size=10.5, anchor="middle")
        f.text(x + 77, 134, b[cut + 1:], size=10.5, anchor="middle")
        x += 165
    f.text(36, 188, "saved on end, on return from main, and on ask · not saved on fail or on error", size=11.5)
    f.text(36, 208, "deleted three months after the last run or read · pinned conversations are kept", size=11.5)
    f.text(36, 228, "agents see it only through agent./conv. variables and their prompts", size=11.5)
    return f.render()


@figure("roles")
def _roles():
    f = Fig("roles", 220, "Four roles; each includes the ones below it")
    roles = [("User", "search, converse, own profile", "soft"), ("Developer", "+ agents, dev configuration, agent reports", "card"),
             ("Administrator", "+ users, system configuration, usage reports", "dark"), ("Account owner", "+ owner role, license, billing", "accent")]
    for i, (a, b, k) in enumerate(roles):
        w = 380 + i * 100
        f.box(20, 170 - i * 46, w, 40, "", kind=k)
        f.text(36, 190 - i * 46, a, size=12.5, weight=700, fill="white" if k in ("dark", "accent") else "ink")
        f.text(w + 6, 190 - i * 46, b, size=11, anchor="end", fill="white" if k in ("dark", "accent") else "muted")
        if k in ("dark", "accent"):
            f.parts[-1] = f.parts[-1].replace('fill="#fff"', 'fill="rgba(255,255,255,.8)"')
    return f.render()


@figure("encryption")
def _encryption():
    f = Fig("encryption", 250, "Two ways to hold the encryption key")
    f.group(20, 20, 330, 210, "CLOUD-MANAGED (DEFAULT)")
    f.box(40, 60, 130, 50, "agent server", kind="dark", size=12)
    f.box(210, 60, 120, 50, "cloud", "key per account", kind="accent")
    f.arrow(170, 78, 210, 78, both=True)
    f.text(190, 50, "gets the key", size=10.5, anchor="middle")
    f.arrow(105, 110, 105, 150)
    f.box(40, 150, 130, 50, "AES-GCM", "encrypts state", kind="card", size=12)
    f.arrow(170, 175, 270, 120, "ciphertext only", dashed=True)
    f.group(370, 20, 330, 210, "END-TO-END (CLIENT)")
    f.box(390, 60, 130, 50, "agent server", kind="dark", size=12)
    f.box(560, 60, 120, 50, "keyFunction", "on the allowlist", kind="card", size=12)
    f.arrow(520, 78, 560, 78, both=True)
    f.text(540, 50, "key by name", size=10.5, anchor="middle")
    f.arrow(455, 110, 455, 150)
    f.box(390, 150, 130, 50, "AES-GCM", "encrypts state", kind="card", size=12)
    f.box(560, 150, 120, 50, "cloud", "ciphertext only", kind="accent")
    f.arrow(520, 175, 560, 175)
    return f.render()


@figure("search-results")
def _search_results():
    f = Fig("search-results", 200, "What a search returns")
    f.box(20, 40, 200, 110, "one agent", "the query clearly belongs to it", kind="ok")
    f.text(120, 128, "runs at once (default)", size=11, anchor="middle")
    f.box(260, 40, 200, 110, "two or three", "overlap or an ambiguous query", kind="card")
    f.text(360, 128, "the user picks", size=11, anchor="middle")
    f.box(500, 40, 200, 110, "none", "outside every description", kind="soft")
    f.text(600, 128, "nothing runs", size=11, anchor="middle")
    f.text(20, 178, "Matching is semantic and answers in well under a second; the description is the only input a developer controls.", size=11)
    return f.render()


@figure("sandbox")
def _sandbox():
    f = Fig("sandbox", 250, "What decides what an expression may do")
    f.box(20, 30, 680, 200, "", kind="soft", r=14)
    f.text(36, 50, "a Python expression in braces", size=12, weight=700, fill="ink")
    layers = [("allowlist", "the only names it can reach; public members of allowlisted objects; no import, no dunders"),
              ("operator rules", "each operator allowed, denied or rewritten to a bounded safe function"),
              ("runtime limits", "time, loop iterations, database rows, definition size, LLM spend"),
              ("scope", "earlier locals, agent./conv. variables, sys and command namespaces — nothing else")]
    y = 70
    for a, b in layers:
        f.box(36, y, 150, 32, a, kind="card", size=12)
        f.text(200, y + 16, b, size=11.5)
        y += 40
    return f.render()


# ---- GUI mock-ups --------------------------------------------------------------
RAIL = ["#AGENTS", "Drafts", "Published", "Search", "#PROFILES", "LLM", "Prompt", "API", "Database", "MCP",
        "#GUARDRAILS", "Compile rules", "Allowlist", "Runtime"]
RAIL2 = ["#OPERATIONS", "Agent servers", "Connection pools", "Secrets & encryption", "#REPORTS", "Performance", "Cost", "Errors", "Usage",
         "#ACCOUNT", "Users", "Authentication", "License"]


def _report(name, title, header_cols, rows, widths, trend_labels):
    f = Fig(name, 320, title)
    x, y, w, h = f.screen(20, 20, 680, 280, RAIL2, f"Acme Corp / {title.split(':')[0]}", active=title.split(":")[0].split(" ")[-1].capitalize() if False else None)
    f.box(x, y - 4, 120, 22, "Last 7 days  ⌄", kind="soft", size=9.5, r=5)
    f.text(x + w, y + 7, "daily buckets", size=8.5, anchor="end")
    for i, lbl in enumerate(trend_labels):
        tx = x + i * (w / len(trend_labels))
        f.text(tx, y + 32, lbl, size=8.5, weight=700)
        f.sparkline(tx, y + 42, w / len(trend_labels) - 24, 30, [3, 5, 4, 7, 6, 9, 8][: 7], kind=["accent", "ok", "warn"][i % 3])
    f.table(x, y + 88, w, header_cols, rows, widths=widths, rowh=21)
    return f.render()


@figure("report-performance")
def _report_performance():
    return _report("report-performance", "Performance: executions, users, success rate and latency per agent",
                   ["Agent", "Executions", "Users", "Success", "Avg", "P95", "Last run"],
                   [["weather", "162", "24", "100%", "1.7 s", "2.9 s", "Aug 27"], ["hr_policy", "58", "19", "98%", "1.2 s", "2.1 s", "Aug 27"],
                    ["order_lookup", "53", "6", "94%", "3.4 s", "6.8 s", "Aug 26"], ["docs_rag", "35", "11", "100%", "2.6 s", "4.0 s", "Aug 26"]],
                   [95, 70, 50, 60, 55, 55, 70], ["Executions", "Duration", "Distinct agents"])


@figure("report-errors")
def _report_errors():
    return _report("report-errors", "Errors: failures per agent, by result code, with the messages behind them",
                   ["Agent", "Errors", "Executions", "Rate", "Users", "Codes", "Last"],
                   [["order_lookup", "3", "53", "5.7%", "2", "callFailed", "Aug 26"], ["hr_policy", "1", "58", "1.7%", "1", "timedOut", "Aug 25"]],
                   [95, 55, 70, 50, 50, 90, 60], ["Errors", "Executions", "Users affected"])


@figure("report-cost")
def _report_cost():
    return _report("report-cost", "Cost: LLM spend per agent, from token counts and the profile's prices",
                   ["Agent", "Executions", "Users", "Total", "Average", "Maximum", "Last run"],
                   [["docs_rag", "35", "11", "$0.41", "$0.012", "$0.031", "Aug 26"], ["weather", "162", "24", "$0.29", "$0.002", "$0.004", "Aug 27"],
                    ["order_lookup", "53", "6", "$0.22", "$0.004", "$0.011", "Aug 26"]],
                   [95, 70, 50, 60, 65, 70, 60], ["Total cost", "Average cost", "P95 cost"])


@figure("report-usage")
def _report_usage():
    return _report("report-usage", "Usage: what each user ran, for administrators",
                   ["User", "Executions", "Agents", "Success", "Cost", "Last run"],
                   [["Mei Chen", "88", "5", "99%", "$0.31", "Aug 27"], ["Diego Alvarez", "41", "7", "95%", "$0.27", "Aug 27"], ["Priya Natarajan", "23", "4", "100%", "$0.09", "Aug 26"]],
                   [120, 70, 60, 60, 60, 60], ["Active users", "Total duration"])

def _detail(name, title, crumb, kpis, cols, rows, widths, trend_labels, extra=None, height=300):
    f = Fig(name, height + 40, title)
    x, y, w, h = f.screen(20, 20, 680, height, RAIL2, crumb)
    kw = (w - 12 * (len(kpis) - 1)) / len(kpis)
    kx = x
    for val, lbl in kpis:
        f.box(kx, y - 4, kw, 40, "", kind="soft", r=6)
        f.text(kx + 10, y + 10, val, size=13, weight=700, fill="ink")
        f.text(kx + 10, y + 27, lbl, size=8.5)
        kx += kw + 12
    for i, lbl in enumerate(trend_labels):
        tx = x + i * (w / len(trend_labels))
        f.text(tx, y + 54, lbl, size=8.5, weight=700)
        f.sparkline(tx, y + 62, w / len(trend_labels) - 24, 26, [4, 6, 3, 7, 5, 8, 6], kind=["accent", "ok", "warn"][i % 3])
    yy = f.table(x, y + 102, w, cols, rows, widths=widths, rowh=21)
    if extra:
        extra(f, x, yy + 10, w)
    return f.render()


@figure("report-performance-detail")
def _report_performance_detail():
    return _detail("report-performance-detail", "Agent detail: the same figures per published version, plus the agent's trend",
                   "Acme Corp / Reports / Performance / order_lookup",
                   [("53", "executions"), ("6", "users"), ("94%", "success"), ("3.4 s", "average"), ("6.8 s", "p95")],
                   ["Version", "Executions", "Users", "Success", "Avg", "P95", "Cost", "Last run"],
                   [["Aug 24 09:12", "31", "6", "97%", "3.1 s", "5.9 s", "$0.13", "Aug 27"], ["Aug 12 16:40", "22", "4", "91%", "3.8 s", "7.2 s", "$0.09", "Aug 24"]],
                   [95, 65, 45, 55, 50, 50, 50, 60], ["Executions", "Duration", "Users"], height=260)


@figure("report-errors-detail")
def _report_errors_detail():
    def extra(f, x, y, w):
        f.text(x, y + 6, "Example queries (a sample, most recent first)", size=9, weight=700)
        f.text(x, y + 22, "“where is order 48812” · “status of my order from last week” · “track 48719”", size=9.5, fill="ink")
    return _detail("report-errors-detail", "Error detail: failures by version, then result code, then message and path",
                   "Acme Corp / Reports / Errors / order_lookup",
                   [("3", "errors"), ("53", "executions"), ("5.7%", "error rate"), ("2", "users affected"), ("2", "messages")],
                   ["Version · code", "Message", "Path", "Count", "Users", "Last"],
                   [["Aug 24 · callFailed", "HTTP 503 from orders API", "main.api.orders", "2", "2", "Aug 26"],
                    ["Aug 24 · callFailed", "timeout after 8 s", "main.api.orders", "1", "1", "Aug 25"]],
                   [108, 172, 102, 46, 46, 50], ["Errors", "Executions", "Users affected"], extra)


@figure("report-cost-detail")
def _report_cost_detail():
    return _detail("report-cost-detail", "Cost detail: spend per published version, each with its own trend",
                   "Acme Corp / Reports / Cost / docs_rag",
                   [("$0.41", "total"), ("$0.012", "average"), ("$0.031", "maximum"), ("35", "executions"), ("11", "users")],
                   ["Version", "Executions", "Users", "Total", "Average", "Maximum", "First run", "Last run"],
                   [["Aug 25 11:03", "20", "9", "$0.25", "$0.013", "$0.031", "Aug 25", "Aug 26"], ["Aug 18 08:47", "15", "6", "$0.16", "$0.011", "$0.024", "Aug 18", "Aug 25"]],
                   [95, 65, 45, 50, 55, 60, 60, 60], ["Total cost", "Average cost", "P95 cost"], height=260)


@figure("report-usage-detail")
def _report_usage_detail():
    def extra(f, x, y, w):
        f.table(x, y, 300, ["Result code", "Errors", "Last"], [["callFailed", "1", "Aug 26"]], widths=[130, 80, 80], rowh=20)
    return _detail("report-usage-detail", "User detail: one user's summary, the agents they ran, their trend and their failures",
                   "Acme Corp / Reports / Usage / Mei Chen",
                   [("88", "executions"), ("5", "agents"), ("99%", "success"), ("$0.31", "LLM cost"), ("6", "active days")],
                   ["Agent", "Executions", "Success", "Cost", "Avg", "Last run"],
                   [["weather", "41", "100%", "$0.07", "1.6 s", "Aug 27"], ["hr_policy", "24", "100%", "$0.09", "1.3 s", "Aug 27"], ["order_lookup", "12", "92%", "$0.05", "3.5 s", "Aug 26"]],
                   [110, 70, 60, 55, 55, 60], ["Executions", "Cost", "Duration"], extra)


def render(name: str) -> str:
    return FIGURES[name]()
