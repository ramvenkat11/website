# The allowlist

The allowlist is the complete set of names that an agent's Python expressions may use.

Expressions do not get Python's builtins. The allowlist takes their place. A name that is not
on the allowlist does not exist for an agent, so an expression that uses it is refused before
the agent ever runs.

The allowlist applies to every agent in the account. Developers edit it in the GUI under
Guardrails.

## One entry per line

Each line names one thing to allow. Blank lines are ignored.

Anything after a `#` is a comment. A line that is only a comment is ignored, so comments can
be used to group a long allowlist into sections.

```text
# Text handling
json.loads
json.dumps
re.sub              # replace matches in a string
```

## What an entry can be

There are six forms. The last column shows how an agent writes it in an expression.

| Form | Example | Used as |
|---|---|---|
| A Python builtin | `len` | `len(items)` |
| A builtin type | `str` | `str(5)` |
| One method of a builtin type | `str.join` | `str.join('-', parts)` |
| One name from a module | `math.sqrt` | `math.sqrt(16)` |
| A whole module | `math` | `math.sqrt(16)` |
| Everything public in a module | `math.*` | `sqrt(16)` |

A module inside a package is named in full. `urllib.parse` allows that module, and
`xml.etree.ElementTree` allows that one.

The same forms allow your own code. `mycompany.vault.get_secret` is resolved the same way as
`math.sqrt`, as long as the package is installed beside the agent server.

### Renaming an entry with `as`

Any entry can be given the name that expressions will use.

```text
math.sqrt as sqrt                # sqrt(16)
datetime.datetime as datetime    # datetime(2026, 1, 2)
```

Without `as`, an expression uses the entry as written. `math.sqrt` is used as `math.sqrt(16)`.

An entry that ends in `.*` cannot be renamed. There is nothing to rename, because that form
brings in many names at once. An `as` on such a line is refused when the allowlist is saved.

### Choosing between the forms

Naming one function is the narrowest choice, and it is the one we suggest. `math.sqrt` allows
that function and nothing else in the module.

Allowing a whole module is convenient when agents use many of its functions. It allows every
public function in that module, so it is worth knowing what is in the module first.

The `.*` form puts the names into the expression directly, without the module in front. It
also replaces any earlier entry of the same name. `math.*` provides a `pow`, so a `pow` entry
higher up the list is no longer Python's `pow`. Prefer one of the other forms unless short
names are what you want.

## What a name gives an agent

An entry allows the name itself and the public members of the object behind it.

A class brings its methods with it. An entry of `str` allows `str.join` and `str.split`
without an entry for either. The same is true of `dict`, `list` and the other builtin types.

An allowlisted class can be used to construct an object, and the public members of that object
can be used.

### A module does not open the modules it uses

A module entry allows what is in that module. It does not allow the modules that module
imports.

Python modules import each other freely. The `json` module imports `codecs`, and `uuid`
imports `os`. Without this rule, allowing `json` would quietly allow `codecs.open`, and
allowing `uuid` would allow the operating system.

```text
json                # json.dumps and json.loads are allowed
                    # json.codecs is refused
```

The same holds for a package. Allowing `urllib` does not allow `urllib.parse`. Name
`urllib.parse` when that is what agents need.

### What is always refused

Any name that starts with an underscore is refused. This covers private names and dunder
names. The rule holds for a variable, an attribute, a function and a keyword argument. It
holds on an allowlisted object too.

`format` and `format_map` are refused on every object. A format string is read when the
expression runs, so it can reach places that are checked nowhere else. Use an f-string
instead.

`import` is not available in an expression. Everything an agent can reach is named in the
allowlist.

## Two names that are always present

`getattr` and `setattr` are available in every expression, with no entry.

The agent server provides its own versions. They accept only a public attribute name. A name
that starts with an underscore is refused, and so are `format` and `format_map`. An attribute
reached through `getattr` therefore obeys the same rules as one reached with a dot.

These versions take precedence. An allowlist entry named `getattr` or `setattr` does not
replace them.

## Functions must not block

Expressions run on the agent server's shared event loop. A function that blocks that loop
holds up every agent on the server, so such a function does not belong on the allowlist.
`time.sleep` and synchronous network calls are examples.

Async functions are welcome. When the whole expression is a call to an async function, the
result is awaited for you. Inside a larger expression, use `await`.

## When an entry is wrong

Every entry is resolved when the allowlist is saved. If any line fails, the allowlist is not
saved, and each failing line is reported with its own message.

```text
nosuchmodule       Could not be imported.
math.nope          Could not be imported.
math.* as m        A star import cannot be renamed with 'as'.
```

The line is reported exactly as it was written, so a long allowlist shows which rows to fix.

Once the allowlist is saved, every agent server rebuilds its names before the next agent run.
No restart is needed.

Each server resolves each entry in its own Python environment. An entry that cannot be
imported on one server is skipped there, a message is written to that server's log, and the
rest of the allowlist still loads. A package installed on one server and missing on another
shows up this way, so it is worth keeping the environments of your servers the same.

## Registering your own code

The allowlist is also how your own code enters the runtime. Install the package beside the
agent server, on every agent server, and name it in the allowlist.

An LLM adapter is a class that extends `LlmAdapter`. Each such class on the allowlist is
constructed once, with no arguments, when the names are built. A class that cannot be
constructed is reported.

A function that reads your own vault can be called from expressions and from the dynamic
strings of a profile.

A function that a Python operator is rewritten to must be on the allowlist, and it must take
the two values that operator works on.
