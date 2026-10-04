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
- Also changed to $40: the per-member price in `content/pricing.md` (lines 17, 44, 55, 94, 102, 113), `content/pricing2.md:20` and `content/pricing_table.md:8`. Still $30 in `content/pricing.md`: the overage "$30 per additional 300 executions" (lines 20, 34, 94, 105, 120), which the note defines as "the same as a seat"; waiting for Ram to say whether it moves to $40 too.

## 2026-10-02 — Visitor review of the live site

- Done: visited https://search2o.com with headless Playwright Chromium (the Claude in Chrome extension refused the domain as "blocked by your site permissions" despite Chrome's site-access setting) and ran the three homepage demos as a technical first-time visitor: 8 live-demo requests, 4 generator runs, 2 docs questions, plus the getting-started and pricing pages. Screenshots and recorded text are in the session scratchpad, not in the repo.
- Findings reported in chat: the generator is the strongest demo (coherent JSONC in 3–9 s, even from a sloppy sentence); the live demo answers in 1–5 s and names the agent, but `leave_balance` and `fx_rates` ask back for values already in the request (default USD leads to "Our books are already in USD"), "What can you do?" routes to `ethics_hotline`, and the same request gave different mock output on two runs; the docs box refuses the LangChain/LangGraph comparison but answers the on-prem question honestly. "Avoid context rot" is never demonstrated on the page.
- State: no site files changed. Nothing committed, nothing uploaded.
- Added: the review as a local page, `content/review-2026-10-02/index.html`, with the 18 screenshots it cites in `content/review-2026-10-02/shots/` (2 MB). Not linked from the site; not committed, not uploaded.

## 2026-10-03 — demo-agents: refreshed the 200 definitions from s2oserver

- Done: copied `../s2oserver/docs/demo/definitions/*.jsonc` over `html/demo-agents/` again. 83 of the 200 files had changed (3835 lines added, 831 removed); the file names are the same 200 on both sides. `diff -rq` now reports the two directories identical.
- `html/demo-agents.json` was already byte-identical to `../s2oserver/docs/demo/agents.json`, so it is unchanged.
- State: working tree only. Not committed, not uploaded.
- Next: Ram reviews and commits; upload waits for his go-ahead.

## 2026-10-03 — Skill integration docs redone from content/behind_skill.md

- Done: `docsrc/skill-integration/overview.html` (Skills + Search2o) is now the opening of `content/behind_skill.md`, the `skill-flow` figure, the "At a glance" table word for word (`table.fields.compare`, because plain `table.fields` uppercases the header and would show "SEARCH2O") and "What stays with Claude". `docsrc/skill-integration/what-search2o-provides.html` (What Search2o adds) is now the twelve numbered points under Context and tokens, Models, Control and Reach, then "What it costs" and the Anthropic and other sources. The document's list of Search2o sources is left out, because those are inline links to the docs' own pages.
- Links: `https://search2o.com/docs/...` links became relative. The two links that pointed at `what-search2o-provides.html` itself now go to `../search/how-matching-works.html` and `../development/publishing.html`. External links open in a new tab.
- Unchanged: `finding-and-running-an-agent.html`, `installing-the-skill.html`, the section `index.html` lead, and page titles in `gen/toc.py`. The old overview text (the Eric Holmes MCP article, the four risks of a direct skill) and the old ten-item list are gone from the docs.
- State: `gen/build.py` ran (144 pages, no broken internal links on the three rebuilt pages). Not committed, not uploaded. Not checked in a browser.
- Next: Ram reviews; possible follow-ups are the section index lead and whether "What it costs" deserves its own page.

## 2026-10-03 — Skill integration docs: link check and three corrections

- Checked: all 20 external links on the two rewritten pages return 200 and their three `#` anchors exist. Every internal target was read for the fact its link text claims.
- Fixed in `docsrc/skill-integration/what-search2o-provides.html`: (1) "search costs no model tokens" is no longer a link; no docs page states that fact (the old version of this page was the only one). (2) "serves the GUI, the chat bots, the REST API and the skill" is no longer a link, for the same reason. (3) "kept for three months after last use" now reads "7 days after the last use on the Free plan and 90 days on Paid", matching `docsrc/security/data-privacy.html`.
- Open: `content/behind_skill.md` still says "three months" and still links those two facts to `what-search2o-provides.html`. "Under a second" on this page versus "less than 0.5 seconds" on `search/how-matching-works.html` are both true but differ. The "Reports" link goes to `reports/cost.html`, which shows cost per agent and per version, not per person.

## 2026-10-03 — what-is-search2o.html: lead sentence split

