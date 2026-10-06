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

Search either runs the single best match or offers the two that are plausible, never more, so
there are two numbers worth knowing: how often the right agent is the first one, and how often it
is one of the first two.

| catalog | right agent first | right agent among the first two |
|---|---|---|
| a university | 91.0% | 96.8% |
| a clinic group | 90.6% | 97.4% |
| a software company's internal agents | 89.0% | 95.8% |
| a large corporation's departments | 85.5% | 92.3% |
| a retailer's supply chain | 83.8% | 94.3% |
| a catalog of 1,000 agents | 85.5% | 92.2% |

Two things are worth drawing out.

**The spread between catalogs is larger than the spread between any settings we tried.** The
easiest and hardest catalogs here are seven points apart, and both are 100-agent catalogs.
What separates them is how distinct their agents are from one another — which is something you
control when you write your agents, not something search can fix afterwards.

**Size is not the problem people expect it to be.** A catalog of a thousand agents scores
within a point of a catalog of a hundred. Adding agents does not make search worse; adding
agents that overlap does.

### One answer or two

When the best match is clearly ahead, search shows just that one; when the top two are close, it
shows both and lets the user choose. Showing one more often saves the user a click, but a single
answer that is wrong is worse than two that include the right one, so we set the line by checking
every single answer search gave against a reviewer's judgment (see below).

| catalog | questions answered with one result | of all questions, a single answer that was wrong |
|---|---|---|
| a university | 80.8% | 0.6% |
| a clinic group | 73.0% | 1.0% |
| a software company's internal agents | 73.6% | 1.2% |
| a large corporation's departments | 75.0% | 1.7% |
| a retailer's supply chain | 65.0% | 1.1% |
| a catalog of 1,000 agents | 64.6% | 0.6% |

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

So a question counted as wrong is often one a person would have answered the same way. We had
every question where search's first choice differed from the answer key — about 2,000 of them —
judged blind: the reviewer saw only the question and the two agents' descriptions, in random
order, without knowing which was the key and which was search's pick. In about three cases out of
four the key stood. In the rest, search's choice was as good or better. Counting those, the right
agent comes first more often than the table above says:

| catalog | right agent first, as marked | as judged |
|---|---|---|
| a university | 91.0% | 92.8% |
| a clinic group | 90.6% | 92.0% |
| a software company's internal agents | 89.0% | 91.7% |
| a large corporation's departments | 85.5% | 87.8% |
| a retailer's supply chain | 83.8% | 87.0% |
| a catalog of 1,000 agents | 85.5% | 89.2% |

Some of the questions are confusing enough that we would get them wrong ourselves.

Real people ask what they mean, in their own words. We expect search to do better on those
questions than on ours.

The fastest way to find out where yours sits is to put your own agents in and ask your own
questions.

---

## Where we go from here

We will be making constant improvement to search quality and speed.  