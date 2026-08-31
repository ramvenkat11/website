# Introduction

AI agents are converging around a few major approaches. We compare Search2o with **Skills** and the **LangChain ecosystem** because they represent two of the most prominent approaches outside vendor-specific agent platforms.

# Skills

A skill is a reusable package of instructions and resources for an LLM. The LLM selects the skill, determines the workflow from its natural-language instructions, and executes it using the available tools.

# LangChain ecosystem

LangChain provides the building blocks for agent applications. LangGraph adds explicit workflow and state orchestration, while LangSmith provides tracing, evaluation, deployment, and operational tooling.

Together, they form a developer framework for building and running custom agentic applications.

# Search2o

Search2o is built around a different premise: **search is the orchestration layer**. Its agent framework, runtime, and end-user interface are designed around that model, creating an end-to-end platform for building, publishing, discovering, and using agents.



# Comparison table
| | **Skills** | **LangChain ecosystem** | **Search2o** |
|---|---|---|---|
| **Discovery / selection** | LLM selects the relevant skill from its description. | Not built in; the application must know or determine which graph/agent to invoke. | **Built in.** Search matches the user's request to the right agent; users do not need to know what agents exist. |
| **Primary abstraction** | Instructions + resources. | Executable graph / workflow. | Executable agent defined in JSON. |
| **Who determines the workflow?** | The LLM interprets the skill and dynamically determines how to carry out the task. | The developer explicitly programs the workflow. | The developer defines a predefined executable workflow. |
| **Control flow** | Primarily natural-language instructions interpreted by the LLM. | Explicit Python/JS graph, nodes, edges, and state. | Explicit commands and Python expressions within the agent. |
| **LLM role** | Central orchestrator: selects skills, interprets instructions, and determines execution. | Used by whichever graph nodes require LLM reasoning. | Used only where the predefined agent requires it. |
| **Runtime flexibility** | Very high; the effective workflow can change from one execution to another. | Developer controls the overall structure, though nodes and routing can themselves be agentic. | Workflow is predefined; runtime data and LLM decisions can vary within it. |
| **Determinism** | Lowest of the three. | High where graph logic is deterministic. | High; execution follows the published workflow. |
| **Execution overhead** | On each request, the LLM must select the skill, interpret its instructions, and determine the workflow. | Executes an already-defined graph. | Search typically selects the agent within **300 ms**, then executes the already-defined agent. |
| **Dynamic interaction between skills / agents** | Multiple skills can be used within the same task, with the LLM deciding which skills to load and how to combine them. | Multiple agents or subgraphs can interact, but the handoff and coordination model is designed by the developer. | **Conversations span agents.** A follow-up can go to a different agent, and agents can build on each other’s work through shared conversation context. |
| **State / conversation** | Depends on the host agent. | Explicit graph state and persistence. | Conversation context is built into the platform and can be shared across different agent executions. |
| **Durable execution / checkpointing** | Host-dependent. | First-class LangGraph capability. | Not the core execution model; agents are request-oriented executions. |
| **Human interaction during execution** | LLM/host dependent. | Human-in-the-loop and interrupts are first-class concepts. | Agents can explicitly ask the user for additional input and continue execution. |
| **Development environment** | Usually files edited with normal development tools. | Python/JS development using LangChain/LangGraph libraries and tooling. | **Built-in agent development environment** for creating, testing, and publishing agents. |
| **Publishing** | Distribution depends on the host ecosystem. | Application deployment is separate from graph development. | Publishing is part of the platform; published agents become searchable. |
| **Organization-wide discovery** | Depends on the host product. | Must be designed and implemented by the application. | Native searchable catalog of published agents across the organization. |
| **End-user UI** | Not part of the Skills standard; supplied by the host product. | Not part of the LangGraph runtime; the application normally supplies its own UI. | **Built in.** Search, execution, streaming results, conversations, follow-ups, and interaction with agents are part of the product. |
| **APIs / databases / MCP / LLM configuration** | Usually encoded in skill instructions or supplied by the hosting agent. | Defined in application code/configuration and integration libraries. | Central **profiles** for APIs, databases, MCP servers, LLMs, and prompts; agents refer to them by name. |
| **Administrative functions / UI** | Not part of the Skills standard; depends on the host product. | LangSmith provides administration for the LangChain/LangGraph platform, but application-level administration is largely left to the developer. | **Built in.** Multi-user support, authentication, roles, configuration, notifications, and an audit trail showing who changed what are part of the platform. |
| **Observability / reports** | Host-dependent. | LangSmith provides tracing, evaluation, and observability. | Built-in reports for agent performance, failures, LLM cost, and usage. |
| **Deployment architecture** | Runs wherever the hosting agent runs. | LangGraph application/runtime must be deployed; LangSmith also provides managed deployment. | **Hybrid architecture:** a stateless Search2o server runs in the customer's environment while Search2o Cloud provides discovery, configuration, and platform services. |
| **Infrastructure burden** | Very little for the skill itself; the host bears the runtime infrastructure. | You operate the application/runtime stack, including persistence and other supporting infrastructure where required. | No separate agent orchestration platform to build or operate; the Search2o server and Search2o Cloud provide it. |
| **Portability** | Strong; Skills are an open format intended to work across compatible agents. | Application code is substantially tied to LangChain/LangGraph APIs. | Agents are Search2o-specific. |
| **Development effort** | Lowest for tasks that can reliably be expressed as instructions. | Highest; essentially custom application development. | Between the two: workflows are explicit, but the surrounding platform is already provided. |
| **Best suited for** | Giving a general-purpose LLM reusable procedures and specialized knowledge. | Building custom agentic applications with complex state and execution requirements. | Building and publishing many controlled enterprise agents that users can discover and run through one search interface. |
| **Best analogy** | A playbook handed to an intelligent employee. | A custom application/workflow engine you build. | A searchable enterprise application platform for executable agents. |