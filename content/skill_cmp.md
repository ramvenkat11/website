# Search2o vs Agent Skills (SKILL.md) — comparison working sheet, pass 2

Changes from your notes are marked **[changed]** in the Winner column, with the reasoning in Why. Where I disagreed with a note, I kept your note in the Notes column and added my reply after it, so you can rule.

## Assumptions about Skills (correct these first)

- A skill is a folder with `SKILL.md` — name and description in the frontmatter, instructions in the body — plus optional scripts and resources.
- The model sees every available skill's name and description and loads a skill's body when it judges the request matches.
- Scripts run in the vendor's code-execution sandbox with the agent's tool permissions.
- Skills are shared per person or distributed per organization; each person runs a skill inside their own session.
- The format is open and has been adopted by tools beyond Anthropic's.

## The organizing axis

A skill is a capability a person adds to their own assistant. Even when distributed organization-wide, each person runs it in their own session, with their own permissions, and the author is out of the picture once it is shared.

A Search2o agent is a service: built by a developer, operated by an administrator, run by people who never see the definition, against systems the runner may have no direct access to.

Everything on the Search2o side of the tables follows from that. Validation before release only matters if someone else will run it. Reports only matter if the author won't be there when it fails. Roles, publish gates, versioning with rollback, cost per agent, error paths per version, human-in-the-loop that resumes days later on another device — all of it exists because the runner is not the author.

Everything on the Skills side follows from the opposite. Authoring is easy because the author is also the beneficiary and can fix it in the moment. Flexibility is a virtue because the person watching can correct a wrong turn. A transcript is enough audit because the runner was present.

The same fact reads as a strength on one side of the axis and a defect on the other. "The model improvises on inputs the author didn't anticipate" is a feature in a personal tool and a fault in a service. The final document should be organized around the question — is the person who builds it the person who runs it? — not around a score.

## 1. Points the axis adds

These rows exist only because author and runner can be different people.

| Point | Winner | Why | Notes |
|---|---|---|---|
| Whose permissions it runs with | Depends | A skill acts as the person and reaches only what they can. An agent acts through profiles and reaches what the profile allows regardless of who asked — a help-desk agent can file a ticket for someone with no ticketing access; access control becomes the agent's responsibility. | |
| Who is present when it fails | Search2o | A skill author is absent when a colleague runs it and nothing tells them. An agent failure lands in the error report with a version and a command path. | |
| Consistency across runners | Search2o | A skill's behavior varies with the runner's phrasing, context, and model. An agent runs the same commands for everyone. | |
| Onboarding the runner | Tie **[changed]** | Both need an account. Both present the runner with a box they already understand — a search box or a chat window — and the runner never sees a SKILL.md any more than they see an agent definition; the model loads the skill on its own. The only difference is whether the organization already has the assistant deployed, and that is the distribution row, counted once below. | Your note: "Both need an account. Search2o's interface is search or chat box that everyone understands. Skill.md is the new technology for them on which they need to get trained." — Agreed on the first two; on the third I'd push back: the runner of a distributed skill never touches SKILL.md, they just type into Claude. The training burden is the author's, and that's already the authoring row. So Tie rather than Search2o. |
| Accountability and cost attribution | Search2o | Usage per user, cost per agent. A skill's cost dissolves into the runner's token bill. | |
| Scaling from one author to many runners | Search2o | Publish, describe, done. A skill scales by being copied into each assistant; updates propagate only where the platform manages that. | |
| Support burden on the author | Search2o | An operator handles failures and access. A skill author becomes the help desk for their skill. | |
| Doing only what it was designed to do | Search2o **[new]** | The paired row to "inputs the author did not anticipate" in section 3. For a service run on behalf of others, an agent that does exactly what it was written to do is the requirement, not a limitation. | From your note on section 3. Kept as two rows so the document can show the same fact from both sides of the axis. |

## 2. Finding the right capability

| Point | Winner | Why | Notes |
|---|---|---|---|
| Routing mechanism | Search2o | Embedding search with thresholds vs the model reading a list of descriptions and choosing. | |
| Refusal when nothing fits | Search2o | Search returns zero results; the model always does something. | |
| Ambiguity handling | Tie | Search offers two or three when close; the model asks a clarifying question. | |
| Catalogue scale | Search2o | Measured at 1,000 agents. Every skill description sits in context, so cost and accuracy degrade with count. | |
| Published accuracy evidence | Search2o | A measured page exists. Nobody publishes skill-selection accuracy. | |
| Routing latency | Search2o | Sub-second search vs a model turn to read and decide. | |
| Routing cost | Search2o | Search is free per request; every skill description costs tokens on every turn. | |

