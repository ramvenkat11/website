# Prompts and const

An agent talks to an LLM through **prompts**, and it can carry fixed settings in an encrypted **const**. Both live alongside the agent's definition: you edit them in the same draft, validate them with the same run, and publish them together.

This page explains how each one works, what values they accept, and what happens when something is wrong.

---

## Prompts

### What a prompt is

A prompt is a named entry in the agent's `agentPrompts`. Each `llm` command names the prompt it uses:

```json
{
  "functions": {
    "main": {
      "commands": {
        "llm": { "profile": "claude_haiku", "prompt": "chat" },
        "output": "{ result }"
      }
    }
  }
}
```

```json
{
  "agentPrompts": {
    "chat": {
      "system": "You are a concise travel assistant. Answer in at most three sentences.",
      "user": "{ sys.query }",
      "scope": "conversation",
      "doc": "The main conversation with the traveller."
    }
  }
}
```

A prompt has four fields:

| Field | Required | What it is |
|---|---|---|
| `system` | One of `system` or `user` | The system prompt. |
| `user` | One of `system` or `user` | What is added as the user's turn each time an `llm` command uses this prompt. |
| `scope` | No (default `conversation`) | How long the prompt's history is kept: `local`, `agent` or `conversation`. |
| `doc` | No | A short description of what the prompt is for. AI assistance in the editor reads this instead of the prompt's text. |

Prompt names follow the same rules as other names in an agent: a letter first, then letters, digits and underscores.

### Prompts are expressions

`system` and `user` are text, and any part written as `{ ... }` is a Python expression, evaluated when the `llm` command runs. An expression can read:

- local variables set earlier in the same function (`{ city }`),
- function arguments (`{ topic }` inside a function called with `topic`),
- agent and conversation variables (`{ agent.mood }`, `{ conv.lang }`),
- the `sys` namespace (`{ sys.query }`, `{ sys.userEmail }`),
- the agent's const (`{ const.city }`, see below).

```json
"chat": {
  "system": "{ 'You answer questions about ' + const.product + '. Reply in ' + const.language + '.' }",
  "user": "{ f'{sys.query} (customer tier: {tier})' }"
}
```

The same rules as every other expression apply: only allowlisted functions, no dunder or private names, printable ASCII inside the braces. Non-ASCII text is fine inside values, including const values, just not written directly inside `{ ... }`. Use an escape such as `é`, or keep the text in const.

**When each part is evaluated:**

- `system` is evaluated on every `llm` call that uses the prompt, and replaces the previous system prompt. A prompt whose system text depends on a variable follows that variable.
- `user` is evaluated once per `llm` command and added as one user turn. Tool round trips inside that command do not add it again.
- After an agent pauses with `ask` and resumes, the prompt is **not** re-evaluated: the `llm` command continues from where it stopped.

### What `system` and `user` may evaluate to

**`system` must be text.**

**`user` may be:**

- text: `"{ sys.query }"`
- a content part:
  - text: `{"contentType": "text", "text": "..."}`
  - image: `{"contentType": "image", "data": "<base64>", "mimeType": "image/png"}`
- a list of those, which becomes one user turn with several parts.

Content parts have exactly the same shape as the parts an agent sends to the user with the `output` command. An image the agent received or produced can be passed straight into a prompt.

Sending an image with a question:

```json
"vision": {
  "system": "Describe images in one sentence.",
  "user": "{ ['What is in this picture?', {'contentType': 'image', 'data': photo, 'mimeType': 'image/jpeg'}] }"
}
```

Anything else is refused **before the LLM is called**, with an error that names the prompt and field. That includes numbers, true/false, a dict that is not a content part, an unknown `contentType`, an image without `mimeType`, and a list inside a list. For example:

- `prompts.chat.user must be text, a content part or a list of them, not int.`
- `prompts.chat.user item 2 must be text, a content part or a list of them, not int.`
- `prompts.chat.user is an image part without a mimeType.`
- `The expression at prompts.chat.system is expected to evaluate to str but it evaluated to int.`

To put a number or a structure into a prompt, convert it yourself, for example `{ str(count) }` or `{ json.dumps(order) }`. You then decide how it reads.

### Scope: how long a prompt remembers

