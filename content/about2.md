# One system to build, run and use AI agents

Search2o is an agent platform for the enterprise. Developers build task-focused agents, the platform runs them safely against enterprise systems, and people across the organization use them through search and conversation.

**Framework.** Each agent handles one well-defined task and combines deterministic workflow steps with LLM-driven reasoning. Developers write agents as structured definitions and publish them, versioned, to a common system.

**Runtime.** Agents execute on the Search2o agent server. It calls enterprise systems, holds each agent to its time and LLM-cost budgets, and pauses for user approval before critical actions.

**Search.** Search2o matches the meaning of a request to an agent built to handle it, runs that agent and returns its output. Users don't pick an agent from a catalog, and they can get started quickly because they already understand search. This is what lets hundreds of independent agents work as one system, with no routing to wire by hand.

**Conversations.** Follow-up requests continue in the same conversation, where the user can bring in other agents that build on earlier results. The user decides the combination; nothing is prewired.

**Interfaces.** The same agents can be reached from several places. End users search and hold conversations in the browser interface or from chat applications. Agent harnesses such as Claude Code can search for and run Search2o agents as part of their own work. A REST API opens the agents to other frameworks and custom applications.

**Observability.** Every agent run is reported in real time: who asked, what ran, how long it took, any errors and the LLM token cost. Developers also get a trace of a run when building and debugging an agent.

**Administration.** Administrators manage the workspace and its members, with single sign-on and an audit trail.

**Deployment.** Search2o is a hybrid cloud system. Administrators run only stateless agent servers in their own environment; the rest is a cloud service that does not depend on your existing application infrastructure. Customers can turn on end-to-end encryption by supplying their own encryption key on the client side. A private cloud is available for enterprises.