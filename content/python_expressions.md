# Python expressions

An agent is written in JSON. The string values in that JSON can be Python expressions. A key cannot be an expression. 

This page
explains what Search2o does with those expressions, from the moment a developer saves an agent
to the moment the expression runs.

## What counts as an expression

A string value is an expression when the whole string is wrapped in braces.

```jsonc
"var": {
  "total": "{ price * quantity }",
  "label": "Order total",
  "greeting": "{ f'Hello {sys.inputs[\"name\"]}' }"
}
```

`total` is an expression. `label` is plain text. `greeting` is an expression that builds a
string with an f-string.

The braces must enclose the whole value. `"Hello {name}"` is plain text, and the agent sees the
braces literally. To mix text and values, write an f-string inside the braces.

A value that starts with `{` and ends with `}` is always read as an expression. So the string
`'{"a": 1}'` is not text. That value is the Python dict `{"a": 1}`.

An expression is one Python expression. Statements are not allowed. There is no assignment, no
`import`, no `def` and no semicolons. The `var` command is how an agent sets a variable.

## Where expressions can be used

Expressions can be used in most command fields. The fields of the `var`, `if`, `output` and
`api` commands are typical examples.

Expressions can also be used in a few fields of the profiles in the configuration. Examples are
the URL and headers of an API profile, and the connection string of a database profile.
Profiles are shared by every agent in the account, so a secret usually appears there, for
example `"{ f'Bearer {sys.secret[\"OPENAI_API_KEY\"]}' }"`.

Prompt profiles are an exception. The text of a prompt profile is always literal. This has to be done so end to end encryption works for prompt profiles. 

## Two stages

An expression is checked twice and run once.

1. **When the agent is validated.** The Search2o Cloud reads each expression and refuses the
   agent if an expression breaks a rule. The agent server then checks that the names and secrets
   the expressions use exist.
2. **When the agent runs.** The agent server evaluates the expression in the controlled runtime.

The agent server runs the version of each expression that passed the first stage. The controlled
runtime adds its own protection: an expression sees only the allowlist, never Python's builtins.

## Stage one: validation

### What the cloud refuses

The cloud parses each expression with Python's own parser. An expression that is not valid
Python is refused with the line and column of the error.

The cloud then refuses these constructs:

| Construct | Example | Why |
|---|---|---|
| A name or attribute that starts with an underscore | `x.__class__`, `obj._cache` | Private and special members lead out of the agent's data. |
| `str.format` and `str.format_map` | `'{0.x}'.format(v)` | A format string reads attributes at run time. Use an f-string instead. |
| `lambda` | `lambda x: x + 1` | An expression cannot define a function. |
| The walrus operator | `(n := len(items))` | An expression cannot assign. |
| Calling the result of an expression | `handlers[0](x)`, `f()()` | Only a function called by name, or a method, can be called. |
| A keyword argument that starts with an underscore | `f(_x=1)` | Same reason as private members. |
| Characters outside printable ASCII | `'café'` | Use a Python escape. In the JSON the backslash is doubled: `"{ 'caf\\u00e9' }"`. |
| Deep comprehensions | four nested list comprehensions | The account sets the limits. The defaults are a depth of 4 and 3 `for` clauses. |
| An operator the account has turned off | `a << b` | The account decides which operators are allowed. |

### Rules for `sys`

`sys` holds what the runtime provides. `sys` can only be used as `sys.<member>`. An expression
cannot pass `sys` to a function or store `sys` in a variable.

A secret can only be read as `sys.secret['NAME']`, with the name written out. A key held in a
variable is refused. So is `sys.secret` on its own. This rule means every secret an agent uses
is visible in the agent's definition.

A member of `sys` that does not exist is refused. `sys.inputs`, `sys.query`, `sys.secret` and
`sys.exists` are always present. `sys.userEmail`, `sys.userSession`, `sys.serverIp` and
`sys.cookies` are present only when an administrator enables them.

Inside a command, `command.<field>` reads a field that the same command has already set. A field
that the command does not have is refused.

### Operator rewriting

The account can map an operator to a function. When `**` is mapped to `bounded_pow`, the
expression `a ** b` runs as `bounded_pow(a, b)`. This is how an account puts a limit on an
operation such as a very large power. The function must be in the allowlist and take two values.

### What the agent server checks

The cloud does not know which functions the agent server provides or which secrets the agent
server holds. So the cloud hands two lists to the agent server: the names the expressions use,
and the secrets the expressions read.

The agent server refuses the agent when a name is not in the allowlist or a secret cannot be
found. Each message gives the path of the first place the name or secret is used.

Secrets from environment variables and files live on one machine. The check therefore tells a
developer that the secret exists on the agent server that validated the agent. Another agent
server in the same account must have the same secrets. Hosted secrets are shared by the whole
account.

### The validation run

Validation also runs the agent once with the developer's validation query. An expression that
fails on real data fails here, before the agent can be published.

## Stage two: running

### The names an expression can see

An expression runs inside the function that contains it. The expression can read:

- The function's local variables and arguments, by name.
- Agent variables, as `agent.name`.
- Conversation variables, as `conv.name`.
- `sys` and `command`.
- `result`, which holds the result of the last command that produces one.
- `exc`, which holds the error being handled inside an `onError` block.
- The names in the allowlist.

Nothing else exists. Python's builtins are not available. The allowlist takes their place, so
`len` or `sorted` works only when the allowlist lists `len` or `sorted`.

### Checking whether a variable exists

Reading a variable that was never set is an error. `sys.exists(scope, name)` answers whether the
variable exists first. The scope is one of `local`, `agent`, `conv` or `allowlist`.

```jsonc
"var": {
  "agent.visits": "{ (agent.visits if sys.exists('agent', 'visits') else 0) + 1 }"
}
```

`sys.exists('allowlist', 'json')` answers whether the allowlist grants `json`.

### What the allowlist hands over

A function or class in the allowlist is the real Python object. A method on a value works as in
Python, so `'abc'.upper()` and `items.append(x)` work.

A module in the allowlist is not handed over as a module. The agent gets the module's functions,
classes and constants. The agent does not get the other modules that the module imports. So
granting `json` does not also grant the modules that `json` uses internally.

A name under a granted module that the allowlist does not list is refused when the line runs.

### Awaiting

An expression can `await` an async function from the allowlist. The runtime detects the `await`
and runs the expression as a coroutine. To run several calls at once, use the `parallel`
command.

### The value an expression produces

An expression produces any Python value. Each field expects a type, and a value of the wrong
type is an error that names the type the field expected. For example, the `timeout` of an `api`
command must be a whole number.

Agent variables and conversation variables are saved with the conversation. Their values must be
JSON. A JSON value is a string, a number, a boolean or `None`. A list or dict of JSON values is also JSON. A local variable can hold any value.

### Errors

An expression that raises an error stops the command. The message gives the path of the command
and the Python error. An `onError` block on the command or the function can handle the error
instead. Inside that block `exc` holds the error.

### Limits

The rules on this page decide what an expression can reach. The rules do not limit how much work
an expression does. An expression runs on the agent server alongside every other agent run, so a
very long computation delays the other runs. The limits that apply are those set in the
configuration: run time, loop iterations, database rows and the operator rewrites described
above.
