<!-- Source: html/conversation.html -->

<!-- Key: "Kicker:" is the small label above a heading. "> **Figure.**" gives the figure's description, then its visible labels, top to bottom; edit the wording, not the drawing. "> **Annotated code.**" is a code sample; its numbered notes are the callouts. -->

Title: Conversation — Search2o

Meta description: Conversations let agents build on each other. A conversation keeps what every agent in it did, said and was told. A follow-up is searched like a new request, and the agent that matches continues from that record.

---

Kicker: Conversation

# Conversations let agents build on each other.

A conversation keeps what every agent in it did, said and was told. A follow-up is searched like a new request, and the agent that matches continues from that record. No agent calls another; the conversation carries the work from one to the next.

> **Figure.** One conversation across two independent agents. Search matches the first request to the Travel desk agent, which asks before booking. A second request is matched to the Reimbursements agent, which continues the same conversation and files the expenses for the trip.
>
> - Conversation
> - Book my trip for Tuesday's all-day meeting in New York (1)
> - **(1) [Discovery](search.html)** Search matched the request to Travel desk agent, and the UI ran it automatically. The request carried no conversation id, so a new, empty conversation started.
> - (2) · Travel desk · UA1191 departs 06:00 Tuesday, back at 19:30, and a night at the Marriott near the office. $1,240. **Book it?** · Book · Hold · Submit
> - **(2) [Human in the loop](docs/commands/ask.html)** The agent’s state is stored, and when the user answers, the agent continues from where it paused.
> - (3) · Travel desk · Booked UA1191 and the hotel night. The confirmation is in your inbox.
> - **(3) [Conversation context](#state)** Travel desk agent ended here, and the agent server saved the conversation automatically: the variables the agent set under `conv.`, and its conversation-scope prompts with their history.
> - File the expenses for that trip
> - (4) · Reimbursements · Filed the New York trip, $1,240, against your cost center. Sent to your manager for approval.
> - **(4) [Building on each other](docs/agent-execution/building-on-each-other.html)** Search matched the follow-up to Reimbursements. The request carried the conversation id, so the saved conversation was restored first. Its prompt has the same name as Travel desk’s, so its model continued that exchange. No agent called the other.

## What a conversation keeps

When an agent ends or pauses, the agent server saves the conversation’s state. The agent does nothing for this. The next run in the conversation, by the same agent or another, starts from it. Another conversation cannot see it, and a conversation belongs to one user, so another user cannot see it either.

**The runs so far.** Which agent ran, with which inputs, what it answered, and where it stopped when it paused with a question.

**The prompts.** For every prompt used in the conversation, its history: the user turns, the model’s answers and the tool results. This history is what lets a model in a follow-up remember the earlier exchange.

**The variables.** Conversation variables, which every agent in the conversation reads and writes, and each agent’s own variables. An agent saves what later agents will need as a conversation variable, such as the trip.

## Prompts carry the exchange

A prompt is what an `llm` command sends to a model: a system text, a user text and the history of the exchange so far. Each prompt has a scope, which says how long its history lives and which agents share it.

**conversation** , the default. One history for the whole conversation, shared by every agent that has a prompt of the same name. A second agent sees what was said to the first.

**agent** . The agent’s own history for the whole conversation. Another agent in the same conversation does not see it.

**local** . A history for one run, empty at the start of every run. For one-off tasks inside a run, such as classifying or summarizing, where earlier runs should not influence the answer.

Each prompt has a name, and the name is what connects agents. A second agent continues the first agent’s exchange only when its prompt has the same name and the conversation scope. A prompt with another name starts a history of its own. How a prompt is written and evaluated is in [Prompts](docs/agent-definition/prompts.html).

## Agree on names

Agents build on each other through names: the prompt name that continues the exchange, and the conversation variables that carry what one agent found to the next. Nothing enforces the names, so an organization agrees on them before its agents can work together.

A naming scheme is short. One standard prompt name, such as `chat`, for every agent’s exchange with the user. A name for each thing agents hand to each other, such as `conv.trip`, `conv.customer` or `conv.order`, with what it holds. An agent that follows the scheme fits into any conversation in the account. One that invents its own names starts from nothing, and leaves nothing the next agent can find. See [Agreeing on names](docs/agent-execution/building-on-each-other.html#agree-on-names) in the documentation.

## A follow-up can go to a different agent

A follow-up in a conversation is searched like a new request. When it belongs to another agent, that agent runs next, with the conversation’s state in place. When nothing new matches, the agent that answered last answers again.

What an interface does with the matches is its own [search behavior](docs/search/search-settings.html): the bundled UI runs the best match at once; your own interface can offer the two best as a choice.

Which agent runs next is always the client’s decision. An agent cannot run another agent. A request with several parts is driven from outside: an agent harness with the Search2o skill splits it, sends each part through search and `execAgent` on the same conversation, and composes one answer. [How agents build on each other](docs/agent-execution/building-on-each-other.html).

Kicker: Live demo

## Ask for something, then follow up

The [search and conversation demo](demo-search.html) runs in a live Search2o account with 200 agents, from human resources and finance to engineering and sales. Ask for something, then ask a follow-up and watch the conversation move to another agent that knows what the first one found.

## Kept safe, kept yours

State is [encrypted](docs/security/encryption.html) before it leaves the agent server, and the cloud never decrypts it. An account can [keep the state in its own organization](docs/hooks/conversation-state.html) instead of the cloud. On the free service, a conversation unused for 7 days is deleted unless the user [pins](docs/rest-api/conversations.html) it, and a user can delete a conversation at any time.

## Where to read more

[Conversation state](docs/agent-execution/conversation-state.html) covers what is saved and when. [Agents building on each other](docs/agent-execution/building-on-each-other.html) covers who decides what runs next, and [Prompts](docs/agent-definition/prompts.html) covers scope and the prompt name. In the REST API, [running agents](docs/rest-api/running-agents.html) covers the call above and [conversations](docs/rest-api/conversations.html) covers listing, renaming, pinning and deleting.
