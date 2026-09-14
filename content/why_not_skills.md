# Search2o vs Agent Skills (SKILL.md) — a product and technology comparison

## The organizing axis

A skill is a capability a person adds to their own assistant. On claude.ai, custom skills are individual to each user and cannot be centrally managed; on the Claude API they are shared workspace-wide; in Claude Code they are personal or per project. In every case each person runs a skill inside their own session, with their own permissions, and the author is out of the picture once it is shared.

A Search2o agent is a service: built by a developer, operated by an administrator, run by people who never see the definition, against systems the runner may have no direct access to.

Each side is shaped by its position on that axis. Search2o has validation before release, reports, roles, publish gates, versioning with rollback, cost per agent, and human-in-the-loop that resumes days later, because the runner is not the author. Skills have effortless authoring, improvisation on unexpected input, a transcript as the only record, and nothing to operate, because the author is the runner and is present to steer.

The same fact reads as a strength on one side and a defect on the other. "The model improvises on inputs the author didn't anticipate" is a feature in a personal tool and a fault in a service. "The agent does only what it was written to do" is a guarantee in a service and a limitation in a personal tool. The rows below show both readings wherever they exist.

## 1. What the axis decides

| Point | Winner | Why |
|---|---|---|
| Whose permissions it runs with | Depends | A skill acts as the person and reaches only what they can. An agent acts through profiles and reaches what the profile allows regardless of who asked — a help-desk agent can file a ticket for someone with no ticketing access; access control becomes the agent's responsibility. |
| Who is present when it fails | Search2o | A skill author is absent when a colleague runs it, and nothing tells them. An agent failure lands in the error report with a version and a command path. |
| Consistency across runners | Search2o | A skill's behavior varies with the runner's phrasing, context, and model; Anthropic advises testing each skill across the models an organization uses because effectiveness varies by model. An agent runs the same commands for everyone. |
| Doing only what it was designed to do | Search2o | For a service run on behalf of others, an agent that does exactly what it was written to do is the requirement. |
| Handling inputs the author did not anticipate | Skills | The model improvises. For a person watching, that is the point; the two rows above and this one are the same fact. |
| Handling requests nobody built a capability for | Skills | The assistant answers from general ability. Search2o returns nothing unless an agent exists — correct for a service, a gap for the person typing. |
| Onboarding the runner | Tie | Both need an account, and both present a box the runner already understands. The runner never sees a SKILL.md any more than an agent definition. |
| Accountability and cost attribution | Search2o | Usage per user, cost per agent. Anthropic's documentation states that usage analytics are not available through the Skills API and recommends application-level logging. |
| Scaling from one author to many runners | Search2o | Publish, describe, done. On claude.ai each team member uploads a custom skill separately and there is no organization-wide distribution; on the API a skill is workspace-wide; skills do not sync across surfaces. |
| Support burden on the author | Search2o | An operator handles failures and access. A skill author becomes the help desk for their skill. |
| Operational burden on the organization | Skills | Nothing to run. Search2o's customer operates the agent server: deploy, patch, scale, monitor. |
| Improvement without author effort | Skills | A skill gets better when the model gets better. An agent does what its commands say until someone edits it. |

## 2. Finding the right capability

| Point | Winner | Why |
|---|---|---|
| Routing mechanism | Search2o | Embedding search with thresholds, tunable per account, vs the model reading every skill's name and description in its system prompt and choosing. |
| Behavior when nothing fits | Search2o | Search returns zero results below a measured threshold. An assistant can decline too, but by judgment, with no threshold to inspect or tune. |
| Ambiguity handling | Tie | Search offers two or three when close; the model asks a clarifying question. |
| Catalogue scale | Search2o | Measured at 1,000 agents. Anthropic's documentation advises limiting the number of skills loaded at once to keep recall accuracy reliable, caps API requests at 20 skills each, and suggests routing requests to different skill sets by task type when a role needs more — a router in front of the skills. |
| Published accuracy evidence | Search2o | A measured page exists. Anthropic publishes no selection-accuracy figures; it asks each organization to measure triggering accuracy with its own evaluation suite of three to five queries per skill. |
| Routing overhead | Search2o | Sub-second and no tokens per request, vs roughly 100 tokens of metadata per skill on every turn plus a model turn to choose. |
| Coverage beyond the catalogue | Skills | Anything the assistant can do is reachable without anyone publishing it. Search2o's coverage is exactly its published agents. |

## 3. Building one

