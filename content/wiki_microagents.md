# Microagents — Wikipedia article draft

Oct 14, 2026 · @Ram Venkat


https://claude.ai/chat/267638f9-3bdf-4f56-ae5e-f1a83c08f443?artifact=1124d6ca-c1aa-46d3-b129-62ac365e6b1e

## Editor's notes

This is a sourced skeleton for you to rewrite in your own words before submitting. Wikipedia's guidance discourages LLM-written article text, and English Wikipedia can speedily delete pages that are evidently unreviewed LLM output (criterion G15, adopted in August 2025; it applies to objective signs such as text addressed to the user or references that do not exist).

**Verification.** Every reference and every cited claim was checked against its source on 14 October 2026, and the corrections are applied below. Two details could not be checked because the publishers' sites were unreachable: the page numbers of reference 25 and the journal details of reference 31; both are marked.

**How to use the draft**

- Every sentence carries a numbered reference; keep the claim-to-source pairing when you rewrite.
- Text in \[square brackets\] is a note to you, not article text.
- Opinions are attributed in-line ("Davis argues…"). Keep the attribution: most sources are vendor blogs and opinion columns, which Wikipedia treats as attributed views, not facts.

**Open decisions**

1. Title and spelling. Sources use "microagents", "micro-agents", "micro agents" and "MicroAgents". Proposed: *Microagents* (plural, following the *Microservices* precedent), with redirects from *Microagent*, *Micro-agent*, *Micro-agents* and *Micro agents*. The appendix records which spelling each source uses.

Microagents

2. Scope. The microservices-analogy meaning only; every other meaning goes under "Other uses of the term".

Yes

3. Standalone article. Your call; the AfC reviewer decides on sourcing. If the draft is declined for notability, the same content fits as a section of *Multi-agent system* or *Agentic AI* without rewriting.

yes, a standalone article

**COI / AfC checklist**

- [ ] Declare the conflict on your user page with the UserboxCOI template, naming your company and its use of the term.
Already done
- [ ] Put the connected-contributor template on the draft's talk page, and note the conflict in your edit summaries.

Not sure what this means. 

- [ ] Search Wikipedia for Microagent, Microagents, Micro-agent and Micro agent first. No page under these titles was found on 14 October 2026, but Wikipedia's own search could not be reached to confirm it.
Done - Wiki does not let me create a draft if there's already one.

- [ ] Create the page as *Draft:Microagents* and submit it through Articles for Creation; do not move it to mainspace yourself.

Wiki has a way to do this. I am just following their workflow. 

- [ ] No mention of, link to, or citation of your company anywhere in the article.

ok

- [ ] Rewrite in your own words; keep each claim tied to its reference; add nothing the sources do not say.

I have nothing to rewrite. 

- [ ] Cite nothing from the "excluded" list in the appendix.

I haven't made any changes

- [ ] Expect the reviewer to challenge notability; see the verdict below.

Where are you pointing to?

**Source quality** (after the sweep)

- Independent, staff-written coverage: four funding-news articles on BlinkOps (SiliconANGLE, SecurityWeek, Globes, CTech; July 2025) use "micro-agents" as the company's product label without defining it. No staff-written article in any major outlet defines microagents as a pattern.
- Peer-reviewed: the OpenHands paper (ICLR 2025, a different sense) and the Otago and AGH micro-agent papers (the pre-LLM sense). No peer-reviewed paper frames microagents as the microservices analogue; two unreviewed preprints do (MAKER, November 2025; deVadoss, May 2026).
- Attributed opinion: three CIO contributor columns (Tadepalli, two; Badeev, one).
- Primary and vendor: Microsoft, Temporal (blog and webinar), Vectorize, the ThoughtSpot talk, BlinkOps, Karsun, Cognizant, and the repositories (Furter, Microsoft's demo, AgentM, Latimer's Swarm fork).
- No use of the term found in analyst reports, books, the MCP, A2A and AGNTCY specifications, major framework documentation, or Anthropic's agent guide (details in the appendix).

**Notability verdict.** The term is in real use in at least three senses, but every source that defines the microservices-sense pattern is primary or vendor-published, and the only independent reporting uses the word as one company's product label. On this evidence an AfC reviewer is likely to decline the draft under the general notability guideline and the neologism guideline. What would change that: a staff-written explainer in a reliable outlet, an analyst report, or a peer-reviewed survey that uses the term. Two things the sweep could not check: Google Books full text and paywalled analyst reports.

**Three things the article must not say**, because no source supports them: that the term is widely adopted; that any one person or company coined it; that agent frameworks or standards support it.

## Lead

&#91;The lead has no heading in the live article. Reference numbers match the References section below.\]

