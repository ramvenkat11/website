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
