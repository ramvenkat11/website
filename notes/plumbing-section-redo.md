# Home section 2 ("All the plumbing taken care of"): redo from a box to parts

Open discussion, 2026-11-04. Picked option C and built it into section 2 (uncommitted).

## Decided so far
- Ram wants the home page to say, with a picture and a line, that the agent server includes
  everything needed: framework, IDE, runtime, routing and state management.
- It goes in section 2 (`#framework-runtime` in html/index.html), not the hero and not a new section.
- The lead line is already added under the h2: "The agent server includes everything needed:
  framework, IDE, runtime, routing and state management." (uses `.section-head p`).
- The heading may be renamed later to something more formal.
- The figure (`.fw-fig`: a ring of 28 `.fw-piece` links around a request -> Your agent -> response
  strip) is to be redone around the five parts. There may be more parts to accommodate.
- Uncommitted in the working tree (Ram commits): hero lead rewrite, hero demo caption, unlinked
  figure labels, REST client in the "Fits in" figure, this lead line. Nothing uploaded.

## How today's 28 pieces fall into the parts (decided 2026-11-04, six parts)
- LLMs: LLM calls, tool calling loop, MCP, model neutrality (moved here from Runtime).
- Agent workflow: API and database calls, parallel execution, error handling, human in the loop,
  progress, streaming, externalized prompts, externalized system calls (the two externalized
  pieces come last).
- Development environment (was IDE): draft with AI (leads, most important), agent editor, trace and
  validation, agent versioning, multi-developer publishing.
- Runtime: live configuration, hooks, audit log, connection pools, secret vault, authentication,
  runtime limits, guardrails, observability.
- Routing: nothing today; search would go here.
- State management: save/restore conversations, agent memory.

## Answers, 2026-11-04
1. Five parts, final. Runtime keeps its ten pieces.
2. Parts as the big shapes, pieces as small text inside.
3. Shape: decide visually from notes/plumbing-mockups.html (options A five blocks, B layer stack,
   C ring in five arcs). Open it in a browser; the button at bottom right flips dark mode.
4. The request -> your agent -> response strip stays.
5. Both link: each part to its page (framework.html, docs/development/index.html, runtime.html,
   search.html, conversation.html), each piece to its docs page.
6. Routing and state management scope: after the picture is chosen.

## Questions for Ram (asked 2026-11-04, answered above)
1. Are the five parts the final list, or are there more? Runtime carries ten pieces, several of
   them really security and operations. Split out "Security" or "Administration", or keep under runtime?
2. Show the pieces at all, or only the parts? Options: parts only with one line of examples each;
   parts with every piece listed inside; parts as the big shapes with pieces as small text inside.
3. Which shape for "from a box to these parts": five blocks inside the server outline with
   "Your agent" in the middle; a layer stack (framework on runtime); or the ring kept but divided
   into five labelled arcs?
4. Does the request -> your agent -> response strip stay in the middle, or does the agent become
   one of the parts' contents?
5. Should each part link to one page (framework -> framework.html, routing -> search.html) with the
   pieces keeping their docs links, or should only the pieces link?
6. What does routing cover: search picking the agent only, or also the conversation continuing
   with the same agent across turns? Does state management include anything beyond conversations
   and memory, such as the agent's working data between calls?

## Built, 2026-11-04 (after Ram picked C)
- Section 2 figure is now five part boxes in a ring around the vertical request -> Your agent ->
  response strip: Framework across the top, IDE and Runtime beside the strip, Routing and State
  management below. Pieces are small text chips inside each part, no icons. Every part title and
  every piece links. Agent box subtitle is back to "Your business logic: calls, prompts, decisions".
- Below 860 the strip goes horizontal above a two-column grid; below 700 one column; below 420 the
  strip is vertical again so the agent box keeps its width.
- Still open: question 6 (routing and state management scope). Routing holds the placeholder
  "Search picks the agent" until then. Heading rename still possible.

## Split, 2026-11-04 (Ram's decision)
- Framework split into LLMs (links docs/llm/index.html) and Agent workflow (links framework.html).
  Ram picked "Agent workflow" over "Agentic workflow". Tool calling loop stays under LLMs,
  streaming under Agent workflow, model neutrality moved from Runtime to LLMs.
