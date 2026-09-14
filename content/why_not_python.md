# Why not Python?

A fair question is why an agent is JSON with Python expressions rather than a Python program.

Python is a general-purpose language. Search2o is a language for one domain: AI agents.

An agent is an ordered list of commands, held as data with a fixed structure. Because the structure and commands are known in advance, the definition can be validated before it runs, generated from a description, read as steps, and bounded at runtime.

Python expressions supply the granular logic inside each command without giving up those properties.

| Aspect | A Python program | A Search2o agent |
| --- | --- | --- |
| **Writing it** | A programmer, or an AI, writes the code. Only tests tell you whether it does what was asked. | Draft with AI writes or edits the definition from a description. The schema constrains the output to a valid agent, and a validation run checks that it executes. |
| **Before it runs** | Syntax, plus whatever the author set up: type checkers, linters, tests. | Always, without setup: the schema, the syntax and names in every expression, and every reference to a function or a profile. A validation run must pass before publishing. |
| **Reading it** | You read the code. | An ordered list of named commands. The people who own the process can follow the steps. |
| **Trusting it** | The interpreter can reach the file system, the network and the process. Sandboxing has to be added around it. | Expressions run in the agent runtime: only allowlisted names are reachable, no `import`, no dunder access, no private member access. |
| **Limits** | Whatever the author or the hosting environment enforces. | Run time, loop iterations, database rows and LLM spend are capped for every agent, by administrators. |
| **Shipping a change** | Build, deploy, restart. | Publish. Every agent server in the account runs the new version on its next run. |
| **Measuring it** | Whatever was instrumented. | Every run records its duration, result and LLM cost. Reports cover every agent. |

The trade is expressiveness. An agent can only do what its commands and allowlisted functions allow. That is the point, and a task that doesn't fit the command model belongs in a Python function that an agent calls.