**Microagents** (also written *micro-agents* or *micro agents*) are small, single-purpose artificial intelligence agents, each limited to one well-defined task, that are combined with other such agents to carry out larger workflows.\[1\]\[2\]\[5\] The term has been used in this sense since late 2023 by software vendors and practitioners, who compare the approach to microservices in software architecture: a system is broken into narrowly scoped, independently deployable units that communicate through defined interfaces, rather than one large agent that holds every tool and instruction.\[1\]\[2\]\[3\]\[4\]\[9\] Proponents argue that a narrow scope keeps each agent's context small and its behaviour easier to test, maintain and replace.\[1\]\[2\]\[3\] Both proponents and critics note that splitting a system among many agents brings back problems familiar from microservices: coordination, state management and failure handling,\[2\]\[3\] network latency,\[3\]\[11\] and a proliferation of agents.\[8\]

There is no single accepted definition. The word is also used for unrelated things, including keyword-triggered instruction files in the OpenHands coding agent,\[20\]\[21\] platform-level helper agents in the aiXplain platform,\[22\] the most primitive layer of agent in a line of multi-agent-systems research that predates large language models,\[25\]\[29\] and self-propelled microscopic particles in physics.\[31\]


## Definition and characteristics

No standard definition exists, and the sources describe the idea in their own terms. 

- Chris Rickman and Alex Chao of Microsoft's Semantic Kernel team (2024) described a "MicroAgent pattern" that pairs each agent with one service: the agent's system instructions are written for that service alone, and natural language is the interface between the loosely coupled agents.\[1\]
- Chris Latimer of Vectorize (2024) described microagents as smaller services with clear responsibilities, each with its own bounded context in the sense of domain-driven design, which collaborate and hand requests to one another.\[3\]
- Cornelia Davis of Temporal (2026) described a set of microagents "each doing one thing and one thing well", in the manner of the Unix philosophy; a narrower scope, she argued, means a smaller context window and better model performance on the scoped task.\[2\]
- Ashish Shubham of ThoughtSpot (2026) defined a MicroAgent as a lightweight, independently deployable package of two parts, a Model Context Protocol server that exposes domain tools and a prompt template that encodes domain expertise, with sessions, authentication and streaming handled by a shared base service.\[4\]
- Rao Tadepalli, writing in CIO (2026), called micro agents specialised systems that perform narrow, well-defined tasks within a workflow, typically inside existing applications, and said they operate at the task level rather than the workflow level.\[5\]
- BlinkOps, a security-automation vendor (2025), described a micro-agent as an expert built to do one thing very well, pairing model reasoning with deterministic skills.\[19\]
- The authors of the MAKER research system (2025) assigned agents tiny "micro-roles" instead of human-sized roles and called the resulting units focused microagents.\[7\]

Common to most of these descriptions are a single responsibility; a deliberately bounded scope, including a bounded set of tools and instructions; independent development, deployment and replacement; and composition into larger systems by an orchestrating agent or by ordinary program code.\[1\]\[2\]\[3\]\[4\]\[12\] Some sources use the prefix only to mean small or specialised and draw no comparison with microservices.\[12\]\[19\]\[22\]

Spelling is unsettled: sources write *microagents*,\[1\]\[2\]\[3\] *micro-agents*,\[13\]\[18\]\[19\] *micro agents*\[5\]\[12\] and *MicroAgents*.\[1\]\[4\]

## Comparison with microservices

The comparison with microservices is the defining feature of most descriptions, and each source draws it differently.

Microsoft's authors listed the microservice benefits they hoped to carry over, ease of maintenance, fault isolation, efficiency and deployment agility, and observed that a single "mono-agent" would otherwise have to fit every function and plugin into one model context and choose among possibly thousands of services.\[1\] Latimer mapped microservice practices directly onto agents: a bounded context per agent, separate containers with service discovery in production, and in-process function calls during local development.\[3\] Davis argued that splitting work among agents brings many of the benefits microservices brought, smaller scope, independent evolution, a smaller blast radius and clear ownership, along with the same system-level problems of coordination, state, time and failure, for which the microservices era had already worked out patterns such as event-driven architecture.\[2\] Shubham cast the Model Context Protocol as the service boundary, in the role an API contract plays for microservices, with shared infrastructure standing in for the service mesh or API gateway.\[4\] Tadepalli wrote that micro agents resemble AI-powered microservices.\[5\] The MAKER authors devoted a section to parallels with microservices (modularity, independent development, scalability, monitoring and design for failure) and suggested that microagents could be seen as a natural evolution of microservices.\[7\]

Some writers stress the differences. Hari Narayanan of Karsun (2026) distinguished a microservice, which executes a command, from a micro-agent, which is given a goal and decides how to reach it, and suggested existing microservices become the tools that agents call.\[18\] John deVadoss (2026) treated microservices as a cautionary precedent rather than a model, arguing that enterprises build many small agents because microservices made the pattern familiar and that this proliferation is a hazard.\[8\]

The broader analogy between AI agents and microservices is also discussed by sources that do not use the term, including a Stack Overflow Podcast episode, "Treating your agents like microservices" (2025),\[34\] and an IBM essay on the evolution from microservices to agents (2025).\[35\] \[This sentence shows the analogy is wider than the word; a reviewer may call it tangential. Keep or cut.\]

## History

### Earlier uses in multi-agent systems

