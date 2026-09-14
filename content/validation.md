# Validating a draft

Before a draft can be published, it has to **validate**: the agent server checks it and then runs it
against a sample question. Validation proves the agent compiles, passes the security checks, finds
everything it needs in your account, and runs to the end. Publish stays unavailable until it does.

Validation happens in the draft editor, on the **Validate** tab below the agent definition.

## What validation checks

Validation runs in three stages. Problems from the first two are reported together, and the agent
runs only if neither finds any.

1. **Compile and security checks.** The definition is compiled fresh, with this account's current
   settings. Every command and field must be one the agent schema allows. Every Python expression
   must pass the security checks, such as no dunders and no operator your compile rules disallow.
   The agent may read only the `sys` variables your account makes available, and every profile it
   names must exist.
2. **What the agent server can find.** Any name an expression calls must be on this account's
   expression allowlist, and any secret the agent reads must exist.
3. **A real run.** The agent runs against the draft's **validation query**, exactly as it would for a
   user, with tracing turned on so you can see every step.

The draft validates only if the run finishes successfully. Both results are stored with the draft:
that it compiled and passed the checks, and that it ran. **Saving any change to the draft clears
both**, so the draft has to validate again before it can be published.

## Run a validation

1. Open the draft and select the **Validate** tab.
2. Enter a **validation query**: a typical question a user would ask this agent. It is saved with
   the draft.
3. Select **Validate/Trace**, or press Ctrl+Enter (⌘⏎ on a Mac). Unsaved changes are saved first.

While it runs, the Validate tab reads **Validating**, and **Stop** appears beside it in the output
panel. Stopping ends the run, and nothing from it is saved. The Draft with AI tab is locked until the
run finishes, so its result cannot land out of sight.

### Run follow-up questions

A real user rarely asks just one question. They ask something, read the answer, and continue in the
same conversation. Validation lets you test that too, by asking follow-up questions of the
conversation your validation run started.

Every draft has its own validation conversation, separate from anyone's searches. It holds what the
agent carried over between turns, such as its `agent.` and `conv.` variables, just as a user's
conversation would.

1. **Start the conversation.** Validate with the saved validation query. Once the agent has run, the
   conversation exists, whether the run finished or paused on an `ask`.
2. **Ask a follow-up.** The box's label changes from **Validation query** to **Follow-up question**.
   Type the next question a user might ask, and select **Validate/Trace** or press Ctrl+Enter.
3. **Keep going.** Each follow-up continues the same conversation, and the box empties after each
   run, ready for the next question. The output console shows the latest run.

Things worth knowing:

- **Follow-up questions are not saved with the draft.** The saved validation query stays exactly as
  it was, however many follow-ups you ask.
- **You can change the agent in the middle of a conversation.** Every run compiles the draft as it is
  now, so you can fix something the second turn exposed and ask the same follow-up again, without
  starting over.
- **A follow-up is a full validation.** It goes through the same checks, and a follow-up that runs
  successfully marks the draft as validated.
- **A failed run ends the conversation in the editor.** After compile errors or a runtime error, the
  box goes back to the validation query, and the next run starts the conversation again from the
  first question.
- **Start over whenever you like.** Select **Start over with the validation query** to leave the
  conversation. The next run asks the saved query in a fresh conversation. Reloading the page does
  the same.
- **Publishing or deleting the draft deletes its validation conversation.**

Two messages you may see:

- *"Type a follow-up question, or start a new conversation."* The follow-up box is empty. Type a
  question, or start over with the validation query.
- *"Validation cannot be run on the follow-up query as the stored state could not be found."* The
  conversation the follow-up was meant to continue is no longer stored. Start over with the
  validation query.

### When the agent asks for input

If the agent reaches an `ask` command, the run pauses and the form the user would see appears in the
panel. This is not a failure. Fill in the form and submit it to continue the run.

## Read the result

The **Validate** tab always shows where the draft stands, even while you are on Draft with AI:

| Status | Meaning |
| --- | --- |
| **Not validated** | Never validated, or changed since it last validated. |
| **Validating** | A run is in progress. |
| **Failed** | The last run in this session found problems. |
| **Validated** | The draft compiled and ran. It can be published. |

