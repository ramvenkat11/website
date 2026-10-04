# Search2o and LangChain: what's the difference?

Oct 3, 2026 · @Ram Venkat

## The short answer

LangChain's frameworks are for building an agent. Search2o is for an organization running many agents as one system: developers write them, and everyone else runs them from one search box. The two overlap in places, which is why the question comes up, but they start from different problems.

"LangChain" is several products, and the difference is not the same for each:

- **The frameworks.** [LangChain](https://docs.langchain.com/oss/python/langchain/overview), [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) and Deep Agents are open-source libraries for building an agent in Python or TypeScript. LangSmith is the platform for tracing, evaluating and deploying what gets built. These do a different job from Search2o.
- **[LangSmith Fleet](https://docs.langchain.com/langsmith/fleet).** A no-code product: anyone can create an agent by describing a task, then share it. Its goal is close to Search2o's, agents for a whole company, and its route there is different.

## At a glance

|  | Search2o | LangChain frameworks | LangSmith Fleet |
| --- | --- | --- | --- |
| Starting point | An organization running many agents as one system | A developer building an agent in code | Anyone creating an agent without code |
| Who writes agents | Developers | Developers | Anyone, by describing the task |
| Who uses them | Everyone in the organization | Whoever the application was built for | The creator, and the colleagues it is shared with |
| How a request reaches an agent | Search finds the agent | Through the application's own entry point | A person picks the agent by name |
| What decides the steps | The command list its developer wrote | The developer's code, the model, or a mix | The model |

## Who writes agents, and who uses them?

In Search2o these are different people. Developers write agents and publish them. Everyone else types what they need, and does not have to know which agents exist.

With LangChain's frameworks, a development team builds an agent application and owns all of it. Its users are whoever it was built for: the team itself, colleagues, or the company's customers.

With Fleet, an agent usually starts with the person who needs it. They describe a routine task in plain language and Fleet builds the agent. It can then be shared with colleagues, and a central team can publish one for the whole workspace to run ([launch post](https://www.langchain.com/blog/introducing-langsmith-fleet)).

## How does a request reach the right agent?

In Search2o, search decides. Every published agent carries a description, a request is matched against all of them, and the best match runs. When nothing fits, search returns no agent instead of improvising an answer.

Agents written by different developers need no knowledge of each other. A follow-up in the same conversation can run a different agent, which reads what the previous one produced.

In LangChain, a developer or a person decides. An application built with the frameworks has its own entry point, and its developer decides which agents it contains and how work moves between them. LangChain documents [patterns](https://docs.langchain.com/oss/python/langchain/multi-agent) for that, including subagents, handoffs and a router.

In Fleet, each agent has a name and a person picks it, in chat or by @mentioning its Slack handle.

## What is an agent?

In Search2o, an agent is a definition: an ordered list of commands in JSON, with Python expressions, for one well-defined task. Commands call an API, query a database, call a model or ask the person a question. The command list decides what runs next; the model is one of the commands, not the thing choosing them.

A definition holds no arbitrary code, and it must pass a validation run before it can be published.

In LangChain's frameworks, an agent is code, with the whole language available. With LangChain's `create_agent` and with Deep Agents, a model works in a loop and chooses the next tool. With LangGraph, the developer lays out a graph and decides which steps are fixed code and which are left to the model.

So predictable execution exists on both sides. In LangGraph it is something the developer builds; in Search2o it is the only way an agent runs.

In Fleet, an agent is a set of instructions and tools, and the model decides the steps.

## Product or toolkit?

Search2o is one product: an agent server inside your organization, a cloud service for search, state and reports, a browser interface, and a REST API. Routing, saved state, version history, roles and usage reports come with it.

LangChain's frameworks are a toolkit, and LangSmith is a set of separate products around them. They are general-purpose: the team that uses them decides what kind of agent system to build. Search2o is built on one idea: structured agent definitions combined with a search engine that finds the right one for each request.

## Which one do I need?

That depends on the job.

LangChain's frameworks fit when:

- you are building one agent application, such as a customer-facing assistant or a coding agent, and want full control in code
- the work is open-ended or long-running, and the model should plan the steps
- you need to score agent output against datasets, or keep a step-by-step trace of every production run

Fleet fits when the people who need an agent should create it themselves, without a developer.

Search2o fits when:

- the organization will have many agents, written by different developers, and people should reach all of them from one place
- the tasks are well defined and should follow steps a developer wrote, within set limits on time and model cost
- developers should spend their time writing agents, not building the routing, state, versioning and reporting around them

## Can I use both?

Yes. They connect through standard interfaces, in both directions.

- **LangChain calling Search2o.** Search2o's [REST API](https://search2o.com/docs/rest-api/index.html) lets any program search for an agent and run it. An agent built with LangChain or LangGraph can call it as a tool, the way the [Search2o skill](https://search2o.com/docs/skill-integration/index.html) does for Claude Code.
- **Search2o calling LangChain.** A Search2o agent can call REST APIs and MCP servers. LangSmith's Agent Server exposes each deployed agent [as an MCP tool](https://docs.langchain.com/langsmith/server-mcp) and through its own REST API.

## Sources

LangChain statements were checked against LangChain's own pages on October 3, 2026. Search2o statements come from the [Search2o documentation](https://search2o.com/docs).

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [LangSmith Fleet](https://docs.langchain.com/langsmith/fleet)
- [Introducing LangSmith Fleet](https://www.langchain.com/blog/introducing-langsmith-fleet), March 19, 2026
- [MCP endpoint in Agent Server](https://docs.langchain.com/langsmith/server-mcp)