- Grid is now 3 by 3: LLMs | strip | Agent workflow, Development environment | strip | Runtime,
  Routing | strip | State management. Below 860: LLMs and Agent workflow, strip, then pairs.
  Below 700: one column, strip after Agent workflow.
- Rows share heights, so at 1280 the LLMs box (two chip rows) is as tall as Agent workflow (four).
  Alternative is align-items: start, which makes each box its own height but unaligns the columns.
- Then (same day): externalized prompts and system calls moved to the end of Agent workflow.
  Columns now mean something: left is development (LLMs, Agent workflow, Development
  environment), right is running (Routing, Runtime, State management). Routing sits beside
  "request", Runtime beside the agent, State management beside "response". Below 860: LLMs and
  Routing, strip, then the remaining pairs. Below 700: the three dev parts, strip, the three
  running parts. DOM order matches.

## Strip removed, 2026-11-04 (Ram: "Does the middle block even add value?")
- Agreed it had become a spacer after the split. Removed the request -> Your agent -> response
  strip and its CSS (.fw-run, .fw-io, .fw-arr, .fw-agent). Subheading under the title carries
  the message: "Your agent code is just the business logic." (non-breaking space before "logic").
- Figure is two rows of three inside the dashed Agent server outline: LLMs, Agent workflow,
  Development environment above; Routing, Runtime, State management below. Below 860 two
  columns in reading order (LLMs/Agent workflow, Development environment/Routing,
  Runtime/State management); below 700 one column.
- Rows still share a height, so LLMs, Routing and State management have space under their chips
  at 1000 and up.

## Conversation section added, 2026-11-04
- New home section #conversations between the hero and "One server", as planned on 2026-10-24.
  Title "Let your users converse with your enterprise agents" (Ram picked it), subheading
  "A follow-up can go to a different agent. No agent calls another."
- Figure is the conversation page's hero chat copied as is, with the four side notes cut to one
  line each. Links: search.html, docs/commands/ask.html, conversation.html#state,
  docs/agent-execution/building-on-each-other.html.
- The figure's layout rules were scoped to #mechanism; now `:is(#mechanism, #conversations)`
  so both pages share them. A plain class lost to the 1000px .hero-convo rule and pushed the
  second note below the chat, hence the id-level selector.
- Ram, same day: the parked "three surfaces" clients section is not needed with the home page as it is now. Dropped.
- Ram, same day: the conversation page's top figure (#mechanism) is removed; the home page
  carries it now. "What a conversation keeps" is the page's first section. CSS rules now scoped
  to #conversations only.
- Section 4 "Fits into your environment as is" got a subheading (decided with Ram, 2026-11-04):
  "Chat from the apps you already use. Automate through REST. Open your enterprise agentic
  workflows to agent harnesses." Non-breaking space in "agent harnesses".
- Section 4 title is now "Interfaces for people, programs and agent harnesses" (Ram picked it,
  2026-11-04); the old "Fits into your environment as is" is gone. The title's three nouns match
  the subheading's three sentences in order.
- Conversation section wording, Ram 2026-11-04: title "Let users converse with your enterprise
  agents" (no "your" before users), subheading "Conversations run multiple agents in the same
  context." Then changed to "Agents stay independent and build on each other within a conversation."
- Ram, 2026-11-04 (later): section 2 title back to "All the plumbing taken care of". Subheading
  "Your agent code is just the business logic." stays.
- Section 4 caption under the figure (2026-11-04): "The agent server keeps no state.
  Conversations and memories live in Search2o Cloud, encrypted by default." Links to
  docs/security/data-privacy.html and docs/security/encryption.html, same two the figure's cloud
  box uses. Reuses the hero-caption style.
- Cloud state wording moved into the figure's State box (Ram did not want a caption below the
  image): "Conversations and memories live here, / encrypted by default". The "keeps no state"
  sentence was dropped because the server box already says Stateless. Span max-width 300px.
- Section 4 title changed again (Ram, 2026-11-04): "Cloud managed state, multiple client
  interfaces". No period, to match the other home h2s.
