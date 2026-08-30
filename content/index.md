# Search2o - search that executes

Search2o is a platform for creating and running AI agents, built around a search interface.

At the core of Search2o is a JSON/Python framework that lets developers rapidly build agents. Developers also describe each agent’s function in plain English. Users simply submit requests—the platform matches each request to the agent built to handle it, runs the agent, and maintains state for follow-ups.

Search2o consists of two parts - a stateless Python 3.12+ agent server that runs in your organization and a cloud backend that manages state.

---

## How It Works

The user types a request - Search2o displays the matching agent.

When the request is submitted, the agent executes that request in a controlled runtime within the agent server.

Using the built-in framework, the agent reasons with LLMs, interacts with enterprise systems, and streams its output to the user.

After execution, the conversation context is encrypted and stored in Search2o Cloud.

The user can then submit follow-up requests. Every agent used in the conversation shares the same context, allowing agents to build on one another’s work.


---

## Example workflow




## (Each line is either a short section or a title link that opens a new page)

* System architecture
* Agent framework - Small illustration image on the left - List of features on the right. (Would link to a live demo of agents in the future)
* LLM support - model agnostic, byok, private models, support for any LLM
* Security - Controlled runtime, allowlist, Secrets, End to end encryption of conversation
* UI - End user, developer (...), admin (user, servers)
* Reporting - Agent performance reports, LLM usage reports

---

## Getting started

* Register
* pip install search2o
* Run on your local machine with the license and preferably, one LLM key
* Create your first agent
  * Trace and debug
  * Publish
* Describe your agent 
* Run a search
* Add users
* Shutdown the server. Start it in a common place.


## Agent framework

* Simple JSON structure: An agent is a list[Function] and a Function is a list[Command]
* 21 commands that cover any agentic workflow  
* 

* Connect to your APIs and databases.
* Use OpenAI, Anthropic, and Gemini - add support for other LLMs.
* Call tools, with or without MCP.
* Search and invoke other agents from within agents.
* Human-in-the-loop workflows with UI integration.
* Externalize models and prompts.
* User group based agent access control and tag based agent filtering.
* Create your own orchestrator to handle queries and execute agents.

---

