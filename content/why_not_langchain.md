# Why not LangChain?

## How this comparison works

The LangChain ecosystem is not one product. LangChain and LangGraph are open-source frameworks for building agents in code. LangSmith is a commercial platform with several products inside it — Observability and Evaluation, Deployment (the Agent Server), Sandboxes, an LLM Gateway, Engine. LangSmith Fleet is a no-code product for creating and sharing agents across a company. They have separate licenses, deployment paths, and prices, and they don't compose into one install: Fleet's per-agent permissions apply to Fleet agents, not to a LangGraph graph you deployed, and LangGraph's determinism applies to graphs you author, not to Fleet agents.

A feature-by-feature comparison with LangGraph would come out nearly even, and the evenness would be an artifact. LangGraph is a toolkit: anything Search2o has built in, a developer can implement on LangGraph, so every row would read "tie" or "the toolkit, because it can do anything," and none of it would say anything about the purpose above. A toolkit for building an agent and a system for running hundreds of them are not trying to do the same job, and a feature-parity contest between them measures the wrong thing.

So this document asks one question, derived from the purpose: **what does it take, with each, to create and manage hundreds of agents as a single system across an enterprise?** The rows are the things that purpose requires. The columns are the three ways a buyer could pursue it:

- **Search2o** — the product this document is about.
- **LangSmith Fleet** — LangChain's product for agents across a company: no-code agents, shared and permissioned, with approvals and tracing. The closest in purpose.
- **The developer stack** — LangGraph for the agents, LangSmith Deployment to run them, LangSmith Observability and Evaluation to see and test them, Agent Chat UI in front. The build-it-yourself route, and the one a platform team weighs when it considers building rather than buying.

Each cell says one of four things, and nothing else:

- **Built in** — present without configuration or code beyond ordinary use.
- **Configurable** — present, but you set it up, choose it, or pay a plan tier for it.
    - **You build it** — achievable with the tools provided; you write and operate the code.
- **Absent** — not available in that configuration.

"You build it" is not a criticism of the developer stack; it's what a toolkit is. "Absent" is not a criticism of Fleet or Search2o; each omits things by design. Where a cell rests only on what a product's documentation describes, it says "as documented." The tally at the end counts cells per column, and its limits are stated there.

Sources and dates are at the end. LangChain-side statements were checked against LangChain's documentation on September 17, 2026.

---

## 1. Creating agents

| What the purpose requires | Search2o | LangSmith Fleet | Developer stack |
|---|---|---|---|
| Authoring by non-developers | **Absent** — a developer writes the definition, with Draft with AI producing the draft | **Built in** — describe the agent and Fleet builds it; templates | **Absent** — Python or TypeScript |
| Authoring by developers, with full control of what the agent does | **Built in** — an ordered command list in JSON with Python expressions, 23 commands | **Absent** — instructions and tools; agent files can be exported for pro-code work | **Built in** — the whole language, typed state, arbitrary graphs |
| AI-generated draft from a description that knows the account's configuration | **Built in** — JSON against a schema, generated with the account's LLM, MCP, API, database, and prompt profiles, so the draft is structurally valid and references real profiles by construction | **Built in** — the output is a prompt and tool selection, valid by nature | **You build it** — a coding assistant writes free-form code with nothing constraining imports, state, or API versions; LangChain's docs are available to assistants over MCP |
| Structural validation before the agent runs | **Built in** — schema validation and compile rules on every expression | **Absent** — a prompt has no structure to validate | **You build it** — tests and type checks in code |
| Execution-based validation gate before publishing | **Built in** — mandatory run with trace; nothing publishes without it | **Absent** — run it and iterate; sharing exposes whatever was last saved | **You build it** — a CI pipeline and tests of your own |
| Evaluation of agent quality against datasets | **Absent** — Search2o measures its router, not your agents | **Configurable** — Fleet runs are traced in LangSmith, where evaluators apply | **Configurable** — LangSmith Evaluation: datasets, offline and online evaluators, LLM-as-judge |
| Version history and rollback | **Built in** — previous versions kept, one click to restore | **Absent, as documented** — the docs describe editing in place | **Configurable** — git for code; Deployment versions assistants |
| Concurrent editing with merge | **Built in** — three-way merge in the product | **Absent** — edit in place | **Configurable** — git |
| Describing an agent so a request can find it | **Built in** — a description is required and checked before indexing | **Absent** — an agent has a name and a Slack handle | **Absent** |

## 2. Finding the right agent for a request

| What the purpose requires | Search2o | LangSmith Fleet | Developer stack |
|---|---|---|---|
| Routing a request to one of hundreds of independently built agents | **Built in** — embedding search over descriptions; agents by different authors need no wiring | **Absent** — a person picks the agent by name: each agent can have its own Slack handle and is triggered by @mention or direct message | **You build it** — a supervisor or handoff graph whose author knows the children |
| Refusing when no agent fits | **Built in** — zero results below a measured threshold | **Absent** — the chosen agent answers from the model's judgment | **You build it** |
| Offering a choice when two agents are close | **Built in** — a setting | **Absent** | **You build it** |
| Routing accuracy measured at scale | **Built in** — published results at 1,000 agents | **Absent** — no router to measure | **You build it** — LangSmith gives the evaluation tooling |
| Answering requests no agent covers | **Absent** — by design; nothing runs without a matching agent | **Built in** — a Fleet agent is a model with tools and answers whatever it can | **You build it** |
| Event-driven and scheduled triggers | **You build it** — the REST API runs agents; the caller schedules | **Built in** — channels such as a new email or a Slack mention, and schedules | **Built in** — Deployment's cron jobs, background runs, and task queue |

