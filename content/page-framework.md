<!-- Source: html/framework.html -->

<!-- Key: "Kicker:" is the small label above a heading. "> **Figure.**" gives the figure's description, then its visible labels, top to bottom; edit the wording, not the drawing. "> **Annotated code.**" is a code sample; its numbered notes are the callouts. -->

Title: Agent framework — Search2o

Meta description: An agent is a JSON file with 20 commands and Python expressions in braces. Write what the agent does; the agent server handles credentials, connections, streaming, memory, and limits.

---

Kicker: Agent framework

# An agent is JSON with Python expressions.

Below is a complete agent. It sends the user’s question to a language model and streams the answer back.

> **Annotated code.** The first agent, annotated

File: answer.json

```jsonc
{
  "functions": {
    "main": {
      "commands": {
        "llm": {
          "profile": "gpt5_mini",
          "prompt": "answer",
          "streamOutput": true
        }
      }
    }
  }
}
```

Notes:

1. Every agent starts in the function named `main`. An agent can have other functions as well, and the next example adds one.
2. The `llm` command sends a prompt to a model and streams the answer back to the user as it is generated.
3. The named profile holds the model name, API key, and host, so none of them appear in the agent file.
4. The named prompt is set in the UI, not in this file. Its user text is `{ sys.query }`. The braces mark a Python expression, and `sys.query` contains the user’s question.

Every agent has the same shape.

> **Figure.** The structure of an agent: functions, each holding commands
>
> - Agent · one JSON document
> - "functions"
> - "main" · runs first
> - "commands"
> - "api": { "profile": "orders", … }
> - "llm": { "profile": "gpt5_mini", "prompt": "orders", … }
> - "getOrder" · called by name, or by the model as a tool
> - "commands"
> - "api": { … }
> - "return": "{ result }"
> - Python expression · profile

An agent is a set of named functions. Each function is a list of commands that run in the order they are written. A command is a key, and its value contains the command’s fields. A string enclosed in braces is a Python expression; any other string is plain text. When a command connects to a model, API, or database, it names a profile that holds the connection details. An `llm` command also names a prompt, which is set in the UI and contains the text sent to the model.

## Giving the agent an API to call

This agent answers questions about orders. It has a function that looks up an order through an API, and the model decides when to call it. Agent files use JSONC, a form of JSON that allows comments, so this file includes a few.

> **Annotated code.** An agent with a tool, annotated

File: orders.jsonc

```jsonc
{
  // Answers questions about orders.
  // The model calls getOrder when it needs one.
  "functions": {
    "getOrder": {
      "description": "Looks up one order by its number.",
      "args": { "orderId": { "type": "str" } },
      "commands": {
        "progress": "Looking up the order",
        "log": "{ f'Order {orderId} requested by {sys.userEmail}' }",
        "api": {
          "profile": "orders",
          "path": "{ f'/orders/{orderId}' }"
        },
        "trace": "{ f'Status: {result['status']}' }",
        "progress.done": "Found the order",
        "return": "{ result }"   // the order goes back to the model
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

1. A function that declares arguments becomes a tool the model can call. The model reads the description, decides when it needs the function, and supplies the arguments.
2. Each of these two commands is a single line. The `progress` command shows the user a short message while the agent works. The `log` command writes a line to the agent server’s log, which stays in your environment.
3. The `api` command calls the API named by the profile. The host, credentials, and headers come from the profile; only the path comes from the agent. The parsed response is placed in `result`.
4. The `trace` command writes to the execution trace that you read while validating a draft. In production it does nothing.
5. To use a command a second time in the same function, add a dot and a suffix to its name. The suffix can be any word or number; it only keeps the two keys distinct.
6. Listing `getOrder` here gives the model that function as a tool. The model calls it whenever a question needs an order looked up.

## Twenty commands cover every agent

Every agent uses only these commands. The developer focuses on what the agent should do, and the framework handles everything else.

> **Figure.** The 20 commands, by group
>
> - Variables · [`var`](docs/commands/var.html)
> - Flow control · [`if`](docs/commands/if.html) · [`while`](docs/commands/while.html) · [`for`](docs/commands/for.html) · [`break`](docs/commands/break.html) · [`continue`](docs/commands/continue.html) · [`func`](docs/commands/func.html) · [`return`](docs/commands/return.html) · [`parallel`](docs/commands/parallel.html)
> - LLM interaction · [`llm`](docs/commands/llm.html) · [`memory`](docs/commands/memory.html)
> - External systems · [`api`](docs/commands/api.html) · [`db`](docs/commands/db.html)
> - Human-in-the-loop · [`ask`](docs/commands/ask.html)
> - Agent output · [`output`](docs/commands/output.html)
> - Agent termination · [`end`](docs/commands/end.html) · [`fail`](docs/commands/fail.html)
> - Observability · [`progress`](docs/commands/progress.html) · [`trace`](docs/commands/trace.html) · [`log`](docs/commands/log.html)

A command is written on one line when it needs only a string, and as an object when it needs more than one field. The [syntax page](docs/agent-definition/syntax.html) explains all the rules.

Kicker: Live demo

## Describe an agent and read the definition it produces

Draft with AI creates the first draft of an agent from a sentence describing what the agent should do. The same assistant is available in the draft editor, where it can also change an existing agent. Try the [Draft with AI demo](demo-draft.html) with your own description or one of the examples.

Kicker: Development process

## Draft, validate, publish

An agent goes through three stages before users can run it.

## Draft

A draft is private to the developer who created it. You can write it in the [editor](docs/development/code-editor.html), which understands the agent language and points out mistakes as you type. You can also let [Draft with AI](docs/development/draft-with-ai.html) create the first version from a sentence, then refine it by hand.

## Validate

Validation checks the definition against the schema and security rules. It also confirms that everything the agent refers to exists in the account. The agent server then runs the draft with a sample question and shows the [trace](docs/development/trace-and-validation.html): every command that ran, the values it received, and what it returned. An agent cannot be published until it passes validation.

## Publish

When an agent is [published](docs/development/publishing.html), it receives a version number and a description written in plain English. [Search](docs/search/index.html) indexes that description, and users find the agent by asking for what it does in their own words.

The [agent runtime](docs/runtime/controlled-execution.html) handles everything the agent does not specify: credentials, connections to outside systems, streaming, conversation memory, pauses for a person’s answer, and the time and cost [limits](docs/runtime/runtime-limits.html) for every run.

## Where to read more

The [agent definition](docs/agent-definition/index.html) section explains the structure of an agent, its variables, and its Python expressions in detail. The [command reference](docs/commands/index.html) describes every command. The [getting started guide](docs/getting-started/your-first-agent.html) explains how to write and run your first agent.
