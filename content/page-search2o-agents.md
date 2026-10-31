<!-- Source: docsrc/introduction/search2o-agents.html (published as html/docs/introduction/search2o-agents.html) -->

<!-- Key: "Kicker:" is the small label above a heading. "> **Figure.**" gives the figure's description, then its visible labels, top to bottom; edit the wording, not the drawing. "> **Annotated code.**" is a code sample; its numbered notes are the callouts. -->

# Search2o agents

Search2o agents are to AI what microservices are to applications.

A Search2o agent is built for a single task and runs on the agent server. It does not call other agents. It takes an input, produces an output and finishes in seconds, and it is expected to run thousands of times, for different users.

A Search2o agent has clear boundaries: the systems it can reach, its maximum run time and its LLM cost.

A Search2o agent also carries a plain-language description of the task and its boundaries. Search uses that description to find the agent for a request.

## Examples

Search2o agents:

- **Vacation request**: takes the dates, checks the balance, files the request, reports the result.
- **Invoice status**: an invoice number in, where it stands in accounts payable out.
- **Expense filing for a trip**: retrieves the trip's amounts, files the claim, asks before submitting.

Each is one verb, one or two systems, and a run measured in seconds.

The same rule applies in every case: a Search2o agent has a boundary on systems, time and cost, and a small set of paths that can be validated. That boundary is also what makes a description precise enough for search to match. The less the boundaries of agents overlap, the more easily search matches a request to a single agent.

## What a Search2o agent is not

- An agent that runs on a person's own machine.
- An agent built to run for hours or days.
- An agent run only by the people who built it.
- A general-purpose agent that calls other agents for specific tasks.

## How a Search2o agent runs

A request that matches the agent's description starts it; see [How matching behaves](../search/how-matching-works.html). The agent runs for a short time, may ask the user for inputs or an approval on the way, and produces a response.

## Benefits of the boundary

**Validation.** A Search2o agent has a small number of specific paths, as a workflow does, rather than an open-ended set. That is what makes it possible to validate the agent before it is published: a real run against a validation query, with every step in the trace. See [Trace and validation](../development/trace-and-validation.html).

**Dependability.** The same request takes the same path through the same commands, so the agent behaves the same way on every run. A failure has a place: the command it failed at, in the run's record.

**Safety.** The agent reaches only the systems its profiles name, runs inside the [agent runtime](../runtime/controlled-execution.html), and stops at its [time and cost budgets](../runtime/runtime-limits.html).

**Observability.** Every run is recorded: who requested it, what ran, how long it took, what failed, and what the LLM calls cost. The [reports](../reports/index.html) show these per agent and per user.

## How Search2o agents work together

Search2o agents do not call each other. They build on each other's work through the shared context of a [conversation](../agent-execution/conversation-state.html): the prompts and the conversation variables. Two agents share a prompt's history when both have a prompt of the same name with the `conversation` scope; see [Prompts](../agent-definition/prompts.html#sharing-a-history-between-agents).

A shared prompt history does not depend on the model, so a second agent in the same conversation can use a different LLM and still continue the exchange. [Conversation variables](../agent-definition/variables.html) carry the context that is not in a prompt, such as the user's authorization.
