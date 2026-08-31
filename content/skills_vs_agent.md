## SKILL.md vs. an Agent

A `SKILL.md` and an agent solve a similar problem: they package knowledge about how to handle a class of requests so that it can be selected at runtime.

A `SKILL.md` does this primarily through natural-language instructions. The runtime makes a set of skills available to the LLM. The LLM selects a relevant skill, loads its instructions, decides how to carry out the task, and uses whatever tools, scripts, references, or other capabilities the host runtime provides.

An agent defines the task as an executable workflow. Search first selects the agent that matches the user's request, then the agent runtime executes its predefined workflow, calling an LLM only at the points where one is needed.

Conceptually:

**Skill:** LLM selects a skill, builds a dynamic workflow, and orchestrates execution.
**Agent:** Search selects a predefined executable workflow, which uses an LLM where needed.

### How they work differently

With a skill:

1. The runtime makes a set of skills available to the LLM.
2. The LLM decides which skill or skills are relevant.
3. The corresponding `SKILL.md` instructions and any required resources are loaded.
4. The LLM determines the execution plan.
5. The LLM invokes tools, scripts, or other capabilities as needed and continues orchestrating the task.

With an agent:

1. Search matches the user's request against the available agents.
2. The best match can run automatically, or the user can choose from the ranked matches.
3. The agent runtime executes the agent's predefined workflow.
4. Control flow, state, external calls, LLM calls, user interaction, and output are explicit operations in that workflow.
5. The LLM is called only where the workflow requires model reasoning or generation.

                                 |
