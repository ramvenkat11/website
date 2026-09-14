# The agent editor

An agent is written as a definition: a JSON document with a `functions` object, each function holding
the commands it runs. The **Agent definition** editor on the draft page is where you write it. It is
built on Monaco, the editor inside Visual Studio Code, and it knows the Search2o agent language, so
it can suggest what comes next and point out mistakes as you type.

## What the editor knows

The editor learns the agent language from the **agent schema** that your agent server publishes. It is
the same description the compiler checks your agent against. It covers every command, the fields each
command takes, what type each field holds, and a sentence describing each one.

Because of that:

- **New commands appear automatically.** When Search2o adds a command or a field, the editor offers it
  without a new UI release.
- **Suggestions and checks agree with validation.** What the editor suggests is what the compiler
  accepts.

The schema is loaded the first time you open the editor, and kept for the rest of the session. If it
cannot be loaded, the editor still works as a plain JSON editor, without the suggestions and schema
checks described below.

## Adding a command

Inside a function's `commands` block, start a new line and type `"`. A list of every command allowed
there opens, grouped by what it does:

| Group | Commands |
| --- | --- |
| Variables | `var` |
| Flow control | `if`, `while`, `for`, `break`, `continue`, `func`, `return`, `parallel` |
| Output progress information | `progress`, `trace`, `log` |
| Terminate agent | `end`, `fail` |
| Call external systems | `api`, `db` |
| Engage with LLM | `prompt`, `llm`, `memory` |
| Deep agents | `search`, `invoke` |
| Human in the loop | `ask` |
| Agent output | `output` |

- **Keep typing** to filter the list.
- **Up and Down** move through it. The box under the list describes the highlighted command.
- **Enter or Tab**, or a click, inserts the command. **Escape** closes the list.

The list shows only commands that are allowed where you are typing, and it opens as tall as the window
allows.

Choosing a command inserts it **ready to fill in**, not just its name:

- **Starter fields.** It comes with the fields you will almost always need. `if` arrives with
  `condition`, `then` and `else`; `for` with `iter`, `loopVar` and `do`; `api` with `url`, `params` and
  `body`; `invoke` with `agent` and `inputs`.
- **Starter values.** Each field gets a sensible value to replace:
  - a Python expression field gets `"{  }"`;
  - a block of commands gets `{}`;
  - a list of objects, such as the fields of an `ask`, arrives with one empty object;
  - a field with a fixed set of values gets its first value;
  - a field with a default gets that default.
- **Repeated commands are numbered.** A block cannot hold the same key twice, so when the block
  already has a `var`, the next one is inserted as `var.1`, then `var.2`.
- **Tidy insertion.** The command is indented to match its surroundings, a comma is added to the end
  of the previous entry if it needs one, and the cursor lands where you type next. For a list of
  objects, that is inside the first object.

## Suggestions as you type

Everywhere else a key belongs, the editor shows the next likely key as **grey text** ahead of the
cursor. Press **Tab** or **Enter** to accept it, or keep typing to ignore it.

- **Inside a function:** `description`, `args`, `commands` and `onError`.
- **Inside a function argument:** `type`, `description` and `required`.
- **Inside a command:** that command's fields. Fields the command requires come first, so if you delete
  an `if`'s `condition`, it is the first thing suggested back.
- **Inside a list of objects**, such as an `ask` command's `inputs`: the fields each entry takes.

Only keys that are not already there are suggested. The suggestion appears even on an empty line, so
an unfinished object shows you what it is still missing.

### Suggestions from your own agent

Some suggestions cannot come from the schema, because they depend on what you have written:

- **Inside `parallel`**, each key names one of your agent's own functions. The editor suggests the
  functions this definition declares, with their descriptions.
- **Inside one of those entries**, it suggests that function's declared arguments, with their types and
  descriptions.

These are read from the definition as you type, so a function you added a moment ago is suggested at
once. They are suggestions, not restrictions: a name you type yourself is left alone, and validation
decides whether it is right.

### When nothing is suggested

- **"No suggestions here."** You typed a key where the agent language does not describe one, so there
  is nothing to offer.
- **"An object goes here."** You typed a quote directly inside a list whose entries must be objects.
  Each entry starts with `{`.

## Checks as you type

The editor checks the definition continuously and underlines problems:

- **Syntax errors**, such as a missing bracket or a stray character.
- **Anything the agent language does not allow**, such as an unknown command or field, or a value of
  the wrong type.

**Hover over an underlined problem to read what is wrong.** A box opens beside the pointer with the
message, for example that a command is not allowed or that a value has the wrong type. Hovering over
anything that is not underlined shows nothing.

`//` and `/* */` comments are allowed, and are not reported as errors. Use them to leave notes in the
definition.

These checks catch most mistakes early, but they are not the final word. **Validate** compiles the
agent with your account's settings and runs it, and reports each problem with a sentence and its
location. See the **Validating a draft** page.

## Reading the definition

- **Expressions stand out.** A value written as a Python expression, like `"{ total + 1 }"`, is shown
  with bold braces and its contents in a monospace font, so expressions are easy to tell apart from
  plain text values.
- **Matching brackets share a colour**, and **indent guides** show how blocks nest.
- **Folding.** Collapse a function or command with the arrow beside its line number.
- **The editor grows with the definition** rather than scrolling inside a box. The page scrolls
  instead.
- **Light and dark.** The editor follows the app's theme.

## Formatting

- **Quotes and brackets close automatically** as you type them.
- **Pasted text and new lines are formatted** as they go in.
- **Format document** reformats the whole definition with consistent indentation of two spaces.

## The toolbar

The toolbar above the editor holds every action. Hover over a button to see its name and shortcut.

| Button | Shortcut |
| --- | --- |
| Find | ⌘F / Ctrl+F |
| Replace | ⌥⌘F / Ctrl+H |
| Find next, Find previous | |
| Toggle comment | ⌘/ / Ctrl+/ |
| Block comment | |
| Format document | ⇧⌥F / Shift+Alt+F |
| Word wrap on or off (on at the start) | |
| Line numbers on or off | |
| Indent guides on or off | |
| Go to line | ⌃G / Ctrl+G |
| Fold all, Unfold all | |
| Undo | ⌘Z / Ctrl+Z |
| Redo | ⇧⌘Z / Ctrl+Y |

## Around the editor

- **Save** with **Ctrl+S** (⌘S on a Mac) from anywhere on the page, including while typing in the
  editor. "Saved" appears briefly beside the **Agent definition** heading.
- **Validate** with **Ctrl+Enter** (⌘⏎) from anywhere on the page *except* inside the editor, where that
  key belongs to the editor. Use the **Validate/Trace** button, or click outside the editor first.
- **Jump to a problem.** Validation errors and lines in the validation output show where in the agent
  they happened, such as `main.commands.llm`. Select one to scroll to that command and select the whole
  of it. If you have since removed or renamed it, you are told so.
- **Two kinds of undo.** The editor's own **Undo** steps back through your typing. **Undo AI edit**,
  beside the heading, steps back through changes made by **Draft with AI**, up to the last
  ten.

## What the editor does not do

- **No documentation on hover.** Hovering shows a problem's message, never a description of the command
  or field under the pointer, which was distracting while reading. The box under the
  command list describes each command, and the Docs page answers questions about the language.
- **No suggestions for values from your account.** Profile names, secret names and functions on your
  expression allowlist are not suggested; you type them. Validation checks that each one exists.
- **It does not decide what is valid.** The editor is a first line of defence. The compiler on the
  agent server has the final say when you validate and publish.
