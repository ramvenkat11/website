<!-- Source: html/runtime.html -->

<!-- Key: "Kicker:" is the small label above a heading. "> **Figure.**" gives the figure's description, then its visible labels, top to bottom; edit the wording, not the drawing. "> **Annotated code.**" is a code sample; its numbered notes are the callouts. -->

Title: Agent runtime — Search2o

Meta description: The agent says what to do; the runtime decides what it may do. Every agent server builds the same runtime from the account configuration and limits every agent run in time and cost.

---

Kicker: Agent runtime

# The agent says what to do. The runtime decides what it may do.

Every agent server builds a runtime from the account’s configuration and runs each agent inside it. Below is the orders agent from the framework page, annotated to show what the runtime supplies.

> **Annotated code.** The orders agent, annotated with what the runtime supplies

File: orders.jsonc

```jsonc
{
  "functions": {
    "getOrder": {
      "args": { "orderId": { "type": "str" } },
      "commands": {
        "api": {
          "profile": "orders",
          "path": "{ f'/orders/{orderId}' }"
        },
        "return": "{ result }"
      }
    },
    "main": {
      "commands": {
        "llm": {
          "profile": "gpt5_mini",
          "prompt": "orders",
          "functions": ["getOrder"],
          "streamOutput": true
        }
      }
    }
  }
}
```

Notes:

1. The profile holds the host, credentials, and headers; the agent never sees them. Profiles are shared across the account, so an agent can reach only the destinations named by those profiles.
2. A Python expression runs with the account’s allowlist instead of Python’s built-ins. Any name not on the allowlist is unavailable to the agent. Validation catches `import`, names that begin with an underscore, and other constructs rejected by the compile rules.
3. The LLM profile holds the model, key, and prices. After every call, the agent server adds the cost to the run’s total and stops the run when it exceeds the agent’s cost limit.
4. The runtime also handles streaming, conversation memory, pauses for a person’s answer, and the run’s time limit. The agent does not specify any of them.

An agent is a definition written by a developer, validated with a real run before publication, versioned, and kept unchanged while it runs. Credentials stay out of the definition. A secret is read as `sys.secret['NAME']`, and the agent server resolves its value at run time. The definition therefore shows which secrets an agent uses, but never their values. An agent’s variables belong to that agent; by design, the conversation is the only channel between agents.

## What the runtime holds

An agent server stores no state of its own, but it holds a runtime in memory. The runtime contains everything an agent needs and is built from the account’s configuration. Every part is edited in the UI.

> **Figure.** The parts of the runtime: guardrails, profiles and operations
>
> - Runtime · one per agent server, in memory
> - Guardrails · developers
> - [Allowlist](docs/runtime/allowlist.html)
> - [System variables](docs/runtime/system-variables.html)
> - [Compile rules](docs/runtime/compile-rules.html)
> - [Runtime limits](docs/runtime/runtime-limits.html)
> - Profiles · developers
> - [LLM](docs/profiles/llm-profiles.html)
> - [API](docs/profiles/api-profiles.html)
> - [Database](docs/profiles/db-profiles.html)
> - [MCP server](docs/profiles/mcp-servers.html)
> - Operations · administrators
> - [Connection pools](docs/runtime/connection-pools.html)
> - [Secrets](docs/security/secret-vault.html)
> - [Encryption](docs/security/encryption.html)
> - [Hooks](docs/hooks/index.html)

Guardrails limit what an expression can do. The allowlist defines what it can access, the compile rules define which operators and expression forms are accepted, and the runtime limits cap loop iterations, database rows, and definition length. Profiles are the only way to reach models, APIs, databases, and MCP servers. Every HTTP call goes through a connection pool sized by administrators. Hooks are your own code. They run around agent runs and publishing, before LLM and API calls, and when handling conversation state, secrets, and encryption keys. Every part has a version, so two people cannot silently overwrite each other, and every change is recorded in the [audit log](docs/system-management/audit-log.html).

## Two limits on every agent: time and cost

Every agent has two limits and is published and run with both. These limits belong to the agent, not the account.

The time limit is the number of seconds one agent run may take. A run that exceeds it ends with the result code `timedOut`. The cost limit is the amount, in US dollars, that one run may spend on LLM calls. The agent server calculates the cost of every call using the LLM profile, stops the run when the total exceeds the limit, and tells the user why. An agent that looks up one record can be limited to a few seconds and a few cents; an agent that researches a question can receive more of both. A draft starts with default limits, and its validation run must stay within them. Publishing applies the same limits to the agent. A developer can change the limits on a published agent, and the [reports](docs/reports/index.html) show how much time and money each agent’s runs use.

Kicker: Every agent server

## A change is live on the next agent run, on every server

Every agent server builds its runtime from the same configuration, so an agent behaves the same wherever it runs. Changes to a part or profile reach every server without a restart.

## A part changes

A developer or administrator saves a part or profile in the UI. Search2o Cloud stores it with a timestamp.

## The next agent run asks

When an agent run starts, the agent server contacts the cloud. The reply includes the time of the latest change. If that change is newer than the server’s runtime, the server requests everything that has changed since its last check and receives only those parts.

## The runtime is swapped

The server builds a new runtime from the changed parts and the unchanged parts of the old runtime. The agent run then starts with the new runtime. Two servers that start the same agent at the same time use the same runtime.

An agent keeps the runtime it started with for the entire run. The old runtime’s connections stay open until the last agent using them finishes, so a change never interrupts an agent in the middle of a call. The agent server is a stateless process. It runs within your enterprise’s chosen isolation and in a [cluster](docs/system-management/agent-servers.html).

## What leaves the agent server

Search2o Cloud receives the search request and conversation state, which are [encrypted](docs/security/encryption.html) before they leave the agent server. API, database, MCP, and LLM traffic goes to the destinations specified by the profiles. Everything else the agent handles—including API responses, database rows, credentials, and variables—stays on the agent server for the duration of the run. [Data privacy](docs/security/data-privacy.html) explains where each kind of data goes.

## Where to read more

The [controlled execution](docs/runtime/controlled-execution.html) page is the summary of every control. The [agent runtime](docs/runtime/index.html) section describes each part, and [profiles](docs/profiles/index.html), [hooks](docs/hooks/index.html) and [security and privacy](docs/security/index.html) have sections of their own.