The hyphenated form "micro-agent" was used from 2001 by researchers at the University of Otago for the lowest and most primitive level of agent in their multi-level Opal architecture: micro-agents communicate through simple method calls, and larger agents are composed recursively from micro-agents.\[38\]\[25\]\[26\] Christopher Frantz and colleagues later built the μ² platform on this idea and ported it to Android (2011–2012).\[27\]\[28\] A 2014 paper by a group at AGH University of Science and Technology in Kraków described μ² ("micro-squared") as a multi-agent platform centred on micro-agents and restated the definition as "a small-size agent, that can be recursively constructed from other micro-agents".\[29\] An unrelated coinage is the "fuzzy micro-agents" that Brian Magerko and colleagues at Georgia Tech used for improvisational behaviour in interactive narrative (2010).\[30\] \[No source links this work to the later use for language-model agents; do not imply a lineage.\]

In 2023 Fetch.ai used "Microagents" for a limited subset of the capabilities of its Web3 autonomous economic agents and said they would be "for Web3 what microservices are for Web2".\[24\]

### Use for language-model agents

The earliest use found in the current sense is an open-source project by Aymen Furter, announced on Hacker News on 18 December 2023, which generates small agents on demand, validates them and stores them for reuse; its README of January 2024 explains the name as "microservice-sized (hence, microagents)".\[9\]\[10\] On 22 January 2024 Chris Rickman and Alex Chao of Microsoft published "MicroAgents: Exploring Agentic Architecture with Microservices" on the Semantic Kernel blog, naming the pattern and reporting an initial experiment that compared it with a single "mono-agent".\[1\]\[11\] Later uses include Steve Ickman's AgentM library (August 2024),\[12\] Vectorize's account of decomposing a retailer's customer-service agent (December 2024),\[3\] a ConFoo Montreal talk on building "super agents" from micro-agents (February 2025),\[16\] and BlinkOps' "security micro-agents", which received trade-press coverage when the company raised a US$50 million Series B round in July 2025.\[13\]\[14\]\[15\]\[39\] From late 2025 the term appeared in two arXiv preprints,\[7\]\[8\] in opinion columns in CIO,\[6\]\[5\] in a Temporal blog post and webinar (April and August 2026),\[2\]\[17\] and in a talk by ThoughtSpot's Ashish Shubham at the WeAreDevelopers World Congress 2026 North America (September 2026).\[4\]

&#91;The sources do not cite one another and none credits an originator, so the article should not say who coined the term or that any one source popularised it.\]

## Composition and orchestration

Microagents are meant to be combined, and the sources describe several arrangements.

- **A coordinating agent that delegates.** In Microsoft's experiment a manager agent handled a vacation-booking request by delegating to specialised agents, among them a calendar agent and a travel agent; it sent one natural-language request to the calendar agent rather than calling date and event functions itself.\[1\] Davis describes a higher-level travel agent that understands a trip spans several categories and delegates to transport, lodging and entertainment agents.\[2\]
- **Layers.** Tadepalli proposes three layers: micro agents for task execution, "macro agents" that coordinate micro agents through an end-to-end process such as an insurance claim, and "meta agents" that monitor, audit and govern the others.\[5\] Badeev likewise describes micro-agents with atomic functions as a base layer beneath coordinating agents.\[6\] Lapierre's ConFoo talk combines single-purpose micro-agents into one "super agent",\[16\] and Shubham's "super-agents" compose MicroAgents through configuration, with a shared base service routing tool calls over the Model Context Protocol.\[4\]
- **Program code as orchestrator.** Steve Ickman's AgentM library inverts the usual arrangement: deterministic application code is the orchestrator and calls a micro agent (a library function such as *filterList*, *sortList* or *mapList*) only when a step needs a language model.\[12\]
- **Fine-grained decomposition with error correction.** The MAKER system decomposes a task into a very large number of steps, each handled by a focused microagent, and uses voting among agents to correct errors; its authors report completing a task of more than one million LLM steps with zero errors.\[7\]\[37\]

Davis also argues that agents running for minutes or hours need event-driven, durable execution rather than request/response calls, as the orchestration of microservices did.\[2\] \[Davis works for Temporal, which sells durable execution; attribute, and keep it to one sentence.\]

## Implementations and examples

- **Microsoft Semantic Kernel experiment and demonstration (2024).** The blog post's experiment spread eight critical and twelve irrelevant APIs across five microagents and compared them with a single mono-agent on a vacation-booking task using GPT-4 Turbo; it reported completion rates it called effectively equivalent, 80–85% for both designs.\[1\] A companion C# demonstration defines eight agents, some deliberately irrelevant to its tasks, and its README later reported higher success rates but higher latency for the microagent design on calendar, banking and travel tasks.\[11\] \[The two documents disagree; attribute each figure to its document or omit the figures.\]
- **Microagents by Aymen Furter (2023–2024).** A Python framework that generates agents in response to tasks, tests them and stores validated agents for reuse; the agents execute Python code directly and, in the project's words, are microservice-sized.\[9\]
- **AgentM (2024).** JavaScript and Python libraries by Steve Ickman that expose micro agents as ordinary functions (for example *filterList*, *mapList*, *sortList*, *groundedAnswer*) built on OpenAI structured outputs, with the application's own code as orchestrator.\[12\] \[Ickman's GitHub profile lists Microsoft; he was a lead contributor to the Bot Framework SDK and Teams AI library. Mention only if a reviewer-proof source is found.\]
- **Microagent (2024).** Latimer's fork of OpenAI's Swarm framework that adds support for other model providers.\[3\]\[36\]
- **BlinkOps Security Micro-Agent Builder (2025).** A commercial no-code builder for task-specific security agents that can communicate with one another; the company raised a US$50 million Series B round in July 2025.\[13\]\[14\]\[15\]
- **MAKER (2025).** A research system from Cognizant AI Lab that distributes a task across focused microagents with error correction (see above).\[7\]\[37\]

