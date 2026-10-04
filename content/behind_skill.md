# Search2o behind a skill: what it buys

Oct 3, 2026 · @Ram Venkat

Build each repeatable task on your company's systems as a task-specific agent in Search2o, and install one skill in Claude Code. The skill makes two calls on your agent server: `search` finds the agent for a request, and `execAgent` runs it. Claude Code keeps the agentic loop; the work on your systems runs on the agent server.

The usual alternative is a skill per workflow, with MCP servers or scripts that reach company systems from each laptop. There, Claude reads the instructions and writes and runs the steps itself, on every run, in every person's session.

This page lists what changes when those workflows become Search2o agents. Claims about either side link to their sources, listed at the end. Claude Code stands here for any client that supports Agent Skills.

## At a glance

| What changes | A skill per workflow, with MCP servers or scripts | One skill, agents in Search2o |
| --- | --- | --- |
| Where a workflow lives | In instructions Claude interprets on each run | In a fixed, validated, versioned agent that runs on your server |
| What enters Claude's context | The instructions, every step Claude writes, every intermediate result | The skill's instructions, the names and titles of matching agents, each agent's output |
| Model tokens per run | Finding the skill, loading it, and a model call for each step Claude writes | One skill, two calls by Claude, and the agent's `llm` steps; search and other commands cost none |
| When the assistant's model changes | Each skill is due a retest | One skill is due a retest |
| Models a step can use | Claude models | Any vendor's, chosen per step in a profile |
| What a laptop holds | A route and a credential for each system, or for the MCP server in front of it | One revocable token for the agent server |
| What can act on your systems | What the model decides at run time, within the person's access and permission rules | Published agents, inside their profiles, allowlist, time and cost bounds |
| Record of a run | Session telemetry, if you collect it | Agent, version, person, duration, result and cost, in built-in reports |
| Adding a workflow | A skill has to reach each person's machine or account | An agent is published |

## Context and tokens

### 1. Claude's context holds results, not workflows

