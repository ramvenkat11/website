# Core concepts behind the agent server

## Stateless servers, stateful cloud

Agent server has no dependency in your enterprise. It is stateless and maintains its state in the Search2o cloud. Conversations and other sensitive information are encrypted. 

Links:
- Parts of the system -> docs/introduction/parts-of-the-system.html
- Encryption -> docs/security/encryption.html

## Structured microagents

Search2o agents are microagents with structured definitions. AI can generate one fully formed and developers can validate it before publishing. 20 built-in commands handle the workflow and all the plumbing, so that developers can focus on the business logic.

Links:
- Agent framework -> framework.html
- Live demo -> framework.html#demo

## Search by intention

Search is what lets hundreds of microagents act as one system. It matches a user request to the agent built to handle it, using the description the developer wrote. It runs in under half a second and has a high accuracy.

Links:
- Search -> search.html
- Search quality -> search.html#quality
- Live demo -> search.html#demo

## Prompts live across agents

Agents do not call each other. Instead, an agent continues a prompt from where the previous agent left off in a conversation. It can also use other information that the conversation holds. This allows agents to build on each other dynamically, without any hardcoded wiring.

Links:
- Conversations -> search.html#conversation
- Live demo -> search.html#demo


Links:
- REST API -> docs/rest-api/overview.html
- GUI -> docs/gui/index.html
- Slack and Teams -> docs/chat-integrations/index.html
- search2o-skill -> https://github.com/Search2o/search2o-skill
