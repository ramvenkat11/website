# website - search2o.com and its documentation

Moved here from `s2oserver/docs/website` on 2026-08-30. Everything website related lives here:
the five site pages, the documentation source and generator, the built site, and the deploy
procedure. The full history of decisions made while this lived in s2oserver is in
`../s2oserver/CLAUDE.md` (search it for "website", "docs", "home page").

## Standing instructions
- POLITE, not curt (Ram, 2026-09-03, after a full-docs pass). Advice is offered, not ordered:
  "we would suggest", "it helps to", "is best kept", "please" for a real request. Bare commands
  ("Say so.", "Do not build against the figure.", "Tell people to compare the codes.") read as
  brusque and must be rephrased. This does NOT license filler or hedging - the sentences stay
  short and clear. Product FACTS stay firm ("ask is not allowed inside a for block"), and so do
  security rules ("must never appear in an agent definition"). Table cells and field glosses
  stay terse: that is a table, not a tone.
- After completing any task, update this file with what was done and what is next. Do it
  without asking, and commit ONLY this file (`git commit CLAUDE.md -m ...`) without mentioning it.
  Ram owns every other commit - never commit code or content; he reviews first.
- Narrate; never go silent for more than ~20 seconds. Say what a long step is before starting it.
- Tight scope: do what was asked, report related findings instead of fixing them uninvited.
- Cite files as `path/file.html:123` (Ram runs Claude in a JetBrains terminal).
- Ask before anything irreversible; deleting from the S3 bucket is irreversible.