When Claude carries out a workflow, the workflow itself is written into its context. Claude generates each step as it goes: a command, a script, a tool call. Each step stays in the conversation with its result, and [the whole conversation is re-sent](https://code.claude.com/docs/en/prompt-caching) on every later request.

Anthropic describes what this does. With direct tool calls, [each intermediate result passes through the model](https://www.anthropic.com/engineering/code-execution-with-mcp); a document read from one system and written to another crosses the context twice. As a context grows, the model [recalls what is in it less accurately](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), an effect known as context rot.

Instructions and tool definitions add to it. A skill's body, once loaded, [stays in context across turns](https://code.claude.com/docs/en/skills#skill-content-lifecycle). MCP tool definitions are [deferred by default](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search), but each search [loads up to five](https://code.claude.com/docs/en/agent-sdk/tool-search), which stay until that part of the conversation is compacted.

With Search2o the workflow is not written at run time. It is a published agent, and it runs on the agent server. Claude's context receives the Search2o skill's instructions, the names and titles of the matching agents, and each agent's output. The agent's commands, API responses, database rows and variables [stay on the agent server](https://search2o.com/docs/agent-execution/controlled-runtime.html).

### 2. The workflow is not generated again on every run

A workflow that Claude carries out costs model tokens at three points, each time anyone runs it. Finding the skill: the description of every installed skill is in every request, [about 100 tokens each](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). Loading it: the skill body, which Anthropic sizes at under 5,000 tokens, enters the context and stays. Generating the workflow: Claude writes the steps in a loop of model calls, one for each step.

Each call [re-sends the full conversation](https://code.claude.com/docs/en/prompt-caching); prompt caching bills the re-read at a lower rate but does not remove it.

Anthropic makes the same point about code inside a skill. A bundled script costs only its output in tokens, which its documentation describes as much more efficient than having Claude write equivalent code each time. A Search2o agent applies that to the whole workflow, and moves it off the laptop.

In Search2o, [search costs no model tokens](https://search2o.com/docs/skill-integration/what-search2o-provides.html), and an agent's flow control, API calls and database calls cost none. Only an `llm` command spends tokens: on the model its profile names, under the company's key, within the agent's [cost bound](https://search2o.com/docs/agent-execution/controlled-runtime.html).

On Claude's side the cost is fixed: one skill, two calls and the result, however many agents exist and however many steps each one takes. When two hundred people run the same workflow, the difference repeats two hundred times.

### 3. One skill entry stands for the whole catalogue

Every installed skill puts its name and description in Claude's context, [about 100 tokens each](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), and Claude chooses among them by reading the descriptions. Anthropic [advises limiting](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise) how many are loaded at once: with too many, Claude may pick the wrong skill or miss the right one. In Claude Code the listing has a budget of [1% of the context window](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short); past it, descriptions are dropped, least-used skills first, and only names remain.

The Search2o skill takes one entry. Behind it, search matches the request against every published agent's description in under a second, with no model call. Adding an agent changes nothing in the skill or on any laptop.

Search accuracy is [measured and published](https://search2o.com/docs/search/search-quality.html). The tests ran on catalogues Search2o built. On a catalogue of 1,000 agents, the right agent came first for 85.5% of 10,000 questions and was among the first three for 94.1%. On five catalogues of 50 to 100 agents the figures were 83.8–91.0% and 94.9–98.2%.

These figures measure search on its own. Through the skill, Claude reads the titles of the matches and runs the one that fits.

## Models

### 4. Workflows do not change when the assistant's model changes

A skill is a prompt, and its effect depends on the model that reads it. Anthropic says so: a skill's effectiveness [depends on the underlying model](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), it should be tested with every model you plan to use, and evaluations should be [rerun as models evolve](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise).

Claude Code's bundled [`/claude-api prompt-audit`](https://code.claude.com/docs/en/skills) flags instructions written for older models in prompts, skills and tool descriptions. Its model aliases [move to newer versions over time](https://code.claude.com/docs/en/model-config) unless pinned.

Users report the same from their side: [prompts that stopped working](https://theagentarchitect.substack.com/p/claude-sonnet-4-prompts-stopped-working) when Sonnet 4.5 replaced 3.7, [skills that degraded output](https://www.mindstudio.ai/blog/how-to-fix-claude-code-skills-prompts) after a model upgrade, and a [pull request refreshing a skills repository's prompts](https://github.com/rohitg00/pro-workflow/pull/113) for current models.

A Search2o agent is a fixed list of commands. Which calls it makes, in what order and with what checks, does not depend on the model driving Claude Code. When the assistant's model changes, one skill is due a retest, not one per workflow.

An `llm` step inside an agent is still a prompt. It keeps running on the model its profile names, so a new model reaches your agents when you change the profile, not when the assistant upgrades. That prompt is due the same retest when you do.

### 5. Each step uses the model that fits, from any vendor

Claude Code is built for Claude models. Anthropic's documentation says it "[doesn't support routing Claude Code to non-Claude models](https://code.claude.com/docs/en/llm-gateway) through any gateway". Within Claude, a skill or a subagent can [name a different model](https://code.claude.com/docs/en/skills).

In an agent, each `llm` command names a profile, and [a profile is one model at one vendor](https://search2o.com/docs/profiles/llm-profiles.html). OpenAI, Anthropic and Gemini are bundled. Any endpoint that speaks one of their protocols needs only a profile; anything else needs an adapter.

One agent can extract fields with a small model, reason with a larger one, and keep a sensitive step on a model you host. A profile is [changed once and every agent that uses it follows](https://search2o.com/docs/profiles/overview.html) on its next run, so retiring a model is one edit.

## Control

### 6. Laptops hold one token, not system credentials

For a skill's script, or an MCP server set up on the laptop, to reach a company system, the laptop needs a network route and a credential: for the system itself, or for the MCP server in front of it. In Claude Code, a skill's scripts have [the same network access as any other program](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) on the person's computer.

With Search2o the laptop reaches one host, the agent server, with one credential: a per-person [integration token](https://search2o.com/docs/skill-integration/installing-the-skill.html). The token can search, run agents and manage that person's own conversations. It cannot read or change configuration, and it can be revoked.

Credentials for the systems themselves are [read on the agent server at run time](https://search2o.com/docs/security/data-privacy.html) and never reach the laptop or Claude. Direct routes from laptops to those systems can be closed. This is the place an agent gateway takes, except that Search2o also runs the agents.

### 7. Claude chooses which agent runs; it does not write what runs

When Claude carries out a workflow, the actions are decided at run time by the model and run with the person's access. Claude Code's [permission rules](https://code.claude.com/docs/en/permissions) decide which of them need the person's approval.

Anthropic's guidance warns that a malicious skill [can direct Claude to invoke tools or run code](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) in ways that do not match its stated purpose. It also warns that content fetched from outside may carry malicious instructions.

A published agent's actions are [fixed by its author](https://search2o.com/docs/agent-execution/controlled-runtime.html). It reaches only what its profiles name, and its expressions call only what the account's allowlist permits. Each run stops at the agent's time and cost bounds.

With direct routes closed, an assistant that is mistaken, or misled by text it has read, can run only published agents, as that person, with the inputs it supplies. It cannot run new code against your systems.

### 8. Intermediate data stays on your server

In a model-driven workflow, every API response and query result the model handles is sent to the model's vendor as part of the conversation.

In an agent, API responses, database rows and credentials [stay on the agent server](https://search2o.com/docs/security/data-privacy.html) unless the agent writes them into its output or a conversation variable. Claude, and the vendor behind it, sees only what the agent's author chose to output. Data reaches an LLM inside the agent only where an `llm` command sends it, to the vendor that step's profile names.

### 9. The same request takes the same steps

A skill guides what Claude does; it does not define it. Anthropic lists [instruction following](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise) among the things to evaluate in a skill, with Claude skipping validation steps as its example of failure.

A skill can bundle a script for the fixed parts, and Anthropic recommends it. The script still runs on the laptop, with the person's access.

An agent [takes the same path through the same commands](https://search2o.com/docs/introduction/task-specific-agents.html) on every run. Nothing is published without a real validation run. Every publish creates a version, each run is recorded against the version that ran, and a failure names the command it failed at.

The output of an `llm` step can still vary, as any model call does.

### 10. Every run is recorded in one place

Search2o [records every run](https://search2o.com/docs/introduction/task-specific-agents.html): who requested it, what ran, how long it took, what failed, and what the LLM calls cost. [Reports](https://search2o.com/docs/reports/cost.html) show these per agent, per version and per person. Cost is computed from the prices set in each LLM profile. A run started from Claude Code appears under the person's name, beside runs from the GUI and the chat bots.

Claude Code can [export OpenTelemetry metrics and events](https://code.claude.com/docs/en/monitoring-usage) to a collector you operate: model requests with tokens and cost, tool calls and skill activations, attributed to a user. It is opt-in, and the names of user-configured MCP servers and tools are withheld unless detail logging is on.

That is a record of model and tool activity in a session. Search2o's is a record of the business action: which agent, which version, for whom, with what result.

## Reach

### 11. Publish once, for every person, surface and assistant

A new agent is available to everyone as soon as it is published and described. Nothing is installed on a laptop, and the skill does not change. A corrected agent replaces the old version for everyone on the next run.

A skill is a set of files. It has to reach each person's machine or account, through a repository, a plugin, managed settings or account sync. The Search2o skill is installed the same way, once, with a token for each person.

The same published agent [serves the GUI, the chat bots, the REST API and the skill](https://search2o.com/docs/skill-integration/what-search2o-provides.html). The skill folder follows the open [Agent Skills](https://agentskills.io) standard, so it works unmodified in other clients, Cursor and OpenAI Codex among them. The work that goes into an agent is not tied to one assistant.

### 12. State outlives the session

Agents in one conversation share state that Search2o saves: the prompt history and conversation variables, [stored encrypted and kept for three months](https://search2o.com/docs/security/data-privacy.html) after last use. Two agents written by different developers build on each other's work without knowing about each other.

An agent can pause to ask the person a question and continue when the answer arrives. A password is [never typed into the chat](https://search2o.com/docs/skill-integration/finding-and-running-an-agent.html); the assistant gives the person a link to the conversation in the GUI instead.

That state does not depend on Claude's context. If the session is compacted or closed, the conversation is still there, under the person's account.

## What stays with Claude

Claude Code keeps the agentic loop. It [splits a request into parts](https://search2o.com/docs/skill-integration/finding-and-running-an-agent.html), sends each through `search` and `execAgent`, decides the order and the conditions from the results, and composes one answer.

A support engineer types: *Has order 48812 shipped? If not, open a ticket with the warehouse.* Claude runs the order-lookup agent and reads "not shipped". It then finds and runs the warehouse-ticket agent in the same conversation. Search2o did each step inside the company; Claude decided the order and the condition.

Claude also keeps everything it does without Search2o: files, code, and requests nobody has built an agent for. When nothing fits, search returns no match instead of guessing. In [published tests](https://search2o.com/docs/search/search-quality.html) it refused 100% of unrelated questions and 82–86% of in-domain questions that no agent covered. Claude then answers as it normally would.

## What it costs

- **Someone writes the agents.** A developer learns a JSON definition with 23 commands. [Draft with AI](https://search2o.com/docs/development/draft-with-ai.html) writes a draft from a description and leaves queries and API paths for the developer to fill in. Each agent is then validated and published.
- **You run the agent server.** It installs with pip and is stateless. It is still a service your company operates.
- **Requests pass through Search2o Cloud.** The request text is sent in plain form to be matched, then stored encrypted. So is the text of a long-term memory an agent stores. API responses and database rows are not sent unless an agent writes them into its output or a conversation variable.
- **Definitions and state are stored in Search2o Cloud.** Agent definitions and profiles are stored in plain form, except prompt profiles, and without secret values. Conversation state is stored encrypted. By default Search2o manages the encryption key; with end-to-end encryption the key stays in your organization.
- **The skill is still a skill.** Claude decides from its description whether a request is for a company agent, and picks among the matches. The description needs fitting to your company.
- **Agent output is still input.** What an agent returns enters Claude's context, including text the agent fetched from elsewhere. The skill tells Claude to treat it as data, not as instructions.

## Sources

Pages opened on October 3, 2026.

**Anthropic**

- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
- [Scale to many tools with tool search](https://code.claude.com/docs/en/agent-sdk/tool-search)
- [Configure permissions](https://code.claude.com/docs/en/permissions)
- [Model configuration](https://code.claude.com/docs/en/model-config)
- [Other LLM gateways](https://code.claude.com/docs/en/llm-gateway)
- [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)
- [Monitoring](https://code.claude.com/docs/en/monitoring-usage)
- [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp), November 4, 2025
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), September 29, 2025

**Search2o**

- [Skills + Search2o](https://search2o.com/docs/skill-integration/overview.html)
- [What Search2o adds](https://search2o.com/docs/skill-integration/what-search2o-provides.html)
- [What the skill does](https://search2o.com/docs/skill-integration/finding-and-running-an-agent.html)
- [Installing the skill](https://search2o.com/docs/skill-integration/installing-the-skill.html)
- [Task-specific agents](https://search2o.com/docs/introduction/task-specific-agents.html)
- [Controlled runtime](https://search2o.com/docs/agent-execution/controlled-runtime.html)
- [Search quality](https://search2o.com/docs/search/search-quality.html)
- [How profiles work](https://search2o.com/docs/profiles/overview.html) and [LLM profiles](https://search2o.com/docs/profiles/llm-profiles.html)
- [Data privacy](https://search2o.com/docs/security/data-privacy.html)
- [LLM cost report](https://search2o.com/docs/reports/cost.html)
- [Draft with AI](https://search2o.com/docs/development/draft-with-ai.html)

**Others**

- [Agent Skills standard](https://agentskills.io)
- Chris Tyson, [The Day Anthropic Broke 90% of My Prompts](https://theagentarchitect.substack.com/p/claude-sonnet-4-prompts-stopped-working), October 3, 2025
- MindStudio, [Fix Degraded Claude Code Output: Trim Skills, Not Add Them](https://www.mindstudio.ai/blog/how-to-fix-claude-code-skills-prompts), August 12, 2026
- [Refresh skill prompts for current Claude models](https://github.com/rohitg00/pro-workflow/pull/113), a pull request on rohitg00/pro-workflow
