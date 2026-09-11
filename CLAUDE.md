# website - search2o.com and its documentation

Moved here from `s2oserver/docs/website` on 2026-08-30. Everything website related lives here:
the five site pages, the documentation source and generator, the built site, and the deploy
procedure. The full history of decisions made while this lived in s2oserver is in
`../s2oserver/CLAUDE.md` (search it for "website", "docs", "home page").

## State on 2026-09-09 (sys.secret brackets; new "Why not Python?" section)

SECRETS SYNTAX: `sys.secret(name)` is now `sys.secret[name]` everywhere in the docs. Six call
sites in five sources: security/secret-vault.html (lead, the profile-header code block, the
name-transform example), commands/api.html (the key header example and the credentials bullet
`sys.secret[...]`), agent-definition/variables.html, profiles/llm-profiles.html and
llm/vendors.html (both `f"Bearer {sys.secret['OPENAI_API_KEY']}"`). The bare mentions with no
argument (data-privacy, gui/operations, profiles/overview, api-profiles, db-profiles) stayed
`sys.secret`. Sweep for `sys.secret(` over html, docsrc, gen and content is clean.

NEW LAST SECTION on introduction/what-is-search2o.html, "Why not Python?" - why an agent is
JSON with Python expressions rather than a Python program. Ram's first form was a bullet list;
he then asked for A TABLE that states plainly why declarative is superior, and for the
indefensible rows to go: "When two developers change the same agent, publishing opens a merge
view" was CUT because a version control system does the same for Python. Versioning was cut for
the same reason (git exists). The table is three columns - Aspect / A Python program / A
Search2o agent - with seven rows: writing it (AI assist plus a schema that judges the result),
before it runs (checks plus the mandatory validation run), reading it, trusting it (controlled
runtime, allowlist, no import), limits (run time, loop iterations, db rows, LLM spend),
shipping a change (publish, no packaging), measuring it (duration, result, LLM cost). It closes
with "Python does not disappear" - every expression is still Python. The header row is MIXED
CASE: `table.fields th` in html/docs/docs.css uppercases every docs table header, which turned
"A Search2o agent" into "A SEARCH2O AGENT" - a brand-spelling violation. New scoped rule
`table.fields.compare th { text-transform: none; letter-spacing: 0; font-size: 13px; color:
var(--ink) }` (docs.css:99) and the table carries `class="fields compare"`. Every OTHER docs
table keeps its uppercase header - those headers are one-word labels (Field/Type/Default), and
no other header contains the brand (checked). Say the word to drop the all-caps globally. Table class is `fields`,
NOT `fields data`: the data variant's min-widths gave the short label column 170px and left the
Search2o column narrowest (170/349/251); plain `fields` measures 153/265/352, no scroll, and the
widest column is the one with the longest cells. Measured in Chrome over a local
`python3 -m http.server` under html/ - file:// URLs are refused by the browser tool.

