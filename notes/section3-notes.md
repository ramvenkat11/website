# Home section 3: the six notes beside the agent code

Current text in html/index.html (2026-11-04). Edit here; the numbers match the badges in the code card.

## 1. Developing an agent
Agent syntax (json, python), Draft wth AI, Code editor, trace, validate, publish

## 2. Calling enterprise systems
The API endpoint details come from profile. Databases and MCP servers work the same way. result holds the response from the API. 

Links: helpdesk profile -> docs/profiles/index.html

## 3. LLM calls 
The profile names the model and holds the key. Six adapters are bundled: OpenAI, Anthropic and Gemini, and Ollama, vLLM and SGLang for models you host. Change the model by changing this one word.

Links: Six adapters -> docs/llm/vendors.html

## 4. Prompts live outside the code
The prompt is written and changed in the UI, so a wording change is not a code change.

Links: prompt -> docs/agent-definition/prompts.html

## 5. The tool loop is the server's job
The model calls openTicket when a request needs a ticket. The server runs the call and feeds the result back. Tool calling

Links: Tool calling -> docs/commands/llm.html#tool-calling

## 6. Everything after the answer
The answer streams to the client. The conversation is saved for the next turn. 

Links: Runtime -> runtime.html
