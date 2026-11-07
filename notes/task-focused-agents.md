# Task-focused agents

Markdown copy of docsrc/introduction/search2o-agents.html (published at docs/introduction/search2o-agents.html), 2026-11-06. Edit here; links are the page's, relative to docs/introduction/.

A Search2o agent is built for a single task. It does not call other agents. It takes an input, produces an output and it completes in seconds. It runs on the agent server, and it is expected to run thousands of times, for different users.

The agent has clear boundaries: the systems it can reach, its maximum run time and its LLM cost.

Each agent also carries a plain-language description of the task and its boundaries. Search uses that description to find the agent for a request.

## Examples

Task-focused agents:

- **Vacation request**: takes the dates, checks the balance, files the request, reports the result.
- **Invoice status**: an invoice number in, where it stands in accounts payable out.
- **Expense filing for a trip**: retrieves the trip's amounts, files the claim, asks before submitting.


The same rule applies in every case: a Search2o agent has a boundary on systems, time and cost, and a small set of paths that can be validated. That boundary is also what makes a description precise enough for search to match. The less the boundaries of agents overlap, the more easily search matches a request to a single agent.


## What a Search2o agent is not

- A personal agent.
- An agent built to always run.
- A general-purpose agent that calls other agents for specific tasks.

## How a Search2o agent runs

A request that matches the agent's description starts it; see [How matching behaves](../search/how-matching-works.html). The agent runs for a short time, typically a few seconds, may ask the user for inputs or an approval on the way, and produces a response.

## Benefits of the boundary

**Validation.** A Search2o agent has a small number of specific paths, as a workflow does, rather than an open-ended set. That makes it possible to validate the agent before it is published: a real run against a validation query, with every step in the trace. See [Trace and validation](../development/trace-and-validation.html).

**Dependability.** The same request takes the same path through the same commands, so the agent behaves the same way on every run. 

**Safety.** The agent reaches only the systems its profiles name, runs inside the [agent runtime](../runtime/controlled-execution.html), and stops at its [time and cost budgets](../runtime/runtime-limits.html). User specific restrictions are handled inside the agent code. 

**Observability.** Every run is recorded: who requested it, what ran, how long it took, what failed, and what the LLM calls cost. The [reports](../reports/index.html) show these per agent and per user.

## How Search2o agents work together

Search2o agents do not call each other. They build on each other's work in a [conversation](../agent-execution/conversation-state.html): the prompts and the conversation variables at the conversation scope. It is important to have a common data model or prompt naming convention for this to work right; see [Prompts](../agent-definition/prompts.html#sharing-a-history-between-agents).


