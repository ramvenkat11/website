## 2026-10-02 — Home page hero figure: agents row and claim band

- Done: in the hero architecture figure (`html/index.html`, `html/styles/styles.css`), the "Agents" label, the three agent-name chips and "+ hundreds more" now sit on one row. The chips shrink with the figure width (container-query units on `.cc-agents`, 11.5px down to 10px). The "Validated / Bounded / Observable / Model-neutral" list moved out of `.cc-agents` to be a direct child of the server node, under its own divider, so that the claim is visually separate from the facts.
- Phones (viewport under 500px): the row cannot fit, so the label and chips flow as two rows: "Agents leave_balance fx_rates" then "product_recalls + hundreds more". A `padding-right: max(0px, 100% - 330px)` on `.cc-agents` keeps "+ hundreds more" from being left alone on a row at 452–499px.
- Checked with headless Chrome screenshots at 1440, 1001, 500, 460, 390 and 360px. Headless Chrome does not exit after `--screenshot` on this page and cannot go below a 500px window; run it in the background, stop it once the image exists, and use an iframe page for phone widths.
- State: not committed, not uploaded.
- Open: between 1001px and about 1150px the "Validated…" list wraps "Model-neutral" to a second row (it did before this change).

## 2026-10-02 — Hero figure: "Validated…" list on one row

- Done: the `.cc-attrs` list in the hero figure now scales with the server node (`font-size: clamp(12px, 3.4cqi, 15px)`, icon and gaps in `em`), so that "Model-neutral" stays on the first row from 500px upward. The container for the `cqi` units moved from `.cc-agents` to the hero server node (`.cc-arch.hero-arch .arch-flow > .arch-node`). The `@media (min-width: 1200px)` override for `.cc-attrs` was removed; tablets (641–1000px) now show the list at 15px instead of 14px.
- Phones (under 500px): one row would need about 9px text, so the list is a fixed 2 × 2 grid (Validated, Bounded / Observable, Model-neutral), shrinking below 360px.
- Checked with screenshots at 1440, 1001, 498, 460, 412, 390, 360 and 320px, dark theme only.
- State: not committed, not uploaded.

## 2026-10-02 — Hero figure: phone arrow under search2o-skill

- Done: in the `@media (max-width: 640px)` block of `html/styles/styles.css`, `.cc-join i:first-child` had `height: 16px; margin-top: 10px`, 4px short of the 30px row, so that the arrow under the search2o-skill chip stopped above the horizontal line. Height is now 20px. The arrow was already short before today's changes.
- Checked with a 3x screenshot at 500px wide, cropped with `sips -c … --cropOffset`. An iframe page is not usable for this crop: the demo input takes focus and scrolls the frame.
- State: not committed, not uploaded.

## 2026-10-02 — demo-agents.html: the 200 demo agents

- Done: `html/demo-agents.json` is a straight copy of `../s2oserver/docs/demo/agents.json` (200 agents, 20 groups of 10; copy it again whenever the demo account changes). `html/demo-agents.html` is a hand-written top page with the usual header and footer, no header entry; its inline script fetches the JSON and renders a jump list of groups and one section per group (title, agent name in code, description). On fetch failure it shows a line linking to the raw file. Styles: `.agents-status`, `.group-jump`, `.agent-group`, `.agent-list` next to `.page-body` in `html/styles/styles.css`.
- Links: `html/index.html` has "See the 200 agents in this demo →" under the hero demo box (`.hero-demo-link`); `html/demo.html` links "200 agents" in the hero note. Sitemap: `html/sitemap.xml` and `SITE_PAGES` in `gen/build.py`.
- Checked at 1280px and 500px with a local `python3 -m http.server` (fetch needs http, not file://), dark theme only.
- State: not committed, not uploaded.

## 2026-10-02 — Hero demo: agents link moved into data-search-empty

- Done: `html/index.html` `data-search-empty` now reads "...with [200 agents](demo-agents.html) using models..." (Ram: the attribute accepts markdown). The separate `.hero-demo-link` line under the box and its CSS are removed.
- Open: `html/demo/demo.js` built 2026-10-02 14:54 still renders the brackets literally; the link appears once ui1 rebuilds the bundle with markdown support.
- State: not committed, not uploaded.

## 2026-10-02 — demo-agents.html: source on click and per-agent anchors

- Done: `html/demo-agents/` holds a straight copy of `../s2oserver/docs/demo/definitions/*.jsonc` (200 files, 193 KB; copy again with the JSON). Each row on `demo-agents.html` has a "Show source" button that fetches `demo-agents/<name>.jsonc` once and opens a `.codecard` with the file name, line count, copy button and highlighted JSONC (the six regexes from `gen/build.py` `_TOKENS["jsonc"]`, ported to the page script). Token colours for `.codecard` were added to `styles.css`; the card is capped at 560px tall and scrolls.
- Anchors: every row has `id="<agentName>"`, so `demo-agents.html#leave_balance` scrolls to that agent and opens its source (also on hashchange). Group sections keep `group-<slug>` ids, so names cannot clash. The home page search results can link to `demo-agents.html#<agentName>`.
- Checked at 1280px and 500px over the local server with `#benefits_enrollment`.
- State: not committed, not uploaded.

## 2026-10-02 — Price changed to $40 per user per month

- Done: `html/pricing.html` (meta description, og:description, the Prod paragraph) now says $40 per user per month instead of $30. No other shipped page states the amount; `docs/support-licensing/license.html` says "priced per user per month" without a figure.
- Open: `content/pricing.md` and `content/pricing2.md` (planning notes, not shipped) still say $30.
- State: not committed, not uploaded.
