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

## 2026-10-04 — Third review: what stands between a visitor and an eval sign-up

- Scope set by Ram: only obstacles to a normal person creating an eval account. Walked home → "Try it free" → form at 1440px and 390px; read `html/js/site.js` for what the form accepts; did not submit.
- Result, reported in chat (no review page written): nothing on the site stands in the way. "Try it free" is in the sticky header on every page and at both widths; the form is three fields and a checkbox, fully on the first screen at desktop; the key appears at once, no email, no card.
- One conditional item: `site.js` has the server error `freeEmailCurrentlyNotAllowed` ("Public email domains are currently not allowed"). If the registration server has that rule on, a visitor with a gmail address learns it only after clicking "Create account"; the label says "Work email" and nothing more. Whether the rule is on is a server setting I did not test.

## 2026-10-04 — Sign-up path review closed

- Ram: the public-email rule is off; only throwaway addresses (mailinator and the like) are refused. So the one conditional item falls away, and the review's result is that nothing stands between a visitor and an eval sign-up.

## 2026-10-04 — Images on mobile: scan at 390px (no changes made)

- Ram: "the images are not showing right on mobile". Scanned all 157 built pages at 390px with Playwright (script `imgs.js` in the session scratchpad): every `figure`, `aside.arch`, `img` and `svg` in `main`.
- Found: all docs `figure.fig` SVGs (viewBox 720 wide, `width: 100%` in `html/docs/docs.css:149`) render 342px wide, scale 0.47, so their text is 4–5.4px. All `figure.shot` screenshots (1374–1568px captures, `--shot-w` 520–560px) render 342px wide. No page overflows horizontally, no image fails to load, both-theme images never show together. The home page diagrams are HTML and reflow correctly.
- Not yet confirmed with Ram that this is the problem he sees. Candidate fix: on narrow screens give `figure.fig` and `figure.shot` a horizontal scroll at a readable minimum width, or open the full image on tap.

## 2026-10-04 — Ollama and vLLM: five bundled LLM adapters

- Facts read from `../search2o/search2o/llm/` (`llmcontext.py`, `ollamaadapter.py`, `vllmadapter.py`) and that project's WORKLOG: bundled adapters are `anthropic`, `gemini`, `openai`, `ollama`, `vllm`. Both new ones extend the OpenAI adapter and call the server's `/v1/responses`. A profile's `url` is posted to as written, so it carries the full path. Ollama ignores `tool_choice`; the `ollama` adapter gets structured output through a JSON schema. vLLM needs `--enable-auto-tool-choice` and `--tool-call-parser` for tool calls. No seeded profiles were added for either.
- Docs changed: `docsrc/llm/vendors.html` (lead, `adapter` row, new section "Models you host: Ollama and vLLM" with a profile table, "Any compatible LLM" reworded), `docsrc/llm/llm-adapters.html` (five adapters, four sentences), `docsrc/llm/index.html` and the LLM card in `docsrc/index.html`, `docsrc/profiles/llm-profiles.html` ("Other vendors"), `docsrc/getting-started/running-the-server.html`, `docs_links.md` (label "LLM vendors").
- `content/behind_skill.md` changes carried into `docsrc/skill-integration/overview.html` (reworded tokens row, new row "What the model work costs", models row) and `what-search2o-provides.html` (points 2, 4, 5, 8, 11 and the sources). The earlier corrections on that page stay (retention 7/90 days, two unlinked claims).
- Home hero: `html/index.html` LLMs box reads "OpenAI · Anthropic · Gemini · Ollama · vLLM · Other", with non-breaking spaces before the dots so it breaks three and three at desktop. Box height unchanged (105px desktop, 130px phone).
- Not changed, reported to Ram: the "Model neutrality" card on the home page and step 3 of `html/gettingstarted.html` still name three vendors; GUI screenshots in the docs were not checked for an adapter list.
- State: docs rebuilt (146 pages). Not committed, not uploaded. `https://docs.vllm.ai/en/latest/` answered 429 to the link check twice; `https://ollama.com` 200.

## 2026-10-04 — Home page "Model neutrality" card names five