## How Ram wants the writing (he judges every line)
Clear, simple English that communicates. One idea per sentence. At most two commas in a
sentence. Every line unambiguous: use the noun instead of "it", "one", "this", "they" unless the
referent is in the same clause ("describe each agent", never "describe each one"). No filler
("the workflows that matter"), no hedging, no grammar slips ("if you make grammar mistakes, I
will cry"). He cannot read long proposals on the console: apply the change, then summarise in a
few lines. When a figure misses twice, ask numbered questions about what it should communicate
instead of redrawing a third time.

Vocabulary: agent server, Search2o Cloud (or "the cloud"), the GUI, the controlled runtime.
NEVER "sandbox". NEVER "compile/compiles/compilation" - the one exception is the product name of
the configuration part, "Compile rules". Marketing copy never says "compile agents" either.

## State on 2026-09-05 (SOURCE AVAILABLE IS BACK; GitHub install)
Ram reversed 2026-09-01 again: the agent server is source available (still proprietary), repo
github.com/Search2o/agent-server, installed with pip install git+https://github.com/Search2o/
agent-server.git or git clone + pip install ./agent-server. PyPI IS GONE from the story - no
page may say PyPI. The repo has README.md (Ram's own, canonical wording: "source available and
proprietary... not open source", no PRs, CONTRIBUTING.md welcome items), LICENSE and
CONTRIBUTING.md. Changes: home hero pip chip -> ghost button "Install from GitHub" (repo
link); diagram server subtitle "Stateless · Python 3.12+" -> "Stateless · source available"
(fits, 0 overflow); gen/figures.py architecture node "stateless · pip install search2o" ->
"stateless · source available"; gettingstarted.html step 2 rewritten (codecard: git+ pip, or
clone + pip install ./agent-server; extras from-clone "./agent-server[postgres]"; dim licence
line; meta descriptions updated); registering-and-downloading.html rewritten (both install
forms, extras from-clone block noting the "search2o[postgres] @ git+..." form, Source section);
license.html rewritten (source available lead, repo + LICENSE + CONTRIBUTING links, no-PRs
paragraph, GUI/cloud/beta kept) - the old page ALSO had a broken licence-text link
(html/legal/ does not exist; text said ip/, href said legal/) - now links the repo LICENSE
blob; support.html PyPI line -> repo link; docs home Getting started card wording. Sweep for
PyPI/pip install search2o over docsrc/gen/html returns nothing.

## State on 2026-09-04/05 (FULL DOCS FACT AUDIT, 120 pages)
Ram: verify every line. Method: 9 fork auditors (7 died on a session limit; intro/getting-
started and search/development completed), the rest audited in the main loop against
../s2oserver, ../search2o (the agent server package IS at ~/IdeaProjects/search2o - launcher,
routers, execution, UI; use it for server-side facts) and content/*.md.
FIXED (all verified against code): positioning "search box" -> "search interface" (docs home,
what-is-search2o, introduction lead; LITERAL search-box uses stay); "operator rules" ->
"compile rules" (what-is-search2o); "under 300 milliseconds" -> "under a second"
(how-matching-works, matches home); docsBase row added to the-gui ui-config table (5th
setting, verified in package ui/index.html); "human in the loop" sample hyphenated
(ai-assist); variables.html reserved list gained onError (ReadOnlyVariable + explicit check);
THE SERVER-REPORTING FICTION HAD FOUR MORE INSTANCES beyond the two fixed earlier -
runtime/guardrails, misc/llm-adapters, security/controlled-runtime, gui/guardrails - all now
"written to the server's log"; gui/reports.html still claimed error detail shows "sample
queries" (removed - contradicted the 2026-09-03 privacy correction); license-rotation "three
ways" -> "two ways" (env var change fallout); encryption.html key-retention advice was wrong -
memories (1yr, Epoch.s365) and hosted secrets (life of secret) are encrypted under the same
named rotating keys, so "only the last three months of keys" is false; now states all three
lifetimes.
VERIFIED CORRECT (samples): restriction table == compiler prohibitedWhy exactly; onError only
on api/db/llm (FailsafeCommandModelBase); 20480 default; safe_pow exp<=64; pow=rewrite
shifts/matmul=deny defaults; memory 10 labels (maxMemoryLabelsPerAgent) / 25 per store /
1yr / LRU-retrieved eviction; db timeout default 30; ask reserved input "query"; state saved
only on success|ask; conversation TTL s90 refreshed on read+run, pinned off-clock;
notifications s90; sessions 60/720min, script token 60min; addUsers<=25; freeze sysadmin-only;
all 24+5 named REST endpoints exist (cloud api.py + package routers); stream types exactly
progress/trace/data/agent/noop/end for execAgent (draft type is validateDraftStream-only);
chat endpoints incl. /api/user/getConversation (Ram's f1ad8b6 fix) all real.
OPEN FOR RAM (do not fix without his call): (1) "three months" of execution records/reports
claimed in reports/index.html, gui/reports.html, data-privacy.html x2, docsrc/index.html card -
agent_executed has NO ttl in spannerschema and no window cap; records are kept indefinitely
today. Either the server gains the TTL or the docs drop the promise. (2) Ram's new
../search2o/README.md says SOURCE AVAILABLE (public source, no PRs, CONTRIBUTING.md) -
reversing 2026-09-01; docs license.html/registering still say only "proprietary, PyPI" with no
repository mention; if the reversal stands, those pages need his wording. (3) Unverifiable but
consistent: seeded profile names gpt5_mini/gpt_image/claude_haiku/gemini_flash/gemini_image
(operational data), ask-during-validation GUI behavior.

## State on 2026-09-04 (../search2o/README.md rewritten for PyPI)
The pip package repo is ../search2o (distinct from ../s2oserver, the cloud side). Its README
(pyproject readme=README.md, shown on PyPI) was stale: "source-available" (retired 2026-09-01),
a broken getting-started.html link (real page is gettingstarted.html), old vocabulary
("management UI", "tasks"), no LLM-key or docs pointers. Rewritten brief from the new
gettingstarted.html: what Search2o is + this package is the agent server, proprietary licence
note, register/getting-started + docs links, requirements, install + db extras one-liner,
licence env vars, start command, GUI at /ui. No registration form (points to the site).
Ram commits it. NOTE: the README's links target pages that are live only after Ram deploys -
the site is still the placeholder.

## State on 2026-09-04 (gettingstarted.html lightened, Ram's density pass)
Ram: too dense, remove empty words, hero repeated the steps, "your laptop is A GOOD place to
start" (not "the right place"). Hero lead is now one short line + the docs pointer (the .note
line is gone). Licence-key rules moved into a codecard (two export lines with a # comment);
the both/neither rule is a dim line. The colleagues/share-key guidance moved OUT of Run the
server INTO Bring your team (it duplicated that step). Demoted to .dim: db extras, Uvicorn
options, the openapi/docs/redoc URLs. The minimal-agent explainer is now a 3-bullet ul (new
.numbered ul/li rules in styles.css). Register text softened ("nothing is charged unless...",
"please store it").

## State on 2026-09-04 (gettingstarted.html rewritten SELF-SUFFICIENT + real registration form)
Ram: the page must let someone get started without the docs; content pulled from docsrc
(install extras, licence env vars, LLM keys, start command, GUI sign-in, the full first-agent
walkthrough with the minimal-agent JSON from your-first-agent.html, describe+search, team).
Eight steps now; hero note says "This page has everything you need to get started."
THE REAL REGISTRATION FORM is in (from content/register/prod_register.html, restyled to
.form-card): two steps against https://api.search2o.com (/reg1 email+name+account+password+
terms+hCaptcha sends a code; /reg2 code -> licence key SHOWN ONCE). hCaptcha script in the
page head; sitekey ff281746-...; hCaptcha warns on localhost, works on the real domain. New
CSS: .form-card .hint/.terms/.h-captcha, .reg-out ok/err, .reg-key. The old mailto form and
its script are gone. FACT CORRECTED BY THE FORM: the licence key is NOT emailed - it is shown
once at the end of registration; registering-and-downloading.html updated too.
GUI URL CORRECTED AGAIN (Ram): the GUI is at BASE_URL/ui, NOT the root - his earlier md said
root and I had changed the docs to root; now /ui everywhere (the-gui.html lead+sign-in,
running-the-server.html list, agent-servers.html table, gettingstarted.html). The agent JSON
block was brace-walk verified (string-aware; depth 0) and neither codecard h-scrolls.

## State on 2026-09-04 (group REORDER, agreed with Ram)
Final order: Variables / Flow control / LLM interaction / External systems / Deep agents /
Human-in-the-loop / Agent output / Agent termination / Observability. Rationale: language
basics, then the work groups LLM-first (Ram's swap of my suggestion), then how an agent
finishes, Observability last as the crosscutting aid. Reordered in the three places that
must stay in step: agentschema.py commandGroups (page headings + GUI editor), gen/toc.py
command entries (sidebar + prev/next), and the home page .cg rows. Rebuilt and verified.

## State on 2026-09-04 (two more group renames)
Progress and diagnostics -> Observability; Call external systems -> External systems. Renamed
in all three places at once: ../s2oserver/models/agentschema.py (uncommitted, Ram's),
gen/toc.py, and the home page .cg-l labels. Rebuilt; no inbound links to the changed anchors.
Group names now: Variables / Flow control / Observability / Agent termination / External
systems / LLM interaction / Deep agents / Human-in-the-loop / Agent output.

## State on 2026-09-04 (command groups renamed to the home page names)
Renamed in ../s2oserver/models/agentschema.py commandGroups (RAM'S REPO - HE COMMITS): Output
progress information -> Progress and diagnostics, Terminate agent -> Agent termination, Engage
with LLM -> LLM interaction, Human in the loop -> Human-in-the-loop. No server test asserts
the titles. Website: gen/toc.py sidebar groups renamed to match (the third tuple element),
ai-assist.html's bold "Human in the loop" hyphenated, docs rebuilt (120 pages) - schema drives
the page headings, toc drives the sidebar, and the two must be renamed TOGETHER. No inbound
links existed to the changed heading anchors (#output-progress-information etc.).
SIDEBAR GROUPS ARE NO LONGER UPPERCASE (Ram, mid-task): uppercase could not fit "Progress and
diagnostics" in the 166px column at any size >=10.5px, and Ram then ruled out all-caps
entirely. .sidebar li.sb-group is now 12.5px w800 mixed case, no text-transform, no
letter-spacing, nowrap kept; all nine labels measure ok.

## State on 2026-09-04 (about page wording pass, Ram's 19-row table)
13 edits applied verbatim from his Suggested column to html/about.html (the Keep/dash rows
untouched): "retrieves information", "programs that combine", "run safely", "accommodate
change / evolve", the tightened implies-more-than-search list, "without depending on existing
application infrastructure", "in their environment", "publish them to", "get started quickly",
"Search2o was founded by" (LinkedIn link preserved), "That experience includes systems built
for..." with "over many years" dropped, "Search2o Cloud runs on Google Cloud", "product
questions". The em dash in the file is &mdash; - a literal — in a match string finds nothing.
Meta/og descriptions checked: unaffected by these edits, still accurate.

## State on 2026-09-04 (home page wording pass, Ram's 19-row table)
All applied to html/index.html verbatim from his Better column (16 replacements; three rows
shared lines): hero "runs it", "A user enters... browser or chat application", "Search matches
the request", agent-server split into two sentences, "returns matches in under a second",
group labels Progress and diagnostics / Agent termination / LLM interaction /
Human-in-the-loop, Gemini models sentence + "Other LLMs require only a small adapter class",
"required integration endpoints", "The agent editor... contextual help", "Validation runs
produce a full trace", "Profiles keep LLM, prompt, API, database, and MCP server configuration
out of agent code", "reports show trends" + "corresponding agent or user", band line "Search2o
license and one LLM API key", meta+og "runs the agent". OPEN INCONSISTENCY: the docs and the
GUI editor still use the server schema's group names (Output progress information / Terminate
agent / Engage with LLM / Human in the loop) - renaming those means editing AgentSchema
commandGroups in ../s2oserver and rebuilding; Ram has not asked.

## State on 2026-09-04 (home get-started band slimmed, KEPT)
Ram: too many getting-started surfaces; chose the slim-band option over full removal and kept
it after seeing both themes. The four .bandsteps cards (a compressed copy of
gettingstarted.html) are gone from html/index.html; the band is kicker + "From install to your
first search" + one line + the two buttons (378px). All .bandsteps CSS removed from styles.css
(the main block and the two responsive rules; .cardgrid/.form-grid selector kept). Band
measures 378px before and after the CSS removal - nothing else depended on it.

## State on 2026-09-04, later still ("What a server reports" was FICTION)
The old agent-servers.html section "What a server reports" (servers report allowlist/adapter
failures back and the Agent servers GUI page shows them) described a feature that DOES NOT
EXIST - errors are logged locally on the server and never appear in the GUI. Ram caught it
after the merge carried the section over verbatim. Now: agent-servers.html has "Startup
errors" (logged locally, do not appear in the GUI) and gui/operations.html lost its
"page also shows what each server reported" sentence. LESSON: a pre-existing docs section is
NOT evidence a feature exists - inherited claims need the same verification as new ones.
Also: running-the-server.html:29 now says the UI/docs paths can be REMOVED (server with no
GUI, no interactive API docs), matching agent-servers "What a configuration sets".

## State on 2026-09-04, later (server-process MERGED into agent-servers)
Ram: one topic, not two. server-process.html is gone from toc.py; its content is the top of
system-management/agent-servers.html - lead (FastAPI/Uvicorn, one worker, laptop-to-LB), The
command line (refused options x-code block), What a server serves (URL table), then the
existing Named configurations / What a configuration sets / What a server reports; "Keeping
servers consistent" was folded into a new "Running many servers" (stateless, containerize, no
count limit, drift rules). 120 pages. running-the-server.html links Agent servers again.
LEFTOVER FOR RAM: Ram declined the rm, so docsrc/system-management/server-process.html and
html/docs/system-management/server-process.html still sit on disk, orphaned - not in toc, no
inbound links; the built one would serve as a stale URL if a deploy ever syncs it. Delete both
or say the word.

## State on 2026-09-04 (server topic, getting-started resync, licence env vars)
LIVE SITE IS A PLACEHOLDER (2026-09-03): Ram had the whole S3 bucket emptied and replaced with
one "We'll be back soon." index.html; STANDING RULE: never s3-sync or invalidate again until he
explicitly says he is ready - every change stays local. All work below is local only.
Docs now 121 pages. From content/server.md: NEW page system-management/server-process.html
("The server process", placed before Agent servers) - FastAPI/Uvicorn, args pass through, the
refused options (--reload family/--factory/--workers, as an x-code block: inline code wraps at
hyphens and broke --reload-delay mid-token), default URLs table, stateless scale-out, no server
count limit. From Ram's content/gettingstarted.md edits: LICENSE ENV VARS CHANGED -
SEARCH2O_LICENSE (env:/file: forms) is GONE; now SEARCH2O_LICENSE_KEY or _KEY_FILE, both set =
error, neither/empty = exit. license-key.html rewritten; running-the-server.html,
agent-servers.html (config suffix example), license-rotation.html updated. GUI IS AT THE ROOT
now (http://127.0.0.1:9020, not /ui/index.html) - the-gui.html and running-the-server.html
updated. Also added: open-beta welcome (registering-and-downloading), vendors-not-limited link
to llm-adapters, share-key/common-place deployment note, APIs/DBs-reachable-from-server note.
The agent server package code is NOT in ../s2oserver (that checkout is the cloud side), so
content/*.md is the only verifiable source for launcher mechanics.
Also on 2026-09-04: usage-limits.html REPLACED from content/usage_limits.md (service levels
free/eval/paid per ServiceLevel enum; numbers deliberately unpublished; daily on the UTC day;
contact us to raise) - the old per-operation table with 10/day-100/month figures is gone, and
asking-the-docs.html was cleaned of those figures. NEW page
support-licensing/asking-the-docs.html ("Asking the docs", from api.py docsQuestion +
docsapi/docsquestion.py: answers written only from doc pages, no conversation, not support);
linked from gui/personal.html and usage-limits.

## State on 2026-09-03/04 (earlier this session)
Naming sweep: agent names and tags are UNDERSCORE now (content/naming_rules.md is the final
rule set; hr_policy, order_lookup, docs_rag, it_helpdesk, orders_db, hr_internal, eu_support
across docsrc, gen/figures.py and html/index.html; figure ids like report-cost keep hyphens).
tags.html Shape line says underscores; mcp-servers.html gained the MCP naming rule (letters and
digits only, <=16, the mcp_{server}_{tool} reason); var.html and profiles/overview.html now
state "ends with a letter or a digit". "command type" -> "command name" (structure.html:23).
Ram added _NAME_TYPES to gen/build.py: field tables render agent name/profile name/tag/name.
Docs command-reference page: group h3s carry class=cmdgroup-title (build.py:225), styled 21px
w800 in docs.css; SIDEBAR .sb-group relabeled 11.5px w800 var(--ink) ls .03em nowrap (was
10.5px faint - letter-spacing .09em was what wrapped "Call external systems", not the size).
Home page code card: "main" carries "// Execution begins here" (index.html:295).
gettingstarted.html: hero note line "The steps below are the outline..." linking
docs/getting-started/index.html (.page-hero .note, 70ch - ch scales with font size, 62ch at
15.5px was 606px vs the lead's 684px and left a one-word widow); step 3 links license-key.html;
step 7 is "Read the docs, or ask a question" (GUI docs icon + ask-the-docs, then the web URL).
BROWSER CACHE TRAP: the IDE server (localhost:63342) and headless checks both served stale
styles.css/docs.css repeatedly - always hard-reload and verify computed styles before
concluding a CSS change did not take.

## Layout

    html/            the shipped site: index.html, gettingstarted.html, pricing.html, about.html,
                     styles.css, site.js, logo.png, favicon.svg, docs/ (GENERATED - never edit)
    docsrc/          documentation source, one directory per section, one html body per page
    gen/toc.py       the section/page tree (slug, title[, command group]) - the sidebar, the
                     cards, prev/next and the summaries generator all read it
    gen/build.py     docsrc + toc -> html/docs. Reads the MODELS of ../s2oserver (S2OSERVER env
                     var overrides the path) for every generated table
    gen/figures.py   the inline-SVG figures (theme-aware via CSS variables)
    gen/check_examples.py  validates every jsonc example against the agent models
    content/         the original markdown the site pages were written from (read-only history)
    website_deploy.md  the deploy procedure, in full

## Build, check, deploy

    cd ~/IdeaProjects/website
    ../s2oserver/.venv/bin/python gen/build.py            # rebuild html/docs (107 pages)
    ../s2oserver/.venv/bin/python gen/check_examples.py   # every jsonc example must validate
    cd html && aws s3 sync . s3://search2o.com/ --exclude logo.svg --exclude ".DS_Store" \
        --exclude "*/.DS_Store" --acl public-read
    aws cloudfront create-invalidation --distribution-id E330RKTBY31L8X --paths "/docs/*"   # or "/*"

`sync` never deletes: a page removed from the build must be removed from the bucket with
`aws s3 rm` (recursive for a directory), or the old URL keeps serving. Verify with curl after
the invalidation reports Completed (about a minute). The site pages under html/ are edited by
hand; a single page can be pushed with `aws s3 cp ... --acl public-read --content-type text/html`.

The topic summaries the in-app docs search embeds are generated by
`../s2oserver/maintenance/docs_create.py` (it imports gen/build.py from THIS project; run it from
s2oserver with `environ=test PYTHONPATH=.`). It never deletes a file for a page that no longer
exists - remove stale JSON files by hand.

## Placeholders in docsrc pages (expanded by build.py)

    <!--pages:cards-->                  the section's page cards (section index pages)
    <!--fields:command:api-->           a command's field table, from the command model
    <!--fields:model:LlmModel-->        a model's field table
    <!--enum:SearchBehavior-->          enum members with their `# comments` as the meaning
    <!--commands:groups-->              the 23 commands by group
    <!--figure:config-sync-->           an SVG figure from gen/figures.py
    <!--shot:name|width|alt|caption-->  html/docs/img/name-light.png + name-dark.png, one shown
                                        per theme
    <x-code lang="jsonc" [nocheck] [title="..."]>...</x-code>   a code block; jsonc blocks are
                                        validated unless nocheck

Headings get ids from their text (`add_heading_ids`), so `guardrails.html#allowlist` links to the
"Allowlist" heading. Section index pages hold only a lead and the cards placeholder.

## Traps that cost time
- The figure checker: render every figure in headless Chrome and compare each text's getBBox
  against the canvas and its box - a 31-character line at 11.5px is ~166px and eyeballing misses
  a 6px overrun. Headless Chrome here renders the DARK theme; force `<html data-theme="light">`
  for the light one. (The script lived in a session scratchpad; rebuild it from this description.)
- `table.fields td:first-child` is nowrap; a table with long first-column text needs
  `class="fields data"`, which wraps that column and shows a `<small>` detail line.
- A regex that prefixes `../` to links must skip the depth-0 docs home (docsrc/index.html).
- A build that reports "missing sources" means toc.py names a page that docsrc lacks.
- Old GUI screenshots are taken from the agent server on :9020 on the Acme Corp account, in
  both themes (theme comes from the saved profile, not localStorage). Details in s2oserver's
  CLAUDE.md under "GUI pages back to screenshots".
- macOS has no `timeout`; the Bash cwd persists between calls - always cd explicitly.
- Before running build.py, check `git status --porcelain html/docs`: the build overwrites
  html/docs wholesale, and a hand edit sitting there uncommitted would be lost.

## Site facts
- Tagline "Search that executes." is DECIDED; do not re-raise. Hero lines are factual statements
  of what alternatives cannot claim, no lists, no filler.
- Footer: brand line "Search that executes.", bottom-right the platform sentence; no Support
  link anywhere; Contact goes to about.html#contact (the support page was folded into About).
- Dark mode: tokens on :root, the dark set emitted twice (data-theme and prefers-color-scheme);
  Inter is loaded at static weights 400-800 only.
- The "Why Search2o" page is agreed in outline but NOT built. The encrypted description
  change it waited on landed on 2026-08-30; the outline and the exact security wording are in
  s2oserver's CLAUDE.md.
- Decided 2026-08-30: competitors ARE named. html/why.html is the hub (pillars, stat strip,
  security wording, honest boundary) ending in one card per competitor; html/vs/<name>.html is
  one standalone ad-landing subpage per competitor (own verdict hero, framing paragraph,
  sentence-cell table, CTA), starting with Skills.md and LangChain/LangServe. Vs pages are not
  in the nav. This SUPERSEDES the s2oserver note "categories, never vendor names".
- 2026-08-30, later: Ram chose ONE comparison page instead of per-competitor subpages.
  html/compare.html is built from content/compare.md (three framing sections + a 24-row
  4-column .vs-table). "Compare" is in the nav of all site pages AND in the docs nav
  (gen/build.py header template; docs rebuilt). The .vs-table/.verdict CSS at the end of
  styles.css is tokens-only. Both themes verified by headless-Chrome screenshots.
  html/vs/skills.html and html/vs/langchain.html remain as UNUSED, UNTRACKED skeletons -
  nothing links to them; delete or keep is Ram's call (kept for possible ad-landing variants).
  Why Search2o stays a separate future page on the 2026-08-28 outline. Page titles:
  .page-hero h1 is clamp(22px, 2.4vw, 28px) weight 700 on every inner page (Ram wanted titles
  small and quiet); .page-body .section-head is 26px with 64px above (the "Side by side" head).
  The home hero keeps its own size. Not deployed.

## State on 2026-09-03 (privacy corrections)
Three facts corrected in the docs. (1) The error report NO LONGER shows queries - the "who can
read it" cell for the user's query is now "Only the user who typed it", and the claims on
reports/errors.html ("a sample of the queries that produced the error") and reports/index.html
("Only the error reports show queries") are gone. (2) Conversation state reads "Only the user
whose conversation it is; the account's agent servers decrypt it to answer that user's next
request". (3) The cloud provider is named: Search2o Cloud runs on Google Cloud Platform, and
Google is named as the infrastructure provider - the about page already said GCP.
support-licensing/support.html still asks a customer to include the query when reporting a
problem; that is the customer sharing it themselves, so it stands.

## State on 2026-09-03 (chat docs resynced)
content/chat_integration.md was updated and the docs were brought back in line.
SCOPE STATEMENT added at Ram's request, politely: the section index lead and a renamed
overview section "What Search2o provides, and what you build" say Search2o provides the
integration POINTS (API, tokens, connect flow) and not the integration itself, that the bot is
written and run by the customer because each company's platform, network and approval rules
differ, and that we are happy to help - Help icon or info@search2o.com.
New material: finding-an-agent now says searchBehavior and followupBehavior are GUIDANCE, not
a rule - a bot may always run the top match for a more conversational feel, at the cost of
never offering a choice when the match is uncertain. "Letting the person choose" (the four
picker rules) added to the same page;
the Slack Answer-button step (a modal needs a click, a message event carries no trigger_id)
added to running-an-agent; the Slow answers section fully rewritten (per-vendor ack windows,
do not build against the figure, per-application ways to send the later message, and reuse the
placeholder when a conversation turns out to have expired); one more check on the ai-prompts
page about Slack modals.
The four prompt blocks are now GENERATED from content/chat_integration.md and verified
byte-identical - resync them from the source rather than editing the page by hand.

## State on 2026-09-02 (single sign-on page)
New page system-management/single-sign-on.html, directly below Authentication. 119 pages.
Rewritten POLITE at Ram's request - this page states no
commitments and gives no orders. "We expect to support SAML 2.0 and OpenID Connect", "we would
be glad to know", "we would also welcome a pilot", "we intend to keep roles in Search2o".
Headings are "What we expect to support", "We would like to hear from you", "What we expect to
keep the same". No dates anywhere. The
authentication page's lead now links to it instead of saying "will be added in a future
release"; the chat integrations token page links to it too; section lead and docs home card
updated. content/comingsoon.md lists more unbuilt work (passwordless, email code, fob key) -
NOT written up, nobody asked.

## State on 2026-09-02 (title-line alignment)
NEW ALIGNMENT POLICY from Ram, superseding the h2-anchor pass of 2026-08-31: every right-side
picture's TOP aligns with the section's BIG TITLE LINE glyph top - the h1 "Search that
executes." in the hero, the h2 elsewhere. Measured deltas before: hero -89 (the demo hung at
eyebrow level under align-items center), how +5, example +2, search -16, framework -17,
reports -5 (the old "0" for search/framework was a measurement artifact: threshold 60 missed
the card border at L48; use threshold 45 for card edges). Now: .hero-grid is align-items start
with .hero-grid .demo margin-top 75px; .howgrid last-child 2px; shared split rule 36px;
.convo-wrap 37px; .howgrid last-child 37px; #reports .split last-child 36px; shared split
rule 36px. All six measure delta 0.
MEASUREMENT: a brightness threshold does NOT find a card's top edge - the arch card's faint
border and big soft shadow fooled it, so I reported "aligned" when the diagram sat 35px HIGH
and Ram saw no movement. Correct detector: for each row compare pixels against that row's page
background (abs diff > 4) across the card's x-range minus 30px of rounded corner, and take the
first row where 60% differ. Verify by drawing a red guide line at the title glyph top on a crop
and LOOKING. True deltas before the fix were how -35, example -19, reports -11, search 0,
framework 0. Diagram links went 86 -> 51 to keep the how-it-works columns ending level (1px).
The hero demo was also shortened at Ram's request: the streamed line lost "ready for your
review." and .demo-form is now ONE flex row (question, options, Submit), so the panel ends
7px below the left column instead of hanging.
REPORTS IS THE ONE EXCEPTION (Ram): #reports .split is align-items center with no top offset -
a two-line caption beside a tall 2x2 thumbnail grid reads better centred, and the title-line
rule does not apply there. Example workflow keeps the rule and hangs ~200px below its left
column; its transcript card is simply taller. Every other section measures delta 0.

## State on 2026-09-02 (home page reflects chat)
Home page updated for chat integrations, per Ram's guidelines plus judgment. Hero def now ends
"behind one search interface" (was "one search box"; "one" kept - the single entry point is the
point). Diagram: the clients chip row was WRONG - the link's top arrowhead pointed at a loose chip
row, and Ram had already ruled that arrows cannot end nowhere. The chips are gone; the link
label now has a second fainter line, "search interface / from a browser or a chat app"
(.arch-lbl em), so the arrow runs Users <-> organization with both ends on nodes. Links 86px,
gap 0. STANDING RULE: every arrowhead in this diagram must land on a node's edge - check each
end whenever an element is added or removed near a link. Platform cards: Profiles card REPLACED by Chat integrations (bubble
icon; Slack/Teams/Google Chat, bot connects via the API, no password handed over, prompts write
most of the bot); Agent development card lost the Notifications sentence and gained "Profiles
keep LLMs, prompts, APIs, databases and MCP servers out of agent code". Extras: API card says
"build your own UI or chat bot", and how-it-works step 1 opens "User types a request from a
browser or a chat application." Footer sentence and meta description already said "search
interface" and were left alone.

## State on 2026-09-02 (chat integrations)
NEW DOCS SECTION "Chat integrations", placed after REST API in toc.py, written from
content/chat_integration.md. 118 pages now (was 109). Eight pages: overview (what the bot does,
what to decide first), connecting-a-person (pasted token vs the connect flow, the short code,
the approval-page address setting), integration-tokens (capability limits, expiry, revocation,
SSO), finding-an-agent (search plus the behaviour table), running-an-agent (execAgent, threads
vs conversations, the four result cases, asks, slow answers), showing-the-answer (text, images,
HTML), chat-applications (Slack, Teams, Google Chat), ai-prompts (the reference prompt, one
prompt per chat application, and the checks). Docs home card added.
TRAP: build.py escapes x-code contents itself ("sources can hold the raw text"), so NEVER
pre-escape a code block - the first version rendered &quot; and &lt;token&gt; literally. An
HTML entity inside x-code is always a bug; scan for /&[a-z]+;/ inside code blocks.

## State on 2026-09-02 (hero demo)
The hero demo's last beat was "Context encrypted and stored for follow-ups" with a STATE tag.
Ram: the hero picture is not about implementation detail, but do not just delete the row and
leave it flat. My first replacement was WRONG twice and Ram caught both: it sent the
answer to an ask to a DIFFERENT agent (an ask always resumes the SAME agent, docsrc/commands/
ask.html), and it invented a "Signature agent" that would somehow know when a named person
signed. Correct version, checked against ask.html and gui/search.html: the streamed output ends
without a question, then an ASK row shows the FORM that an ask puts in the conversation
(message plus a chooseOne, .demo-form/.demo-tag.ask), then a RUN row shows the OUTCOME only,
"Sent the renewal to Acme for signature". Two further corrections from Ram: the ask form has
ONE submit (the options are a chooseOne with a default selected, not two buttons - see
AskInputModel), and "the same agent carried on where it paused" was implementation detail of
exactly the kind he had just asked me to remove. RULE FOR THIS PICTURE: every line is something
the customer gets, never how the system does it. The Submit is a QUIET outlined pill, not a
filled button - the hero demo must never pull attention from the hero bullets and Get started. New stage-5 delay 2.75s. LESSON: verify
product mechanics in docsrc and the models before drawing them.

## State on 2026-09-01 (licensing)
GITHUB AND SOURCE-AVAILABLE ARE GONE (Ram: the code is proprietary and ships only on PyPI; it
will never be on GitHub). Rewrote docsrc/support-licensing/license.html (proprietary licence,
no repository line, no promise to publish the GUI source), dropped the repository sentence from
support.html, rewrote the PyPI paragraph in getting-started/registering-and-downloading.html,
changed the merging page's analogy from "systems such as GitHub" to "a version control system",
dropped "their source is available" from misc/llm-adapters.html, and removed "source-available"
from the home page step 2 and the diagram subtitle (now "Stateless - Python 3.12+" again).
The toc title is now just "License", and html/gettingstarted.html points at it. The two stale
generated files html/docs/misc/license.html and html/docs/system-management/support.html were
finally deleted with git rm - they were the last GitHub mentions in the tree. content/gettingstarted.md was the last
mention anywhere ("The source is available on github. To build from source...") and Ram asked
on 2026-09-03 for it to go too, so content/ is no longer treated as untouchable when it states
something that is no longer true; that line now reads "The agent server is published on PyPI
under a proprietary license." A sweep of html/, docsrc/, gen/ and content/ for
github|source-available|source is available|build from source|open source returns NOTHING. Sweep for
github|source-available|source is available now returns nothing under html/, docsrc/ and gen/.

## State on 2026-09-01 (about page)
BRAND SPELLING (Ram, saved to memory): the name renders exactly as Search2o - capital S,
lowercase o - and must never be uppercased. The About kicker read "About Search2o" and CSS
text-transform turned it into "SEARCH2O". Forcing mixed case ("ABOUT Search2o") was wrong too:
the kicker is now the plain label "About", matching every other kicker on the site (Pricing,
Getting started, How it works), which keeps the brand out of uppercase contexts entirely.
SEARCH2O_LICENSE stays: an environment variable name is a constant, not the product name.
Also fixed: about.html's meta and og descriptions still described the deleted "opinionated
approach" copy after the rewrite - always update a page's meta when its body is rewritten.

about.html top rewritten from Ram's text, twice. "An opinionated approach" and the four old
prose paragraphs are GONE. Final: h1 "Rethinking search", the traditional-search-versus-
executables paragraph with the bolded question, the quoteblock "That is <hl>search that
executes</hl>.", then four paragraphs - agents ARE the executables and may use LLMs to modify
their own workflow; what an enterprise needs (safe execution, enterprise calls, interactivity,
a changing agent set); what that implies beyond search (framework, runtime, publishing model,
conversations, administration, end-user interface); the hybrid cloud architecture (assumes
nothing about existing infrastructure, administrators run only stateless agent servers,
encryption covers queries, conversations, short- and long-term memories and agent
descriptions); and how developers and users meet - users start on day one because they already
understand search. The old quoteblock
"Search is how users consume agents." is retired. Ram had already edited the founder line to
link his name and had added the GCP hosting line.

## State on 2026-09-01 (later)
COMPARE PAGE REMOVED at Ram's instruction - "not worth it at this stage and it confuses what
Search2o is". html/compare.html deleted with git rm (recoverable), the Compare nav link taken
out of the four site pages and of the gen/build.py docs template, and the compare-only CSS
(.vs-table, .page-hero .verdict) removed. .tablewrap STAYS - 48 docs pages use it. Docs rebuilt:
109 pages, 32 examples valid. html/vs/skills.html and html/vs/langchain.html were
deleted with git rm as well. KEPT: content/compare_table.csv, Ram's edited table - the material
is worth harvesting for the Why Search2o page, stated positively and naming nobody.
POSITIONING (Ram, 2026-09-01): Search2o is NOT positioned against agent frameworks, so the
buyer does not ask "why not LangChain" - a platform is not compared to a library. The real
alternatives are a vendor suite the customer already owns and building a portal in-house, and
the real objection is build versus buy. Sitting beside LangChain in a table implied Search2o
was the same kind of thing, which is the deeper reason the compare page was wrong.
The Why Search2o page from the 2026-08-28 outline is unaffected and still unbuilt.

## State on 2026-09-01
about.html Company section rewritten from Ram's text: founder line naming Ram Venkat with
https://www.linkedin.com/in/ramv1, the enterprise/government provenance paragraph, and the
open-beta operations paragraph. The name filled Ram's "[Your Name]" placeholder from his git
identity - HE MUST CONFIRM the spelling he wants shown publicly.
Agent framework section: the code card carries Ram's own // comments, styled by a new .tk-com
token. VERIFY THE CODE BLOCK MECHANICALLY: strip the tk-* spans, unescape,
and walk the brace depth (ignoring braces inside string literals) - "prompt" sat at indent 5
instead of 8 and the comments at 12 instead of 10 for several renders and I never noticed,
because a syntax-coloured block reads as correct at a glance. His two long comments are split
across three // lines each so no line runs past the card
(furthest text pixel 1112 vs card edge 1168) - never let a code line overflow, the pre scrolls
horizontally and hides it. The wrap added 88px, paid for by .cmdgroups gap 9px -> 20px in the
left column; both columns now end on the same pixel. DECIDED by Ram, do not re-raise: headings, lead
copy and the file bar say JSON because JSON is the marketable term; JSONC is only JSON plus
comments, so it is mentioned casually in the code comment and nowhere else.
Also repaired html/gettingstarted.html:86, whose "License and source" link still pointed at
docs/misc/license.html after the Support and licensing docs move (my regression). No other
site page referenced a moved docs page.

## State on 2026-08-31 (continued)
Docs: 109 pages. New page system-management/usage-limits.html written from
../s2oserver/docs/usage_limits.md (toc, section lead and home card updated; built and checked).
SIMPLIFIED per Ram: JSON responses belong only in the REST API section; the page now says only
that limits exist and what the limits are (table + three short sections; the 429 shape,
resetAt, wording examples, when-a-call-counts detail and the Accuracy section were cut).
Table is ONE ROW PER OPERATION with the windows as columns (per developer a day / a month /
whole account a day, em dash where none) - Ram: never repeat a label down a table's rows.
Deliberately left out from the start: the deleted-and-re-added-user fresh allowance, the
removed per-second rate limiter and its planned replacement, and everything under "Internal".
docsQuestion is LIVE again (api.py:987 with UsageLimits checks) despite the 2026-08-28
going-away note in s2oserver's CLAUDE.md - the page documents documentation questions.
Deploy adds the new page (sync covers adds) and needs the summaries regenerated.

## State on 2026-08-31
Docs: 108 pages in 15 sections. New LAST section "Support and licensing"
(docsrc/support-licensing/): system-management/support.html and misc/license.html moved there;
toc.py, both old section leads, the docs home cards and the two inbound links updated. NOT
deployed. Deploy needs: aws s3 rm of docs/system-management/support.html and
docs/misc/license.html (Ram declined the local rm of the stale copies in html/docs too - remove
before or during deploy); regenerate the in-app summaries with s2oserver docs_create.py and
delete the two stale JSON files by hand. compare.html content is final per Ram's csv + review.
Home how-it-works diagram: the users link is now bidirectional (class "two"; the old one-way
arrow had no rationale - results stream back), and an "Agent framework / runs your agents" box
sits left inside the agent-server node with the chips beside it (.arch-inner/.arch-fw CSS).
That attempt was REVERTED (Ram: the framework must appear early, it is a central theme; the
arrow fix stayed). 2026-09-01: Ram REPLACED all three hero points with his own text -
"A structured JSON/Python framework for rapidly creating agents with AI assistance" (braces
icon), "An agent server that executes them in a controlled runtime" (shield icon), "A complete
system for developing, publishing, discovering, and using agents across your enterprise"
(layers icon). The framework is now named in point 1. The subject phrase of each point is bold:
"A structured JSON/Python framework", "An agent server", "A complete system". (Ram's rule, saved to memory: never "The ..." on a
concept's first mention - indefinite article or possessive.)
How-it-works: the four steps are Ram's own text (2026-09-01) and are now named after the PARTS
of the system, not actions - Search interface, Agent server, Agent framework, Search2o Cloud.
In the diagram the Agent framework box WRAPS the four chips inside the server node (.arch-fw
contains .arch-chips) - Ram chose chips-inside over box-beside and bar-above. The users link is now labelled "search
interface" (was "search & results") so the diagram carries all four part names; the two-way
arrow already conveys that results come back. A caption under the Users pill was tried and
rejected - two labels in the same spot read as clutter.
Diagram restructured 2026-09-01 (Ram: congested, and it may be taller to match the steps).
Nesting went from four levels to two, then the chips moved AGAIN (Ram): LLMs/APIs/Databases/
Tools now form a SECOND COLUMN beside the agent server (.arch-row, .arch-sys), joined by a
fan-out connector - a stub from the server (.arch-hlink, labelled "calls") meets a vertical
trunk (.arch-sys::before) and one arrow branches into each chip (.arch-branch::before/::after).
Ram chose the fan-out from four options after rejecting an arrow that ended in empty space:
an arrow must land on something. They are orthogonal to the vertical spine
users -> agent server -> cloud, so they must not sit on it. The framework box is a label bar
only, and the server subtitle is "Stateless - source-available" (Python 3.12+ dropped: the
narrower column wrapped it). The cloud node holds exactly two boxes, Search and
Encrypted state, drawn like the Agent framework box inside the server (.arch-parts/.arch-part):
title on top, boxes below, full width. Configuration and Reports were tried as fillers and
REMOVED - nothing may appear in the picture that the steps text does not discuss. The "calls"
label on the fan-out is gone too (obvious from the arrows). Link heights 46->58
(42 for the short one) and org padding 16/14 give the height. Both columns now measure delta
0 at the top and 2px at the bottom. A stacked-card "cluster" effect on the server was tried
and removed - it read as a stray outline, not as several instances.
Column alignment policy (my recommendation, Ram asked for one): .howgrid, .convo-wrap and
.split are align-items start; the reports section's div carries class "split centered" and
.split.centered recenters it (short caption beside tall thumbnails); the hero stays centered.
CONSISTENCY PASS (Ram: one system, stop making him point things out). The page now has two
section families. Banner sections (Platform, Get-started band): full-width base h2 (36px).
Column sections (How it works, Example, Search, Framework, Reports): kicker + 22px h2 INSIDE
the left column (.howgrid h2/.convo-wrap h2/.split h2; inline sizes removed; the how-it-works
section-head moved into its left column), and the picture's top edge aligns with the h2 glyph
top everywhere: margin-top 20px on the grid's last child, 7px for .howgrid (its section-head
spacing differs). Reports lost its centered exception. Hero stays special. Measured deltas
0/+3/-1/-1/-5 px. Lesson: verify alignment by measuring edge rows with PIL in the full-res
screenshot, never by eyeballing a downscaled crop; segment sections by background transitions
before measuring. Hero
def line stays simple (Ram: do not overload it); three hero points is fixed; section order is
fine as is.

## State on 2026-08-30
Docs: 107 pages in 13 sections (Introduction, Getting started, Agent definition, Agent
execution, Command reference, Search, Development process, Agent runtime, Profiles, Reports,
System management, Security and privacy, GUI pages, REST API, Miscellaneous). Everything built,
deployed and verified live.

Later on 2026-08-30: documented three server changes - memory text stored encrypted on the
cloud with the label in plain form, descriptors kept only in encrypted form, draft validation
moved from /api/exec to /api/dev. Edited security/encryption.html, security/data-privacy.html,
rest-api/overview.html, rest-api/running-agents.html; rebuilt (107 pages, 32 examples valid).
Next: Ram reviews the docsrc diff, then deploy (s3 sync + CloudFront "/docs/*" invalidation).
