# Home section 3: the six notes beside the agent code

Current text in html/index.html (2026-11-05). Numbers match the badges in the code card.

## 1. The complete agent
JSON with Python expressions in the braces, and this file is all of it. Draft with AI wrote it from “handles employees’ IT support requests”. The agent editor, a trace of every run, validation and publishing come with the server.

Links: JSON with Python expressions -> docs/agent-definition/syntax.html; Draft with AI -> docs/development/draft-with-ai.html; agent editor -> docs/development/code-editor.html; trace -> docs/development/trace-and-validation.html; publishing -> docs/development/publishing.html

## 2. Calling enterprise systems
The endpoint, credentials and error handling come from the helpdesk profile. The agent holds only the path and the body, and result holds the response. Databases and MCP servers work the same way.

Links: helpdesk profile -> docs/profiles/index.html

## 3. LLM calls
The profile names the model and holds the key. Six adapters are bundled: OpenAI, Anthropic and Gemini, and Ollama, vLLM and SGLang for models you host. Change the model by changing this one word.

Links: Six adapters -> docs/llm/vendors.html

## 4. Prompts live outside the code
The prompt is written and changed in the UI, so a wording change is not a code change.

Links: prompt -> docs/agent-definition/prompts.html

## 5. The tool loop is the server’s job
The model calls openTicket when a request needs a ticket. The server runs the call and feeds the result back. Tool calling

Links: Tool calling -> docs/commands/llm.html#tool-calling

## 6. Everything after the answer
The answer streams to the client. Limits, guardrails, the audit log and the cost report run outside the agent. Runtime

Links: Runtime -> runtime.html

# The previous figure: six parts and the pieces inside each

The box figure that section 3 carried until 2026-11-04 (last committed in 8d0c7fcb), inside a
dashed "Agent server" outline. Each part title linked to its page and each piece to its docs page.

## LLMs (docs/llm/index.html)
LLM calls, Tool calling loop, MCP, Model neutrality

## Agent workflow (framework.html)
API and database calls, Parallel execution, Error handling, Human in the loop, Progress,
Streaming, Externalized prompts, Externalized system calls

## Development environment (docs/development/index.html)
Draft with AI, Agent editor, Trace and validation, Agent versioning, Multi-developer publishing

## Routing (search.html)
Search picks the agent

## Runtime (runtime.html)
Live configuration, Hooks, Audit log, Connection pools, Secret vault, Authentication,
Runtime limits, Guardrails, Observability

## State management (conversation.html)
Save/Restore conversations, Agent memory