| Point | Winner | Why |
|---|---|---|
| Authoring effort | Depends on the author | For a non-programmer, Skills: a markdown file, no runtime to learn. For a programmer expressing a multi-step workflow, the command list is the natural form and prose is the awkward one. For a programmer writing a simple instruction-shaped capability, roughly a tie. |
| Who can author | Skills | Anyone who can write instructions vs a developer who learns 23 commands. |
| Readability by non-developers | Depends on length | A twenty-line JSON workflow reads more easily than a two-hundred-line SKILL.md, and worse than a ten-line one. |
| Precision — knowing exactly what it will do | Search2o | A command list states what happens; prose leaves the model to interpret it, and two readers can disagree about a paragraph of instructions. |
| Time to first working result | Skills | No install, no profiles, no validation pass. |
| Iteration loop | Skills | Edit the file, run again, seconds. Search2o: edit, validate, publish. |
| AI-assisted authoring | Tie | The assistant writes skills; Draft with AI writes agents. |
| Pre-release validation | Search2o | A mandatory execution run with trace before publishing. For skills, Anthropic recommends an evaluation suite covering trigger, no-trigger, and ambiguous queries, coexistence testing against existing skills, and reviewers who are not the author — a process the organization runs, not a gate the platform enforces. |
| Versioning and rollback | Tie | The Skills API has explicit versions, pinning, and rollback to the previous version; claude.ai uploads have none; Claude Code skills get git. Search2o keeps version history with rollback. |
| Concurrent editing | Depends | Skills in a repository get git's merge; skills edited in place get none. Search2o has a three-way merge in the product. |

## 4. Running one

| Point | Winner | Why |
|---|---|---|
| Determinism | Search2o | Fixed command sequence vs model judgment over prose. |
| Error handling — designed | Search2o | `onError` per command and function, transactional `fail`, state untouched on failure. |
| Error handling — improvised | Skills | The model notices a failed step and tries another way without the author having anticipated it. |
| Human-in-the-loop | Search2o | Structured `ask`, resumes days later on another device. A skill asks within the session. |
| Long-running and paused workflows | Search2o | State saved and resumed. A skill lives inside one session. |
| Non-interactive, batch, event-driven runs | Search2o | REST API and workflows. Skills are designed around a conversation. |
| Arbitrary code — capability | Skills | Scripts in Python or bash, run so that only their output enters context. On the Claude API the container has no network access and no runtime package installation; on claude.ai network access varies by settings; in Claude Code scripts have full network access. Search2o allows none by design. |
| Arbitrary code — blast radius of a mistake or an injection | Search2o | A capability sandbox bounds what an expression can reach, uniformly. A script can do whatever its surface allows — nothing outbound on the API, anything on the user's machine in Claude Code. |
| Per-run token cost for routine tasks | Search2o | Only the `llm` command's tokens. A skill run reads the body (under 5k tokens) and reasons every time. |
| Latency of a routine action | Search2o | Direct API and database calls vs model-mediated steps. |
| Composition in one conversation | Tie | The model composes skills fluidly within one person's turn. Search2o composes across requests and via `invoke` and `search`. |
| Conversation state — structure | Search2o | Named variables in two scopes plus the prompt history, saved at defined points. A skill's state is whatever survives in the transcript. |
| Conversation state — durability | Search2o | Persisted, encrypted, resumable across devices for three months. A chat session lives as long as the session does. |
| Conversation state — sharing across capabilities | Tie | Skills share context automatically because one model holds one transcript. Search2o shares it deliberately through `conv.` and the prompt history, across agents written by different people. |
| Conversation state — author effort | Skills | Nothing to design. Search2o requires the author to decide what goes in `conv.`. |
| Long-term memory | Search2o | A `memory` command the author controls: what to store, under which label, for which user, when. The assistant has memory of its own, but Anthropic's Skills documentation describes no mechanism for a skill to direct it. |

## 5. Reaching your systems

