<!-- Source: html/runtime.html -->

<!-- Key: "Kicker:" is the small label above a heading. "> **Figure.**" gives the figure's description, then its visible labels, top to bottom; edit the wording, not the drawing. "> **Annotated code.**" is a code sample; its numbered notes are the callouts. -->

Title: Agent runtime — Search2o

Meta description: The agent says what to do; the runtime decides what it may do. Every agent server builds the same runtime from the account configuration and bounds every agent run in time and cost.

---

Kicker: Agent runtime

# The agent says what to do. The runtime decides what it may do.

Every agent server builds a runtime from the account’s configuration and runs every agent inside it. Below is the orders agent from the framework page, with what the runtime supplies on each line.

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

1. The profile holds the host, the credentials and the headers; the agent never sees them. Profiles are shared across the account, so an agent can reach only the places the profiles name.
2. A Python expression runs with the account’s allowlist in place of Python’s builtins. A name the allowlist does not carry does not exist for the agent. `import`, underscore names and the other constructs the compile rules refuse are caught at validation.
3. The LLM profile carries the model, the key and the prices. After every call the agent server adds the cost to the agent run’s total and stops the agent run when it passes the agent’s cost bound.
4. Streaming, conversation memory, pausing for a person’s answer and the time bound on the agent run are the runtime’s work too. The agent names none of them.

An agent is a definition: written by a developer, validated by a real run before it is published, versioned, and unchanged while it runs. Credentials stay out of it. A secret is read as `sys.secret['NAME']`, and the agent server resolves the value at run time, so the definition shows which secrets an agent uses and never their values. An agent’s variables belong to that agent; the one channel between agents is the conversation, by design.

## What the runtime holds

An agent server holds no state of its own, but it holds a runtime: an in-memory copy of everything an agent needs to run, built from the account’s configuration. Every part is edited in the UI.

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

The guardrails bound what an expression may do: the allowlist names what it can reach, the compile rules say which operators and shapes of expression are accepted, and the runtime limits cap loop iterations, database rows and definition length. Profiles are the only way out to models, APIs, databases and MCP servers, and every HTTP call goes through a connection pool that administrators size. Hooks are your own code, called around runs and publishing, before LLM and API calls, and for conversation state, secrets and encryption keys. Every part carries a version, so two people cannot silently overwrite each other, and every change is recorded in the [audit log](docs/system-management/audit-log.html).

## Two bounds on every agent: time and cost

Every agent carries two bounds of its own and is published and run with both. They belong to the agent, not to the account.

The time bound is the number of seconds one agent run may take; an agent run past it ends with the result code `timedOut`. The cost bound is the LLM spend, in US dollars, one agent run may reach; the agent server prices every call from the LLM profile, stops the agent run when the total passes the bound, and informs the user of the reason. An agent that looks up one record can be held to a few seconds and a few cents; an agent that researches a question is given more of both. A draft starts with default bounds, the validation run is held to them, and publishing carries them to the agent. A developer can change them on a published agent, and the [reports](docs/reports/index.html) show what each agent’s runs take and spend.

Kicker: Every agent server

## A change is live on the next agent run, on every server

Every agent server builds its runtime from the same configuration, so an agent behaves the same wherever it runs. A change to a part or a profile reaches every server without a restart.

## A part changes

A developer or an administrator saves a part or a profile in the UI. Search2o Cloud stores it, stamped with the time.

## The next agent run asks

When an agent run starts, the agent server tells the cloud, and the reply carries the time of the latest change. If it is newer than the server’s runtime, the server asks for what changed since it last asked and receives only those parts.

## The runtime is swapped

The server builds a new runtime from the changed parts and the unchanged pieces of the old one, and the agent run starts against it. Two servers starting the same agent at the same moment run with the same runtime.

An agent keeps the runtime it started with for its whole run, and the old runtime’s connections stay open until the last agent using them finishes, so a change never breaks an agent in the middle of a call. The agent server is a stateless process: it runs inside whatever isolation your organization uses, and in a [cluster](docs/system-management/agent-servers.html).

## What leaves the agent server

Search2o Cloud receives the search request and the conversation state, [encrypted](docs/security/encryption.html) before it leaves the agent server. API, database, MCP and LLM traffic goes where the profiles point. Everything else an agent handles, API responses, database rows, credentials and variables, stays on the agent server for the life of the agent run. [Data privacy](docs/security/data-privacy.html) says where every kind of data ends up.

## Where to read more

The [controlled execution](docs/runtime/controlled-execution.html) page is the summary of every control. The [agent runtime](docs/runtime/index.html) section describes each part, and [profiles](docs/profiles/index.html), [hooks](docs/hooks/index.html) and [security and privacy](docs/security/index.html) have sections of their own.
