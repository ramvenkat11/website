# Naming rules

Everything you name in Search2o follows one rule, with two exceptions.

**Underscore is the separator. Only an MCP server's name cannot contain one, and tags are additionally lowercase.**

Names are case-sensitive and are never trimmed: `Weather_Agent` and `weather_agent` are two different agents, and a trailing space is a validation error rather than something quietly removed.

## The standard name

Most things you name — agents, functions, variables, arguments, profiles, memory labels — share one shape:

- starts with a letter
- contains letters, digits and underscores
- ends with a letter or a digit
- at least two characters

`weather_agent`, `getForecast`, `user_id`, `gpt5_mini` are all valid. `2fa_check` is not, because it starts with a digit. `weather-agent` is not, because a hyphen inside an expression reads as subtraction. `check_` is not, because it ends with a separator.

| Name | Length | Where you write it |
|---|---|---|
| Agent name | 2–32 | Publishing an agent, and the name a draft is saved under |
| Function name | 2–100 | `functions` in an agent definition |
| Variable name | 2–100 | The `var` command, loop variables |
| Argument name | 2–100 | A function's `args`, and an `ask` command's inputs |
| Memory label | 2–100 | The `memory` command's `store` and `delete` |
| Profile name | 2–50 | LLM, API, database and prompt profiles |

An agent name is shorter than a function name because it is seen far more widely — in search results, reports and error messages — and a long one is unreadable in a list.

A profile name is shorter still because you choose it from a menu rather than type it.

Agent names, function names and profile names are all written **inside** agent definitions, next to Python expressions. That is why the separator is an underscore rather than a hyphen: in `{ weather-agent }` the hyphen is subtraction.

## Exception 1: MCP server names

An MCP server's name may contain **letters and digits only — no underscore** — and is at most 16 characters.

This is not a style choice. The name becomes part of the tool name the language model sees, in the form `mcp_{server}_{tool}`. If the server name could contain an underscore, `mcp_a_b_c` would be ambiguous: it could be server `a_b` offering tool `c`, or server `a` offering tool `b_c`. Forbidding the underscore in the server name alone makes the split unambiguous, and leaves tool names — which come from the MCP server and are not yours to change — free to contain underscores.

The 16-character limit comes from the other end. Model providers cap a function name at 64 characters, and `mcp_` plus your server name plus `_` plus the tool name has to fit inside that.

A server may not be named `function`, which is reserved for the agent's own functions in tool calls.

`weatherApi` and `github2` are valid. `weather_api` is not.

## Exception 2: tags

A tag may contain **lowercase letters, digits and underscores**, up to 16 characters. Unlike other names it may start with a digit and may be a single character.

| | |
|---|---|
| An agent's tag | 1–16 characters, required. Defaults to `general` |
| A tag in a search | The same shape, or **empty, which means every tag** |

`general`, `corporate`, `hr_internal`, `eu_support` and `2024` are all valid tags. `HR` is not.

Tags are lowercase for a practical reason: they are the one name typed by whoever is searching rather than written by whoever is building. If case mattered, `Corporate` and `corporate` would become two separate pools of agents that nobody could reconcile afterwards.

Tags may begin with a digit and may be one character because a tag is vocabulary rather than code. `2024` is a reasonable way to tag a set of agents; it is not a reasonable variable name.

## Generated identifiers

Search2o generates these. You never type them, and they follow their own fixed shapes.

| Identifier | Shape |
|---|---|
| Licence key | 22 letters and digits |
| Account id | 22 letters and digits |
| Conversation id | 22 letters and digits |
| Draft id, job id, token id | 22 letters and digits |
| Billing name | Twelve uppercase letters in three groups, `ABCD-EFGH-IJKL` |
| Emailed code | Six uppercase letters |

The emailed code is letters only, with no digits at all. A code is read off one screen and typed into another, and an alphabet without digits cannot confuse `0` with `O` or `1` with `I`.

## Free text

These are descriptions rather than identifiers. They are length-limited but have no shape rule, and may contain spaces and punctuation.

| Field | Length |
|---|---|
| Account name | 3–32 |
| User name | 2–100 |
| Agent title | 1–80 |
| Profile notes | up to 500 |
| Search query | 8–500 |
| Support subject | 1–80 |

An agent has both a **name** and a **title**. The name is the identifier — `weather_agent` — used when one agent invokes another and when reports group by agent. The title is what a person reads in search results — `Weather Agent`. Changing a title is immediate and affects nothing else; a name is fixed once the agent is published.

## When a name is rejected

Validation errors name the field and describe the rule in words rather than showing a pattern:

```
agentName must start with a letter, end with a letter or a number,
and contain only letters, numbers and underscores
```

A name that is too long, too short, or sent to a request that does not accept that field is reported the same way.