| Point | Winner | Why |
|---|---|---|
| Direct access to internal APIs and databases | Search2o | Profiles and commands inside your network. Skills reach internal systems through MCP servers you expose; on the Claude API, skill scripts themselves have no network access. |
| Built-in tools without setup | Skills | Code execution, files, and the assistant's own tools are available immediately. Search2o needs a profile for every external system. |
| Files and documents | Skills | Reading, writing, and transforming files is native, with pre-built document skills. Search2o handles text, images, and HTML as output; it is not a file-processing runtime. |
| Computer and browser use | Skills | Available where the assistant provides it. Search2o has no equivalent. |
| MCP | Tie | Both are clients. |
| Secrets handling | Search2o | Vault and profiles, with secrets kept out of definitions. Anthropic's guidance for skills is to keep credentials in environment variables or a credential store and never in skill files. |
| Where execution happens | Search2o | Your server. Skills run in the vendor's environment, or on the user's machine with Claude Code. |
| Same definition on every surface | Search2o | One published agent serves the GUI, chat integrations, and the REST API. Custom skills do not sync across claude.ai, the API, and Claude Code; each surface needs its own upload. |
| Data residency and privacy | Search2o, narrowly | Data plane in your organization, control plane in Search2o Cloud with queries readable there for matching. Skills put everything in the vendor's cloud. |
| Retention control | Search2o | Conversations expire at three months, are pinnable, and are deletable by the user. Anthropic's documentation states that Agent Skills are not covered by zero-data-retention arrangements and that skill definitions and execution data follow the standard retention policy. |

## 6. Trust and governance

| Point | Winner | Why |
|---|---|---|
| Prompt-injection exposure | Search2o | The set of actions is fixed by the author; the model chooses only among tools the agent declares. Anthropic's documentation states that a skill can direct the model to invoke tools or execute code in ways that don't match its stated purpose, and that fetched external content may carry malicious instructions. |
| Vetting the capability itself | Search2o, narrowly | Agents are authored in-house, validated by execution, and cannot contain arbitrary code, so there is little to vet beyond the allowlist. Skills can bundle scripts and instructions from third parties; Anthropic prescribes a review checklist and offers automated content scanning for Claude Enterprise on claude.ai and Cowork, not on the API. |
| Sandbox — who controls it | Search2o | The customer's allowlist bounds what code can reach. |
| Sandbox — who maintains it | Skills | The vendor hardens and patches the container. The customer maintains nothing. |
| Sandbox — isolation strength | Tie | A vendor-operated container, with no outbound network on the API, vs application-level containment that the customer can wrap in a container with OS limits. Built-in vs configurable. |
| Auditability of what ran | Search2o | Command-level trace and error paths. A skill leaves a transcript; the Skills API logs upload and management operations, not executions. |
| Cost per capability, per version | Search2o | Reports exist. Anthropic's documentation: usage analytics are not currently available through the Skills API. |
| Roles and publish control | Search2o | Four roles and a publish gate. On claude.ai there is no admin management of custom skills; on the API any workspace member's new version becomes the latest unless production pins a version; separation of author and reviewer is recommended, not enforced. |
| Reproducibility for review | Search2o | Same input, same steps. |

## 7. Technology and interfaces

| Point | Winner | Why |
|---|---|---|
| Model neutrality | Search2o | Any vendor or compatible endpoint. Skills run on the vendor's models. |
| Format openness and portability | Skills | Open specification, plain markdown, adopted by other tools. Search2o is a proprietary JSON DSL. |
| End-user interface | Tie | Search2o ships a purpose-built search UI, conversations, and chat-bot integrations. Skills borrow the assistant's chat, which is familiar but not built for finding and running capabilities. |
| Embedding in your own applications | Tie | Both have APIs. |
| Can host the other's shape | Search2o | An `llm` command with a prompt profile and tools is a skill-shaped agent. A skill cannot be a Search2o agent. |

## Tally

The weight of each row differs by perspective. The rows were drawn at similar granularity on both sides; giving each equal weight, the counts are Search2o 39, Skills 16, Tie 10, Depends 4, over 69 rows.

| Section | Search2o | Skills | Tie | Depends |
|---|---|---|---|---|
| 1. What the axis decides | 6 | 4 | 1 | 1 |
| 2. Finding the right capability | 5 | 1 | 1 | 0 |
| 3. Building one | 2 | 3 | 2 | 3 |
| 4. Running one | 11 | 3 | 2 | 0 |
| 5. Reaching your systems | 6 | 3 | 1 | 0 |
| 6. Trust and governance | 7 | 1 | 1 | 0 |
| 7. Technology and interfaces | 2 | 1 | 2 | 0 |
| Total | 39 | 16 | 10 | 4 |

## Sources

Skills-side statements were checked against the following on September 14, 2026. Where a fact varies by surface — claude.ai, the Claude API, Claude Code — the row says so.

- Anthropic, "Agent Skills" overview: platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Anthropic, "Skills for enterprise": platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise
- Search2o documentation: search2o.com/docs, read in full in September 2026