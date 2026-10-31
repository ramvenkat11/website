<!-- Source: docsrc/introduction/search2o-agents.html (published as html/docs/introduction/search2o-agents.html) -->

<!-- Key: "Kicker:" is the small label above a heading. "> **Figure.**" gives the figure's description, then its visible labels, top to bottom; edit the wording, not the drawing. "> **Annotated code.**" is a code sample; its numbered notes are the callouts. -->

# Search2o agents

A Search2o agent is an independent unit built for a single task that runs on the agent server. They do not call other agents. An agent is expected to run thousands of times, for different users, complete running in a short amount of time, take an input and produce an output. Search2o agents are to AI what microservices are to applications.

A Search2o agent has clear boundaries: the systems it can reach, and its time and LLM cost budgets. 

A Search2o agent also carries a plain-language description of the task and its boundaries. Search reads that description to find the agent for a request.

A Search2o agent keeps its state in the conversation, not on the agent server. It has state of its own, the `agent` scope, which only it reads, and it shares state with every agent in the conversation through the `conversation` scope. The agent server saves both when a run ends or pauses, so what one agent produces is available to the next one that runs in the same conversation. The state is per conversation: another conversation cannot see it, and a conversation belongs to one user, so another user cannot see it either. See [Conversation state](../agent-execution/conversation-state.html).

## Examples

Search2o agents:

- **Vacation request** : takes the dates, checks the balance, files the request, reports the result.
- **Invoice status** : an invoice number in, where it stands in accounts payable out.
- **Expense filing for a trip** : retrieves the trip's amounts, files the claim, asks before submitting.

Each is one verb, one or two systems, and a run measured in seconds.

The same rule applies in every case. A Search2o agent has a boundary on systems, time and cost, and a small set of paths that can be validated. That boundary is also what makes a description precise enough for search to match. The less overlap one has on the boundaries, more easily search would be able to match a request to a single agent. 

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
