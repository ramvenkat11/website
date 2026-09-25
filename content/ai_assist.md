# Draft with AI

**Draft with AI** writes and edits an agent for you, inside the draft you are working on.
Describe the agent you want, or the change you want made to this one. The AI returns the
whole draft with that change made, and the editor shows it straight away.

It is not a general chatbot, and it is not the documentation. For questions about how
Search2o works, use the **Docs** icon at the top of the page.

## What it knows

Draft with AI does not start from a blank page. Every request carries four things.

**How an agent is built.** It works from the same command schema the editor and the compiler
use. It knows every command, the fields each one takes, how blocks run in order, and how to
use a command twice (`var`, then `var.2`). It also knows the rules the compiler enforces, so
it avoids writing what would be refused. For example:

- `ask` and `invoke` cannot go inside a `for` loop or an `onError` block. When the work needs
  them, it uses a `while` loop, or has the handler set a variable and asks afterwards.
- A function used as a tool cannot `end`. It uses `fail`, or returns a value for the LLM to
  explain.
- An agent runs again on every turn. `agent.` and `conv.` variables carry over, and one that
  was never set is read safely.

**Your current draft.** Every request edits the draft you have open. The AI keeps every
function, command, name, expression and comment that your request does not touch, exactly as
you wrote them. It changes only what you asked for, and does not rewrite working parts in its
own style. On a new, empty draft, it builds the agent from scratch.

**This account's configuration.**

| | How the AI uses it |
| --- | --- |
| **Used profiles** | It names these profiles exactly, in the command of their type. It reads each profile's notes to learn what the API serves or what the database holds, and to choose between profiles. It never names a profile you have not ticked. |
| **Expression allowlist** | Expressions call only the names on the allowlist, plus the built-in types. If your request needs a function that is not there, it leaves that value empty and says the function must be added to the allowlist first. |
| **Compile rules** | It does not use an operator your account disallows. It writes the value another way, or leaves it empty with a note naming the operator. |
| **System variables** | It reads only the `sys` variables your account makes available. `sys.inputs` and `sys.query` are always there. |

You choose the used profiles in the draft. The allowlist, compile rules and system variables
come from the account's settings under **Guardrails**.

**What it does not know.** It has never seen your database, your API or your MCP tools. So it
never writes SQL, URL paths, request parameters or tool arguments. It puts the command in the
right place, leaves those fields empty, and adds a comment saying what belongs there. An
empty field with a comment takes a moment to fill in. An invented query would compile, pass
validation and publish, then fail against a table that does not exist.

## Use it

1. Open a draft from **Agents → Drafts**, or create a new one.
2. Below the agent definition, select **Draft with AI**. It is selected when the page opens.
3. Under **Used profiles**, tick the profiles the agent should use. They are part of the
   draft and are saved with it, like its title.
4. In the box, describe what you want, and select **Send** or press Ctrl+Enter (⌘⏎ on a Mac).
   Say at least a few words, up to 10,000 characters.

Before anything is sent, **the draft is saved** if it has unsaved changes: its definition,
used profiles, name, title, tag and validation query. The AI works from the saved draft, so
what you see is what it gets. If the save fails, nothing is sent.

While the AI is writing, the button reads **Writing…** and the switch to **Validate** is
locked, so the result cannot land out of sight.

## What comes back

The answer replaces the definition in the editor, and **the draft is saved** with it.

Comments mark what is left for you: a query to write, a URL to fill in, an agent to name. Each
sits above the line it is about. Fill them in, delete the comments you are done with, and
save.

If you ask for something that needs no gaps, the agent comes back finished, with no comments.
If your request is too vague to start from, nothing is changed. You are told, in a sentence or
two, what the AI would need to know.

Always **validate** what comes back before you publish, and check it does what you meant. The
AI works within the rules above, but validation is what proves an agent compiles and runs.

## Undo

Each AI edit can be undone. Select **Undo AI edit** beside the **Agent definition** heading.
The number in the button is how many edits you can step back through, up to the last ten.

- Undo puts back the definition as it was before that AI edit, and saves it.
- If you have typed changes into the definition since the AI edit and not saved them, you are
  asked first. **Keep my changes** leaves everything as it is. **Undo** discards those changes
  and goes back.
- When you edit the definition yourself and save it, the undo history is cleared. From then
  on, the editor's own undo (Ctrl+Z) is the way back.

## Tips

- **Ask for one change at a time.** "Add an ask for the order number before the lookup" is
  easier to check than a whole agent rewritten at once.
- **Tick the profiles first, and keep their notes useful.** A profile's notes are what the AI
  knows about your system. "Orders database: orders, order_lines, customers" leads to a better
  draft than an empty note.
- **Name the agents to call.** The AI does not know which agents exist in your account. To
  have the draft invoke one, say which.
- **If something is refused at validation,** say what the error was in your next request, or
  fix it in the editor. A validation error names the place in the definition it is about.

Draft with AI counts towards your account's usage. If your account has reached its limit, you
are told when you can try again.