- Section 4 subheading cut to one sentence (Ram, 2026-11-04): "Open your enterprise agentic
  workflows to agent harnesses." The chat and REST sentences are gone; the title now carries
  "multiple client interfaces".
- Section 4 subheading (Ram picked, 2026-11-04): "One skill opens hundreds of repeatable,
  bounded, cost-effective agents to agent harnesses."

## Rethink, 2026-11-04 (Ram: "N boxes is highly unimaginative")
- Brief: same message (plumbing done, agent is business logic), add model neutrality with the
  supported LLMs (frontier and free), and make the section say that developing, publishing and
  running agents are easy.
- Four mockups in notes/section3-mockups.html (open in a browser; button at bottom right flips
  dark mode). All use the orders agent from framework.html, shortened.
  A. The path: Develop -> Publish -> Run as three stage cards, each showing the thing itself
     (the sentence to Draft with AI, the published card with version and description, the user's
     question and answer) plus one line on what the server did. LLM chips in Run.
  B. This is the whole agent: the agent definition is the figure; six numbered lines map to what
     the server does around them. A row of model buttons rewrites the profile line.
  C. What you write / what the server does: code left, three stage paragraphs right.
  D. One run, as the server sees it: code left (two highlighted commands), a timed trace right
     where two lines are the agent's and the rest is the server's. Model chips under the code.
- Nothing in html/ changed. Waiting for Ram's pick and answers.
- Ram picked B (2026-11-04): no model switch box, "models you host" not "free", the IT helpdesk
  agent from the hero instead of orders, title held as is. Built into section 3 of
  html/index.html: a codecard it_helpdesk.json (openTicket tool over the helpdesk API, main with
  an llm command) and six numbered notes. The six vendors are named in note 3. The old part
  boxes and their CSS are gone; new rules are the #framework-runtime .pl-* block.
- Section 4 subheading (Ram, 2026-11-04): "One skill opens hundreds of bounded, cost-effective,
  observable agents to agent harnesses." ("repeatable" dropped, "observable" added.)
- Conversation section notes restored to the full texts the conversation page's figure had
  (Ram, 2026-11-05): the one-line cuts are gone from both the side bubbles and the stacked
  phone notes. Source: html/conversation.html at commit 4cbc73b9. Only change: the
  Conversation context link is conversation.html#state, not #state.
- Conversation subheading (Ram, 2026-11-05): "Agents stay focused and independent, yet build on
  each other in a conversation." American "focused"; "yet" for the contrast; "in" not "within".
