# How we test Search2o's search

Source material for a web page. Everything below was measured against the live search index
running the code we ship, with the settings it ships with. Nothing is modeled or extrapolated.

---

## What we test against

Search2o's job is to read a question typed in plain language and find the agent that answers it.
To know how well it does that, we need catalogs of agents and questions with a known right
answer — so we built five, each a realistic working catalog for a different kind of business,
plus one very large catalog to test what happens at scale.

| catalog | agents | questions asked |
|---|---|---|
| a university | 50 | 500 |
| a clinic group | 50 | 500 |
| a software company's internal agents | 100 | 2,000 |
| a large corporation's departments | 100 | 1,000 |
| a retailer's supply chain and merchandising | 100 | 1,000 |
| **a catalog spanning fifty business areas** | **1,000** | **10,000** |

**15,000 questions in total.** Every question has one known correct agent, and every question was
put through the real search.

The five business catalogs are deliberately different from one another in the way that matters
most: how much their agents overlap. A university's agents sit well apart; a retailer's supply
chain agents share a great deal of ground. That difference is the main thing that decides how
hard search is, and it is why we do not report a single number.

---

## How often it finds the right agent

Search either runs the single best match or offers the two or three that are plausible, so there
are two numbers worth knowing: how often the right agent is the first one, and how often it is
among the ones offered.

| catalog | right agent first | right agent among the first three |
|---|---|---|
| a university | 91.0% | 97.6% |
| a clinic group | 90.6% | 98.2% |
| a software company's internal agents | 89.0% | 98.2% |
| a large corporation's departments | 85.4% | 94.9% |
| a retailer's supply chain | 83.8% | 95.6% |
| a catalog of 1,000 agents | 85.5% | 94.1% |

Two things are worth drawing out.

**The spread between catalogs is larger than the spread between any settings we tried.** The
easiest and hardest catalogs here are seven points apart, and both are 100-agent catalogs.
What separates them is how distinct their agents are from one another — which is something you
control when you write your agents, not something search can fix afterwards.

**Size is not the problem people expect it to be.** A catalog of a thousand agents scores
within a point of a catalog of a hundred. Adding agents does not make search worse; adding
agents that overlap does.

---

## Saying "no match" when nothing fits

An agent search that always answers is worse than useless, because the wrong agent will act. So
we test refusal as carefully as we test matching, with two kinds of question that should all be
turned away.

**Questions about something else entirely** — "how to replace brake pads on a 2012 Honda Civic"
asked of a university's catalog. These are refused **100% of the time**.

**Questions about the customer's own world that no agent covers** — asking a university about
appealing a parking ticket when nobody has built a parking agent. These are the hard ones,
because every agent in the catalog is in the same neighborhood and something always looks
close. They are refused **82% to 86% of the time**, depending on the catalog.

The second case is the one that matters in practice. Nobody types a sourdough recipe into a
company's search box; they ask about the one thing nobody has built an agent for yet.

---

## How fast it is

A search compares the question against everything in the catalog and returns the best matches
in **about 200 milliseconds**.

A catalog of a thousand agents takes about the same — a little over 200 milliseconds. That is the number worth remembering: **search
does not get slower as your catalog grows.**

---

## Across languages

Search works on meaning rather than on words, so it handles languages other than English, and it
handles a question asked in one language against agents described in another. Accuracy in a
non-English catalog is within about three points of English, and asking across two different
languages costs about three points more.

---

## An experiment: letting Jev choose between the two or three

Not yet in the product. The numbers in this section come from a test, not from the search we ship.

When search is not sure, it offers two or three agents and the user picks. We tested handing
that choice to Jev, a fast System 1 model from typesafe.ai. Jev is built to make one quick
decision from a fixed list of options. It reads the question and each offered agent's
description, and picks one.

On the questions where search offered two or three agents:

| catalog | search's first choice right | Jev's choice right |
|---|---|---|
| a university | 72.4% | 79.0% |
| a clinic group | 74.2% | 82.2% |
| a software company's internal agents | 69.9% | 77.4% |
| a large corporation's departments | 66.9% | 75.0% |
| a retailer's supply chain | 65.3% | 75.9% |
| a catalog of 1,000 agents | 67.0% | 73.6% |

Counted over every question, as in the first table on this page, the right agent comes first
more often:

| catalog | right agent first, search alone | with Jev choosing |
|---|---|---|
| a university | 91.0% | 92.4% |
| a clinic group | 90.6% | 93.2% |
| a software company's internal agents | 89.0% | 91.4% |
| a large corporation's departments | 85.5% | 87.6% |
| a retailer's supply chain | 83.8% | 88.1% |
| a catalog of 1,000 agents | 85.5% | 88.3% |

The gain is largest where agents overlap most, which is where search needs the help.

Speed is what makes this usable. Jev adds one call, and only to the searches that offered more
than one agent. Measured over thousands of calls, that call takes a median of 159 milliseconds
(90% under 215 ms) when connections are kept open, and 223 milliseconds (90% under 268 ms) when
each call opens its own. Jev's own processing time is a median of 62 milliseconds; the rest is
the network.

Jev needs each agent's description to do this well. Given only the agents' titles, it chose
worse than search's own first choice.

---

## What we do not claim

Every number above comes from catalogs we built, and a real catalog will differ. The honest
way to read them is as a range: a well-separated catalog lands at the top of it, a catalog
full of near-duplicate agents at the bottom, and the difference is mostly in how the agents are
described.

### The numbers are likely lower than real use

The test questions, and the answer each one is marked against, were written by a language
model, and they were made hard on purpose. Many name something that belongs to one agent while
asking for what another agent does: "What are the top drivers behind incident date by
severity?" is marked as belonging to an insurance-claims agent, because "incident date" is one
of its fields, though most people asking it would want the incident-report agent.

So a question counted as wrong is often one a person would have answered the same way. We
reviewed the questions where the right agent was among the choices search offered, but neither
search's first choice nor Jev's choice was that agent. Depending on the catalog,
between a fifth and three quarters of them had an answer key that was no better than the agent
chosen, and often worse. Some of the questions are confusing
enough that we would get them wrong ourselves.

Real people ask what they mean, in their own words. We expect search to do better on those
questions than on ours.

The fastest way to find out where yours sits is to put your own agents in and ask your own
questions.

---

## Where we go from here

We will be making constant improvement to search quality and speed.  