## 3. Building one

| Point | Winner | Why | Notes |
|---|---|---|---|
| Authoring effort | Depends on the author **[changed]** | For a non-programmer, Skills, outright: a markdown file, no runtime to learn. For a programmer expressing a multi-step workflow — call this, loop over that, ask, then write — the command list is the natural form and prose is the awkward one. For a programmer writing a simple instruction-shaped capability, roughly a tie. | Your note. Agreed; split by author. |
| Who can author | Skills | Anyone who can write instructions vs a developer who learns 23 commands. | |
| Readability by non-developers | Depends on length **[changed]** | A twenty-line JSON workflow reads more easily than a two-hundred-line SKILL.md, and worse than a ten-line one. Prose wins at short lengths; structure wins as the workflow grows. | Your note. Agreed, with the precision point moved to its own row below. |
| Precision — knowing exactly what it will do | Search2o **[new]** | A command list states what happens; prose leaves the model to interpret it, and two readers can disagree about what a paragraph of instructions means. An AI can explain a JSON workflow exactly; it can only paraphrase prose. | From your readability note. |
| Time to first working result | Skills | No install, no profiles, no validation pass. | |
| AI-assisted authoring | Tie | Claude writes skills; Draft with AI writes agents. | |
| Pre-release validation | Search2o | Mandatory execution run with trace vs none built in (skill-creator evals — unsure how far that has gone). | |
| Versioning and rollback | Tie | Platform-managed skills have thin versioning; skills in a repo get git. Search2o has version history with rollback. | |
| Concurrent editing | Search2o | Three-way merge in the product vs git or nothing. | |
| Inputs the author did not anticipate | Skills, for a personal tool | The model improvises. This is the other face of "doing only what it was designed to do" in section 1: a feature when the author is watching, a fault when a stranger is relying on it. | Your note: "This is a good thing. Search2o is designed with such predictability in mind." — Agreed; expressed as the paired row rather than a flipped verdict, so the document shows both readings. |

## 4. Running one

| Point | Winner | Why | Notes |
|---|---|---|---|
| Determinism | Search2o | Fixed command sequence vs model judgment over prose. | |
| Error handling | Search2o | `onError` per command and function, transactional `fail`. The model improvises recovery. | |
| Human-in-the-loop | Search2o | Structured `ask`, resumes days later on another device. A skill asks in-session only. | |
| Long-running and paused workflows | Search2o | State saved and resumed. A skill lives inside one session. | |
| Non-interactive, batch, event-driven runs | Search2o | REST API and workflows. Skills are designed around a conversation. | |
| Arbitrary code — capability | Skills | Scripts in Python or bash. Search2o allows none by design. | Your note: "Yes, by design. This makes skills dangerous." — Kept as a capability win for Skills and added the paired row below, because a reader will see both. |
| Arbitrary code — blast radius of a mistake or an injection | Search2o **[new]** | A capability sandbox bounds what an expression can reach; a script can do whatever the container allows. | |
| Per-run token cost for routine tasks | Search2o | Only the `llm` command's tokens. A skill run reads the body and reasons every time. | |
| Composition in one conversation | Tie | The model composes skills fluidly within one person's turn. Search2o composes across requests and via `invoke`/`search`. Tilts to Skills for one person, to Search2o across many. | |
| Latency of a routine action | Search2o | Direct API/DB calls vs model-mediated steps. | |
| Long-term memory | Tie **[new]** | Per-user memory in Search2o; the assistant has its own memory. Different scoping, both present. | |

## 5. Reaching your systems