## 3. Running agents

| What the purpose requires | Search2o | LangSmith Fleet | Developer stack |
|---|---|---|---|
| Deterministic execution — the same request runs the same steps | **Built in** — a fixed command sequence; the model is one command | **Absent** — model-driven by design | **You build it** — a graph can be deterministic if its author keeps it so |
| State that survives failure and pauses, and resumes later | **Built in** — saved at defined points, resumed with completed commands memoized, nothing to set up | **Built in** — Fleet runs on Deployment's durable runtime | **Configurable** — a checkpointer, its database, a state schema with reducers, thread IDs, a durability mode |
| Human-in-the-loop that resumes days later | **Built in** — `ask`, resumable from another device | **Built in** — approvals for important actions | **Configurable** — `interrupt` with a checkpointer |
| Shared context across separately built agents in one conversation | **Built in** — a follow-up can run a different agent that reads what the previous one produced | **Absent** — each agent has its own identity, threads, and memory | **You build it** — a thread belongs to one graph |
| Long-term memory per user | **Built in** — `memory`, per user, labeled, semantically searchable | **Built in** — each agent has memory | **Configurable** — the Store, namespaced, with semantic search |
| Bounded loops and per-run LLM spend | **Built in** — loop caps, no recursion, a per-run price limit | **Absent, as documented** — runs are metered; no per-run cap is documented | **Configurable** — a recursion limit is built in; spend limits through the LLM Gateway or your own code |
| Parallel execution within an agent | **Built in** — `parallel` | **Absent** — the model sequences the work | **Built in** — `Send` and parallel branches |
| Batch and non-interactive runs | **Built in** — the REST API | **Built in** — schedules and channels | **Built in** — Deployment |
| Direct access to internal APIs and databases from inside your network | **Built in** — profiles and commands on a server in your organization | **Absent** — Fleet runs in LangSmith cloud and reaches systems through connected accounts and MCP; self-hosting is in beta on an Enterprise plan | **Configurable** — built in when the Agent Server is hybrid or self-hosted; not when it runs in LangSmith cloud |
| MCP | **Built in** — client | **Built in** — client | **Built in** — client and server, plus A2A |
| Breadth of integrations | **Built in, narrow** — REST, SQL over SQLAlchemy drivers, MCP | **Built in** — Gmail, Slack, GitHub, Salesforce, BigQuery, Notion and more, plus MCP | **Built in** — over a thousand model, tool, retriever, and store integrations |
| Secrets kept out of agent definitions | **Built in** — vault and profiles | **Built in** — a credential model per agent | **Configurable** — environment secrets and custom auth |
| Sandboxed agent code under a customer-controlled allowlist | **Built in** — AST allowlist, compile rules, runtime limits | **Absent** — no code | **Absent** — the code is the boundary; Sandboxes, in private preview, cover code an agent generates |
| Arbitrary code inside an agent | **Absent** — by design | **Absent** | **Built in** |

## 4. Managing hundreds of agents across the enterprise

| What the purpose requires | Search2o | LangSmith Fleet | Developer stack |
|---|---|---|---|
| Roles — who may use, build, and administer | **Built in** — users, developers, administrators, owners | **Built in** — workspace roles plus per-agent permissions | **Configurable** — LangSmith workspace roles for the platform; custom auth handlers you write for application users |
| Per-agent sharing and permissions | **Absent** — roles are account-wide; tags filter search, not access | **Built in** — share with individuals or the workspace; clone, run, or edit | **You build it** — custom auth handlers |
| An agent acting with the invoking user's own credentials | **Absent** — agents act through profiles, with the user's identity available as a variable | **Built in** — "Assistant" agents use each user's own OAuth; "Claws" use fixed credentials | **You build it** |
| A publish gate — nothing reaches users without validation and publish | **Built in** | **Absent** — sharing exposes whatever was last saved | **You build it** — a CI pipeline |
| Central approvals across all agents | **Absent** — approvals live inside each conversation | **Built in** — the Inbox | **You build it** |
| Reports per agent per version — performance, errors, cost, usage | **Built in** — four reports from the moment an agent runs, no instrumentation | **Configurable** — LangSmith dashboards over traces; traces are metered | **Configurable** — tracing enabled, metadata for per-user attribution, traces metered with 14-day retention by default on self-serve plans |
| A trace of every production run | **Absent** — tracing is a development-time feature; production keeps aggregates | **Built in** — every action traced: which agent, on whose behalf, with what credentials | **Configurable** — LangSmith tracing |
| Single sign-on | **Built in** — OIDC | **Configurable** — LangSmith enterprise SSO | **Configurable** — LangSmith enterprise SSO |
| Service accounts for scripts and bots | **Built in** — keyed accounts with their own role | **Built in** — LangSmith API keys | **Built in** — LangSmith API keys |
| Encryption of agent state by default | **Built in** — encrypted before it leaves the agent server, without configuration | **Built in** — vendor-managed encryption at rest | **Configurable** — `LANGGRAPH_AES_KEY` or custom handlers; nothing beyond the database's own protection until set |
| Customer-held encryption keys | **Configurable** — an end-to-end mode where the cloud never decrypts state | **Absent, as documented** | **Configurable** — custom encryption with per-tenant keys and KMS |
| Dev, test, and production separation | **Configurable** — one account per environment, the same profile names resolving differently in each | **Absent, as documented** | **Configurable** — workspaces and deployment revisions |
| Data residency options | **Absent** — Search2o Cloud is US-East | **Built in** — US or EU region | **Built in** — US or EU cloud, hybrid, or self-hosted |

