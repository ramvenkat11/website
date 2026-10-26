# What's new: October 2026

This page covers the changes to Search2o Cloud and the agent server from 12 to 26 October 2026.
The agent server changes ship in agent server 0.12.0.

Some of these changes are not backward compatible. Agents that use any of the following need to
be changed before they run on the new release:

- the `search` or `invoke` command;
- the `prompt` command or prompt profiles;
- output parts with `contentType` `html`;
- image parts that carry their data in `text`.

See [Breaking changes](#breaking-changes) at the end.

---

## Prompts now live in the agent

Prompts used to be account-wide prompt profiles, set up with a `prompt` command. Each agent now
carries its own prompts in `agentPrompts`, and every `llm` command names the prompt it uses.

- **Fields:** a prompt has a `system` text, a `user` text, a `scope` and a `doc`. `system` and
  `user` are expressions, evaluated each time an `llm` command uses the prompt, in the scope of
  the function that calls it.
- **Scope** says how long the prompt's history lasts:
  - `local`: one run. It survives an `ask`, and the next run starts fresh.
  - `agent`: one agent, across the turns of a conversation.
  - `conversation`: shared by every agent in the conversation.
- **What `system` and `user` may be:** `system` must evaluate to text. `user` may be text, a text
  or image content part, or a list of these, the same shapes an `output` command accepts. Anything
  else is refused before the LLM is called, and the error names the field, for example
  `prompts.chat.user`.
- **An empty `user` value** is allowed only when the prompt already has history and the `llm`
  command has tools. Otherwise the call is refused before anything is sent to the LLM, instead of
  failing at the vendor.
- **Limits:** up to 10 prompts per agent, and up to 20,000 characters for each `system` and
  `user` text. Both limits are account settings. The old 5,000-character cap on prompt texts no
  longer applies.
- **Changing prompts:** edit them in a draft, validate it and publish it. A publish that changes
  only prompts keeps the agent's version number, and running agent servers pick up the change.
  The separate endpoints for editing a live agent's prompts were removed.
- **Drafting help:** the AI that writes drafts sees each prompt's name and `doc`, not its text.

Details and examples are on the [Prompts and const](prompts_and_const.md) page.

## Tool calls are dropped once the LLM answers

When an `llm` command finishes, its tool calls and tool results are removed from the prompt's
history. The user turn and the final answer stay.

This keeps histories small. It also lets one prompt be used with LLMs from different vendors,
whose tool-call records are not compatible with each other. A tool loop that is paused by an `ask`
keeps its tool calls until it finishes. If an agent needs a tool result later, it should store
the result in a variable.

## `const`: fixed settings for an agent

An agent can now carry a `const`, a JSON object of fixed values that its expressions read as
`const.name`.

- **Read-only:** each run gets its own copy, so a run that changes a value it read cannot affect
  other runs.
- **Encrypted:** like the agent's description, `const` is encrypted between the agent server and
  the cloud. With an `encryptionKey` hook, the cloud never sees it in plain text.
- **Checked when a draft is validated:** if the draft reads a top-level key that `const` doesn't
  have, validation reports it at that key.
- **Size:** up to 50,000 characters once encrypted, about 37,000 characters of plain ASCII JSON.
- **Publishing:** a publish that changes only `const` keeps the agent's version, and the next run
  uses the new values.
- **Decryption errors:** if a stored `const` cannot be decrypted, getDraft and getAgent return the
  reason in a new `constError` field instead of returning an empty value without a reason.

## Validation catches more mistakes

The cloud now refuses these when a draft is validated, instead of failing at run time:

- **A variable that can never be set.** A read fails only when no path before it can set the
  variable. When it might be set on some paths, the read is allowed.
- **A prompt that reads a name the agent never sets.**
- **A function-level `onError` that reads a variable from the function body.** It can see only
  the function's arguments, its own variables, `exc` and `result`.

Error messages are clearer:

- A missing field is named by its full path, for example "commands (item 1, llm, prompt) is
  required."
- A value that fits none of a field's types gets one message ("must be text, a list or an
  object") instead of one per type.
- Non-ASCII characters inside an expression get a message that names them and shows the
  `é` escape to use instead.
- An `ask` whose input doesn't fit its schema now shows a readable message instead of a
  list.

A `for` whose `iter` is a literal list with expressions in it, such as
`["a", "{ sys.query }"]`, now works. Before, it failed with an internal error.

## Commands

- **`search` and `invoke` were removed.** An agent can no longer call another agent directly.
  The `/api/exec/search` endpoint stays.
- **`for` loops:** with no `maxIterations` set, a loop that reaches the account's limit now fails
  with a message, the same as `while` does, instead of stopping without saying so. When
  `maxIterations` is set, the loop still stops quietly at that count, and `0` now means zero
  iterations. A single `loopVar` over pairs such as `dict.items()` gets the whole pair.
- **API responses that aren't text,** or that are labelled JSON but aren't valid UTF-8, are
  returned as base64 instead of failing.
- **The `output` command no longer accepts `contentType` `html`.** Output parts are `text` or
  `image`.
- **Image parts** carry their base64 data in `data`, with `mimeType` (it was `text`). This
  matches MCP and Gemini. The same image part works as `output` and as a prompt's `user` value.

## LLM calls

- **Cost limits are a hard stop.** Reaching an agent's cost limit ends the run, even inside
  `onError`, a tool call or a `parallel` branch. Before, an `onError` could catch it.
- **Every attempt that is paid for is charged.** Retries and structured-output retries count
  toward the cost limit too.
- **Retries:** only timeouts, connection errors and HTTP 429 and 5xx responses are retried, with
  a short wait that grows on each attempt. A 400, 401 or 404 fails at once. A request that cannot
  be built is not sent, and is not reported as a connection error.
- **Anthropic extended thinking** now works with tool calls. Structured output with thinking
  turned on is refused before the call with a clear reason, because Anthropic does not allow
  forced tool calls while thinking is on.
- **Images across vendors:** an image that one vendor generated, such as Gemini, can now go to
  OpenAI in a later turn.
- **OpenAI token counts:** image tokens are no longer also counted as text tokens.
- **Error messages from Ollama, vLLM and SGLang** are now shown in full, whatever shape the server
  sends them in.

## Database profiles

- **One connection pool per profile.** If the profile's connection string changes, for example
  when a vault secret is rotated, the old pool is closed and a new one opened. Old pools no longer
  stay open until restart.
- **`poolKey`:** when the connection string differs per user, for example because each user signs
  in with their own credentials, set `poolKey` to an expression that tells them apart, such as
  `{ sys.userEmail }`, so each user gets their own pool. Leave it empty to share one pool.
- **`idleTimeout`** (in the profile's pool settings, default 300 seconds): a pool that has not
  been used for this long is closed. 0 keeps pools open.
- **Connection strings with braced values** such as `PWD={a;b;c}` are masked correctly in logs
  and messages.

## Agent servers

- **Deleted agents stop everywhere.** When an agent is deleted, every agent server in the account
  drops its cached copy at its next configuration refresh. Before, only a restart cleared it.
- **Graceful shutdown:** when an agent server stops, running agents get time to finish before
  they are stopped. Set the time with `shutdownGrace` in the agent server settings (default 10
  seconds).
- **Encryption key names** may contain only letters, numbers and `_ - . : /`, and must start and
  end with a letter or number. This covers AWS key ARNs and aliases and GCP KMS key paths.
- **Masking:** credentials after `Basic`, `Token` and `ApiKey` (not only `Bearer`), and whole
  quoted secret values, are masked in traces and logs.
- **Errors loading an agent,** such as a `const` that cannot be decrypted or missing run limits,
  are reported as a problem with the agent, not as a system issue.
- **Vault errors:** a secret that could not be fetched from the vault reports the vault's own
  error.
- **The bundled GUI** is served so that a new version shows up on the next reload.

## Cloud

- **Audit log:** every publish writes an `agentPublished` entry that lists the fields that changed.
  A republish also writes `titleUpdated` and `budgetUpdated` when those changed, and
  `promptsUpdated`, which lists the prompts added, removed and changed (names only, never text).
- **Deleting a user** also deletes that user's integration tokens.
- **Drafts:** getDraftList returns up to 1,000 drafts per call (it was 25), the same as
  getAgentList.

---

## Breaking changes

| Change | What to do |
|---|---|
| `search` and `invoke` commands removed | Remove them from agents. A published agent that still contains them fails to run. |
| `prompt` command and prompt profiles removed | Move each prompt into the agent's `agentPrompts`, and name it in each `llm` command. |
| Endpoints for editing a live agent's prompts removed | Change prompts through a draft and publish it. |
| `contentType` `html` removed from output parts | Use `text`. Saved conversations that contain html parts no longer load. |
| Image part field `text` renamed to `data` | Put base64 image data in `data`, with `mimeType`. |
| Cost limit can no longer be caught by `onError` | Don't rely on `onError` to carry on after the limit is reached. |
| `for` with no `maxIterations` fails at the account limit | Set `maxIterations` if the loop should stop quietly. |
| Encryption key names restricted | Rename any key whose name contains other characters, such as `|`. |