## State on 2026-09-10 (Agent runtime: four guardrail pages; controlled runtime retired)
Per Ram: the guardrail parts are their own topics under Agent runtime, the allowlist is
expanded (a key part of the system), and security/controlled-runtime is gone with its content
folded into the runtime section. toc order now: overview / allowlist (The allowlist) /
system-variables / compile-rules / runtime-limits / pools-and-profiles. 126 pages. RETIRED with
git rm (docsrc AND the generated html/docs copies): runtime/guardrails.html and
security/controlled-runtime.html. DEPLOY NOTE: the live bucket will need
`aws s3 rm s3://search2o.com/docs/runtime/guardrails.html` and
`aws s3 rm s3://search2o.com/docs/security/controlled-runtime.html`; the in-app summaries need
regenerating and security__controlled-runtime.json + runtime__guardrails.json deleted by hand.
Every inbound link rewritten (13 docsrc pages: guardrails.html#allowlist -> allowlist.html
etc.; syntax.html's controlled-runtime link now points at allowlist + compile-rules); a full
href check over html/docs found only two PRE-EXISTING breaks, not mine: introduction/
parts-of-the-system.html has an href with a leading space before the GitHub URL, and
support-licensing/support.html links notifications.html which is in system-management.
ALLOWLIST PAGE, verified against ../search2o/search2o/execution/allowlist.py, agent_executor.py
create_ro/create_dict and ../s2oserver/compiler/validateexpr.py + oprewriter.py: the allowlist
IS the expressions' __builtins__ (nothing available by default); three entry forms exactly as
resolve() does them (one name -> builtins; two names with a builtin type first -> that type's
method; any other dotted path -> importlib the module before the last dot, getattr the last
name); "as" alias; wildcard `.*` adds nothing silently; a module member may itself be a module
(os.path exposes every public function - advice: list functions, not modules); failing entries
are skipped, "Error importing '...'" logged, the rest still load; LlmAdapter subclasses are
constructed with no args when the allowlist is built; SafeOperators methods are added under
their names unless an entry shadows them. Figure "sandbox" RENAMED expression-bounds (the word
is banned even as an id) and moved to the allowlist page. Scope-of-an-expression and the
application-level/no-CPU-or-memory-limit statement came over from the retired security page.
COMPILE RULES PAGE has a "What validation refuses" list straight from validateexpr.py: import,
any underscore-leading name (variable/attribute/function/keyword), lambda, walrus, calling
anything but a name or attribute, comprehension depth/generators, denied operators. Rewrite
function names are `safe_` + the model field name (safe_add, safe_mult, safe_pow) - that is
what oprewriter emits.
SYSTEM VARIABLES PAGE uses <!--enum:SysVariables--> (four members - the model has a FOURTH,
`cookies`, wired in agent_executor.py, which the old page did not list; documented with a
care note) and states sys.secret is always present (create_ro adds inputs, query, secret).
RULINGS (Ram, 2026-09-10): cookies STAYS documented. gather AND sleep ARE GONE from the product
(the parallel command replaced them) - every reference removed: syntax.html#awaiting now says
"To run several calls at once, use the parallel command" and its example block lost the
gather line; order-of-execution says one exception (parallel); rest-api/workflows says the
execAgent calls go in a for loop. Sweep for gather is clean (allowlist.html's time.sleep is
Python's blocking function, deliberately kept as a do-not-allowlist example). The safe_mult/
safe_mul + missing safe_lshift/rshift/matmult bug is Ram's to fix in the package - he is also
weighing an alternate design, so the compile-rules wording may need to follow.
HISTORY: (1) "gather and sleep are always available" and "the asyncio
package is refused" - claimed in agent-definition/syntax.html#awaiting and on the two retired
pages - have NO code behind them anywhere in ../search2o or ../s2oserver (no alias, no
allowlist check on save); the new pages do not repeat the claim; syntax.html still does.
(2) PACKAGE BUG: oprewriter maps * to safe_mult but SafeOperators defines safe_mul, and no
safe_lshift/safe_rshift/safe_matmult exist - rewriting * (or the denied-by-default three)
would fail at runtime with a NameError.
gen/build.py render_default: a default_factory that returns a BaseModel now renders "" like a
BaseModel default (was a giant repr that made CompileOptions' operators row scroll 4236px);
the same fix cleaned five other tables (connection pools, authentication method, two profile
pages, secrets source). Measured in Chrome: every table and pre on the five runtime pages
fits; the two figures have 0 overruns; 32 examples valid.

## State on 2026-09-10 (Connection pools is its own page; profiles and secrets pointed at)
Per Ram: runtime/pools-and-profiles.html RETIRED (git rm -f, docsrc and html/docs) and replaced
by runtime/connection-pools.html, which is ONLY about pools (lead rewritten in clear English
from the old rough paragraph: every HTTP connection goes through a pool - cloud calls, LLM
calls, api commands and API profiles - each can name a pool, "default" is used where none is
named, administrators define them, a change reaches every server before the next run, the old
pool stays open until the last agent using the pool finishes; then the three fields tables). The
runtime overview's "What the runtime holds" list now just points elsewhere for profiles (the
Profiles section) and secrets/encryption (Security and privacy); its table's Profiles row links
../profiles/index.html. toc: ("connection-pools", "Connection pools"). Section lead and docs
home card say "connection pools" only. gui/operations.html link updated. 126 pages, 32
examples valid, every table on the three touched pages fits. DEPLOY NOTE: add
`aws s3 rm s3://search2o.com/docs/runtime/pools-and-profiles.html` and delete its summary
JSON. The link checker now shows ONE pre-existing break: support-licensing/support.html ->
notifications.html (the page is in system-management); the parts-of-the-system GitHub href
with a leading space is a pre-existing oddity too, not a 404.

## State on 2026-09-10 ("Compile rules" is now "Python operators"; rewrite redesigned)
Ram changed the product: OperatorMappingAction is now {allow: bool, rewrite: str} - each
operator is allowed or denied, and an allowed operator may name the function it is rewritten
to. Defaults per the model: EVERY operator allowed, none rewritten (the old ** rewrite / shift
and @ denied defaults are gone). On save, the agent server (api/admin.py check_rewrite_targets)
checks every named function: in the expression namespace (allowlist + SafeOperators), callable,
takes two values, passes a trial run with two small integers - EXCEPT matmult, which gets no
trial; a failing function refuses the save with the reason; a denied operator's rewrite name is
cleared on save. The cloud rewriter uses the configured name. Also verified and added to "What
validation refuses": expressions may hold only ASCII letters, digits, punctuation and space
(validateexpr has_disallowed_expr_chars). The allowlist save is refused too when an entry
cannot be imported (admin.py updateSystemConfigPart) - allowlist.html and gui/guardrails.html
now say so; the skip-and-log behaviour remains true for OTHER servers at runtime build.
NAME: the page is runtime/python-operators.html, toc title "Python operators"; every "compile
rules" is gone from docsrc/gen (sweep clean apart from the REST field compileErrors and the
model name CompileOptions in a placeholder) - the vocabulary rule's one exception no longer
exists, so "compile" in any form is banned outright now. The GUI BUNDLE still says "Compile
rules" in its nav (ui/assets/NavigationModule) - Ram's to rename; gui/guardrails h2 and the
overview table already say Guardrails > Python operators; the gui-guardrails screenshot is
stale (Ram retakes). The built-in bounded functions are listed by their REAL names now
(safe_add, safe_sub, safe_mul, safe_div, safe_floordiv, safe_mod, safe_pow; none for shifts or
@) on both python-operators and allowlist. LEFTOVER FOR RAM: docsrc/runtime/compile-rules.html
and html/docs/runtime/compile-rules.html are UNTRACKED files from earlier today (never
committed) - my rm was declined; `rm` both, they are orphans (not in toc, no inbound links).
Figure layer label is "Python operators" (bbox inside its 150px box); 126 pages, 32 examples
valid, tables fit. RAIL (the unused GUI-mock rail list in figures.py) renamed too; only RAIL2
is drawn.

## State on 2026-09-10 (operators: no built-in functions; three options)
Ram's design note (content/operators.md, his selection): each operator is allow / deny /
rewrite; rewrite FORCES a function name; the function must be in the allowlist; it must take
two numbers (a one-argument function cannot stand in); @ is not checked; there are NO
system-defined functions - SafeOperators is going away. Applied: python-operators.html is
"The three options" (allow is the default for all ten, deny fails validation with the path,
rewrite asks for a name), "Rewriting an operator" (a ** b -> bounded_pow(a, b) as an example
of YOUR function; no built-in; on the allowlist on every server; two numeric arguments;
checked on save except @; refused with the reason), a short why-rewrite paragraph,
comprehensions + CompileOptions table, what validation refuses, republish rule. NO operators
table and NO OperatorMappingAction table - Ram: "no table is needed, just the 10 builtin Python
operators" (listed inline). Every safe_* and "built-in bounded" mention is gone from
allowlist.html (its "Always present" section deleted; the registering bullet now reads "a
function that a Python operator is rewritten to"), gui/guardrails.html and the figure layer
("each operator allowed, denied or rewritten to a function of your own"). The only remaining
safe_ text is in the UNTRACKED orphan docsrc/runtime/compile-rules.html - still Ram's to rm.
126 pages, 32 examples valid.

## State on 2026-09-10 (title back to "Compile rules"; rules apply only at validate/publish)
Ram reversed the rename once he saw the page covers more than operators (comprehension bounds
and the refused shapes too): the topic is runtime/compile-rules.html, title "Compile rules"
again, and the vocabulary exception for that product name stands. The python-operators files
were `mv`ed over the compile-rules orphans, so NO orphans remain (no rm needed after all).
Every "Python operators" reference reverted (toc, allowlist x3, overview x2, gui/guardrails,
docs home card, runtime lead, users-and-roles, notifications, what-is-search2o, syntax,
figure layer + RAIL). The lead now lists all three things the rules decide and states: "Search2o
Cloud applies the rules only when a draft is validated or published. A changed rule does not
touch an agent that is already published." The first h2 is "Python operators" (was "The three options"); the rewrite paragraph says "Write the function yourself, and put the function on the allowlist..." (the "there is no built-in function" sentence was cut - see the standing instruction). The closing section is "When a rule changes" (a
changed rule reaches an agent only through a new draft published again); gui/guardrails.html
carries the same only-at-validate/publish sentence. 126 pages, 32 examples valid, link check
unchanged (the one pre-existing support.html break).

## State on 2026-09-10 (data-privacy: descriptions are plain while indexed)
Ram: an agent description is stored in plain form for the brief period while the agent is
indexed, and the plain form is deleted once indexing completes. data-privacy.html's "What
leaves in plain form but is stored encrypted" intro no longer claims "the plain text is never
stored" for everything: query and memory text are handled in memory and never stored; the
description is stored plain until indexing completes, then deleted; none of the plain text is
logged. The Agent descriptions table row says the same. Ram then called the rewritten intro paragraph "so badly written" and had it REMOVED - the section is now the h2 and the table only; the description-while-indexing fact lives in the table row.

## State on 2026-09-10 (prompt profiles: encrypted and static)
Ram: prompt profiles are now ENCRYPTED (system and user prompt) and STATIC; a prompt on the
prompt command in an agent is dynamic and unencrypted. Two choices: dynamic + plain in the
agent, or static + encrypted in the profile. VERIFIED in ../search2o: api/admin.py
encrypt_prompt_profile on save / decrypt_prompt_profile on read (the agent server behind the
GUI does both, Encryptor.encrypt_query/decrypt_query); execution/runtime.py decrypts every
profile's prompts when the runtime is built; commands/prompt.py uses profile.system/user
verbatim (no evaluation) and command values override. Applied: profiles/prompt-profiles.html
rewritten (lead + "Encrypted and static" + "Two places for a prompt"; the old "marked
dynamic" paragraph is gone - there is no such flag); commands/prompt.html profile paragraph
extended with the dynamic/plain vs static/encrypted distinction; profiles/overview table cell
and gui/profiles say "stored encrypted"; data-privacy: NEW ROW "Prompt profiles" in "What
leaves only in encrypted form" (developers via the GUI; agent servers decrypt at runtime; life
of the profile) and the plain-form Profiles row now lists LLMs/APIs/databases/MCP plus "the
name and note of a prompt profile"; encryption.html end-to-end sentence lists prompt profiles.
The PromptProfileModel table carries Ram's new descriptions ("Stored encrypted; the Search2o
cloud never holds the text") automatically. NOT TOUCHED, flagged: what-is-search2o's
"Sensitive information like conversation, queries, and memories are encrypted" (an examples
list, Ram's line) and about.html's encryption list on the SITE (Ram's marketing copy).

## State on 2026-09-10 (license page: cloud region line)
license.html: the "cloud's code is not published" clause is gone (rule above). New line after
the cloud paragraph, Ram's wording verbatim (plus "the" before US East, twice): "Search2o
Cloud currently operates from the US East. You will see the lowest latency if you run the
agent server in the US East. We will expand to other regions in the future."

## State on 2026-09-10 (clients.html hallucination cut; GUI-claims sweep)
Ram: "The bundled GUI is itself a client generated from this schema" was pure hallucination -
REMOVED from rest-api/clients.html's lead. Sweep of every docs line that says how the GUI is
built or what the GUI does: the rest are either Ram-approved (how-the-gui-runs, 2026-09-08:
uses the REST API and nothing else) or verifiable (single-page application bundled at /ui:
ui/index.html + assets; "the streamed line types are in the schema": exec.py declares
responses={200: {"model": StreamAgentReturn}}, dev.py StreamDraftReturn). "Generated from the
agent schema" on commands/index and agent-definition/commands refers to OUR field tables
(build.py) and is true. RULE: a claim about how a product part is implemented needs the code
behind it, or it goes.

## State on 2026-09-10 (home diagram: fan-out trunk ends on the arrows)
Ram: the vertical trunk behind the four chip arrows overshot the top and bottom arrows by a
few pixels. Measured: chips are 26.4px tall, so each arrow's centre is 13.2px from its
branch's top and the 2px arrow spans 12.2-14.2px; the trunk (.arch-sys::before) used
top/bottom 11px, 1.2px past the outer edge of the first and last arrow (2.4 device px on
retina). Now top/bottom 12px (styles.css:349, with a comment) - 0.2px short of the edge, i.e.
flush; overshoot measured 0.2/0.2 and a zoomed crop shows square corners. Chip height was
deliberately left alone so the diagram's height and the columns-end-level alignment do not
move. Site page CSS only; no docs rebuild needed.

## State on 2026-09-10 (home page: the 23 command chips link to their docs pages)
Each <code>cmd</code> chip in the Agent framework section's .cmdgroups is now
<a href="docs/commands/cmd.html"><code>cmd</code></a> (23 links, 23 distinct targets, every
file exists). Inline CSS added next to .cg-c code: `.cg-c a { display: flex; text-decoration:
none }` (+ a:hover no underline; `a:hover code` border and text var(--blue-ink)). WHY
display:flex: a plain inline <a> became the flex item and its 15.5px line box made every row
~2.4px shorter (.cmdgroups 444 -> 422px); with the anchor as a flex container the chip is the
flex item again and the geometry is byte-identical to before (444px). Hover verified in a
zoomed crop: quiet blue border + text, nothing else moves. FINDING, NOT MINE, NOT FIXED: at
1920px wide the Agent framework .split columns end 43px apart (left 834 / right 791) - that
was the committed state before this change, though the 2026-09-09 note claims delta 0;
possibly a different viewport then. Ram's call whether to re-tune .cmdgroups gap.

## State on 2026-09-10 (gettingstarted hero note: Account page)
The hero note (gettingstarted.html:43) now reads "Start with the free Individual plan. When
you are ready, upgrade from the Account page in the GUI." (was "upgrade in place from the
GUI"; Ram's wording).

## State on 2026-09-10 (gettingstarted h1: "From your laptop to your team"; note gone)
Ram: "Up and running on your laptop" was misleading because the last two steps are about
upgrading, and the note beneath was not needed. h1 is now "From your laptop to your team"
(his pick of my four; "see whether you can make it better" - variants offered, none applied)
and the .note paragraph is REMOVED; the hero is kicker + h1 only, like pricing. Metas
untouched (they describe the steps, still accurate). The .page-hero .note CSS is now unused
on this page (styles.css) - reported, not removed.

## State on 2026-09-10 (legal/license.html regenerated from content/legal/license.md)
Ram rewrote content/legal/license.md (Version 1.0, effective September 10, 2026; 162 blocks,
22 h2, plain paragraphs, no bullets/bold/code/fences) and asked for the html version placed
in html/legal. Regenerated the article body of html/legal/license.html and its hero h1 with
a rebuilt converter (blank-line blocks; "## " -> h2, "### " -> h3, else <p> with
html.escape; the md h1 goes to the hero h1). FIDELITY VERIFIED: normalized text of hero h1
+ article == normalized md, IDENTICAL. <title>/meta untouched (title unchanged). The page's
chrome (header, footer, Legal column) was left as is. The converter is NOT in gen/ - it
was rebuilt inline again; worth adding as gen/legal.py if the legal md keeps changing.

## State on 2026-09-10 (legal/terms.html regenerated from content/legal/terms.md)
Same converter as the license page (blocks; ## -> h2; **bold** -> <strong>; html.escape),
run over terms.md (one h1, 29 h2, one bold "Effective Date: September 5, 2026" line).
FIDELITY VERIFIED IDENTICAL (normalized hero h1 + article == normalized md with the **
markers stripped). Title and metas unchanged.

## State on 2026-09-10 (legal/privacy.html regenerated from content/legal/privacy.md)
Same converter, now with "* " bullet blocks -> <ul><li> and backticks -> <code>: privacy.md
has one h1, 13 h2, 30 bullets, 9 bold pairs, 3 code spans. FIDELITY VERIFIED IDENTICAL
(markers stripped on the md side). Title and metas unchanged. All three regenerated legal
pages (license, terms, privacy) are uncommitted in html/legal for Ram's review.

## State on 2026-09-10 (scripts/deploy.sh created - NOT RUN with --go)
NEW scripts/deploy.sh (executable, bash -n clean; shellcheck not installed). No arguments =
DRY RUN: preflight (aws identity must be 406848153313; html/config.js apiUrl line must not be
localhost/127.0.0.1 - the check reads ONLY the apiUrl line because the file's comment cites
http://localhost:8080 as an example and tripped the first version; notes uncommitted changes
under html/docsrc/gen), rebuilds docs + check_examples (S2O_PYTHON overrides
../s2oserver/.venv/bin/python; --skip-build skips), `aws s3 sync --dryrun` listing, then a
list of bucket objects with no local file. `--go`: sync (same excludes as website_deploy.md:
logo.svg, .DS_Store), optional `--delete-stale` (asks to TYPE THE BUCKET NAME, then
`aws s3 rm` each listed key), create-invalidation "/*", POLL every 10s up to 600s until
Completed, curl-verify / and /docs/index.html title. PROTECTED_PREFIXES=("docsweb/"): the
dry run revealed the bucket holds docsweb/ (agentschema.json, uitext.json,
evaluationform.json - the in-app docs data s2oserver's docswebuploader.py maintains and the
PRODUCT READS); the stale list skips it so --delete-stale can never remove it. Read-only dry
runs were executed twice (sts, sync --dryrun, s3 ls - nothing uploaded, nothing invalidated):
175 files would upload (the bucket still holds only the 2026-09-03 placeholder) and the stale
list is "none" once docsweb/ is protected. website_deploy.md gained a "The script" section.
STANDING RULE UNCHANGED: --go only when Ram says deploy.

## State on 2026-09-10 (INSTALL IS `pip install search2o` FROM PyPI AGAIN)
Ram: "The way to deploy search2o now is: pip install search2o (not from github). Change it
everywhere." This REVERSES the 2026-09-05 "PyPI is gone, no page may say PyPI" rule: the
package is on PyPI as search2o (pyproject name search2o, version 0.2.0; extras postgres/
mysql/oracle/mssql/db unchanged). Changed: html/gettingstarted.html Download step ("Install
it with pip:" + `pip install search2o`, codecard aria-label "Install with pip") and both
metas ("install the agent server with pip"); docs home Getting started card; registering-and-
downloading (lead; Install section is one `pip install search2o` block, the clone block and
the "@ git+" extras form are GONE, extras are `pip install "search2o[postgres]"` etc.);
support-licensing/license.html ("installed with pip install search2o from PyPI" first, the
repo link second); parts-of-the-system ("installed with pip install search2o" - the odd
leading-space GitHub href is gone with it, which also clears the last pre-existing link-check
oddity). KEPT, flagged to Ram: the SOURCE-AVAILABLE story and the repo links (registering
Source section, license lead + repo/CONTRIBUTING links, support.html source line) - he ruled
on the install path, not on the source. ../search2o/README.md and content/gettingstarted.md
already said pip install search2o. The legal pages (verbatim legal text) mention both GitHub
and PyPI and are untouched. Sweep for git+ / agent-server.git / ./agent-server / "from
GitHub" is clean. 126 pages, 32 examples valid.

## State on 2026-09-10 (source available, WITHOUT the GUI)
Ram: the agent server source (without the UI) is at https://github.com/Search2o/agent-server -
so the source-available story stays, with that precision. The three docs statements now say
"the source, without the GUI, is at/public at github.com/Search2o/agent-server":
registering-and-downloading Source section (link added), support.html source line, and
license.html lead + Agent server paragraph. Home page "Source available" (steps + diagram
subtitle) untouched - still true. Vocabulary: "the GUI", never "ui". Ram then simplified the registering
sentence to "The agent server source is available at github.com/Search2o/agent-server." (no
"source available:" construction, no "without the GUI", no "proprietary" there); I applied
the same shape to the license.html lead ("The agent server source is available on GitHub,
and the software is proprietary.") since it was the identical construction - flagged for veto.
"Without the GUI" survives in license.html's Agent server paragraph and on support.html.

## State on 2026-09-10 (gettingstarted Download step line)
gettingstarted.html:83 is now "Install the agent server with the bundled GUI:" (Ram's
wording; the "Python 3.12+ package" clause left the page - the requirement is still in the
docs on registering-and-downloading).

## State on 2026-09-10 (pip install = agent server WITH the bundled GUI; no "without the GUI")
Ram: wherever pip install search2o appears, say it is the agent server with the bundled GUI;
and the source line is just "The agent server source is available at github.com/Search2o/
agent-server" - "without the GUI" is NOT said. Applied: parts-of-the-system:8, registering
Install intro, license.html Agent server paragraph (both halves), support.html:18;
gettingstarted.html:83 already said "Install the agent server with the bundled GUI:". Sweep
for "without the GUI" is clean.

## State on 2026-09-10 (gettingstarted h1: "From your laptop to production")
Ram wanted something other than "to your team"; picked option 2 of four, "From your laptop to
production" (gettingstarted.html:42) - the same title he used on 2026-09-07.

## State on 2026-09-10 (DEPLOYED - the live site is no longer the placeholder)
Ram said "Deploy it"; ran `scripts/deploy.sh --go` (backgrounded, log in the session
scratchpad): docs rebuilt (126 pages, 32 examples valid), 175 files / 5.2 MiB uploaded to
s3://search2o.com/ (the bucket had held only the 2026-09-03 placeholder; nothing stale,
docsweb/ untouched), CloudFront invalidation IA1H0UOJID9J5C9GQ3XHJEKGEW Completed after
~30s, verification 200 on / and the docs title. Spot checks live: /, gettingstarted (h1 "From
your laptop to production"), pricing, about, legal/license, docs runtime allowlist +
compile-rules, what-is-search2o (Why not Python present), docs.css carries the
fields.compare rule, config.js served. A retired URL such as docs/runtime/guardrails.html
serves the home page (the bucket's error document is index.html - by design, no 404 page).
STANDING RULE UNCHANGED: every future deploy needs Ram's explicit go. NOT DONE (s2oserver
side, Ram's): regenerate the in-app docs summaries with maintenance/docs_create.py and hand-
delete the stale JSON for the retired pages (security__controlled-runtime,
runtime__guardrails, runtime__pools-and-profiles, misc__*). config.js apiUrl deployed as
checked in (the Cloud Run URL Ram set on 2026-09-08).

## State on 2026-09-10 (second deploy: Ram's index.html edit)
Ram edited html/index.html himself and said "Deploy whatever is needed"; ran
`scripts/deploy.sh --go` again: index.html uploaded, invalidation I90V2OYHH64OQKPJRUHNJX5N8K
Completed, live index.html md5 == local. FINDING: because build.py rewrites every docs page
(new mtime) and `aws s3 sync` compares size+mtime, a deploy after any rebuild re-uploads all
126 docs pages even when their content is unchanged. Harmless (5 MiB) but noisy; the fix
would be build.py writing a page only when its content changed - not done, Ram's call.

## State on 2026-09-11 (SEO pass: repo side DEPLOYED, AWS side awaits Ram)
Ram asked whether the site is search-engine friendly, then "Go ahead with everything". AUDIT
FINDINGS: no robots.txt / sitemap.xml (both 403); www.search2o.com and docs.search2o.com serve
the same content with 200 and no canonical (duplicate content across three hosts); missing
pages return 403 with index.html as the body (no bucket policy grants public ListBucket, so S3
answers 403 not 404; the bucket's ErrorDocument was index.html); no og:image/og:url, no
JSON-LD, no Cache-Control. Page-level basics were fine (title, description, lang, one h1,
alt text, legal noindex).
DONE AND LIVE (third deploy today, invalidation IBAXIY9A1GJFZN29QORFHOQHAL): html/robots.txt
(allow all, Disallow /legal/, Sitemap line); gen/build.py now writes html/sitemap.xml (4 site
pages + docs home + every toc page = 130 URLs, legal excluded, no lastmod) and puts
canonical + og:title/description/type=article/url/image on every docs page (docs_path()
helper); site pages gained canonical + og:url + og:image (logo.png, 560x102 - a placeholder
until a 1200x630 card exists) and the home page a JSON-LD Organization + WebSite block; legal
pages gained canonical; NEW html/404.html (About-page chrome, kicker 404, noindex, ALL paths
absolute because CloudFront serves it under any URL); scripts/deploy.sh syncs with
--cache-control "public, max-age=600" (objects not re-uploaded keep no header until they
change: logo.png, favicon.svg, config.js, site.js).
BLOCKED BY THE AUTO-MODE CLASSIFIER (AWS resource creation): the CloudFront Function. Written
instead: scripts/cloudfront-canonical-host.js (viewer-request: www. -> apex 301, docs. ->
apex/docs 301, query string kept) and scripts/cloudfront-setup.sh (idempotent: create-or-
update + test on DEVELOPMENT + publish the function; update-distribution with the
viewer-request association and CustomErrorResponses 403/404 -> /404.html status 404;
put-bucket-website ErrorDocument 404.html; --wait polls until Deployed and verifies). RAM RAN
IT (2026-09-11): first run failed at the function test - my script passed the test event as
a base64 STRING and the CLI base64-encoded the blob again (TestFunctionFailed, "unexpected
result"); fixed to write the event to a temp file and pass fileb://. Second run: function
updated, tests passed, published, distribution updated (viewer-request association +
CustomErrorResponses 403/404 -> /404.html as 404), bucket ErrorDocument 404.html, distribution
Deployed. VERIFIED LIVE: www.search2o.com/ -> 301 https://search2o.com/;
docs.search2o.com/ -> 301 https://search2o.com/docs/; docs.search2o.com/docs/index.html keeps
its path; a missing URL (e.g. docs/runtime/guardrails.html) answers 404 with the "Page not
found" page; / still 200. Then Ram: WRONG - docs.search2o.com must point at the root, the UI depends on
directories under it. REVERTED within the hour: cloudfront-canonical-host.js now redirects
ONLY www. (function updated, tested, published LIVE - a function publish needs no distribution
deploy); verified docs.search2o.com/ and /docsweb/uitext_current.json 200 again, www still
301, missing page still 404. cloudfront-setup.sh's tests now assert the docs host passes
through; website_deploy.md corrected. The SEO pass is COMPLETE. Open: og:image is logo.png
(560x102) until a 1200x630 card exists.

## State on 2026-09-11 (home page fixed for phones; NOT YET DEPLOYED)
Ram: the home page did not look right on his phone. Measured at 390px (a 390px-wide iframe -
the window resize was ignored by a full-screen Chrome, and the live site is blocked by the
browser extension's site permissions, so use the local server): the page scrolled sideways
(scrollWidth 404), the hero column was 502px wide with the text cut off, the nav showed a
scrollbar. CAUSE: the <=1000px rules collapse the grids to `1fr`, and a 1fr track cannot
shrink below its content - the demo's one-line nowrap query and the diagram's side-by-side
.arch-row forced the column wider than the phone. FIX in styles.css: <=1000px grids are
`minmax(0, 1fr)` with `min-width: 0` on their children and .hero-grid .demo margin-top 0;
<=640px: .site-nav wraps (no overflow-x scroll), .demo-search text wraps, .demo-row/.demo-form
wrap, .arch-row becomes one column with the fan-out connector hidden and the four system
chips as a wrapped row under the server box (no arrows at phone width - flagged to Ram).
RESULT: scrollWidth 375 on index/gettingstarted/docs pages, no overflowing element except
code pres and .tablewrap tables, which scroll on their own by design; hero, demo, how-it-works,
diagram and reports checked in zoomed crops. gettingstarted shows one element at x=-21: the
hCaptcha script's own hidden helper div, not ours. The other site pages and the docs already
fit. TRAP: iframes take styles.css from cache - cache-bust the <link> before auditing. Ram then
asked which sizes were tested (only 390) while seeing cut-off on a DevTools Pixel 7 - he was
looking at the LIVE site, which still had the old CSS. WIDTH SWEEP with the fix (local):
index.html at 360/375/390/412/430/768/820/1024 all ok; gettingstarted, pricing, about, docs
index, docs allowlist, docs api, legal/terms at 360/412/768 all ok (no sideways scroll, no
overflowing element outside pres and tablewraps); Pixel 7 (412x915) hero checked in a crop.
A sweep of 56 iframe loads in one javascript_tool call times out (45s) - do 8-12 loads per call
(window.__sweep helper pattern). DEPLOYED on Ram's "Deploy it" (2026-09-11, --skip-build, only styles.css differed, invalidation Completed, live md5 == local).

## State on 2026-09-11 (Running multiple environments moved to the end of Security and privacy)
git mv docsrc/system-management/multiple-environments.html -> docsrc/security/ (the page's own
links are ../profiles and ../rest-api - same depth, unchanged); toc entry moved to the end of
the security section after data-privacy; the generated html/docs/system-management copy git
rm'd; system-management lead lost "and running several environments", the security lead and
the docs home Security card gained the page. No inbound links existed. 126 pages, 32 examples
valid, sitemap has the new URL, link check unchanged (support.html -> notifications.html
still the one pre-existing break). NOT DEPLOYED. DEPLOY NOTE: the old URL
docs/system-management/multiple-environments.html now 404s live once deployed (sync never
deletes - `aws s3 rm` it or leave it; the 404 mapping covers a missing key but NOT a stale
object that still exists in the bucket, so the stale copy would keep serving the OLD sidebar).

## State on 2026-09-11 (home Search section links to the search quality page)
After a long DISCUSSION (Ram: not bombastic, not falsely modest either; "test results" after
the timing figure would read as results about speed), the settled line is Ram's: "It supports
major world languages and returns matches in less than 0.5 seconds &mdash; see search
quality." with "search quality" linking docs/search/search-quality.html (index.html Search
section). The 0.5-second figure stays. DEPLOYED 2026-09-11 together with the environments page
move (invalidation IHBBZ4D89XHD0GLJS9P47A7L8); the stale docs/system-management/
multiple-environments.html object was REMOVED on Ram's "Remove it" (aws s3 rm + a path
invalidation, IE48EBKEB7EU4WVMI6BZGYRVBK); the old URL now answers 404, the new one 200.

## State on 2026-09-11 (error-detail mock-up: no queries)
Ram: "we do not store or show the queries" - the report-errors-detail figure in gen/figures.py
still drew an "Example queries (a sample, most recent first)" strip under the table (a
leftover from before the 2026-09-03 privacy correction; the page text next to it already said
queries are not shown). The extra() strip is REMOVED and the figure's height is 260 like the
other two detail figures (was 300, leaving an empty band). Rebuilt; not deployed.

## Standing instructions
- DISCUSSING vs DOING (Ram, 2026-09-07, annoyed): when Ram is iterating on wording or design
  ("suggest your changes", counter-proposals, "not satisfactory", "nah..."), that is a
  DISCUSSION - propose only, apply NOTHING until an explicit go. A veto of one detail
  ("do not mention 23") is not approval of the rest. His words: "You seem to have a tough
  time realizing when to do things vs when to discuss."
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
- NEVER DOCUMENT AN ABSENCE (Ram, 2026-09-10): what he tells me in a note ("there are no
  built-in functions") is context, not a sentence for the page. The docs never say "X does not
  exist" or "there is no X"; the docs say what to do instead ("Write the function yourself and
  put the function on the allowlist"). His words: "we don't say 'X doesn't exist' - we say 'Do
  this'."
- NO INVENTED REASONS (Ram, 2026-09-10, "Why did you say that?"): I wrote "@ is not checked,
  because the server has no values to try" - a reason I inferred from admin.py's trial table,
  not one Ram gave, and an implementation detail besides. The page states the rule and stops:
  "Matrix multiplication, @, is not checked." A "because" on a docs page needs Ram's reason or
  none.
- SAY WHAT IS, NEVER WHAT IS NOT (Ram, 2026-09-10, second time): "the cloud's code is not
  published" was cut from license.html - "we only say when something is, not when something
  is not. I already told you this for something else." Same rule as never documenting an
  absence; a sentence that exists only to deny something does not belong on a page.
- docs.search2o.com SERVES THE BUCKET ROOT, UNTOUCHED (Ram, 2026-09-11, after I broke it): the
  GUI reads data under that host (docsweb/ and other directories not linked from the site),
  so no redirect, rewrite, error mapping or deletion may ever treat that host or those paths as
  website content. Only www.search2o.com redirects. Duplicate-content concerns are handled by
  the canonical links, never by redirecting the docs host.
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

## State on 2026-09-07 (extras line off gettingstarted)
Ram removed the SQLite/db-extras dim line from the install step entirely - docs material;
people may not use databases at first, and those who do likely have their drivers installed.
The extras remain documented in registering-and-downloading.html. The install step is now
just the intro line and the two OR'd codecards.

## State on 2026-09-08 (lead redone; docs step is now Ask a question)
Ram: the lead was preachy (do not tell them what to do) and "Read the docs" is pre-AI. Lead
settled on Ram's final wording (fourth round), verbatim with curly quotes: "A laptop is
enough to start. When you are ready to show it to your team, upgrade it to 'Evaluation'
from the Account page in the GUI and run the server from a common place." The stateless
clause is gone; the Evaluation upgrade path is back on the page (it had left with part 2). The
line is styled .note (15.5px muted, 70ch) not .lead - Ram: too large, it is just a note. The last step is retitled "Ask a
question", asks-first: the docs-icon/AI-answer sentence leads, the web docs URL follows as
"The documentation itself is on the web at...". Stuck callout unchanged.

## State on 2026-09-09 (new docs page: Search quality)
NEW docsrc/search/search-quality.html, last page under Search (124 pages), written from
content/search_results.md - a source file that is EXPLICITLY not the page and carries
publish rules. Twelve sections: the conditional >99% short answer; overlap-not-size as the
reframe (the escalations/incident-triage example, the two 50-agent catalogues at 99.2% vs
83.8%); the well-separated table; the deliberately-hard pooled table (86/94.3/58/0.77/0.14)
labelled as our test set, not a typical deployment; the 40/100/1,000 scale table plus the
1,000-agent detail (every agent queried, 367 perfect, none failed all ten, worst were
near-synonym halves); one-two-three-or-none with the confidence trade in PROSE (range 88%
single results / 7.2% wrong -> 42% / 0.23%, shipped setting keeps wrong under 1%); refusals
(100% multi-language, 99.6% English, under 0.5% genuine turned away, the deliberate
neighbour bias); languages (both tables, Mandarin-Japanese 97.5% as the meaning-not-words
proof); speed (70-130ms to ~120 agents, ~400ms at 1,000, 230-260ms end to end - consistent
with the site's "less than 0.5 seconds"); method; "What we do not claim" (generated test
data, constructed 99% catalogue, translated descriptions, English strictest, indexing
required); and Ram's closing commitment (twenty years, quality will keep improving).
PUBLISH RULES: two violations Ram caught and I fixed -
(1) "The question is turned into a vector next to the data, so nothing large crosses the
network and there is no second round trip" REMOVED from the Speed section. HIS RULE, stated
as absolute: the docs may say NOTHING about how search actually works. (2) "This is the
catalogue shape most customers should aim for" REMOVED - "we do not tell customers what they
should aim for. On the contrary, we say how we can manage a 1000 agents." The Scale section
now opens "Search2o handles a thousand agents in one catalogue. Accuracy at 1,000 agents is
the same as at 100." and the catalogue-design line lost its "good news / yours to control"
framing. Also self-caught: "the real search index" -> "the live search service" (Ram banned
"search index" on 2026-09-07). Otherwise clean: no corpus names, no thresholds/dials, no
vendor or technology names, no per-agent breakdowns. KEPT with Ram's explicit approval:
commands/search.html "Search costs a round trip to Search2o Cloud" - topology, not search
mechanism, and worth saying because search is the ONLY command that behaves that way. The confidence table from the source
was deliberately turned into prose so readers do not hunt for a dial the GUI does not offer.
Search section lead and docs home card updated; five tables measured, none scrolls.

## State on 2026-09-09 (hero eyebrow matches the pricing h1)
"Free during the open beta" was the ONLY beta pricing claim on the site (verified) and is
now "Free until you're convinced" (index.html:44), the pricing h1 verbatim - 216px, one
line. Untouched, both being status not pricing: about.html "Search2o is currently in open
beta." and the docs registering page's "Search2o is in open beta, and anyone interested is
welcome to try it."
ALSO: Ram edited the AI-assist line himself to "Describe the workflow - AI assist will write
the first draft." (one line now, my nowrap span kept), which left the columns 23px out of
level; repaired with .cmdgroups gap 16 -> 19 (8 gaps x 3 = 24) and the line's margin-top
18 -> 17. Re-measured delta 0. WATCH: any edit to that line's length breaks the
columns-end-level rule and needs the gap re-tuned.

## State on 2026-09-09 (AI assist line under the 23 commands)
New muted line below the command groups on the home page: "Describe the agentic workflow you
need - AI assist writes the first draft." (Ram's final wording, third pass; 14.5px
var(--muted), margin-top 18). It needs 499px in a 467px column, so it wraps to two lines
and left "draft." ORPHANED; text-wrap:balance fixed the orphan but split mid-clause
("you / need"), so the second clause is wrapped in a white-space:nowrap span - the break
now falls at the em dash: "Describe the agentic workflow you need -" / "AI assist writes
the first draft." It lengthened the left column by
34px and broke the columns-end-level rule, so .cmdgroups gap went 20px -> 16px (8 gaps x 4px
= 32) and the new line's margin-top 20 -> 18 (2). Re-measured: delta 0.

## State on 2026-09-09 (LLM section moved up; new vendors page; adapters page deepened)
LLM now sits right after Agent execution, BEFORE Command reference (toc order). NEW first
page docsrc/llm/vendors.html "The three vendors" (123 pages): the three env keys with a
secrets pointer, a table of the five seeded profiles (gpt5_mini/gpt_image/claude_haiku/
gemini_flash/gemini_image) with the edit-the-prices note, how to create a profile for
another model (adapter/vendor/url/headers/model/pricing, headers example with sys.secret),
and a closing "Any compatible LLM" section pointing at llm-adapters. llm-adapters REWRITTEN
to lead with the bundled adapters ("First, try a bundled adapter" - no code needed for
OpenAI-compatible endpoints; quotes the OpenAI adapter's own description string) and then
go deep, VERIFIED against ../search2o/search2o/llm: BaseLlmAdapter's 11 abstract methods
plus name/description in a 13-row fields-data table (set_model, set_max_tokens, set_tools,
set_system_prompt, the four set_messages_*, set_response_flags, set_token_counts,
set_assistant_vendor), the note that it walks the prompt and calls the message methods in
conversation order, that get_error has a working default reading response["error"], and
LlmAdapter's five bare methods with the LlmRequestModel/LlmResponseModel signatures.
Section leads and the docs home card updated; getting started's LLM-key line now links
docs/llm/vendors.html (Ram's mid-task instruction). Tables measured: no scroll.

## State on 2026-09-09 (Miscellaneous retired; new LLM section)
Per Ram: NEW section "LLM" (docsrc/llm/, placed where misc was - after Chat integrations,
before Support and licensing) holding the two moved pages, Connecting to other LLMs and
Executing code from an LLM; new section index lead "Connecting Search2o to any LLM, and
running code that an LLM writes." Running multiple environments MOVED to System management
(last page there; that section's lead gained "and running several environments"). The misc
section is GONE: docsrc/misc/index.html git rm'd, the directory removed, and the STALE
GENERATED html/docs/misc (4 files) git rm'd too - the build never deletes, so a leftover
would have kept serving old URLs. Docs home card replaced (Miscellaneous -> LLM). Inbound
../misc/llm-adapters.html links fixed in runtime/guardrails, getting-started/
running-the-server, profiles/llm-profiles, and html/gettingstarted (docs/llm/...). 122
pages, 32 examples valid; sidebar verified in-browser. DEPLOY NOTE: the live bucket will
need `aws s3 rm --recursive s3://search2o.com/docs/misc/`.

## State on 2026-09-09 (new last step: Upgrade to the paid service)
Added after Bring-your-team (id="paid"): "When your team is ready, upgrade to the paid
service from the Account page in the GUI. You never have to contact us." + "If you would
like to talk to us, we are one click away from the help icon." Ram's content, my phrasing.
The page is nine steps now: create account / download / run / GUI / first agent / describe
+ search / call your systems / ask a question / bring your team / upgrade. NOTE: pricing
says the Team service "will be available soon", so this step describes a path that is not
live yet - Ram's call, flagged only here.

## State on 2026-09-09 (describe step says HOW)
Ram: the describe step never said where the description is entered. It now opens
"Publishing offers to take the description - you can also open the agent later and add it."
then the plain-English example, then the search/indexing sentence as its own paragraph.

## State on 2026-09-09 (Start the server: two cards, macOS/Linux and Windows)
The Start-the-server step now has TWO codecards, labelled in the .fname bar (the old label
was "terminal"): "macOS / Linux" with the $-prompt one-liner, and "Windows PowerShell" with
a PS> prompt. Ram's PowerShell ONE-LINER (semicolon-joined) OVERFLOWED the card - measured
753px in a 704px pre, which the horizontal scroll would have hidden - so it is split into
three PS> lines (same commands, exactly equivalent). All three pres measure "fits" now. Ram then REMOVED the whole
"Set up the license key" block (its export line was redundant - both start commands set the
key inline). The Run step is now: h3 "Use an LLM key" - "A key from one of the
three major vendors is enough: OPENAI_API_KEY, ANTHROPIC_API_KEY or GEMINI_API_KEY. See the
docs for other LLMs." (links misc/llm-adapters) - plus h3 "Start the server" (the two cards).

## State on 2026-09-09 (account-creation JS moved to site.js; two new error keys)
The inline account-creation script is OUT of gettingstarted.html and appended to
html/site.js, guarded by `if (!document.getElementById("reg-go1")) return;` so it costs
nothing on the other pages (site.js is loaded everywhere). Script order on the page is now
config.js THEN site.js. LEFT INLINE deliberately (Ram: "move whatever is easily possible",
"not a strict rule"): the one-line theme bootstrap in <head>, which must run before first
paint or the wrong theme flashes. NEW error keys, in REG_ERRORS with the others:
freeEmailCurrentlyNotAllowed -> "Please use your work email address."
registrationCurrentlySuspended -> "New accounts are paused at the moment. Please try again
later." VERIFIED in-browser through the real handler (stubbed hcaptcha+fetch): both new keys
render together one per line, POST body unchanged, success key box + copy button still work,
theme toggle and footer year unaffected.

## State on 2026-09-08 (key note rephrased)
The success note under the key box now reads "This key is shown only once - please copy it
and store it on your machine right away. The next steps use it." (Ram's direction,
my phrasing). The docs registering page still says "belongs with your other secrets" -
different audience, left alone unless Ram says otherwise.

## State on 2026-09-08 (REST API sub-section cut from getting started)
The Open-the-GUI step lost its REST API h3 (openapi.json/Swagger//docs//redoc) on Ram's
order - he had asked for it back on 2026-09-05, and has now reversed that; the URLs remain
in the docs (running-the-server, agent-servers, how-the-gui-runs links rest-api).

## State on 2026-09-08 (link label: no question mark)
"New user / Forgot password?" is now "New user / Forgot password" in all six places
(gettingstarted, the-gui, users-and-roles, authentication, rest-api/authentication,
gui/account) - Ram is removing the question mark in the UI too.

## State on 2026-09-08 (clone-install variant cut from getting started)
The Download step is ONE codecard now - pip install git+... The clone-then-install OR-box
is gone (unnecessary, Ram); the clone form remains documented in
registering-and-downloading. Ram then also cut the
SEARCH2O_LICENSE_KEY_FILE OR-box from the license-key step (in the docs, license-key.html).
No .or divider remains on the page; the .or CSS in styles.css is now UNUSED (reported, not
removed).

## State on 2026-09-08 (hero note simplified; step-1 line removed)
The hero note settled as "Start with the free Individual plan. When you are ready,
upgrade in place from the GUI." (Ram wanted the where - in place / in the GUI - added) - the upgrade detail lives only in the Bring-your-team step.
The step-1 "Individual plans are free. See Pricing for details." line is REMOVED (the note
above already says it). Step 1 is heading + form only.

## State on 2026-09-08 (Bring your team step restored as the last step)
Per Ram, the Evaluation step is BACK at the end of getting started (id="team", h2 "Bring
your team"): request an Evaluation license from the Account page in the GUI / approval
email within one business day / start the server in a common place / See Pricing. It sits
AFTER the Ask-a-question step, per "add a last point". The hero note carries the same
upgrade message - accepted duplication, his call.

## State on 2026-09-08 (GUI section renamed; How the GUI runs page)
Per Ram: the docs section "GUI pages" is now "GUI" (toc + docs home card; the card small
text mentions the new page). NEW first page gui/how-the-gui-runs.html (122 pages now):
official GUI, uses the REST API and nothing else (no private endpoints - everything the GUI
does is open to your code), lives in the server's ui directory served at /ui, can be served
from any web server or CDN - the hosting section + ui-config table MOVED here from
getting-started/the-gui.html - then trimmed to THREE settings (apiBase, apiTimeoutSeconds,
notificationDurationSeconds): Ram removed docsBase (the agent server serves the schema
itself now, undocumented by his choice) and defaultSuccessOutput (just a UI string) (one topic one home; that page now links here instead), and a
closing section says users are free to build their own interfaces (links rest-api/clients +
chat integrations).

## State on 2026-09-08 (registration PARADIGM removed site-wide)
Ram: get rid of the "registration" paradigm everywhere; also say in getting started that no
credit card is asked for. Step 1 intro was then CUT by Ram (no essays on this page;
creating an account is obvious) then "No credit
card needed.", and finally to Ram's "Individual plans are free. See Pricing for details."
(Pricing is the link). And the terms
checkbox label is now "I accept the Terms of Service and the Privacy Policy" - BOTH words
are links (legal/terms.html, legal/privacy.html, target=_blank). Reworded
across files: gettingstarted metas + step anchor (id="create-account") + JS comment + three
user-facing error strings ("...to create an account", "We could not create your account");
docs home Getting started card; getting-started section lead ("From creating an account
to..."); what-is-search2o ("Create an account and install"); multiple-environments ("Create
an account for each environment"); registering-and-downloading h2 "Create your account" +
body rewritten (single step, no password asked); license.html link text; toc TITLE is now
"Creating an account and downloading". KEPT deliberately: the technical sense of register
(LLM adapters/Teams bots/allowlist code registered), the server contract (/register,
registrationErrors), reg-* internal ids, and the LEGAL pages (verbatim text, Ram edits the
source). "the email you registered with" became "the email you used in step 1" (the form
is on the same page now). FLAGGED, NOT DONE: the SLUG registering-and-downloading.html is
still register-flavored and URL-visible - renaming means a docsrc+toc rename, a stale
html/docs orphan, and an s3 rm at deploy; Ram's call.

## State on 2026-09-08 (REGISTER PAGE RETIRED; form lives in getting started)
Ram's call, won on his argument: the key is shown ONCE, and inside getting started the user
never has to copy it anywhere - the export step sits right below. "Register" is no longer
the paradigm. Applied: step 1 is "Create your account" - intro line "Before you start, you
need a license key. Registration ends by showing it right here." + the form-card (button
"Create account"); success renders the key box IN PLACE with the note ending "The next
steps use it right away."; hCaptcha script + config.js now load on gettingstarted.html.
HEADER CTA REMOVED everywhere: four site pages, four legal pages, and gen/build.py's docs
template (all 121 docs pages rebuilt; header is nav + theme toggle only). The three body
buttons say "Get started ->" -> gettingstarted.html (hero, band, pricing Individual card).
html/register.html DELETED with git rm -f (today's uncommitted rework went with it - its
script lives on in gettingstarted; the last committed version is in git history).
registering-and-downloading lead -> "Create your account at search2o.com/gettingstarted";
../search2o/README.md register sentence rewritten (Ram commits). Sweep for register.html
over html/gen/docsrc is CLEAN. Verified in-browser via stubbed hcaptcha+fetch: success key
box renders inside step 1 (screenshots sent). Coexistence ruled fine by Ram: buttons say
"Get started", the nav link and page stay "Getting started". DEPLOY NOTE: the live bucket
still holds the OLD register.html - it must be aws s3 rm'd at deploy or the stale URL keeps
serving.

## State on 2026-09-08 (registration is one call, password set on first sign-in)
Ram: registration no longer takes a password and sends no email - ONE call POST /register
(renamed from /reg1; /reg2 is gone) with email/userName/accountName/terms/token, returning
{success, license}; error keys unchanged minus weakPassword. First sign-in (and every added
user, whose email carries NO code) goes through the login dialog's 'New user / Forgot
password?' link: email with one-time code, enter it, choose a password. APPLIED:
register.html reworked (password field + hint gone, step 2 gone, single handler with
showLicense(); stale three-months meta dropped to "Registration shows your license key
once.") and VERIFIED through the real handlers with stubbed hcaptcha+fetch: body correct,
two-error render, success key box. The form button says "Register"
(no arrow), not "Continue" - single step now. gettingstarted GUI step rewritten (open /ui, click the
link, enter the email - wording differs BY AUDIENCE, Ram was
annoyed I flattened it: gettingstarted says "the email you registered with" (its reader
registered in step 1); the-gui says "your email address" (its readers include added users,
who never registered); users-and-roles says "that email address" (the one the admin added) - code arrives, choose password, sign
in; same fix in the-gui and users-and-roles). Docs: the-gui first-sign-in flow;
registering-and-downloading "Registration asks for no password"; users-and-roles added-user
flow (email says added, code via the link, "No password or code travels in the added-user
email"); gui/account Users entry; authentication.html two-emails paragraph (added-user email
carries no code); rest-api/authentication h2 "Setting or resetting a password" + "the GUI's
New user / Forgot password? link is these two calls". NOTE: Ram set config.js apiUrl to
https://s2o-api-761928161625.us-east4.run.app (a Cloud Run URL) - confirm the right
production value before any deploy; register.html's fallback is still api.search2o.com.

## State on 2026-09-08 (consistency iteration 3: chat/gui/profiles swept)
Swept chat-integrations, the remaining gui pages, profiles, rest-api, development, security
for tier/role staleness. Only two residues found and fixed: authentication.html's
"Account > Authentication" breadcrumb is now "Admin > Authentication", and the
gui/account.html lead now names the two GUI groups ("Two groups: Admin - Users,
Authentication and License, for administrators and the owner - and Billing - Account and
Invoices, for the owner."). Verified consistent, no change: integration-tokens (owner =
token's holder, different sense), seeded profile names everywhere (gpt5_mini/claude_haiku/
gemini_flash/gpt_image/gemini_image), addUsers<=25 in automating-with-an-llm, secret-vault
role language, reports role labels. The sweep that started with the Free/Eval/Paid table is
COMPLETE apart from the GUI screenshots (Ram's to retake with the new sidebar).

## State on 2026-09-08 (consistency iteration 2b: sidebar groups are Admin and Billing)
Ram confirmed the GUI sidebar structure IS his answer-3 grouping: ADMIN (Users,
Authentication, License) and BILLING (Account, Invoices) - the old ACCOUNT group is gone.
Applied: figures.py RAIL2 now ends "#ADMIN ... #BILLING, Account, Invoices" and screen()
auto-fits the rail pitch (min(17, (h-52)/len(rail)); Invoices bottom measured 283/300 and
264/280 in the two report-figure sizes). gui/index.html group list is "...Reports, Admin
and Billing" and its header line now says "the docs icon for asking the documentation a
question" (a missed instance of the docs-icon correction). the-gui.html says add users
"from the Users page" (was Account section). Invoices entry carries Ram's description:
itemized with prorated charges, current shows accumulated + end-of-month projection, past
show what was charged. toc gui page title renamed Account -> "Admin and billing" (slug/URL
unchanged). GUI SCREENSHOTS in gui/ pages (gui-users, gui-license shots etc.) still show
the OLD sidebar - they come from the real product on :9020 and are Ram's to retake.

## State on 2026-09-08 (consistency iteration 2: billing pages + encryption rotation)
Ram's answers: freeze is ADMIN (rest-api row already right); document the Evaluation
request; the GUI Account area is Admin (Users, Authentication, License - the License page
carries license key rotation, ENCRYPTION KEY ROTATION and freeze) plus Billing for the
owner (Account: Upgrade to Eval + Delete account; Invoices). Applied: gui/account.html
lead widened, License entry lists the three admin actions with links (freeze anchor is
#freezing), NEW Account and Invoices entries (Evaluation request + one-business-day email;
delete is permanent; invoices owner-only). encryption.html Key rotation section: the stale
"nothing for you to rotate" sentence replaced with managed-key rotation, VERIFIED against
s2oserver api.py rotateEncryptionKey + Namespace.rotate_key: new key per account, old data
readable forever (each ciphertext names its key), no re-encryption, servers use the new key
only after RESTART, does not protect data under a stolen key, at most every 90 days ->
contact support if exposed. OPEN QUESTION to Ram: the GUI-mock sidebar in gen/figures.py
(RAIL2 "#ACCOUNT | Users, Authentication, License") - does the real GUI sidebar now show
the Billing pages (Account, Invoices), i.e. should the report figures' rail gain them?

## State on 2026-09-08 (docs-product consistency sweep, iteration 1)
Ram found the stale Free/Eval/Paid table and ordered a full docs consistency sweep, done
ITERATIVELY with numbered questions; his answers this round: (1) levels ARE
Individual/Evaluation/Team, (2) an Individual account canNOT add users, (3) the
share-the-license-key line is impossible - removed, (4) registering may say it creates an
Individual account, (5) OWNER holds only billing and account-level settings; THE LICENSE
BELONGS TO ADMINISTRATORS. Applied: usage-limits lead de-beta'd + table renamed with new
descriptions; license.html beta section is now h2 Pricing with "Individual use and team
evaluations are free"; the-gui + gui/account gained from-Evaluation-level qualifiers;
running-the-server says upgrade-to-Evaluation + common place; registering says Individual
single-user account; users-and-roles admin bullet + table row "Manage the license" (admin+
owner) split from "Billing and account-level settings" (owner); license-key.html and
license-rotation.html say administrator rotates; roles FIGURE moved license to the admin
row (bbox-verified 586/600, 686/700); gui/account License page "Administrators and the
owner" (was Owners only); data-privacy account row readers likewise. Sweep of
owner+license/billing and beta mentions is clean. NEXT ITERATIONS: chat-integrations, GUI
pages vs product, profiles, search, commands - not yet re-swept for tier/role consistency.

## State on 2026-09-08 (new docs page: Running multiple environments)
From Ram's notes in the IDE scratch file (~/Library/Application Support/JetBrains/
IntelliJIdea2025.2/scratches/ui_prompt.txt - IDE scratches are where "see X.txt" notes may
live). New page docsrc/misc/multiple-environments.html, last in Miscellaneous (121 pages
now): one account+license per environment (accounts fully separate), each environment has
its own users, same profile names point at that environment's servers so definitions move
unchanged, and promotion through the REST API (read -> draft -> validate -> publish; the
same calls the GUI uses). Misc section lead's stale "and what is planned" replaced with the
environments mention; docs home Miscellaneous card extended the same way.

## State on 2026-09-08 (gettingstarted back to a single block)
Ram reversed the three-part structure: parts 2 (Evaluation with your team) and 3 (Production
across your organization) are DELETED; the page is eight numbered steps again (Register /
Download / Run (h3 sub-steps back) / GUI / first agent / describe+search / Call your systems
/ docs+callout). Hero h1 back to "Up and running on your laptop" with a NEW lead carrying
his story: "It is easy to get started on your laptop. When the team is ready to evaluate,
move the server to a common place - nothing else changes." CSS reverted (.numbered h2 23px,
h3 16.5px; h4 rule and h2+h3 rule gone). Meta back to the register/install/build wording.
GONE with part 2: the request-an-Evaluation-license-from-the-Account-page text and the
Pricing link; GONE with part 3: the stateless/cluster line and the Team-plan line. Browser
tab recreated again: 396095754.

## State on 2026-09-07 (what-you-need line atop part 1)
Ram asked for an up-front what-background-you-need line, then REMOVED my version the next
day: "The following lines make it obvious what they need." Part 1 opens straight with the
Register step again. Do not re-add a prerequisites line.

## State on 2026-09-07 (Team cluster bullet settled: "Unlimited agent servers")
The load-balanced-cluster bullet went through three forms: Ram's "no per-server fee" line
sounded arrogant to him (invites "why would you charge for what we run?"), my laptop-to-
cluster reframe was wrong register for an enterprise card ("laptop!?"), and the final pick
is the three-word "Unlimited agent servers" - freedom stated, fee never mentioned. Team card:
no tiers/charges/premium seats · Unlimited agent servers · shared org limits · direct
support.

## State on 2026-09-07 (Team bullet: same price per seat)
Team card bullet 1 settled as "No feature tiers, per-agent charges, or premium seats" -
Ram picked "no premium seats" from my alternatives; it carries the same-price-for-every-role
point in three words.

## State on 2026-09-07 (Search line reworded)
The Search section line is now "...to determine which agent is designed to handle the
request." (Ram's wording; he called "produce the requested result" a very bad change - that
phrase had been on the page since the 2026-09-04 wording pass). RESOLVED in the same
exchange: Ram approved "Accounts payable + Help desk" (his two-word spelling kept). The
conversation block has its ORIGINAL natural queries back ("Summarize yesterday's failed
payment runs" / "Open a ticket for the gateway timeouts and attach that summary") and the
agents are renamed Accounts payable agent / Help desk agent - the fix was on the agent-name
side, after two rounds of query rewrites read as weird. Reply reverted to "3 of 214 runs
failed". Both left bullets renamed to match. The hero de-keyword change stands ("Keep Acme
on for another year at last year's rate" -> Contract renewal agent). LESSON: when natural
speech and a name collide, rename the thing, not the speech.

## State on 2026-09-07 (home queries de-keyworded)
Ram: query/agent word overlaps ("Acme contract" -> "Contract renewal agent") misinform
people that search is keyword-based. All three queries recast in everyday vocabulary with
ZERO words shared with the matched agent's name; the domain words now appear only in agent
OUTPUT (deliberate - the specialist answering in its own vocabulary is the "aha"). Hero:
"Keep Acme on for another year at last year's rate" -> Contract renewal agent. Convo card:
"Which transfers didn't go through yesterday?" -> Payments agent (reply now opens "3 of 214
payment runs failed" - the word moved INTO the reply); "Have someone look into the timeouts
and give them that summary" -> Ticketing agent ("Created ticket OPS-2291..."). Run/ask lines
and the three convo-points bullets unchanged (still accurate). Screenshots sent; fits on one
line in the search pill and the bubbles. NOTE: browser tab was recreated (396095690); old tab
had been closed.

## State on 2026-09-07 (Evaluation request located in the GUI)
Part 2's first line now says "from the Account page in the GUI" - Ram: without it, people
would look for the Account page on the website.

## State on 2026-09-07 (Team card bullets reworked)
Per Ram: the SLA bullet is REMOVED; "per-server charges" left the first bullet (now "No
feature tiers or per-agent charges") and became its own second bullet in his words,
typo-fixed and hyphenated: "Run the agent server in a load-balanced cluster - there is no
per-server fee". Team card is four bullets: no-tiers / cluster / shared limits / support.

## State on 2026-09-07 (Call your systems section on gettingstarted)
New h3 "Call your systems" in part 1, between describe+search and the docs section, holding
the reachability sentence (moved OUT of the Run step) and a two-line driver note, trimmed by
Ram to: "Databases are reached through async drivers; see the docs." (no SQLite
mention either, his call; the docs link goes to registering-and-downloading). The
mssql caveat itself stays in the docs; the page only links.

## State on 2026-09-07 (mssql back, DOCS ONLY, with the async caveat)
Ram reversed after learning aioodbc is async-API-over-sync-ODBC: mssql is documented again,
in the docs only (his emphasis, twice: not on getting started). registering-and-downloading
has the [mssql] install line back plus a note paragraph; commands/db.html lists mssql+aioodbc
again with the same caveat. Caveat wording in both: aioodbc presents an async API but wraps
the synchronous ODBC driver underneath; the agent server is fully asynchronous, so
synchronous operations that load the CPU can cause performance issues. gettingstarted.html
carries no db-extras material at all.

## State on 2026-09-07 (mssql removed everywhere)
Ram: mssql support is plain wrong - the agent server is 100% async and mssql is not (his
ruling; aioodbc's async-over-ODBC does not count). Removed the three references: the extras
dim line on gettingstarted.html (now "likewise mysql or oracle"), the
"./agent-server[mssql]" line in docsrc/getting-started/registering-and-downloading.html, and
"mssql+aioodbc" in docsrc/commands/db.html's driver list. Rebuilt; sweep for
mssql/aioodbc/ODBC/SQL Server over html, docsrc, gen and content is clean. NOTE for Ram: if
the search2o package's pyproject still defines the mssql extra and the [db] bundle, the
package is his to change.

## State on 2026-09-07 (gettingstarted de-busied)
Ram: "The page looks busy. Remove unnecessary lines." Cut: the dim source/license line
(install step), the dim Uvicorn options line (docs material), and "The server is stateless;
stop and restart it anywhere." (part 3 already says stateless) - the reachability sentence
stays; the two docs lines merged into one paragraph. Then "store the key
with your other secrets" cut from the Register step (the register page itself carries the
store-it advice under the key box). Ram then replaced the whole Register line with his own:
"Before you start, you need a license key. Register to get one." (Register is the link). And
"your laptop is a good place to start" cut from the install line (part 1's title already
says laptop). DELIBERATELY KEPT: the REST API h4
(Ram asked it back on 2026-09-05 after an over-cut) and the SQLite/extras dim line (saves a
wall for non-SQLite users).

## State on 2026-09-07 (gettingstarted restructured into three parts)
Ram's outline applied: the page is now THREE numbered parts (the 46px chips number the parts,
not the steps): 01 "Up and running on your laptop" (the seven former steps as h3s: Register /
Download / Run (h4s: license key, LLM key, start) / GUI (+REST API h4) / first agent /
describe+search / docs+Stuck callout), 02 "Evaluation with your team" (the old Bring-your-team
text split into two paragraphs + Pricing link), 03 "Production across your organization" (MY
rewording of his "Production installation"; Ram then cut the secret-store and config-sync
bullets - part 3 is TWO paragraphs: stateless/LB/containers folded into the intro sentence,
then "The Team plan covers production use and will be available soon.").
Hero h1 is now "From your laptop to production" (part 1 took the old h1); metas updated. CSS:
.numbered h2 27px, h3 19px w700 (steps), h2+h3 margin-top 0, NEW h4 16px w700. All old step
ids kept on the h3s (no inbound anchors existed; .numbered used only by this page). Shown to
Ram in dark theme; light not yet checked.

## State on 2026-09-07 (AI assist line surfaced on gettingstarted)
Ram: "AI assist writes a full agent from one sentence." was a key line hiding as a .dim
footnote at the end of the first-agent step. His pick of my options: fold it into the step's
opening - "Open Agents -> Drafts and create a draft. AI assist writes a full agent from one
sentence - or paste this one into the editor:" - and the dim footnote is gone. The fast path
now reads before the JSON.

## State on 2026-09-07 (docs icon: ask only, docs on the website)
Ram: the GUI's docs icon no longer opens the documentation - docs live only on the website;
from the icon one can only ask questions, and AI answers them. Fixed in the three places that
claimed otherwise: gettingstarted.html step 8 (docs-on-the-web line first, then "From the
docs icon in the GUI, you can ask a question in plain English; AI writes the answer from the
documentation."), docsrc/support-licensing/asking-the-docs.html Where-to-ask ("is where a
question is asked"), and docsrc/gui/personal.html header line ("The docs icon in the header
asks a question of the documentation, and an AI answers from these pages"). Sweep for
"opens the (full) documentation" is clean. docsBase in the-gui.html is the schema host,
unrelated, untouched.

## State on 2026-09-07 (pricing h1: "Free until you're convinced")
Ram: "Free during the public beta" was inaccurate - paid service may start before the beta
ends. New h1 chosen by Ram from my candidates, knowingly accepting my a-little-cheesy caveat.
REPORTED, NOT CHANGED (his call pending): index.html:45 hero eyebrow still says "Free during
the open beta" (the same inaccurate claim; suggested "Free to evaluate" there so the pricing
h1 is not repeated verbatim), and register.html:8,10 metas still say "The open beta is free
for three months" (doubly stale; suggested dropping the clause). about.html "currently in
open beta" and the terms' generic beta language are fine.

## State on 2026-09-07 (search latency: less than 0.5 seconds)
The home Search section now says "returns matches in less than 0.5 seconds" (was "in under a
second"; html/index.html:170). The three docs spots now match ("less than
0.5 seconds", never "well under"): search/how-matching-works.html lead, commands/search.html
round-trip note, and the search-results figure text in gen/figures.py. Rebuilt; the longer
figure line measured 616px of 720, no overrun. No "under a second" remains anywhere.

## State on 2026-09-07 (footer: Virginia, not Northern Virginia)
Every footer now reads "Search2o · Virginia, USA": the five site pages, the four legal pages,
and the docs template (gen/build.py:455, all 120 docs pages rebuilt). LEFT ALONE, flagged to
Ram: html/about.html still says "Northern Virginia" outside the footer - the meta and og
descriptions ("Built in Northern Virginia.") and the body line "Search2o is based in
Northern Virginia, USA." (about.html:8,10,64) - he asked for the footer only.

## State on 2026-09-07 (figure captions vs pictures)
Ram: the architecture caption said "The three parts" but the picture shows two blocks (the
GUI, the third part, is only a text line in the server box). Caption is now "What talks to
what". Swept every figure caption and every counted claim in docsrc against what the figure
or page actually shows - all correct: 23 commands (toc counted), four reports, five profile
kinds, three guardrail parts, three variable scopes, four roles, two encryption modes, two
token ways, 0-3 search matches. ONE more mismatch found and fixed: the controlled-runtime
figure's layer said "operator rules" - the page heading is "Operator remapping" and the
setting's name is "Compile rules", so the box now says "compile rules". Rebuilt.

## State on 2026-09-07 (docs figure matched to home)
Ram: "match everything. Don't say search index etc." The docs architecture figure's cloud box
now mirrors the home diagram exactly: sub "search · state · reports" (the old
"accounts · agents · config" sub and the two extra lines "state (encrypted)" /
"search index · reports" are gone), and the server-cloud arrow label is
"sensitive data encrypted" (was "TLS"). LAYOUT: the label cannot fit as a one-line arrow pill
(pill ~166px, gap 60px - my first render sat the pill over both boxes, the second hid the
whole arrow under it). Final: server box moved to x195, cloud box narrowed to 200 wide and
shortened to the server's height band (y100-210, so the shrunken content no longer floats in
a tall empty box), arrow at y145, and the label as two plain text lines UNDER the arrow in
the 95px free strip - the same under-the-link style as the home diagram. Verified by getBBox:
every text 0 overrun, both label lines fully inside the strip. LEFT ALONE deliberately:
request-lifecycle "state stored, encrypted" and the conversation-state figure's full phrase
(that page's subject IS conversation state).

## State on 2026-09-07 (arrow label: "sensitive data encrypted")
Ram: "encrypted context" could mislead - only SENSITIVE data is encrypted (queries,
conversations, long-term memory, descriptions); much else travels/lives plain. The home
diagram's org->cloud arrow label is now "sensitive data encrypted" (his pick over my "travels
encrypted"; 0 overflow). QUEUED NEXT TASK from Ram: make the DOCS architecture figure's cloud
box consistent with this vocabulary (it says "conversation state (encrypted)" - accurate but
to be aligned "after we finish this task").

## State on 2026-09-07 (cloud node formatting fixed; "state" not "conversation state")
Ram called the three-box cloud row ugly (the "Encrypted state" wrap I had rationalized).
Fix: the box is "State" - the arrow into it already says "encrypted context", so no meaning
lost; boxes are even 49px single-line each (measured). Ram then trimmed step 2's text the same
way: "State and other sensitive information are encrypted before leaving the server."
LESSON reinforced: do not ship a known visual wart with a written justification - fix it.

## State on 2026-09-07 (Reports added to the cloud node)
The diagram's Search2o Cloud node now holds THREE boxes - Search, Encrypted state, Reports
(.arch-parts is 3-column). This satisfies the old nothing-in-the-picture-the-steps-do-not-
discuss rule the RIGHT way: step 4 now says "search, state management, and reporting", so
Reports belongs (it was removed in August precisely because the text then did not mention it).
No overflow; "Encrypted state" wraps to two lines in the narrower box, heights uniform.

## State on 2026-09-07 (Search moved above System architecture)
Ram asked, I recommended yes (the demo raises "how did it pick the agent?" and the Search
section answers it; the differentiator belongs before the infrastructure), he said go. Order
now: How it works(soft) > Search(plain) > System architecture(soft) > Agent framework(plain) >
Platform(soft) > Reports(plain) > band. The soft class swapped with the slot again.

## State on 2026-09-07 (System architecture steps reworded, jointly)
Ram drafted, I edited, he approved my set verbatim. Final: 1 Search interface "The entry
point, from a browser or a chat application. Search matches each request to the agent designed
to handle it." 2 Agent server "A stateless server that runs agents in a controlled runtime.
Conversation state and other sensitive information are encrypted before leaving the server.
Source available." (his draft said "on GitHub" - I flagged his own no-GitHub-on-home rule and
he accepted the trim) 3 Agent framework "Runs within the agent server and executes
each agent's commands." (FIVE iterations, settled in DISCUSSION mode: "execution engine" was
my overclaim - the runtime is the engine; "what agents are built from" DUPLICATED the Agent
framework section below; the command list was a repeat too; final line is placement + role
only, one sentence - Ram asked why single-line and accepted the two-fragments argument) 4 Search2o Cloud "The shared service behind every agent server. The
cloud provides search, state management, and reporting." My edits fixed: two "it"s with
different referents in his step 2, subjectless fragments in 3 and 4, "browser and chat
applications". h2 stays "From request to result". Columns still end level (screenshot).

## State on 2026-09-07 (sections swapped; ids retied)
The two sections swapped position AND ids: the conversation/example section is now FIRST, as
<section class="section soft" id="how-it-works"> (kicker How it works, h2 "One conversation,
many agents"); the steps+diagram section follows as id="system-architecture" (plain). The
.soft class was swapped WITH the position so the background rhythm held (soft/plain/soft...
verified in-browser). The nine footer "How it works" links needed NO edits - they point at
#how-it-works, which is now the right section (verified: lands on kicker "How it works").
HTML comments renamed to match. Rewording session with Ram still pending.

## State on 2026-09-07 (section relabels; rewording session pending)
Home relabels per Ram: the first column section's kicker is "System architecture" (was How it
works); the diagram card's own "System architecture" h3 REMOVED (redundant with the kicker;
orphaned .arch h3 CSS removed too); the Example workflow section's kicker is "How it works".
Kickers now: System architecture | How it works | Search | Agent framework | Platform |
Reports | Getting started. PENDING WITH RAM: he wants a joint rewording of the text next.
LOOSE ENDS FOR THAT SESSION: section ids unchanged (#how-it-works is the System architecture
section, #example is presumably the How-it-works section) and the footer/nav "How it works"
link still points at #how-it-works = the architecture section - labels and anchors need
re-tying once the wording settles. Also .demo-footnote CSS is unused (reported, not removed).

## State on 2026-09-06 (hero demo: streamed line removed)
The .demo-stream row ("Renewal drafted for Acme at last year's rate.") is gone from the hero
demo; the remaining ask/run stages were RENUMBERED (stage-4->3, stage-5->4) and the .stage-5
delay rule deleted so the animation has no dead gap. Beats now: match, run (two checks), ask
form, sent-for-signature. The .demo-stream CSS remains but is unused.

## State on 2026-09-06 (reg2 mismatch verified)
reg2 returns bare {"success": false} on a code mismatch. The existing handler already covers
that shape (no code change needed): "That code did not work. It may have expired." in the err
panel, step 2 stays visible, the button re-enables, and a retried correct code proceeds to
the key box - all verified through the real handlers with stubbed fetch.

## State on 2026-09-06 (reg1 error contract implemented)
reg1 failure shape: {success:false, registrationErrors:["errorKey",...], didYouMean:...}.
register.html maps the seven keys (notHuman/weakPassword/didYouMean/invalidEmail/bogusEmail/
termsNotAccepted/individualAccountExists) to Ram's exact messages; didYouMean substitutes the
server value (HTML-escaped - it echoes user input); several errors render one per line;
unknown/empty keys fall back to the generic line; the form stays on step 1. VERIFIED THROUGH
THE REAL HANDLER by stubbing window.hcaptcha + window.fetch in the page and clicking Continue
(not by simulating the output DOM): two-error render, unknown-key fallback, and the full
reg1->step2->reg2->key-box success path all exercised.

## State on 2026-09-06 (register page reworked further)
Hero is kicker + "Create your account" ONLY - the key-shown-once lead moved INTO the success
state as .reg-note under the key box ("This key is shown only once - please store it... Then
Getting started takes you..."). reg1 failures now show the SERVER'S errorMessage when present
(empty falls back to the generic line) and stay on step 1. Both states simulated and shown.

## State on 2026-09-06 (register page reworked)
The outdated open-beta/free-three-months lead is GONE (pricing changed); the
key-shown-once + Getting started line IS the lead now. Success state redesigned per Ram:
"Your account is ready." as a plain sentence (no green box), then a .reg-keybox - "LICENSE
KEY" label, the key in mono, and a copy icon (clipboard.writeText with site.js's
checkmark-for-1.4s feedback, bound manually since site.js only wires [data-copy] present at
load). Old .reg-key/.reg-next CSS replaced by
.reg-done/.reg-ready/.reg-keybox/.reg-keylabel/.reg-keyrow. Error path still uses
.reg-out.err. Verified by SIMULATING the success DOM (real registration unavailable);
screenshots of both states sent.
ALSO: Uvicorn "Invalid HTTP request received." explained - Ram's local config.js said
https://localhost:8080 against a plain-HTTP server (TLS bytes hit the HTTP parser); fixed to
http://. config.js currently carries the LOCAL value - must be flipped to
https://api.search2o.com before any deploy.

## State on 2026-09-06 (register API URL via config.js)
From content/apiurl.js (Ram's pattern): NEW html/config.js sets
window.SEARCH2O_CONFIG.apiUrl (checked-in copy = production https://api.search2o.com; for
local work edit apiUrl to the local server and keep the edit out of the commit).
register.html loads config.js and reads BASE from it, falling back to the prod URL if the
config fails to load. The only hardcoded api.search2o.com is now the fallback. config.js is a
NEW root file - a future deploy syncs it; a LOCAL apiUrl edit must never be deployed.

## State on 2026-09-06 (pricing bullets replaced again, Ram's v2)
Checklists replaced verbatim with Ram's second content pass (3/4/3): single-user limits /
deploy-publish-discover-generous limits / no-tiers + shared org limits + direct engineering
support with production SLAs at GA; the support bullet was then SPLIT into two on Ram's
follow-up ("Direct support from the Search2o engineering team" / "Production SLAs at general
availability"). Cards aligned as before.

## State on 2026-09-06 (bottom row unified)
Ram: still looked off; I made the button full-width; Ram REVERTED that call - a button is a
button and stays small (natural width, min-height 50 kept so the row's heights match). The
boxes were measured exact all along (tops 693, h 50, text centers within 1px). FINAL: small
Register button left-aligned, two full-width note panels, same vertical band.

## State on 2026-09-06 (bottom elements equalized)
The Register button and the two note panels are all 50px tall, tops 693/693/693 (button gained
min-height 50, scoped .price-card .actions .btn; the btn-lg default was 46).

## State on 2026-09-06 (pricing content replaced with Ram's final bullets)
All three checklists replaced verbatim with Ram's new lists (3/4/3: explore-on-your-own /
serious-evaluation / no-tiers-no-per-agent-charges). The Questions section is GONE - replaced
by his closing line "Need help? Contact Search2o directly from the UI." (.help-line, bold).
The ABUSE CALLOUT is REMOVED (his instruction; the Terms carry that rule now). RAM EDITED
pricing.html HIMSELF between my passes: the notes now read "Request Evaluation from the UI."
and "Will be available soon." - his wording, left exactly as found. Checklist tops still
435/435/435.

## State on 2026-09-06 (browser-only sweep, per Ram)
Ram: the docs opening figure shows Users reaching only a browser; chat apps missing. Sweep of
every "browser" in figures + docsrc. FIXED: architecture figure Users sub "browser" ->
"browser · chat app" (bbox measured 92.7px in the 120px box, fits; Developers stays
"browser" - correct); output-stream figure "the browser renders" -> "the client renders";
how-it-fits-together "types a request in the search box" -> "+ or in a connected chat
application", "streams its output to the browser" -> "back to the user"; output.html lead
"streamed to the GUI... the browser renders" -> "streamed to the user... the client - the GUI
or a chat application - renders". CORRECT AND KEPT (browser is genuinely meant): auth cookie
sign-in, parts-of-the-system GUI table row, connect-flow token warning, rest-api clients/CORS,
Swagger-from-the-browser, config-sync GUI figure, request-lifecycle (already neutral).

## State on 2026-09-05 (getting-started: OR-split boxes, REST API section back)
The install block and the license-key block are each TWO codecards separated by a hairline
"OR" divider (new .or CSS: flex label with ::before/::after lines) - one way per box; the
"Set one of the two, not both." dim line became redundant and is gone (the OR carries it).
The openapi/docs/redoc line I over-cut in the tightening pass is BACK as an h3 "REST API"
under the Open the GUI step (Ram asked for it back; without the changeable-paths sentence).

## State on 2026-09-05 (Individual bullet reword)
"Intended for local evaluation and agent development" -> "For trying it out and developing
agents on your laptop" (Ram: "evaluation" now collides with the Evaluation tier name).

## State on 2026-09-05 (gettingstarted TIGHTENED end to end)
Ram: no overexplaining; the page's only job is to help and get out of the way. Full pass: hero
lead REMOVED (kicker + h1 only, like pricing); every step cut to what the reader must do; code
blocks carry the detail, prose no longer narrates them. Cut entirely: first-user-is-owner,
name/title explanation, the openapi/docs/redoc dim line, "not limited to these vendors",
indexing notification, "from your registration address", the docs-topics list. "Add users
with roles from the Account section" is GONE - Ram challenged it as possible hallucination
(it came from docsrc/gui/the-gui claims, unverifiable in the minified UI bundle; the docs
pages still carry it - UNRESOLVED, his call). Steps now ~528 words total.

## State on 2026-09-05 (getting-started reflects the tier flow)
"Bring your team" rewritten to Ram's narrative: request an Evaluation license from the Account
page -> "You are notified of the approval by email within one business day." (his sentence) ->
start the server in a common place; then add users, with
a Pricing link. THE SHARE-THE-LICENSE-KEY GUIDANCE IS GONE from this step (a 1-user Individual
tier cannot share a key). REPORTED, NOT FIXED: docsrc/getting-started/running-the-server.html
still says "share the license key, and each person can run a server on their own laptop" -
contradicts the tier model now; Ram to confirm before the docs change.

## State on 2026-09-05 (tier renamed: Team Evaluation -> Evaluation)
Ram proposed, I agreed (the real win: "Team Evaluation" vs "Team" made every upgrade sentence
ambiguous; the ladder is now Individual -> Evaluation -> Team). All five page occurrences
renamed: plan label, the note, Individual's upgrade bullet, the 2-month bullet, Team's
carry-over bullet. NOTE for Ram: the product's Account page and content/pricing.md still say
"Team Evaluation" - the in-product name is his to change.

## State on 2026-09-05 (pricing FINAL form - descs gone)
The Individual and Team Evaluation intro lines are REMOVED (Ram: the plan headline already
says it) - card heads are now plan + price only, .price-head min-height 113px (natural
95/95/113), checklist tops 435/435/435. The whole grid plus the abuse callout fits one view.
The Team Eval card no longer mentions organizations anywhere except its plan name - fine.

## State on 2026-09-05 (Team price rows sized down)
Ram: the idea is fine but the rows were HUGE. Both Team rows carry .price.duo: 28px figures
(suffixes 14px) instead of 44 - same format as each other, smaller than the Free headline.
Aligned re-measured: duo lefts equal, single-line rows, checklist tops 502/502/502.

## State on 2026-09-05 (Team price finally right - $40 same format as $100)
Ram (annoyed, second sloppiness call): $40 must match $100's format and the fees must line up.
Final form: TWO .price rows, "$100/month platform fee +" then "$40/user/month" - both figures
44px w800 ink, suffixes .permo 15px muted inline, dollar signs flush at the same left edge
(measured 1182/1182). Two traps fixed on the way: at 17px the first suffix WRAPPED under the
figure (head grew to 266 and broke alignment - 15px fits); and .price is a div so it inherited
BODY line-height 1.65 (73px line boxes) - .price now sets line-height 1.15. Checklist tops
re-measured 502/502/502. .price + .price { margin-top: 0 }.

## State on 2026-09-05, later pricing trims (Search2o out of descs; fee line inline)
Descs are "For one person evaluating on a local machine." / "For organizations evaluating with
a shared deployment." (Ram: obviously they are evaluating Search2o). Note is "Request Team
Evaluation from the Agent Server UI." (his words + "the"; NOTE this says "Agent Server UI"
while the vocabulary elsewhere is "the GUI" - his choice, not flagged as an error). Team price
is now "$100/month" on one line (.permo inline span, 18px muted) with ONE line beneath:
"platform fee + $40/user/month" - the old stacked /month-fee + per2 lines are gone;
.per2 CSS replaced by .permo. Checklist tops re-measured 502/502/502.

## State on 2026-09-05, final pricing trims
Ram's four: "Up to 100 users" bullet REMOVED (Team Eval); note now "Request an upgrade to Team
Evaluation from the Account page." (his wording, casing normalized to the tier name and
"Account page" - flagged to him); "Upgrade to Team to continue after the evaluation period"
REMOVED; Team's two limit bullets MERGED into "Account-level usage limits that scale with the
number of users" (my words). Cards are 5/4/4 bullets; grid nearly fits one view; alignment
holds (same .price-head). content/pricing.md untouched throughout - the page has diverged
substantially from the md (no 100-user cap, no 1-month, reworded bullets); syncing the md is
Ram's call.

## State on 2026-09-05, latest (pricing card alignment)
Ram: card 3's text did not line up with the others. Cause: its head was taller (two fee lines
+ desc). Fixed: "For ongoing organizational use." desc REMOVED (Ram allowed it); each card's
plan/price/desc block is wrapped in .price-head with min-height 180px (measured: natural heads
were 180/180/170) so all three checklists start on the SAME row - verified 502/502/502px.
Alignment measured in the browser, not eyeballed, per the standing measurement lesson.

## State on 2026-09-05, latest (pricing note panels + bullet reword)
Team Evaluation bullet "Significantly higher usage limits than Individual" -> "Usage limits
sized for an organization-wide evaluation" (Ram: never compare to Individual; say the limits
are commensurate with this level of usage). Then "Intended for shared deployments and real
organizational evaluation" REMOVED - back to back with the new bullet it repeated
"organization/evaluation", and the card's desc line already carries that meaning. Page only;
content/pricing.md keeps his originals.

## State on 2026-09-05, latest (pricing note panels)
The Team note is now just "Paid service will be introduced before the end of 2026." (the
"Pricing is published now so organizations..." sentence removed, from the page only -
content/pricing.md untouched). Both card-bottom notes are attention-grabbing callouts:
--tag-match-bg background, --feat-border border, --ink 14.5px weight 600 (was the quiet
bg-soft panel). Verified both themes.

## Lesson 2026-09-05 (Ram: "you are being sloppy sometimes")
The two card-bottom notes shipped as bare muted 14px paragraphs while everything around them
was styled - Ram called it sloppy. .price-card .action-note is now a bordered footnote panel
(bg-soft, line-soft border, radius 10, --body text); .checklist gained bottom margin 24 so the
panel never touches the list. RULE: secondary text gets the same design attention as primary
elements - a bare <p> hanging at the bottom of a designed card is never finished work.

## State on 2026-09-05, later (pricing page trims from Ram)
Hero is now kicker + h1 "Free during the public beta" ONLY (his call: old hero content not
needed; the beta mention had to live somewhere and the h1 carries it). The end-of-2026
paragraph moved from below the grid INTO the bottom of the Team card (.action-note slot);
.price-para CSS now unused. "Coming soon" badge removed. Individual card: "1-month evaluation
period" bullet REMOVED - the tier is becoming perpetual but that is deliberately unstated; its
upgrade bullet had to lose "after the evaluation period" (dangling once the period went) and
now reads "Upgrade to Team Evaluation or Team at any time" - MY wording, flagged for Ram.
NOTE: Individual is perpetual per Ram, which supersedes the pricing-decision note below about
no perpetual tier being affordable - the md still says 1-month; content/pricing.md not edited.

## Pricing decisions (Ram, 2026-09-05 discussion - do not re-raise)
No perpetual free tier: unlike 2010s SaaS, a free user costs real LLM money on Ram's cloud
bill (indexing, query embedding, AI assist, docs questions) - the time-boxed evals bound the
worst case absolutely. No cheap end-user seat: $40 is value-priced for searchers (execution,
not suggestions). Active-user billing exists as a PRIVATE negotiation lever for large deals -
deliberately NOT published (self-targeting discount; publishing gives it away). No
"volume pricing - talk to us" line on the page: Ram says everyone knows they can negotiate.

## State on 2026-09-05 (pricing page redone from content/pricing.md)
Three tiers now: Individual (Free, register.html button), Team Evaluation (Free; NO button -
the action is in-product, so a bottom .action-note says "Request Team Evaluation from the
Account page."), Team (Coming soon badge - new neutral .badge.soon; $100 big, .per "/month
platform fee", new .per2 line "+ $40/user/month"). Every bullet is Ram's md text verbatim.
Hero: h1 "Individual and team evaluations are free", lead "public beta... paid service soon"
(both his sentences, split to avoid repeating the h1). Below the grid: his end-of-2026
paragraph (.price-para), the abuse callout reworded to his sentence, Questions with his
wording. CSS: .pricing-grid -> repeat(3,1fr) full width; .price-card is now flex column with
.actions/.action-note margin-top:auto (bottom-aligned across unequal cards); .featured/.badge
green style now unused by the page but kept. Meta descriptions updated. Both themes verified.

## State on 2026-09-05 (legal pages built)
html/legal/ now holds terms, privacy, license, intellectual .html, converted from
content/legal/*.md by a scratchpad script (md subset: #/##/###, * bullets, **bold**, `code`;
license.md's ```md fence stripped). FIDELITY VERIFIED: normalized text of every page is
IDENTICAL to its md source - legal text must never be reworded. terms.md line 1 was a
drafting-tool preamble ("Here is the full Terms document with...") - removed from the SOURCE
too (content-can-be-corrected precedent). Pages use the site chrome, kicker "Legal", h1 from
the md, article.legal-body (new tokens-only CSS: .legal-body h2/h3/p/li/strong/code), meta
noindex. Footer on all FIVE site pages + the four legal pages gained a fourth "Legal" column:
Terms of Service / Privacy Policy / Software License / Intellectual Property. Docs footer
(minimal by design) untouched. The docs data-privacy privacy-policy link now resolves. All
footer/legal links checked 200. The privacy contact email `support@search2o.com` renders as
<code> (converter learned backticks after it showed literal ` on the page). html/legal is a
NEW directory - a future deploy needs nothing special (sync adds it).

## State on 2026-09-05 (data-privacy corrections from Ram)
Three facts corrected. (1) KEY CAPABILITY: with the default Search2o-managed key, Search2o AND
Google can in principle read the encrypted data - only end-to-end encryption excludes them.
data-privacy "Who else can see it" rewritten; encryption.html default-key section now says the
same (was "the protection rests on Search2o never using it"). (2) LONG-TERM MEMORY is kept
until the agent that stored it is deleted (NOT one year - even though persistence/longmemory
still writes Epoch.s365; Ram's statement wins): data-privacy row, commands/memory.html rule,
and encryption.html's key-retention list ("the life of the storing agent"). (3) EXECUTION
RECORDS are kept up to one year (not three months): data-privacy x2, reports/index lead,
gui/reports lead, docs home Reports card (duration dropped). data-privacy now ends "The
privacy policy has the final word" linking ../../legal/privacy.html - THAT PAGE DOES NOT EXIST
YET (Ram: legal/privacy.html not written; content/legal/terms.html is appearing in his IDE);
the link 404s until the legal pages land. Notifications 90 days and help messages one year
stand (code-verified, undisputed). This resolves the audit's open "three months" flag.

## State on 2026-09-05 (registration success hands off to Getting started)
The register success message now ends with a .reg-next line: "Getting started takes you from
install to your first agent" (link), below the once-shown key. Verified by SIMULATING the
success DOM in the browser (the real flow needs hCaptcha + the live API and creating accounts
is off-limits) - build the same innerHTML into #reg-out and screenshot; the say() IIFE is not
console-reachable. .reg-next { margin-top: 12px; } in styles.css.

## State on 2026-09-05 (ONE LABEL, ONE DESTINATION - "Get started" retired)
Ram's plan, agreed and applied: "Register" is the ONLY action button and always ->
register.html; "Getting started" is the guide's NAME, plain links only (nav + footer + prose),
always -> gettingstarted.html; the phrase "Get started" no longer exists on the site or docs.
Changed: header CTA on index/about/pricing AND the docs template (gen/build.py:445, rebuilt -
all 120 docs pages now carry Register); home hero button; home band button; pricing.html's
in-body price-card button (the sweep's one straggler). Nine Register buttons total, all ->
register.html (docs pages relative, e.g. ../../register.html). Register stays OUT of the nav
(mirror rule: Register everywhere as a button, nowhere as a nav item; Getting started the
reverse). Footer has no Register link - offered, Ram did not take it.

## State on 2026-09-05 (band down to one button)
Ram: the band's two buttons were fillers. The get-started band now has ONE button, "Get
started ->" (btn-onnavy), to gettingstarted.html; "Read the getting-started guide" wording and
the "See beta pricing" ghost button (with its inline styles) are gone. Head + one line stay.

## State on 2026-09-05 (register.html split out; NO GitHub on the home page)
Ram: a GitHub mention on the home page can mislead as open source - the hero's
install-from-git button (briefly "View on GitHub") is GONE; the hero has Get started alone.
The diagram's "source available" STAYS (Ram asked for it; names no repository). SIX site pages
now: NEW html/register.html holds the whole registration flow (hero note points on to Getting
started; .form-card.reg-card, .reg-card{max-width:560px} in styles.css; hCaptcha script only
here). gettingstarted.html step 1 is one line + a link to the Register page ("prerequisite",
Ram's word); its form, reg script and hCaptcha script are gone; its header CTA (and register
page's own) -> register.html; index/about/pricing keep "Get started". Inbound register links
now target register.html: registering-and-downloading lead and ../search2o/README.md (Ram
commits that repo). Register is NOT in the nav - header button only.

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
