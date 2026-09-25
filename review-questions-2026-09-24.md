# Open questions from the site and docs review, 2026-09-24

Sixteen findings I did not change because they touch your wording, a product fact I cannot
verify, or a choice that is yours. Each has the row number from review-2026-09-24.csv, the
text as it stands, the question, and my suggestion. Write your answer after "Answer:"; "ok"
takes the suggestion.

## 1. Who sets the guardrails? (row 4)

docsrc/introduction/why-not-python.html:7 — "Administrators set limits once. Every agent
obeys them. Developers write only the agent logic."

Wrong. Developers set them. Admins set only 

docsrc/introduction/what-is-search2o.html:11 and runtime/overview.html:33-36 say the
allowlist, compile rules and runtime limits belong to the developer role.

Question: which is right? Suggestion: "Developers set limits once." on Why not Python. If
administrators own them, the runtime pages change instead.

Answer:

## 2. Draft with AI and `ask` (row 7)

docsrc/development/draft-with-ai.html:10 — "An `ask` that always runs could never finish
validation, so the AI guards it."

docsrc/development/trace-and-validation.html:38 says an ask during validation pauses the run
and the developer answers it in the GUI.

Question: what does Draft with AI actually do with asks? Suggestion: delete the sentence.

Answer:

## 3. Passwords in a Slack form (row 33)

docsrc/chat-integrations/chat-applications.html:8 — "Slack has no masked input, so never
collect a password or a token in a Slack form."
docsrc/chat-integrations/running-an-agent.html:27 — "Every chat application can render all
five in a form." (the five include password)
docsrc/chat-integrations/ai-prompts.html:134 — the Slack prompt maps "password to plain
text", so a generated bot collects the password in plain text.

Suggestion: one rule on all three pages — a form may carry a password field, but a Slack form
shows it in plain text, so the Slack prompt sends the person to the GUI for a password input,
as the skill does.

Answer:

## 4. The "Executing code from an LLM" page (rows 39, 49)

docsrc/llm/code-from-llm.html:1 — "Search2o will never execute arbitrary Python code. A
future dynamic command will let an LLM generate an agent in Search2o's own JSON format and
execute that agent." Line 5 — "Until the dynamic command ships, use tool calling..."
docsrc/llm/index.html:1 — the section lead promises "running code that an LLM writes"; the
toc title is "Executing code from an LLM".

Question: retire the page, or cut it to the tool-calling advice under a title such as "Tool
calling instead of generated code"? Either way the section lead and toc title follow.

Answer:

## 5. Getting started h1 (row 40)

html/gettingstarted.html:45 — "From your laptop to production". The page's five steps end on
the laptop; the production and team steps were removed.

Suggestion: "Up and running on your laptop" (the title you used on 09-07) or "From install to
your first search".

Answer:

## 6. "Community" support on the Free plan (row 41)

html/pricing.html:73 — Support: Free "Community", Paid "Email". No community channel exists
on the site or in the docs; the docs say support is the help icon and info@search2o.com.

Question: is a community channel planned? If not, "Email" or "Help icon".

Answer:

## 7. Sizing sentence (row 32)

docsrc/system-management/agent-server-sizing.html:23 — "A model at 1.5s per run fills an
agent server with three times as many runs as one at 4.5s."

By the page's own formula (runs at once = 50 x seconds per run) the 4.5 s model holds three
times as many runs at once. Question: which quantity did you mean? Suggestion: "At the same
throughput, a model that answers in 1.5 s keeps a third as many runs in flight as one that
takes 4.5 s."

Answer:

## 8. "Far too small" (row 50)

docsrc/system-management/agent-server-sizing.html:27 — "Its default of 20 connections is far
too small for that work, because each waiting run holds a connection for the whole call."

The docs calling the shipped default "far too small". Suggestion: "The default of 20
connections suits an agent server that mostly computes. When agents call anything, size the
pool above the number of runs at once, because each waiting run holds a connection for the
whole call."

Answer:

## 9. Home Platform card (row 56)

html/index.html:228 — "Never have to restart agent servers. A change to configuration is live
on the next agent run. A running agent keeps running with the old configuration."

The first sentence has no subject. Suggestion: "Agent servers never need a restart."

Answer:

## 10. Demo page h1 (row 58)

html/demo.html — the h1 "Search that executes" sits directly under the header tagline "Search
that executes", so the phrase appears twice within a few lines.

Suggestion: change the h1, e.g. "Try Search2o three ways".

Answer:

## 11. Home page Search line (row 61)

html/index.html:108 — "Search builds an index using natural-language descriptions written by
developers. This makes matching predictable, lets it scale to thousands of agents, and
returns results in under a second — see search quality."

Your line. It describes the mechanism ("builds an index"), which the docs avoid. Leave?

Answer:

## 12. "The US East" (row 78)

docsrc/support-licensing/license.html:14 — "Search2o Cloud currently operates from the US
East. You will see the lowest latency if you run the agent server in the US East."

Your wording. "The US East" is not a place name in English. Suggestion: "the eastern United
States" or "the US East region" (both places).

Answer:

## 13. How the editor shows an expression (row 92)

docsrc/development/code-editor.html:37 — "Expressions stand out: a value written as a Python
expression, like "{ total + 1 }", is shown with bold braces and its contents in a monospace
font."

The whole editor is monospace, so the distinction does not read. Question: what does the
editor actually do to an expression (a colour, a weight)?

Answer:

## 14. British or American spelling (row 119)

The search and chat sections use British spelling: catalogue, neighbourhood, modelled
(search-quality.html), summarised, catalogue (orchestrator.html), behaviour, labelled
(finding-an-agent.html). Everything else is American: summarizes, categorize, behavior,
organization.

"catalogue" appears about thirty times in the search-quality text. Question: standardise on
American? Yes/no.

Answer:

## 15. Can the owner send a help message? (row 126)

docsrc/support-licensing/support.html:4 — "Developers and administrators can use the form."
docsrc/support-licensing/asking-the-docs.html:4 — "Developers, administrators and the owner
can ask."

Question: can the owner also send a help message? If yes, support.html adds the owner.

Answer:

## 16. Northern Virginia (row 117)

html/about.html:8, :10 (meta and og descriptions) — "Built in Northern Virginia."
html/about.html:66 — "Search2o is based in Northern Virginia, USA."
Every footer says "Virginia, USA".

You left this once before. Leave again, or change About to "Virginia"?

Answer:

## For the record, not questions

- Group F (14 rows): docstrings in the search2o / s2oserver models — the api `headers`
  docstring still says `secret(...)`, `profile` still says "Either this or 'url'", the
  `return` command's table has one empty row named "root", the encryption `keys` docstring
  still says only three months of keys need keeping, "UI" and "the Search2o cloud" in several
  docstrings, missing units on the numeric limits. Not editable from this repo.
- Rows 144 and 145: the Terms send every dispute to arbitration while the License sends
  Software disputes to court (License §18 has a conflict rule); the License's no-third-party
  clause has no carve-out for the people it indemnifies, where the Terms have one. A lawyer's
  call.
- Row 116: html/index.html:8 and :10, the meta and og descriptions, still say "built around a
  search interface"; the hero, footer and og:image alt say "with a search interface". Say
  the word and they match.
- Row 125: the REST samples use $TOKEN on search.html and running-agents.html and
  $SEARCH2O_SERVICE_KEY on authentication.html and service-accounts.html for the same header.
  Left as is.