- `html/index.html`: the card now reads "Bring your own keys, or host your own models. OpenAI, Anthropic, Gemini, Ollama, and vLLM are supported out of the box, along with any compatible LLM. Others need only a small adapter." Not committed, not uploaded.

## 2026-10-04 — Getting started: no vendor key needed with Ollama or vLLM

- `html/gettingstarted.html` step "Run the server": the sub-heading "Use an LLM key" is now "Choose an LLM", with a second paragraph saying a model hosted with Ollama or vLLM needs no vendor key (start without one, create an LLM profile after sign-in; links to `docs/llm/vendors.html#models-you-host-ollama-and-vllm`). The start commands still show `ANTHROPIC_API_KEY` as the example.
- `docsrc/getting-started/running-the-server.html` "LLM keys" says the same. Docs rebuilt. Not committed, not uploaded.
- Assumed, not tested: the agent server starts with no vendor key set (the seeded profiles read their key at call time).

## 2026-10-04 — `vendor` field removed from the LLM profile docs

- Ram: the field is gone from LLM profiles (confirmed in `../s2oserver/models/systemconfig.py` and `../search2o` notes). Removed from `docsrc/llm/vendors.html` (two table rows), `docsrc/llm/llm-adapters.html` (the sentence about reports grouping under the field), `docsrc/gui/profiles.html` (caption and the field list), `docsrc/profiles/overview.html` (table cell). The generated field table on `profiles/llm-profiles.html` lost its row on rebuild, because it is built from the s2oserver model.
- Kept: the word "vendor" where it means a company (OpenAI etc.), `vendorTools`, the adapter method `set_assistant_vendor`, and the "Vendor" column of the seeded-profiles table on `llm/vendors.html`.
- Stale, cannot fix here: the screenshot `html/docs/img/gui-profiles-{light,dark}.png` still shows a "Vendor" column (and profile names `anthropic`, `openai` instead of `claude_haiku`, `gpt5_mini`).
- State: docs rebuilt. Not committed, not uploaded.

## 2026-10-04 — GUI screenshots removed from the docs