Each prompt keeps a history: the user turns and the LLM's answers. The scope decides how long that history lives.

| Scope | History lasts | Shared with |
|---|---|---|
| `local` | One run of the agent. It starts empty on every run, survives an `ask` and resume within that run, and is gone on the next run. | Every function in the same run that uses the prompt. |
| `agent` | The whole conversation. | Only this agent. Another agent in the same conversation has its own, separate history for its prompts. |
| `conversation` (default) | The whole conversation. | Every agent in the conversation that uses a prompt of that name and scope. A second agent can see what was said to the first. |

Some guidance:

- Use `local` for one-off tasks inside a run, such as classifying, extracting or summarising, where earlier runs should not influence the answer.
- Use `agent` when the agent should remember its own exchanges with the user but not mix them with other agents'.
- Use `conversation` when several agents take turns in one conversation and should share context.

Several prompts can be used in one run, each with its own history. Using the same prompt twice in a run continues its history.

### What stays in a prompt's history

When an `llm` command finishes with an answer, its history keeps **the user turn and the answer**. The tool calls the LLM made along the way, and their results, are removed. A later call, or the next agent in the conversation, sees what was asked and what was answered, not the intermediate steps. If an agent needs to keep something a tool returned, store it in a variable (`agent.` or `conv.`).

If an `llm` command fails, its user turn is removed again, so a retry does not leave a duplicate question in the history.

An `llm` command may run with an empty `user` only when the prompt already has history and the command offers tools. That lets the LLM continue working with tools without a new question. Otherwise an empty `user` is an error.

### Prompts in functions, loops, tools and parallel branches

Prompts work anywhere an `llm` command can run:

- **Functions:** the expression sees the function's own local variables and arguments.
- **Loops:** each iteration evaluates `user` again, so `{ item }` follows the loop variable.
- **Tool functions:** a function the LLM calls as a tool can run its own `llm` command, and its prompt sees the tool function's locals.
- **Parallel branches:** each branch can run its own `llm` command.

One rule applies to all of these: **two `llm` commands that are running at the same time must use different prompts.** A tool function cannot use the prompt of the `llm` command that called it, and two parallel branches cannot use the same prompt. Doing so fails with:

`The prompt 'chat' is already in use by another llm command that has not finished: one in another parallel branch, or the llm command that called this tool. llm commands running at the same time must use different prompts.`

Give each one its own prompt, for example `summarise_left` and `summarise_right`.

### Limits

| Limit | Current value |
|---|---|
| Prompts per agent | 10 |
| Length of `system`, `user` and `doc` | 20,000 characters each |

### Errors you will see, and when

**When you validate a draft** (before anything runs):

- a syntax error in a prompt expression, reported at the field, for example `prompts.chat.user`;
- a variable that may not be set when the `llm` command runs: `'city' may not be set at the llm call at main.commands.if.then.llm`;
- an agent or conversation variable that nothing sets: `'agent.mood' is not set anywhere in the agent`;
- a function that is not in the allowlist, or a secret that does not exist;
- an `llm` command that names a prompt the agent does not have;
- a `const` key the agent's const does not have (see below);
- more prompts than the limit, or text longer than the limit.

**When the agent runs:**

- an expression that fails, such as a missing dict key or an index out of range: `Could not evaluate the Python expression at prompts.chat.user: list index out of range`;
- a `system` or `user` value of the wrong type (above);
- a prompt already in use (above).

### Changing prompts on a published agent

Prompts are part of the draft. To change a published agent's prompts, make a draft from the agent, edit the prompts, validate and publish. A change to prompts alone keeps the agent's version and takes effect on the agent's next run.

If someone else changed the published agent's title, run limits or prompts after your draft was made, publishing is refused and lists the fields that differ. You can then merge their changes into your draft, or publish again with `overwrite` to replace theirs with yours. Every publish is recorded in the audit log, including the fields it changed.

---

## Const

### What const is

The const is a JSON object of fixed values for one agent, such as product names, tone of voice, thresholds, lists of categories or example texts. The agent reads it as the read-only `const` namespace:

```json
{
  "product": "Acme Router X2",
  "language": "français",
  "maxItems": 5,
  "categories": ["billing", "outage", "setup"],
  "support": { "email": "help@example.com", "hours": "9-17 CET" }
}
```