- Section 3 notes redone (Ram, 2026-11-05): conversation state is the conversation section's
  job now, so note 6 no longer mentions saving the conversation. Note 1 is "The complete agent":
  JSON with Python expressions, Draft with AI, agent editor, trace, validation, publishing.
  Note 2 "Calling enterprise systems" (Ram's title) names what the profile carries and that
  result holds the response. Note 3 "LLM calls" (Ram's title). Notes 4 and 5 unchanged.
  notes/section3-notes.md overwritten with the new texts.
- Hero first sentence (Ram, 2026-11-06): "Developers build agents that are task-focused and
  describe them in plain English." Links: build -> framework.html, task-focused ->
  docs/introduction/search2o-agents.html (was on "agents"), describe -> search.html#description.
  Non-breaking hyphen in task-focused. "on the server" dropped from this sentence.

## Rebuilt, 2026-11-06 (Ram: "Go for it")
- Idea: an agent is a document, not a program. A program contains its plumbing; a document
  names things and leaves them where they are. Against a harness subagent (a prompt the model
  improvises from) the document holds the steps, and the model is one of them.
- Figure: my_tickets.json (main with four steps: api, var, llm, output; no tool calling) on the
  left, numbered step badges on the command keys, three names highlighted (helpdesk,
  gpt5_mini, ticket_status). Three cards on the right show what the names stand for: the API
  profile (URL, Authorization header reading the vault, pool), the LLM profile (vendor, key,
  prices, six adapters) and the prompt (system, user, scope). Curved connectors drawn by a
  small script in js/site.js (hidden under 860, where the figure stacks). File tab links
  "JSON with Python expressions" to the syntax page.
- Caption: "The server runs the steps. The model is one of them. Not a prompt the model
  improvises from. Not a program you deploy." + Agent workflow link. Title and subheading
  unchanged. The six notes are gone; notes/section3-notes.md is now history.

## Split into two sections, 2026-11-06 (Ram)
- New section #approach before #framework-runtime: the positioning. Three columns, A program
  (LangChain, an agents SDK), A prompt (a Claude Code subagent, a Copilot agent), A spec
  (Search2o, highlighted), each with a small silhouette, compared on six rows: what you write,
  who works out the steps, who runs it, the same result every run, systems/time/cost bounded,
  checked before users get it. Draft with AI is in the second row. Provisional title "Three
  ways to build an agent" / "A program, a prompt, or a spec that a server runs." Plain
  background (not .soft) so the other sections' backgrounds stay as they were. Under 700 the
  three columns stack as cards with the row labels inside each.
- Example section (#framework-runtime): title "Nothing new to learn", subheading "An agent is a
  JSON document with Python expressions that spells out the steps. The agent server is the
  program that runs it.", kicker line above the code card "Draft with AI wrote this from 'Tell
  users where their open IT tickets stand.'", caption removed.

## 2026-11-06, later: approach section dropped, code figure moved to the framework page

Ram: "I changed my mind on the section: Three ways to build an agent. I don't want it anymore. In
'Nothing new to learn': Remove the code - Once we introduce code, we have to start explaining
everything. But, the current picture is good and keep it for the framework page - you can move it
there now, if you want. Let's restart the discussion on this section - with the understanding that
we are not going to show JSON code here - or show something minimal like 'Hello, World'".

Done:
- #approach section removed from html/index.html, with its CSS (#approach .ap-*), and the
  #approach entry in the 24px h2 rule.
- #framework-runtime on the home page keeps only its head (Nothing new to learn + subtitle) as a
  placeholder while the section is rethought.
- The my_tickets.json figure (kick line, code card, three cards, connectors) moved to
  html/framework.html as a new section #outside-the-agent between #second-agent and #commands,
  head "The agent holds only the steps". CSS rescoped from #framework-runtime .pl-* to .pl-* (phone
  pre rules needed .pl-fig .pl-code pre to beat .codecard pre); .fw-page .pl-wrap left-aligned;
  site.js connector code now finds .pl-fig on any page.

Open: what the home section shows instead of code.

## 2026-11-06, later: the section rebuilt as one picture

Ram on the two label-only mockups (notes/nothing-new-mockups.html): "Both break the basic rule I
gave you ... do not write essays on the home page." Then: "You know the product so well. Yet, you
are failing miserably to design this section reasonably well. What is the issue?" My answer: I
design by enumeration; the section has to prove one sentence (the agent is a small document of
steps, the server is the program) with a picture, not a list. Ram: "Go ahead".

Built in html/index.html #framework-runtime: a dark "Agent server" block (code-card colours and
border) holding a small white document my_tickets.json with three numbered steps (api, llm,
output) and six dashed parts (Connections, Models, Streaming, Conversation state, Limits, Audit
log). One line under it: "Draft with AI writes it from one sentence." CSS under
#framework-runtime .srv-*; stacks at 700 (document centred, parts in two columns).

## 2026-11-06, later: head settled, figure is two circles

Title "As dependable as code, as easy as a prompt". Subtitle (Ram's words, second sentence softened
at his concern that "First draft created" implied no editing): "Safe, cost-efficient and
observable, like an agent coded in Python. Drafted from a description, like a prompt."

Ram rejected the server-block picture and asked for two intersecting circles: development on one
side (Draft with AI, Code editor, Validate, Publish, Describe), runtime on the other, a small RAG
agent in the overlap. Built as #framework-runtime .vn-*: Development circle (blue) and Runtime
circle (teal; Guardrails, Secret vault, Runtime limits, Audit log, Cost report, each a link), the
agent ask_the_docs.json with steps api, llm, output in the lens. Circles side by side above 600,
stacked below it. The Draft with AI line under the figure is gone; it is a pill in the circle.

## 2026-11-06, later: Ram wants the section to sell, not explain

Ram on the Code vs Prompt mockup: Draft with AI must stay on the Prompt side, the other Prompt
points were weak. Then: "It needs to sell - not explain - but it does need to talk about JSON with
Python expressions." Three directions offered, no edits yet:

A (recommended). Keep his two circles and the JSON lens, but fill the circles with evidence instead
of adjectives. Prompt circle (left): a chat bubble with one sentence, "Answer questions from the
docs site.", and a Draft with AI button. Code circle (right): a run receipt: Validated, Allowlist:
docs API, 1.8 s of 30 s, $0.003, Audit log. The lens keeps ask_the_docs.json; a caption under it
carries the format: "JSON with Python expressions. Nothing new to learn." (or "The whole agent:
20 lines of JSON with Python expressions.").

B. A positioning map: Dependable up, Easy to create right; Coded agents (LangChain, agent SDKs)
top-left, Prompt agents (Claude Code, Copilot agents) bottom-right, the JSON card top-right with
dotted guide lines from both. Draws the title literally; risk: analyst-slide cliché, and it ranks
named products below us.

C. Same circles, three benefit lines a side instead of five adjectives. Code: Validated before
release, Runs inside limits, Every run on record. Prompt: Drafted from a sentence, Readable by
anyone, Live on the next run. Same caption as A.

Rejected: a three-column check-mark table (Python project / JSON with Python expressions / a page
of text). Honest marks for LangChain are "you build it" and "LangSmith", which makes it muddy;
crisp marks would be unfair.

## 2026-11-06, later: full freedom, one mockup

Ram: "You can completely move away from circles ... You can change the title and sub title. You
have full freedom. But I need something good." Built notes/sell-strip.html: a three-beat strip,
Describe (a chat bubble, "Answer questions from the docs site.") > Draft with AI > The agent
(ask_the_docs.json code card, Python expressions in yellow, caption "JSON with Python expressions")
> Validate, publish > Every run (a receipt: Validated, Allowlist docs API, API key from the vault,
Time 1.8 s of 30 s, Cost $0.003 of $0.05, Audit log run 4812). Subtitle changed to "A sentence
becomes an agent in JSON with Python expressions. The agent server validates it, then guards and
records every run." Stacks below 900. Rendered 1280 to 320 light and dark; sweep 0 of 241.

Ram: "The idea is fine. We have to discuss details. You can place this in index.html." Placed in
html/index.html #framework-runtime (replacing the .vn-* circles; CSS now #framework-runtime .ss-*).
His three details applied: section head widened to 860px for a longer subheading; code card fixed
at 300px wide; the description is a quiet input-style box (soft background, body text), not a navy
bubble. Three columns from 1000 up, stacked below. Open: the Every run line items (his: "we can do
that later"), the subheading wording.

Ram: "Describe" in the hero means the search description, so showing a description sentence here
confuses the two; not sure about the right-side box and the arrows; bring back the feature-pill
boxes, smaller, around the central JSON. Done in html/index.html: the code card in the middle,
a Development box (Draft with AI, Code editor, Validate, Publish, Describe) on the left and a
Runtime box (Guardrails, Secret vault, Runtime limits, Audit log, Cost report) on the right, each
a 300px card of wrapped pills, no arrows. Below 1000 the code comes first and the two boxes sit
side by side under it; below 420 they stack. Subtitle unchanged, still to be reworked by Ram.

Ram: "I was talking about the boxes with pills we had before: LLM, dev, runtime etc", i.e. the
six plumbing boxes of the old "All the plumbing taken care of" figure (commit 1757653b^). Rebuilt
in html/index.html: a dashed "Agent server" frame holding the code card in the middle, three boxes
on the left (Development environment, Agent workflow, LLMs) and three on the right (Runtime, State
management, Routing), chips and links as before, everything smaller (13.5px titles, 11.5px chips).
Below 1000 the code sits on top and the boxes form two columns; below 600 one column. Ram also:
"no need to use output - just use streamOutput": the agent is now api + llm with
"streamOutput": true, no output command.

## Syntax section (2026-11-06)
Ram dropped the feature boxes. The section now explains the syntax: code card with one tool
function (findOrders, db), and three cards beside it: Python expressions, Tool calling,
20 commands. Two-tool version was built first and cut to one for height.