- Ram: remove all GUI screenshots; the GUI is a moving target at this stage. (A recapture of the LLM profiles list through Chrome failed first: the extension's tab was hidden, so screenshots timed out.)
- Done: all 17 `<!--shot:...-->` lines removed from 9 files under `docsrc/` (`development/code-editor`, `development/trace-and-validation`, `gui/index`, `gui/search`, `gui/agents`, `gui/profiles`, `gui/guardrails`, `gui/operations`, `gui/account`, `hooks/overview`). No surrounding sentence referred to a screenshot. Docs rebuilt; no page has a `figure.shot` or links to `img/` any more.
- Left in place: the 34 PNG files in `html/docs/img/` (deleting project files needs Ram's permission each time), and the `shot` support in `gen/build.py` and `html/docs/docs.css`, so screenshots can come back later.
- State: not committed, not uploaded. The PNGs are also still in the bucket.

## 2026-10-04 — demo-agents refreshed again from s2oserver

- Done: copied `../s2oserver/docs/demo/definitions/*.jsonc` over `html/demo-agents/` (22 of 200 files had changed; same 200 names) and `../s2oserver/docs/demo/agents.json` over `html/demo-agents.json`. Both now identical to the source.
- `agents.json` has a new field per agent, `model` (the model the agent's LLM profile calls). Group, name, title and description are unchanged for all 200. `html/demo-agents.html` ignores the new field.
- State: not committed, not uploaded.

## 2026-10-05 — demo-agents.html shows each agent's model

- Ram: add the model from `agents.json` to the left column (title, name, model). `html/demo-agents.html`: one line in the render script adds `<code class="agent-model">` under the agent name when the entry has `model`. No CSS change; it takes the existing `.agent-list code` style. Checked at 1280px and 390px with a local server: 200 rows, 200 model lines.
- State: not committed, not uploaded.

## 2026-10-05 — Hero figure: agent names removed

- Ram: no actual agent names; only communicate that there are hundreds. In `html/index.html` the `.cc-agents` row is now one label, "Hundreds of task-specific agents" (the `.arch-chips` with `leave_balance`, `fx_rates`, `product_recalls`, "+ hundreds more" is gone). No CSS change; the chip rules for `.cc-agents .arch-chips` in `styles.css` are now unused.
- Checked by screenshot at 1440px; rendered at 390px but not viewed. Not committed, not uploaded.

## 2026-10-05 — Hero figure: agents shown as a field of blank chips

- Ram rejected the text line "Hundreds of task-specific agents" ("Very bad design! This is hero section. Do not write text."). The `.cc-agents` row is now the label "Agents" plus `.cc-agent-field`: 54 empty `<i>` pills of eight widths in three rows, clipped at 40px and faded out to the right with a mask, so the row reads as many agents continuing past the edge. `aria-hidden`.
- CSS in `html/styles/styles.css`: `.cc-agent-field` rules after the `.cc-agents .arch-chips span.more` rule, and two lines in the phone block (`.cc-agents:has(.cc-agent-field)` no-wrap, field `flex: 1`).
- Checked by screenshot at 1440px and 390px, light theme. Dark theme not viewed. Not committed, not uploaded.
- This is the first redraw of this row; if it misses, ask numbered questions before another attempt.

## 2026-10-05 — Hero figure: "Agents" label centred in the chip field

- Ram: put the Agents wording in the middle, not on the left. `.cc-agents:has(.cc-agent-field)` is now a positioned block; `.cc-agents-lbl` is absolutely centred over the field on a `var(--card)` pill with a soft halo, and the field is centred and fades out at both ends. The phone override is reduced to `padding-right: 0`.
- Checked by screenshot at 1440px and 390px, light theme. Dark theme not viewed. Not committed, not uploaded.

## 2026-10-05 — Light/dark button in the header of every page

- Done: the `.theme-toggle` button (same markup as the docs header in `gen/build.py`) added after the header `</nav>` on the 11 non-docs pages: `html/index.html`, `demo.html`, `demo-agents.html`, `pricing.html`, `about.html`, `gettingstarted.html`, `404.html` and the four `html/legal/*.html`. `js/site.js` already handled the button and every page already read `s2o-theme` in its head.
- `html/styles/styles.css`: `.docs .theme-toggle` and `.docs .site-nav` lost the `.docs` prefix, so the button sits between the tagline and the nav on every page, as in the docs. The rule that stacks the tagline under the logo now applies up to 440px (was 359px), so the button stays on the first header row on phones.
- Tested with Playwright from a local server: on all 11 pages and one docs page a click switches the background from white to `rgb(9, 15, 29)`, saves `s2o-theme`, and updates the aria-label. Header measured at 340, 390, 430, 460 and 800px: button on the first row, no horizontal overflow.
- Not checked: how the demo widget (`html/demo/demo.css`, built by ui1) looks when dark is forced by the button on a light-mode machine.
- State: not committed, not uploaded.

## 2026-10-05 — Search/followup behavior is now UI-only, not cloud config

- Server change (read from ../search2o and ../s2oserver worklogs): `SearchBehavior`, `FollowupBehavior`, `SearchOptionsModel` and the `search` system-config part are removed from the cloud; `/api/exec/search` returns only `{success, searchResults}`; no tag (or `""`) searches every tag (the old default-tag setting is gone).
- Dependency to the cloud config removed from the build: `docsrc/search/search-settings.html` no longer embeds `<!--fields:model:SearchOptionsModel-->` / `<!--enum:SearchBehavior-->` / `<!--enum:FollowupBehavior-->`. That was what made `gen/build.py` raise `KeyError('SearchOptionsModel')` and block prod push release 25 — the build now passes (146 pages). `gen/build.py` docstring example changed from `SearchBehavior` to `AgentExecResult`.
- `search-settings.html` repurposed (not deleted — slug/URL kept so inbound links hold) from an account-config page into a "Search behavior" page: search returns ranked matches; what an interface does with them is its own behavior; the GUI exposes it as a UI setting; a custom interface/bot decides for itself. TOC title and docs_links label changed "Search settings" → "Search behavior".
- Reframed everywhere else: `rest-api/search.html` (response drops the two fields; tag omitted = all tags), `chat-integrations/finding-an-agent.html` and `chat-integrations/ai-prompts.html` (bot decides; no account guidance in the response), `search/how-matching-works.html`, `search/describing-an-agent.html`, `search/tags.html` (no default-tag setting), `gui/search.html`, `skill-integration/finding-and-running-an-agent.html`. Removed "search settings" from the account-config lists in `security/data-privacy.html` and `system-management/users-and-roles.html`. Updated the unbuilt draft `content/chat_integration.md` to match.
- `gui/agents.html`: removed the "Search" subsection (it documented the removed Agents › Search cloud-config panel) and dropped "the search settings" from the lead. Where the UI setting now lives in the GUI is a ui1 detail I could not verify; flagged to Ram.
- Checked: no `searchBehavior`/`followupBehavior`/`SearchOptionsModel`/enum-value/"search settings" strings remain in docsrc or html/docs; no broken internal links on the touched pages.
- State: not committed, not uploaded.

## 2026-10-05 — Search behavior: documented as a per-user GUI setting

- Ram: the UI setting now lives under user settings in the GUI (client-side). Added it to `docsrc/gui/personal.html` Profile section, next to the theme, and reworded the "The bundled GUI" paragraph of `docsrc/search/search-settings.html` to call it a per-user preference under the profile (link to gui/personal.html), not account configuration. Docs rebuilt; links clean. Not committed, not uploaded.

## 2026-10-05 — Search quality page rewritten; no third match anywhere in docs

- `docsrc/search/search-quality.html` rewritten from `content/search_testing.md`: new "right agent first / among the first two" table, new "One answer or two" subsection and table, refusal 100% and 82–86% kept, speed updated to ~200ms (kept the end-to-end/US-East note), new "The numbers are likely lower than real use" subsection with the blind-judged as-marked/as-judged table, clean closing line. The entire "An experiment: letting Jev choose" section is removed — no Jev on the page.
- No third match, across all docs: changed "two or three"/"up to three"/"at most three"/"first three" to two in `search/how-matching-works.html`, `commands/search.html`, `rest-api/search.html`, `search/orchestrator.html`, `search/search-settings.html`, `gui/search.html`, `chat-integrations/finding-an-agent.html`, `chat-integrations/ai-prompts.html`, and the cited figures in `skill-integration/what-search2o-provides.html` (now "among the first two for 92.2%" and "92.3–97.4%"). The `search-results` figure in `gen/figures.py` box changed from "two or three" to "two". Unbuilt draft `content/chat_integration.md` updated to match.
- Left as true (not match counts): "three parts of the system", "three bundled protocols", validation "three stages", Slack "three seconds", "Build two or three agents" on getting-started, etc.
- Flagged to Ram: the source's "both are 100-agent catalogs" clause is inconsistent with its own table (the top catalog, a university, has 50 agents), so I used "about seven points apart" and dropped that clause.
- Checked: no Jev and no third-match phrasing left in docsrc or html/docs; build clean (146 pages).
- State: not committed, not uploaded.

## 2026-10-05 — Home page: diagram branches + enterprise "Separate environments" card

- (a) Architecture diagram (`#system-architecture` in `html/index.html`): the agent-server branch "LLMs/Prompts" is now "LLMs", and all four branches (LLMs, APIs, Databases, MCP) are plain text — the links to the profile docs pages are removed.
- (b) "Built for the enterprise" (`#platform`): the Reports card is replaced by "Separate environments" (layers icon). Body: one account per environment (dev/staging/prod); an agent names its profiles and the profiles carry the endpoints, so the same agent runs in each; links all five profile types (LLM, prompt, API, database, MCP) and `security/multiple-environments.html`. Wording checked against that page (one account per environment, profiles point to each environment's systems).
- The diagram's own cloud "Reports" part (Search / State / Reports) is untouched — the request was about the enterprise card only.
- Checked by screenshot at 1280px; branches confirmed link-free. Not committed, not uploaded.

## 2026-10-05 — Home "Separate environments" card shortened to match the others

- The card body was ~280 chars vs ~155-169 for the other enterprise cards. Rewrote it to ~150 chars, keeping all five profile links and the multiple-environments link: "Dev, staging and production run as separate accounts, each with its own LLM, prompt, API, database and MCP profiles pointing at that environment." Not committed, not uploaded.

## 2026-10-05 — Home enterprise card: "Separate environments" -> "Profiles"

- Ram: rename the card to "Profiles" and say how profiles keep the five things out of agent code, vary independently, and are tracked in the audit log (the enablements — environments, model standardization, restricting agent reach — don't fit the box). `html/index.html`: heading "Profiles"; body "An agent's LLM, prompt, API, database and MCP live in profiles, not its code. Each changes independently, and every change is in the audit log." Links: profiles section index and the audit log. Length ~140, in line with the other cards. Kept the layers icon. Not committed, not uploaded.

## 2026-10-05 — Profiles card: dropped "prompt" (prompt profile is optional)

- Ram: a prompt can be inline in the agent; the prompt profile is optional, so it does not belong in "live in profiles, not its code". `html/index.html` Profiles card now lists LLM, API, database and MCP. Not committed, not uploaded.

## 2026-10-05 — Profiles card: prompts back, as optional
- Ram: say "optionally prompts" rather than dropping them. Card now: "An agent's LLM, API, database, MCP and optionally its prompts live in profiles, not its code. Each changes independently, and every change is in the audit log." (169 chars). Not committed, not uploaded.

## 2026-10-05 — Architecture diagram width matched to the other diagrams
- `#system-architecture .howgrid` overrode the grid to `1.4fr 1fr` (gap 48), making the diagram 597px wide vs ~520 for the hero and framework diagrams, with wasted whitespace on the right. Changed to `1fr 1fr` (gap 64) like every other section; diagram is now 504px and the system branches sit next to the agent server. CSS-only, one line. Not committed, not uploaded.

## 2026-10-05 — Architecture diagram: actor boxes left-aligned
- `.arch-actors` was `justify-content: center`; changed to `flex-start` so the Users and Developers · Admins boxes sit at the org box's left edge (over the agent server), with the free space on the right. CSS-only, one line. Not committed, not uploaded.

## 2026-10-05 — Architecture section: gap/columns now identical to the framework section
- Correcting the previous change: I had set `#system-architecture .howgrid` to gap 64px, double the sibling framework section's 32px, leaving a big gap between the diagram and the demo. Set it to `minmax(0,1fr) minmax(0,1fr)` gap 32px — now measured identical to `#framework .fw-grid`: diagram 520, gap 32, demo (right box) 520 starting at the same x. CSS-only. Not committed, not uploaded.

## 2026-10-06 — Getting started: Run the server section rewritten
- `html/gettingstarted.html` step 3 now: the two start commands first (license key only, no vendor key in the command), then two bullets (Ollama/vLLM needs no key, create an LLM profile after sign-in; OpenAI/Anthropic/Gemini set one of the three keys before starting), then a "docs for other LLMs" link. The "Choose an LLM" / "Start the server" h3s are gone. Docs links stay relative. `.numbered ul/li` styles already existed, so no CSS change. Verified with a headless render. Not committed, not uploaded.
- Pre-existing, not touched: the two code cards in that step sit flush against each other (`.codecard` has no vertical margin); the gap only shows where two cards are consecutive.
- Follow-up: Ram added a sentence after the bullets; linked "secret names" to `docs/security/secret-vault.html#environment-variables` (the section that names the three vendor variables) and "LLM profiles" to `docs/profiles/llm-profiles.html`. Links relative.
- Step 4: "Enter the email you used in step 1" was easy to read as any email; now bold "same email you used to create your account in step 1" with the reason (a code only goes to that address).
- Moved "After you sign in: create an LLM profile" out of step 3 into step 5 (Get started) as its first paragraph. The remaining single bullet in step 3 became a paragraph.
- Step 3 paragraph sat flush under the PowerShell code card once the bullets became a paragraph (the list's li margin had been hiding it). Added `.numbered .codecard { margin-bottom: 14px; }`. This also spaces the two step 3 cards apart and the step 2 GitHub line from its card. Verified with a headless render.