"Failed" is not stored. After you reload the page, a draft that failed reads "Not validated".

### Validation errors

When the compile, security or configuration checks find problems, they are listed under
**Validation errors**, compile errors first. Each one says what is wrong, and where:

- **at `main.commands.llm`** — select the location to jump to that command in the editor, with the
  whole command selected. A location that no longer exists, because you have edited the definition
  since, says so.
- **Allowlist item** — the agent calls something that is not on this account's expression allowlist.
  Select **Open Allowlist** to add it, or change the expression.
- **Secret** — the agent reads a secret this account does not have. Set it up where your secrets are
  kept.

### Runtime errors

If the definition passes the checks but the run fails, the error that ended it is shown as a
**Runtime error**, for example an expression that could not be evaluated or an API call that failed.
The output console shows everything that happened up to that point.

## The validation output

Below the errors, the **Validation output** console lists the run step by step. Each line shows how
long after the start it happened, what happened, and, when the line belongs to a command, where in
the agent it was. Select that location to jump to the command in the editor.

A traced run mixes very different things, and the payloads are usually the largest part. The
**filters** above the console let you put a kind of line away and bring it back:

| Filter | What it shows |
| --- | --- |
| **Agent output** | What the agent produced: the output a user would see. |
| **Progress** | Progress notes sent while the run is under way. |
| **Agent trace** | The agent author's own notes, written with the `trace` command. |
| **Flow** | Command and function boundaries, `if` and loop conditions, `break` and `continue` when they fire, `end`, and the compile checks. |
| **Input** | What each command was called with: the LLM request, API URL and headers, SQL, a search's query and tag, prompt text, a function's arguments, and the fields an `ask` presented. |
| **Output** | What each command produced: LLM content and token counts, API bodies, database row counts, search results, a function's return value, what a `var` assigned, and the answers to an `ask`. |
| **Tool** | Tool calls the LLM makes, with their arguments and results, and MCP discovery. |
| **Invoke** | Nested agents: the inputs another agent was invoked with, and what it returned or whether it paused. |
| **Error** | Every failure, whatever raised it. Showing only this filter gives the complete list of errors. |

- Each filter shows how many lines of its kind the run produced. Hover over it to see what it covers.
- **Every filter is on at the start**, so a run is never shown partially without you choosing it.
- A kind the run did not produce is shown greyed out, rather than hidden.
- **Show all** and **Hide all** turn every filter on or off at once. Each appears only when it would
  change something.
- The header counts the lines shown, and how many are hidden by the filters.
- Filters only change what you see. They never re-run anything, so you can read the flow, put the
  payloads away and bring them back without paying for another run.

**Clear** empties the console and removes the errors shown for the last run. It does not change
whether the draft is validated: if the last run failed, the Validate tab goes back to showing the
stored status.

Validation runs are your own testing, so they are not counted in the agent's execution, cost or
performance reports.

## Why validation errors are not fixed automatically by AI

The draft editor has **Draft with AI**, which can write and edit the agent. It would be easy to add a
"fix with AI" button that sends a failed validation to the AI. We deliberately don't.

A validation run is a **real run against your own systems**. Its output, trace and runtime errors
carry whatever those systems returned:

- rows from your databases and bodies from your APIs;
- what your LLMs said, and the prompts that were sent to them;
- the validation query, and values such as the user's email address or cookies when the agent reads
  them;
- error messages, which often quote the value that caused them.

Search2o does not send your agent's output to an LLM. Draft with AI gets the draft's definition, your
request, the profiles the draft uses with their notes, and this account's allowlist, disallowed
operators and available `sys` variables. Nothing produced by running the agent is included: no
output, no trace, no runtime error, and no validation query. An automatic fix would have to break
that, so it is not offered.

What you can do instead:

- **Fix it in the editor.** Validation errors point at the command they are about.
- **Describe the problem to Draft with AI yourself.** For example, "the `for` loop contains an `ask`,
  which is not allowed". Compile errors describe the definition, not your data, so repeating one in
  your request is safe. Anything you type into the request is sent, so do not paste output or trace
  lines into it.
- **Keep credentials out of the definition.** The definition itself is sent to Draft with AI. Put
  connection strings, API keys and URLs that carry credentials in profiles and secrets, not inline in
  the agent.