```json
"output": "{ f'Contact {const.support[\"email\"]} between {const.support[\"hours\"]}.' }"
```

Keep values that differ between agents, or that you want to change without touching the agent's logic, in const rather than written into the definition.

### Where you can use it

Anywhere an expression is allowed: in `var`, `if`, `for` (for example `"iter": "{ const.categories }"`), `api` bodies, `output`, function arguments, and prompts:

```json
"chat": {
  "system": "{ 'You are the support assistant for ' + const.product + '. Answer in ' + const.language + '.' }",
  "user": "{ sys.query }"
}
```

`sys.exists('const', 'maxItems')` tells you whether a key is present.

### Read-only, and fresh for every run

You cannot set `const` from an agent: `var` cannot target it. Each run gets its own copy, so even if an agent changes a list or dict it read from const, for example by adding a key to a local variable that holds `const.support`, that change stays within that run. The next run, for any user, sees the const exactly as it was published.

### Encrypted

The const is encrypted by the agent server before it leaves for Search2o Cloud, the same way an agent's description is. The cloud stores and returns only the encrypted value. The editor shows it decrypted, so you edit plain JSON.

With end-to-end encryption (the `encryptionKey` hook), the key never leaves your environment and the const cannot be read outside your agent servers.

### Validation

When a draft is validated:

- every `const.NAME` the agent reads, in commands or in prompts, is checked against the const's top-level keys. A missing key is reported where it is used: `'nokey' is not in the agent's const.` Keys are case-sensitive.
- if the agent reads `const.anything` and has no const, or an empty one, those reads are reported the same way.
- a const that is not a JSON object (for example a list), or that is not valid JSON, is reported at `const`.

Only top-level keys are checked before the run. A missing nested key, such as `const.support['phone']`, fails when that expression runs: `Could not evaluate the Python expression at ...: 'phone'`. Use `.get()` if a nested value is optional.

Use top-level keys that are valid names (letters, digits, underscores), so they can be read as `const.name`.

### Size

The encrypted const can be up to 50,000 characters. Encryption makes text about a third longer, and characters outside ASCII take more room, so a const of plain ASCII text fits up to roughly 37,000 characters, and less if it holds accented or other non-ASCII characters. A const that is too long is refused when you save it:

`The const is too long. Encrypted, it is 53,541 characters, over the 50,000 that can be stored. Encryption adds about a third, more for characters outside ASCII.`

### Changing const on a published agent

Like prompts, the const belongs to the draft: make a draft from the agent, change the const, validate and publish. A change to const alone keeps the agent's version and is used from the agent's next run.

---

## Putting it together

A support agent that answers in the customer's language, about the right product, with images allowed:

```json
{
  "agentDefinition": {
    "functions": {
      "main": {
        "commands": {
          "if": {
            "condition": "{ 'photo' in sys.inputs }",
            "then": { "llm": { "profile": "claude_haiku", "prompt": "with_photo" } },
            "else": { "llm": { "profile": "claude_haiku", "prompt": "chat" } }
          },
          "output": "{ result }"
        }
      }
    }
  },
  "agentPrompts": {
    "chat": {
      "system": "{ 'You support ' + const.product + '. Reply in ' + const.language + ', in at most ' + str(const.maxItems) + ' sentences.' }",
      "user": "{ sys.query }",
      "scope": "agent",
      "doc": "Text questions from the customer."
    },
    "with_photo": {
      "system": "{ 'You support ' + const.product + '. Describe what you see, then answer. Reply in ' + const.language + '.' }",
      "user": "{ [sys.query, {'contentType': 'image', 'data': sys.inputs['photo'], 'mimeType': 'image/jpeg'}] }",
      "scope": "agent",
      "doc": "Questions that come with a photo of the device."
    }
  },
  "const": {
    "product": "Acme Router X2",
    "language": "français",
    "maxItems": 5
  }
}
```

- The photo, when there is one, arrives as a base64 input named `photo` alongside the query.
- Validation checks that `const.product`, `const.language` and `const.maxItems` exist.
- Both prompts use `agent` scope, so this agent remembers its own conversation with the customer, and other agents in the conversation keep theirs.
- Changing the product or language later is a const-only publish: no change to the agent's logic, and the next run picks it up.