| Point | Winner | Why | Notes |
|---|---|---|---|
| Direct access to internal APIs and databases | Search2o | Profiles and commands inside your network. Skills reach systems through MCP servers you expose. | |
| Breadth of integrations | Skills | Files, web, computer use, vendor tools, plus MCP. Search2o has REST, SQL, MCP. | |
| MCP | Tie | Both are clients. | |
| Secrets handling | Search2o | Vault and profiles vs environment and MCP server config. | |
| Where execution happens | Search2o | Your server. Skills run in the vendor's environment (local only with Claude Code). | |
| Data residency and privacy | Search2o, narrowly | Data plane in your org, control plane in Search2o Cloud. Skills put everything in the vendor's cloud. Not a clean win given the plaintext-query boundary. | |
| Retention control | Search2o **[new]** | Conversations expire at three months, are pinnable, and are deletable by the user; retention under a skill follows the vendor's policy. | |

## 6. Trust and governance

| Point | Winner | Why | Notes |
|---|---|---|---|
| Prompt-injection exposure | Search2o | The model does not choose actions, so injected text cannot redirect the sequence. A skill-driven model can be steered. | |
| Sandbox — control | Search2o | The customer's allowlist bounds what code can reach. | |
| Sandbox — isolation strength | Tie **[changed]** | Skills' container is built in and operated by the vendor. Search2o's application-level containment has no CPU or memory limits of its own, but the agent server is a process the customer can run in a container with OS limits — isolation is a deployment choice rather than absent. Built-in versus configurable. | Your note: "Nothing stops a vendor from running Search2o agent server in a sandbox." — Agreed. Changed from Skills to Tie; the docs should say this explicitly so the reviewer doesn't have to infer it. |
| Auditability of what ran | Search2o | Command-level trace and error paths. A skill leaves a transcript. | |
| Cost per capability, per version | Search2o | Reports exist. Skills have none. | |
| Roles and publish control | Search2o | Four roles. Skills are shared by admins or personal; no publish gate. | |
| Reproducibility for regulated review | Search2o | Same input, same steps. | |

## 7. Ecosystem and business

| Point | Winner | Why | Notes |
|---|---|---|---|
| Model neutrality | Search2o | Any vendor or compatible endpoint. Skills run on the vendor's models. | |
| Format openness and portability | Skills | Open spec, plain markdown, adopted elsewhere. Search2o is a proprietary JSON DSL. | |
| Distribution and reach | Skills | Every Claude user, plus other tools. | |
| Maturity and community | Skills | Months of wide use vs a launch. | |
| End-user interface | Tie **[changed]** | Search2o ships a purpose-built search UI, conversations, and chat-bot integrations. Skills ship no interface of their own; they borrow the assistant's chat, which is polished and familiar but not built for finding and running capabilities. Purpose-built versus borrowed. | Your note: "Search2o has an integrated search user interface. Skills has none." — Agreed that the row as written was wrong. Not a clean Search2o win either, since the borrowed UI is one the runner already uses; hence Tie, with the distinction stated. |
| Embedding in your own apps | Tie | Both have APIs. | |
| Pricing model | Depends | Skills ride on seats or tokens. Search2o adds a license on top of your own LLM spend. Cheaper at small scale for Skills, cheaper per routine run for Search2o. | |
| Can host the other's shape | Search2o | An `llm` command with a prompt profile and tools is a skill-shaped agent. A skill cannot be a Search2o agent. | |

## Missing rows (add here)

| Point | Winner | Why | Notes |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## Changes in this pass

- Onboarding the runner: Search2o → Tie. Pushed back on the training point; the runner never sees the skill file.
- Authoring effort: Skills → Depends on the author, split as you described.
- Readability: Skills → Depends on length; precision split out as its own row (Search2o).
- Inputs the author did not anticipate: kept as Skills for a personal tool, paired with a new row "Doing only what it was designed to do" (Search2o) under the axis.
- Arbitrary code: kept as a capability win for Skills, paired with a new "blast radius" row (Search2o).
- Sandbox isolation: Skills → Tie, per your note; recommend stating the container deployment in the docs.
- End-user interface: Skills → Tie, reframed as purpose-built versus borrowed.
- New rows: precision, blast radius, long-term memory (tie), retention control, doing only what it was designed to do.
- Axis section expanded with the consequences paragraphs so the final document can lead with them.

## Tally (for reference only)

Search2o 38, Skills 10, Tie 10, Depends 4. The count moved toward Search2o this pass mostly by splitting rows, which is a reason not to lean on it. The four rows that decide most adoptions are unchanged and still on the Skills side: who can author, time to first result, distribution, maturity.