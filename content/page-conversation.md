<!-- Source: html/conversation.html -->

<!-- Key: "Kicker:" is the small label above a heading. "> **Figure.**" gives the figure's description, then its visible labels, top to bottom; edit the wording, not the drawing. "> **Annotated code.**" is a code sample; its numbered notes are the callouts. -->

Title: Conversation — Search2o

Meta description: Conversations let agents build on each other. A conversation keeps variables and prompts. A follow-up is searched like a new request, and the matching agent continues from that record.

---

Kicker: Conversation

# Conversations let agents build on each other.

A conversation keeps variables and prompts. A follow-up is searched like a new request, and the matching agent continues from that record. No agent calls another; the conversation carries the work from one agent to the next.

> **Figure.** One conversation across two independent agents. Search matches the first request to the Travel desk agent, which asks for confirmation before booking. It matches a second request to the Reimbursements agent, which continues the same conversation and files the trip expenses.
>
> - Conversation
> - Book my trip for Tuesday's all-day meeting in New York (1)
> - **(1) [Discovery](search.html)** Search matched the request to the Travel desk agent, and the UI ran it automatically. The request had no conversation ID, so a new, empty conversation started.
> - (2) · Travel desk · UA1191 departs 06:00 Tuesday, back at 19:30, and a night at the Marriott near the office. $1,240. **Book it?** · Book · Hold · Submit
> - **(2) [Human in the loop](docs/commands/ask.html)** The agent’s state is stored, and when the user answers, the agent continues from where it paused.
> - (3) · Travel desk · Booked UA1191 and the hotel night. The confirmation is in your inbox.
> - **(3) [Conversation context](#state)** The Travel desk agent ended here, and the agent server automatically saved the conversation: the variables the agent set under `conv.`, plus its conversation-scoped prompts and their history.
> - File the expenses for that trip
> - (4) · Reimbursements · Filed the New York trip, $1,240, against your cost center. Sent to your manager for approval.
> - **(4) [Building on each other](docs/agent-execution/building-on-each-other.html)** Search matched the follow-up to Reimbursements. The request included the conversation ID, so the saved conversation was restored first. Its prompt has the same name as the Travel desk prompt, so its model continued that exchange. Neither agent called the other.

## What a conversation keeps

When an agent ends or pauses, the agent server saves the conversation’s state automatically. The next run in the conversation, whether by the same agent or another, starts from that state. Other conversations cannot see it. A conversation also belongs to one user, so other users cannot see it either.

**The runs so far.** Which agent ran, what inputs it received, what it answered, and where it stopped if it paused to ask a question.

**The prompts.** The history of every prompt used in the conversation: the user’s turns, the model’s answers, and the tool results. This history lets a model handling a follow-up remember the earlier exchange.

**The variables.** The conversation variables that every agent in the conversation can read and write, plus each agent’s own variables. An agent stores information that later agents will need, such as trip details, in a conversation variable.

## Prompts carry the exchange

A prompt is what an `llm` command sends to a model: system text, user text, and the history of the exchange so far. Each prompt has a scope that determines how long its history lasts and which agents share it.

**conversation** (the default). One history for the whole conversation, shared by every agent that has a prompt with the same name. A second agent can see what was said to the first.

**agent**. The agent’s own history for the whole conversation. Other agents in the same conversation cannot see it.

**local**. A history for one run, empty at the start of every run. Use it for one-off tasks, such as classifying or summarizing, where earlier runs should not affect the answer.

Each prompt has a name, and that name connects agents. A second agent continues the first agent’s exchange only when its prompt has the same name and uses the conversation scope. A prompt with a different name starts its own history. [Prompts](docs/agent-definition/prompts.html) explains how prompts are written and evaluated.

## Agree on names

Agents build on each other through names: the prompt name that continues the exchange, and the conversation variables that pass one agent’s findings to the next. The system does not enforce these names, so an enterprise must agree on them before its agents can work together.

A naming scheme can be short: one standard prompt name, such as `chat`, for every agent’s exchange with the user, and one name for each item agents pass to each other, such as `conv.trip`, `conv.customer`, or `conv.order`, along with what it holds. An agent that follows the scheme fits into any conversation in the account. An agent that invents its own names starts with nothing and leaves nothing the next agent can find. See [Agreeing on names](docs/agent-execution/building-on-each-other.html#agree-on-names) in the documentation.

## A follow-up can go to a different agent

A follow-up in a conversation is searched like a new request. If it belongs to another agent, that agent runs next with the conversation’s state already in place. If no new agent matches, the agent that answered last answers again.

What an interface does with the matches depends on its [search behavior](docs/search/search-settings.html). The bundled UI runs the best match immediately; your own interface can let the user choose between the two best matches.

The client always decides which agent runs next. An agent cannot run another agent. A request with several parts is coordinated from outside: an agent harness with the Search2o skill splits the request, sends each part through search and `execAgent` in the same conversation, and combines the results into one answer. See [How agents build on each other](docs/agent-execution/building-on-each-other.html).

Kicker: Live demo

## Ask for something, then follow up

The [search and conversation demo](demo-search.html) runs in a live Search2o account with 200 agents, from human resources and finance to engineering and sales. Ask for something, then ask a follow-up and watch the conversation move to another agent that knows what the first one found.

## Kept safe, kept yours

State is [encrypted](docs/security/encryption.html) before it leaves the agent server, and the cloud never decrypts it. An account can [keep the state in its own enterprise](docs/hooks/conversation-state.html) instead of storing it in the cloud. On the free service, a conversation that has been unused for 7 days is deleted unless the user [pins](docs/rest-api/conversations.html) it. A user can also delete a conversation at any time.

## Where to read more

[Conversation state](docs/agent-execution/conversation-state.html) covers what is saved and when. [Agents building on each other](docs/agent-execution/building-on-each-other.html) covers who decides what runs next, and [Prompts](docs/agent-definition/prompts.html) covers scope and the prompt name. In the REST API, [running agents](docs/rest-api/running-agents.html) covers the call above and [conversations](docs/rest-api/conversations.html) covers listing, renaming, pinning and deleting.
