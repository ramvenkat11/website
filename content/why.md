# Why Search2o

**Search2o is a platform where agents are the developers' business, and users just get their work done.**

With the Search2o [agent framework](https://search2o.com/framework.html), a developer builds, tests, and publishes an agent in minutes. It goes to a central server and is there for everyone at once. Nothing is installed anywhere.

Agents come and go. Developers add, change, and remove them, all the time. Users don't have to keep track of any of it. They have no list to learn and no names to remember. They say what they want, and search runs the agent built for it.

Because every agent lives in one place, there is one version to fix, one set of credentials to guard, and a record of every run.

## Which one fits

| What you want | Use |
|---|---|
| Developers publish agents. Users say what they need, and the right agent runs. | **Search2o** |
| Build a general purpose agent application in Python | LangChain / LangGraph, CrewAI, LlamaIndex |
| Give people an agent to run on their own machine | Skills |
| Build agents inside one vendor's products | That vendor's builder: Copilot Studio, Agentforce, OpenAI Frontier |

## Search2o and LangChain

LangChain and LangGraph are tools for building a general purpose agent application in Python. The team that builds it also builds everything around it: how requests reach it, where it runs, who can use it, how it is updated, and how it is tracked. The same goes for other Python frameworks such as CrewAI and LlamaIndex.

**Choose LangChain when** you are building one application and want full control in code, or when the agent has to work on its own for a long time.

**Choose Search2o when** agents written by developers have to be used by other people. Everything around the agent is already there and is the same for every agent. The developer writes the task and publishes it.

**Together:** a LangGraph application can call Search2o to find and run a published agent, and a Search2o agent can call what you have deployed elsewhere. [More detail](https://search2o.com/docs/comparisons/langchain.html)

## Search2o and skills

A skill puts a copy of the agent with every person who uses it. It runs on their machine, with their credentials and their model, at whatever version they last pulled.

**Choose skills when** the work belongs on the user's machine: their files, their spreadsheets, their code.

**Choose Search2o when** the work reaches company systems. Credentials and logic stay on the server, there is one version, and every run is recorded.

**Together:** one [small skill](https://search2o.com/docs/skill-integration/index.html) lets Claude Code find and run published agents. A Search2o agent returns inventory data as a CSV, and a local skill loads it into Excel and analyzes it, in one request.

## Search2o and Microsoft, Salesforce, OpenAI

Copilot Studio, Agentforce, and OpenAI Frontier also let you build agents for other people to use. Each is at its best inside its own vendor's products, models, and cloud.

**Choose the vendor's builder when** the work lives inside that vendor's products. It comes with tools made for them, and you may need those.

**Choose Search2o when** the work crosses systems, or when you want to decide where agents run and which model they use. The agent server runs in your environment, works with any model including local ones, and reaches any API, database, or MCP server you point it at.

**Together:** nothing has to be replaced. Search2o agents can call those platforms through their APIs.

## When Search2o is not the right choice

- You are building an agent only for yourself to run.
- You want to give people the agent itself, to read, change, and run locally.
- You want a general purpose ReAct agent: one agent that reasons in a loop and picks from many tools to handle any request. A Search2o agent does one task.
- You need agents that work on their own for hours or days.
- You want non-developers to build agents without code.

[What a Search2o agent is, and is not](https://search2o.com/docs/introduction/search2o-agents.html)

## Try it

The agent server is free and source available. The cloud service is free during the beta, and usage based after that.

- **[Chat with published agents](https://search2o.com/demo-search.html)**. No signup.
- **[Get started](https://search2o.com/gettingstarted.html)**. Free account and `pip install search2o`.
- **[Talk to us](https://search2o.com/about.html#contact)**. Tell us what you want to publish. We will help you build the first agents.