- Done: in `docsrc/introduction/what-is-search2o.html` the lead now ends "...runs the agent, and returns the answer. The answer starts a conversation that the user can continue." Docs rebuilt; only `html/docs/introduction/what-is-search2o.html` changed, because the page description and the card blurb are cut off before that sentence.
- State: not committed, not uploaded.

## 2026-10-03 — New docs section: Comparisons, with "Search2o and LangChain"

- Done: `gen/toc.py` has a "Comparisons" section (slug `comparisons`) before "Support and licensing", with one page, `langchain` ("Search2o and LangChain"). `docsrc/comparisons/langchain.html` is `content/langchain.md` converted: the first paragraph is the lead (the "The short answer" heading and the byline are dropped), the table uses `table.fields.compare`, the three `https://search2o.com/docs/...` links are relative, external links open in a new tab. `docsrc/comparisons/index.html` says other comparisons will be added as needed.
- Also: a Comparisons card on the docs home (`docsrc/index.html`, under "Reference and more") and a Comparisons block in `docs_links.md`. `html/sitemap.xml` picks up the two pages from the build.
- State: build wrote 146 pages; every page under `html/docs/` changed because the sidebar gained a section. No broken internal links on the new pages; the six LangChain URLs return 200. Not committed, not uploaded, not checked in a browser.
- Open: `docs_links.md` has no "Skill integration" block.

## 2026-10-03 — Home hero: third heading line made secondary

- Done: `html/styles/styles.css` has a new rule `.hero h1 .line` (16px, weight 500, `var(--muted)`, 10px above, normal letter spacing), so that "Avoid context rot, unpredictable workflows, and runaway LLM costs." reads as a supporting line under the two 24px/800 lines. `html/index.html` is untouched by this; the longer wording of that line was already an uncommitted edit by Ram.
- Checked: headless Chrome screenshot at 1280px, dark theme. Phone width not verified (headless Chrome does not go below about 500px wide).
- State: not committed, not uploaded.

## 2026-10-03 — Home hero: third heading line, gentler step down

- Ram found the muted 16px/500 version abrupt ("suddenly the color goes away"). `.hero h1 .line` in `html/styles/styles.css` is now 19px, weight 600, 6px above, and inherits the heading colour (`--ink`), so the three lines read ink, gradient, ink, and the third is lower only in size and weight.
- Checked at 1280px in the dark theme by headless screenshot. Not committed, not uploaded.

## 2026-10-04 — Home hero: third heading line, back to the first version with a stronger grey

- Ram found the 19px/600 ink version too prominent and preferred the first one, which he had called abrupt in colour. `.hero h1 .line` is now the first version (16px, weight 500, 10px above) with `var(--body)` instead of `var(--muted)`.
- If this misses too, ask numbered questions (size, weight, colour) instead of trying a fourth variant.
- Checked at 1280px, dark theme, headless screenshot. Not committed, not uploaded.

## 2026-10-04 — Second visitor review of the live site

- Done: repeated the 2 October review (prompt in `content/prompt.txt`) against https://search2o.com, which was byte-identical to the local `html/` for index, demo, styles and scripts. Headless Playwright Chromium, reusing the module in the 2 October session's scratchpad. 16 live-demo requests, 5 generator runs, 4 docs questions, phone width, getting-started and pricing.
- Added: `content/review-2026-10-04/index.html` with 27 screenshots in `content/review-2026-10-04/shots/` (3 MB). Same layout as the 2 October page, plus "What changed since 2 October" and "The third headline line". Not linked from the site, not committed, not uploaded.
- Fixed since 2 October: `fx_rates` answers in one step and handles the follow-up; unrelated request gets "No agent matches this question"; ambiguous requests show a list of matches; the docs box answers the LangChain question; phone reaches the demo after 1.2 screens; agent names link to source.
- Open: `leave_balance` never returns a balance (asks type, then "I don't have your employee ID"; or points to the HR portal). Questions about Search2o typed into the hero box match mock agents (`paper_summaries`, `research_grants`...). The docs box invented agent syntax in 2 of 4 answers (`"definition": [{"command": "query_db"}]`) and gives no links. Same recall request returned different mock facts in two sessions. "What can you do?" lists `ethics_hotline` first. Enter after clicking the send arrow repeats the search (seen headless only).
- Hero third line: unexplained by design (Ram). The docs box explains all three claims in 10–12 s; the hero box cannot.
- State: no site files changed by this task.

## 2026-10-04 — Ram's verdict on the second visitor review

- Ram: the review nitpicked and tested in ways normal visitors will not; none of the listed errors is concerning; the site lacks nothing. Mock data is labelled, agent source is one click away, Eval is free so the GUI need not be shown before sign-up.
- `content/review-2026-10-04/index.html` is unchanged and still lists those items; treat its "Gap" and "Fails" entries as rejected unless Ram says otherwise.