## Limitations and criticism

- **Context and coordination.** Microsoft's authors observed that a mono-agent keeps context by coordinating everything itself, that context is decisive for either design, and that completion rates fall with weaker models;\[1\] their demonstration README reports higher latency for the microagent design because of the additional network requests.\[11\]
- **Operational cost.** Latimer lists coordination overhead, additional points of failure, state management across agent boundaries, harder integration testing and network latency.\[3\]
- **Repeating the microservices era.** Davis argues that decomposition brings back the coordination, state and failure problems of microservices, and that the memory APIs of current agent frameworks, naming LangGraph and AWS AgentCore, leave much of the state-management burden to developers.\[2\]
- **Task-level scope.** Tadepalli writes that micro agents operate at the task level rather than the workflow level and therefore need coordinating and governing layers above them.\[5\]
- **Proliferation.** In a 2026 preprint, deVadoss reports that a "role-based micro-agent swarm" was the worst-performing architecture in his comparison (23.1% safe-success rate against 70.6% for the design he proposes) and describes "micro-agent proliferation" as an architectural hazard.\[8\] \[Single-author preprint; attribute.\]

&#91;Evidence note for you, not article text: the quantitative evidence is thin. Microsoft describes its experiment as a basic validation showing initial qualitative differences, Vectorize's case study reports no outcomes, and the two preprints are not peer reviewed. Wikipedia cannot say this unless a source says it.\]

## Other uses of the term

- **OpenHands.** In the OpenHands coding agent, "microagents" were at first specialised agents defined by a prompt and a configuration file (April 2024);\[41\] the project's 2024 paper describes a "micro agent" as an agent specialised to one task by reusing a generalist agent's implementation.\[20\] By November 2024 the name also covered Markdown files of instructions that are injected into the agent's prompt when a trigger keyword appears;\[40\]\[21\] the project's documentation renamed these "skills" in November 2025.\[42\]
- **aiXplain.** In the aiXplain platform, "micro-agents" are helper agents (a response generator, planner, orchestrator, inspector and "bodyguard") that handle cross-cutting concerns such as planning, coordination and access control for primary agents.\[22\]
- **vLLM.** The vLLM project's "Micro-Agent" (2026) denotes collaborations among several models inside the model-serving layer, exposed to callers behind a single model name.\[23\]
- **Fetch.ai.** "Microagents" (2023) were a limited subset of the capabilities of Fetch.ai's Web3 autonomous economic agents.\[24\]
- **Microsoft Defender for IoT.** A "micro agent" is a lightweight security agent for IoT devices, which Microsoft plans to retire in June 2027.\[33\]
- **Multi-agent systems research.** The Otago micro-agent architecture and μ² platform, and Georgia Tech's improvisational micro-agents (see History).\[25\]\[27\]\[30\]
- **Physics.** "Microagents" also denotes self-propelled microscopic particles.\[31\]
- **Name collision.** "MicroAgent" is also the name of a 2026 research framework for decomposing applications into microservices, unrelated to the pattern described here.\[32\]

&#91;Left out as too minor for the article: the "Microagents" AI-agent-gateway product (microagents.io), the AstraBert/srimon12 Rust library, Builder.io's "micro-agent" coding tool and bassemZohdy/micro-agents (0 stars). Mentioning them would invite an undue-weight objection.\]

## See also

&#91;All titles below were found on English Wikipedia on 14 October 2026. "Agentic AI" redirects to "AI agent", so the list uses the target. "Semantic Kernel" was removed because no article could be found.\]

- Microservices
- Multi-agent system
- Intelligent agent
- AI agent
- Model Context Protocol
- Agent2Agent
- Domain-driven design
- Unix philosophy
- Separation of concerns

## References

&#91;Numbers match the inline markers. Bracketed remarks are notes to you.\]

