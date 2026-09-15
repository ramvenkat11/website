# Why not Python?

Because an agent is not a program. It is data: the steps an agent takes, written in a language made only for agents.

Search2o uses a domain-specific language, and only the commands are new: the syntax is JSON, the expressions are Python, and there are 23 commands, each with a schema. Everything in it means something the platform understands.

That one fact does all the work.

Because the language is fixed, the editor understands it and an AI can write it. Draft with AI produces an agent from a description, and validation confirms it before it is published.

The platform can check what a program cannot know about itself. An `ask` command, a question to a person, is allowed in a `while` loop and not in a `for` loop, because a suspended `while` loop resumes exactly where it stopped and a `for` loop over a generator cannot. The agent is rejected at publishing, not at 3 a.m.

Every profile, whether LLM, MCP, prompt, API or database, knows which agents use it, and cannot be deleted while one does.

Administrators set limits once. Every agent obeys them. Developers write only the agent logic.

Python is still inside every command, doing what it is good at: computing. The structure around it does everything else.