## 5. Operating it

| What the purpose requires | Search2o | LangSmith Fleet | Developer stack |
|---|---|---|---|
| What you install and run | **Built in** — `pip install search2o`, two environment variables, run; the same process on a laptop or in a cluster | **Built in** — nothing to run; a hosted service | **Configurable** — Agent Servers with PostgreSQL and Redis on Docker or Kubernetes; or LangSmith cloud runs it for you with the data plane outside your organization |
| Databases and queues you operate | **Built in** — none; the server is stateless | **Built in** — none | **You build it** — PostgreSQL and Redis for hybrid, standalone, and self-hosted; a full self-hosted LangSmith adds ClickHouse and is sized by its docs at 16 vCPUs and 64 GB |
| Configuration changes without restarts | **Built in** — live on the next run; a running agent keeps its configuration | **Built in** — hosted | **Configurable** — deployment revisions; standalone servers redeploy |
| Horizontal scaling | **Built in** — add servers; no session affinity | **Built in** — hosted | **Configurable** — Kubernetes with KEDA for hybrid and self-hosted; managed in LangSmith cloud |
| Running with no vendor service at all | **Absent** — search, state, and reports live in Search2o Cloud | **Absent** | **Built in** — open-source LangGraph with your own checkpointer, or a standalone Agent Server |
| Open-source license | **Absent** — source-available, proprietary | **Absent** — proprietary | **Built in** for the frameworks — LangChain and LangGraph are MIT; Deployment and Observability are proprietary |
| Model neutrality | **Built in** — any vendor or compatible endpoint, adapters for the rest | **Configurable** — models through the LangSmith platform, a custom model configurable | **Built in** |
| An end-user front door across all agents | **Built in** — one search box that finds and runs any published agent | **Built in** — a chat where the person chooses the agent, and per-agent Slack bots | **You build it** — Agent Chat UI is a chat for one assistant at a time |
| Slack, Teams, and Google Chat | **Configurable** — you build the bot from the reference prompts and API | **Built in** — Slack, Teams, and Gmail | **You build it** |
| A REST API for embedding in your own applications | **Built in** | **Built in** | **Built in** |

---

## Tally

The counts below are of cells, not of importance. Every row counts once, whether it decides a purchase or not; "built in, narrow" counts as built in; and "absent by design" counts as absent. Read the tables, then the counts, in that order.

| | Search2o | LangSmith Fleet | Developer stack |
|---|---|---|---|
| Built in | 37 | 26 | 13 |
| Configurable | 3 | 4 | 19 |
| You build it | 1 | 0 | 17 |
| Absent | 11 | 22 | 3 |
| Rows | 52 | 52 | 52 |

What the columns say, in one line each. Search2o has the most of the purpose built in and is absent where it chose to be: non-developer authoring, agent evaluation, per-agent permissions, act-as-user, central approvals, production traces, residency, arbitrary code. Fleet has the sharing, approvals, identity, and tracing of a company-wide product built in and is absent on the things that make execution predictable: routing, refusal, determinism, validation, versions, bounded spend. The developer stack is built-in least and absent almost nowhere, because it is a toolkit: most of the purpose is either configured or built, and a team that builds it gets exactly the system it wrote.

## Sources

- LangGraph overview and durable execution: docs.langchain.com/oss/python/langgraph/overview and /durable-execution
- LangSmith Deployment and Agent Server: docs.langchain.com/langsmith/deployment and /agent-server
- LangSmith hybrid, standalone, and self-hosted deployment: docs.langchain.com/langsmith/hybrid, /deploy-hybrid, /deploy-standalone-server, /kubernetes
- LangSmith encryption at rest: docs.langchain.com/langsmith/encryption
- LangSmith Fleet: docs.langchain.com/langsmith/fleet and langchain.com/blog/introducing-langsmith-fleet (March 19, 2026)
- Search2o documentation: search2o.com/docs, read in full in September 2026

Where a cell says "as documented," the claim rests on what the documentation describes and would change if the product has the capability undocumented.