1. Rickman, Chris; Chao, Alex (22 January 2024). ["MicroAgents: Exploring Agentic Architecture with Microservices"](https://devblogs.microsoft.com/semantic-kernel/microagents-exploring-agentic-architecture-with-microservices/). Semantic Kernel blog, Microsoft. \[Same post also served from the renamed [Microsoft Agent Framework blog](https://devblogs.microsoft.com/agent-framework/microagents-exploring-agentic-architecture-with-microservices/).\]
2. Davis, Cornelia (23 April 2026). ["What agentic AI borrowed from microservices (and made worse)"](https://temporal.io/blog/what-agentic-ai-borrowed-from-microservices). Temporal Technologies.
3. Latimer, Chris (12 December 2024). ["Microagents: building better AI agents with microservices"](https://vectorize.io/blog/microagents-building-better-ai-agents-with-microservices). Vectorize.
4. Shubham, Ashish (2026). ["MicroAgents: The Microservices of the Agentic Era"](https://sessionize.com/s/ashish-shubham1474/microagents-the-microservices-of-the-agentic-era/184473) (talk abstract). Sessionize. Related abstract: ["From Microservices to MicroAgents: MCP as the New Service Boundary"](https://sessionize.com/s/ashish-shubham1474/from-microservices-to-microagents-mcp-as-the-new-s/178652). Talk given at WeAreDevelopers World Congress 2026 North America; [recording](https://www.wearedevelopers.com/videos/100560-microagents-the-microservices-of-the-agentic-era) published 25 September 2026 (free account required).
5. Tadepalli, Rao (14 April 2026). ["Micro and macro agents: The emerging architecture of the agentic enterprise"](https://www.cio.com/article/4157977/micro-and-macro-agents-the-emerging-architecture-of-the-agentic-enterprise.html). CIO (opinion, Foundry Expert Contributor Network).
6. Badeev, Ilia (30 September 2025). ["Taming AI agents: The autonomous workforce of 2026"](https://www.cio.com/article/4064998/taming-ai-agents-the-autonomous-workforce-of-2026.html). CIO (opinion, Foundry Expert Contributor Network).
7. Meyerson, Elliot; Paolo, Giuseppe; Dailey, Roberto; Shahrzad, Hormoz; Francon, Olivier; Hayes, Conor F.; Qiu, Xin; Hodjat, Babak; Miikkulainen, Risto (12 November 2025). ["Solving a Million-Step LLM Task with Zero Errors"](https://arxiv.org/abs/2511.09030). arXiv:2511.09030 (preprint).
8. deVadoss, John (7 May 2026). ["Designing Intelligent Enterprise Agents: A Capability-Aligned Multi-Agent Architecture"](https://arxiv.org/abs/2605.08258). arXiv:2605.08258 (preprint).
9. Furter, Aymen (2023–2024). ["Microagents Framework"](https://github.com/aymenfurter/microagents) (software repository, described as "Self-improving Agents"; first commit 11 December 2023, v0.1.0 released 21 January 2024). GitHub.
10. ["Show HN: Microagents: Agents capable of self-editing their prompts / Python code"](https://news.ycombinator.com/item?id=38679453). Hacker News, 18 December 2023. \[Primary source, for the date only.\]
11. Rickman, Chris; Chao, Alex (2024). ["MicroAgentsDemo"](https://github.com/crckman/MicroAgentsDemo) (companion code to the Microsoft post; repository created 1 February 2024). GitHub.
12. Ickman, Steven (2024). ["AgentM: A library of 'Micro Agents' that make it easy to add reliable intelligence to any application"](https://github.com/Stevenic/agentm-js) (software repository; first commit 31 August 2024). GitHub. Python version: [agentm-py](https://github.com/Stevenic/agentm-py).
13. Riley, Duncan (28 July 2025). ["BlinkOps raises $50M to expand deployment of no-code security micro-agents"](https://siliconangle.com/2025/07/28/blinkops-raises-50m-expand-deployment-no-code-security-micro-agents/). SiliconANGLE.
14. Kovacs, Eduard (30 July 2025). ["BlinkOps Raises $50 Million for Agentic Security Automation Platform"](https://www.securityweek.com/blinkops-raises-50-million-for-agentic-security-automation-platform/). SecurityWeek.
15. Orbach, Meir (28 July 2025). ["BlinkOps secures $50M for its micro agent cyber platform"](https://www.calcalistech.com/ctechnews/article/hjwr1jhvge). CTech (Calcalist).
16. Lapierre, Carl (27 February 2025). ["Building Super Agents with Micro-Agent Orchestration"](https://confoo.ca/en/2025/session/building-super-agents-with-micro-agent-orchestration) (talk abstract). ConFoo Montreal 2025.
17. ["From Monoliths to Micro-Agents: The Next Architectural Shift in AI"](https://pages.temporal.io/webinar-monoliths-to-microagents) (webinar, 6 August 2026; Cornelia Davis, Ethan Ruhe, Charles Zedlewski). Temporal Technologies.
18. Narayanan, Hari (26 January 2026). ["From Microservices to Micro-Agents: The Next Evolution of Software Architecture"](https://karsun-llc.com/blog/from-microservices-to-micro-agents-the-next-evolution-of-software-architecture/). Karsun Solutions (Karsun Innovation Center blog).
19. BlinkOps (21 October 2025). ["Micro-Agents vs. Monolithic AI: Why Smaller is Better"](https://blinkops.com/blog/micro-agents-vs-monolithic-ai-why-smaller-is-better).
20. Wang, Xingyao; Li, Boxuan; Song, Yufan; Xu, Frank F.; Tang, Xiangru; et al. (2025). ["OpenHands: An Open Platform for AI Software Developers as Generalist Agents"](https://arxiv.org/abs/2407.16741). International Conference on Learning Representations (ICLR 2025). arXiv:2407.16741. [Proceedings page](https://proceedings.iclr.cc/paper_files/paper/2025/hash/a4b6ad6b48850c0c331d1259fc66a69c-Abstract-Conference.html).
21. OpenHands documentation. ["Skills Overview"](https://docs.openhands.dev/overview/skills) (states that the legacy .openhands/microagents/ directories remain supported).
22. aiXplain documentation. ["Micro-Agents"](https://docs.aixplain.com/concepts/micro-agents).
23. vLLM Semantic Router Team (29 June 2026). ["Micro-Agent: Beat Frontier Models with Collaboration inside Model API"](https://vllm.ai/blog/2026-06-29-micro-agent-frontier-models). vLLM blog.
24. Fetch.ai (7 March 2023). ["The Dawn of Microagents"](https://medium.com/fetch-ai/the-dawn-of-microagents-753d7d3d6dbf). Fetch.ai on Medium. \[Company-published; usable only for Fetch.ai's own usage.\]
25. Purvis, Martin; Nowostawski, Mariusz; Cranefield, Stephen (2002). "A multi-level approach and infrastructure for agent-oriented software development". Proceedings of the First International Joint Conference on Autonomous Agents and Multiagent Systems (AAMAS '02), pp. 88–89. [doi:10.1145/544757.544763](https://doi.org/10.1145/544757.544763). \[Page numbers from DBLP; confirm in the ACM Digital Library.\]
26. Purvis, Martin; Cranefield, Stephen; Nowostawski, Mariusz; Carter, Dan (March 2002). ["Opal: A Multi-Level Infrastructure for Agent-Oriented Software Development"](https://ourarchive.otago.ac.nz/esploro/outputs/workingPaper/Opal-A-multi-level-infrastructure-for-agent-oriented/9926480313201891). Information Science Discussion Paper Series 2002/01, University of Otago. hdl:10523/1089.
27. Frantz, Christopher; Nowostawski, Mariusz; Purvis, Martin K. (2011). "Dynamic Ad Hoc Coordination of Distributed Tasks Using Micro-Agents". In *Agents in Principle, Agents in Practice* (PRIMA 2011), Lecture Notes in Computer Science 7047, pp. 275–286. Springer. [doi:10.1007/978-3-642-25044-6\_22](https://doi.org/10.1007/978-3-642-25044-6_22).
28. Frantz, Christopher; Nowostawski, Mariusz; Purvis, Martin K. (2012). "Micro-agents on Android: Interfacing Agents with Mobile Applications". In *Advanced Agent Technology: AAMAS 2011 Workshops*, Lecture Notes in Computer Science 7068, pp. 488–502. Springer. [doi:10.1007/978-3-642-27216-5\_37](https://doi.org/10.1007/978-3-642-27216-5_37).
29. Krzywicki, Daniel; Faber, Łukasz; Byrski, Aleksander; Kisiel-Dorohinicki, Marek (2014). "Computing Agents for Decision Support Systems". *Future Generation Computer Systems* 37: 390–400. [doi:10.1016/j.future.2014.02.002](https://doi.org/10.1016/j.future.2014.02.002); [arXiv:1402.2793](https://arxiv.org/abs/1402.2793).
30. Magerko, Brian; Fiesler, Casey; Baumer, Allan (2010). "Fuzzy Micro-Agents for Interactive Narrative". Proceedings of the Sixth AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment (AIIDE 2010), pp. 156–161. [doi:10.1609/aiide.v6i1.12412](https://doi.org/10.1609/aiide.v6i1.12412).
31. Masoudi, Mohammad Hossein; Naji, Ali (2025). "Smart navigation through a rotating barrier: Deep reinforcement learning with application to size-based separation of active microagents". *The Journal of Chemical Physics* 162 (14). [doi:10.1063/5.0269792](https://doi.org/10.1063/5.0269792); [arXiv:2411.05587](https://arxiv.org/abs/2411.05587). \[Journal details from OpenAlex and PubMed; the publisher's page could not be opened.\]
32. Su, Zishan; Huang, Junjie; Shan, Shiwen; Chen, Xingyan; Zeng, Hui; Su, Yuxin; Wang, Yanlin; Lyu, Michael R. (2026). ["MicroAgent: Context-Augmented Multi-Agent Framework for Automatic Microservice Decomposition"](https://arxiv.org/abs/2606.29742). IEEE/ACM International Conference on Automated Software Engineering (ASE 2026). doi:10.1145/3832783.3834441.
33. Microsoft Learn. ["Standalone micro agent overview"](https://learn.microsoft.com/en-us/azure/defender-for-iot/device-builders/concept-standalone-micro-agent-overview). Microsoft Defender for IoT documentation.
34. ["Treating your agents like microservices"](https://stackoverflow.blog/2025/12/05/treating-your-agents-like-microservices). The Stack Overflow Podcast, 5 December 2025 (guest Guillaume De Saint Marc, Outshift by Cisco).
35. Kralj, Miha (20 May 2025). ["From microservices to AI agents: The evolution of application architecture"](https://www.ibm.com/think/insights/evolution-application-architecture). IBM Think.
36. Latimer, Chris (2024). ["microagent: A fork of OpenAI Swarm that supports Groq and Anthropic"](https://github.com/chrislatimer/microagent) (software repository). GitHub.
37. Meyerson, Elliot (13 November 2025). ["Shattering the Illusion: MAKER Achieves Million-Step, Zero-Error LLM Reasoning"](https://www.cognizant.com/ca/en/ai-lab/blog/maker). Cognizant AI Lab.
38. Nowostawski, Mariusz; Bush, Geoff; Purvis, Martin; Cranefield, Stephen (March 2001). ["A Multi-Level Approach and Infrastructure for Agent-Oriented Software Development"](https://ourarchive.otago.ac.nz/esploro/outputs/workingPaper/A-multi-level-approach-and-infrastructure-for/9926478498701891). Information Science Discussion Paper Series 2001/06, University of Otago. hdl:10523/1006.
39. ["Israeli micro-agents security co BlinkOps raises $50m"](https://en.globes.co.il/en/article-israeli-micro-agents-security-co-blinkops-raises-50m-1001517306). Globes, 28 July 2025.
40. OpenHands repository, [pull request #4568 "Use keyword matching for CodeAct microagents"](https://github.com/OpenHands/OpenHands/pull/4568) (merged 9 November 2024). GitHub. \[Primary source, for the date only.\]
41. OpenHands repository, [pull request #1238 "Microagents and Delegation"](https://github.com/OpenHands/OpenHands/pull/1238) (merged 24 April 2024). GitHub. \[Primary source, for the date only.\]
42. OpenHands documentation repository, [pull request #129 "Rebrand microagents to skills and centralize documentation"](https://github.com/OpenHands/docs/pull/129) (25 November 2025). GitHub. \[Primary source, for the date only.\]

## Appendix: source assessment

Class: A = independent, reliable, secondary; B = attributed opinion in a reliable outlet; C = primary or self-published (vendor blog, docs, repository, talk abstract, press release); D = unreliable (SEO glossary, aggregator, content farm). "Supports" says what the source can carry on Wikipedia.

| Ref | Source | Type | Class | Spelling | Supports |
| --- | --- | --- | --- | --- | --- |
| 1 | Microsoft Semantic Kernel blog, Rickman & Chao, 22 Jan 2024 | vendor engineering blog | C | MicroAgents / microagent | Microsoft's pattern, experiment and trade-offs, attributed |
| 2 | Temporal blog, Davis, 23 Apr 2026 | vendor blog | C | microagents | Davis's argument, attributed; author sells durable execution |
| 3 | Vectorize blog, Latimer, 12 Dec 2024 | vendor blog (by the company's co-founder and CEO) | C | microagents | Latimer's definition and anonymised case study, attributed; no outcomes |
| 4 | Shubham, Sessionize abstracts; talk at WeAreDevelopers, Sep 2026 | self-submitted abstract; recording behind sign-up | C | MicroAgents | Shubham's MCP-based definition, attributed |
| 5 | CIO, Tadepalli, 14 Apr 2026 | contributor opinion in trade outlet | B | micro agents | the micro/macro/meta framing, attributed; not independent coverage |
| 6 | CIO, Badeev, 30 Sep 2025 | contributor opinion in trade outlet | B | Micro-agents | layered view, attributed |
| 7 | MAKER, Meyerson et al., arXiv Nov 2025 | preprint, no peer review, 0 citations when checked | C | microagents | research usage and microservices parallel, attributed |
| 8 | deVadoss, arXiv May 2026 | single-author preprint | C | micro-agent | criticism, attributed |
| 9 | aymenfurter/microagents, GitHub | repository (823 stars) | C | microagents | existence, dates, project's own rationale |
| 10 | Show HN, 18 Dec 2023 | forum post | C | Microagents | launch date only |
| 11 | crckman/MicroAgentsDemo, GitHub | repository (17 stars) | C | MicroAgents | demo design and its README figures |
| 12 | Stevenic/agentm-js, GitHub | repository (34 stars) | C | Micro Agents | AgentM's design, attributed to its README |
| 13 | SiliconANGLE, Riley, 28 Jul 2025 | staff-written funding news | A (borderline) | micro-agents | that the term is used commercially; no definition |
| 14 | SecurityWeek, Kovacs, 30 Jul 2025 | staff-written funding news | A (borderline) | micro-agents | same |
| 15 | CTech/Calcalist, Orbach, 28 Jul 2025 | staff-written funding news | A (borderline) | micro agent(s) | same; CEO quote on "one thing extremely well" |
| 16 | ConFoo 2025, Lapierre | conference abstract | C | micro-agent | talk existed; "super agent" framing |
| 17 | Temporal webinar page, 6 Aug 2026 | vendor marketing page | C | Micro-Agents | Temporal's framing; note hyphen differs from its blog |
| 18 | Karsun blog, Narayanan, 26 Jan 2026 | contractor marketing blog | C | micro-agents | the command-vs-goal distinction, attributed |
| 19 | BlinkOps blog, 21 Oct 2025 | vendor blog | C | micro-agent | BlinkOps's own definition |
| 20 | OpenHands paper, ICLR 2025 | peer-reviewed | A for the paper's own content | micro agent | OpenHands's task-specialised sense |
| 21 | OpenHands docs | project docs | C | microagents | OpenHands's instruction-file sense |
| 22 | aiXplain docs (v1.0, undated) | product docs | C | micro-agents | aiXplain's helper-agent sense |
| 23 | vLLM blog, 29 Jun 2026 | project blog | C | Micro-Agent | vLLM's serving-layer sense |
| 24 | Fetch.ai on Medium, 7 Mar 2023 | company-published | C (about-self) | Microagents | Fetch.ai's 2023 Web3 usage |
| 25 | Purvis, Nowostawski, Cranefield, AAMAS 2002 | peer-reviewed (2-page) | A | micro-agents | Otago definition |
| 26 | Opal discussion paper, Otago 2002 | working paper | C | micro-agents | Otago definition in detail |
| 27 | Frantz et al., PRIMA 2011 (LNCS 7047) | peer-reviewed | A | micro-agents / μ-agents | μ² platform |
| 28 | Frantz et al., AAMAS 2011 workshops (LNCS 7068) | peer-reviewed workshop | A | micro-agents | Android port |
| 29 | Krzywicki et al., FGCS 2014 | peer-reviewed journal (30 citations) | A | micro-agents | restated definition |
| 30 | Magerko et al., AIIDE 2010 | peer-reviewed | A | micro-agents | unrelated coinage |
| 31 | Masoudi & Naji, J. Chem. Phys. 2025 | peer-reviewed | A | microagents | physics sense |
| 32 | Su et al., ASE 2026 | peer-reviewed (distinguished paper) | A | MicroAgent | name collision only |
| 33 | Microsoft Learn, Defender for IoT | product docs | C | micro agent | unrelated security-agent sense |
| 34 | Stack Overflow Podcast, 5 Dec 2025 | editorial podcast | A/B | (term not used) | the wider agents-as-microservices analogy |
| 35 | IBM Think, Kralj, 20 May 2025 | vendor essay | C | (term not used) | same, attributed |
| 36 | chrislatimer/microagent, GitHub | repository (132 stars) | C | Microagent | existence of the Swarm fork |
| 37 | Cognizant AI Lab blog, 13 Nov 2025 | vendor blog | C | microagents | MAKER summary |
| 38 | Otago discussion paper 2001/06 | working paper | C | micro-agents | earliest Otago definition |
| 39 | Globes, 28 Jul 2025 | staff/correspondent funding news | A (borderline) | micro-agents | commercial use of the term |
| 40 | OpenHands PR #4568 | repository history | C | microagents | date of the keyword-triggered files |

Refs 41 and 42 (OpenHands pull requests #1238 and #129 on GitHub) are repository history, class C, cited only for dates.

**Checked and excluded from the article** (do not cite): Fulcrum Digital "Micro-Agent Architecture" glossary (D, SEO page for the vendor's platform); Growth Memo "What are microagents?" (D/C, newsletter glossary); Emergent Mind "Microagent decomposition" topic page (D, AI-generated, and it misattributes the term to a paper that does not use it); Stack Archive summary of the Temporal post (D, AI-assisted); Fact.MR "Micro Agents Market" report page (D, sales page); Medium posts by Goldfinger (May 2025) and Seyongaur (Aug 2025) and the dev.to posts by Kishor (Aug 2025) and Kondratiuk (Apr 2026) (C, self-published, no standing); Wild Moose and Forvis Mazars posts (C, no added substance); bassemZohdy/micro-agents (C, created Aug 2026, 0 stars); the "Microagents" gateway (publisher unverifiable); the AstraBert/srimon12 Rust library (0 stars); Bentley et al., arXiv 2509.03380 (does not use the term, despite the Emergent Mind page).

**Searched with no result for the term** (research for you; not citable): Gartner, Forrester, IDC, Constellation, Omdia public pages; books from O'Reilly, Manning, Packt, No Starch (tables of contents only; Google Books full text was unreachable); InfoQ, The New Stack, VentureBeat, ZDNet, TechCrunch, Wired, The Register, InfoWorld, Computerworld, SD Times, TechTarget, IEEE Spectrum, MIT Technology Review, CACM, Diginomica, Forbes staff, Fortune, Business Insider; the MCP, A2A and AGNTCY specifications; the documentation of LangChain, LangGraph, CrewAI, AutoGen, Microsoft Agent Framework, Google ADK, OpenAI Agents SDK, smolagents and Pydantic AI; Anthropic's "Building effective agents"; the Thoughtworks Technology Radar; QCon, KubeCon, Build, I/O, re:Invent and AI Engineer programmes.
