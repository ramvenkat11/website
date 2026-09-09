# How good is Search2o's search?

**Source material for a web page. This is not the page itself.** It carries every number we
have measured, in general terms, plus explicit guidance on what may and may not be published.
A section at the end lists the claims that are safe to make and the details that must stay
internal.

Everything here was measured against the live search index, running the production code with
the settings it ships with. Nothing is simulated, modelled or extrapolated.

---

## 1. The one-line answer

A user types a question. Search2o finds the agent that answers it, and either runs the single
best match or offers the two or three that are plausible. If nothing fits, it says so rather
than guessing.

**When agent descriptions do not overlap and the question is unambiguous, the right agent is
found more than 99% of the time.** When descriptions genuinely overlap, search offers the
handful of candidates instead of pretending to be certain.

---

## 2. The thing that decides accuracy is OVERLAP, not catalogue size

This is the single most important idea for the page, because it reframes every number below.

If two agents cover the same ground — an "escalations" agent and an "incident triage" agent, a
"contract review" agent and a "renewal manager" — then a question like *"who signs off on
this?"* genuinely belongs to both. No search engine can be certain, because the ambiguity is in
the catalogue, not in the search. What good search does there is offer both.

We measured this directly. Two catalogues of the **same size** — 50 agents each — scored
**99.2%** and **83.8%** top-1 accuracy. The only difference was how far apart the agents'
subject matter sat. Fifteen points of accuracy came from catalogue design, not from search.

So the honest headline is conditional, and the condition is one the customer controls.

---

## 3. Headline results

### 3a. A well-separated catalogue: better than 99%

50 agents, each from a different industry — deliberately non-overlapping in subject, not merely
in wording. 500 questions.

| | |
|---|---|
| Right agent is the single top match | **99.2%** |
| Right agent is in the results shown | **99.6%** |
| Searches that return exactly one result | **95–98%** |
| Wrong single answers | **1 in 500 searches** |

**This is the number to quote for a focused catalogue**, and it is what most customers who
describe their agents carefully should expect.

### 3b. Deliberately overlapping catalogues: our hardest test material

Pooled across six test catalogues, 1,418 agents and **15,180 questions**. These catalogues were
built to be hard — several are stuffed with near-synonym agent pairs on purpose, so that we
measure the difficult case rather than the flattering one.

| | |
|---|---|
| Right agent is the single top match | **86%** |
| Right agent is in the results shown | **94.3%** |
| Searches that return exactly one result | **58%** |
| Searches that return a confident but wrong single answer | **0.77%** |
| Searches that return nothing when something was available | **0.14%** |

Read the last two lines together with the first: even on our hardest material, fewer than one
search in a hundred gives a confidently wrong single answer.

**These pooled figures describe our test set, not a typical deployment.** Per catalogue, the
share of searches answered with a single result ranges from 52% to 79% — the well-separated
ones sit at the top of that range, the near-synonym ones at the bottom.

---

## 4. Scale: tested at 40, 100 and 1,000 agents

| catalogue size | questions | top match is correct | right agent is in the results shown |
|---|---|---|---|
| 40 agents | 400 | 94.0% | 98.2% |
| 100 agents | 1,000 and 2,000 | 85.8% – 86.5% | 94.3% – 95.4% |
| 1,000 agents | 10,000 | 85.8% | 93.6% |

The 1,000-agent test is the one worth describing in detail, because it is the one people doubt:

- **Every one of the 1,000 agents was queried** — ten questions each, 10,000 questions in
  total. This is not a sample of the easy ones.
- **367 of the 1,000 agents answered all ten of their questions correctly.**
- **Not one agent failed all ten.** There is no agent in a thousand that cannot be found.
- The worst agents scored 2 of 10, and every one of them was half of a near-synonym pair.

**Going from 100 to 1,000 agents cost essentially nothing** — 86% top-1 at both. That is the
result that matters for anyone planning a large catalogue, and it is why point 2 above is the
real story: accuracy tracks how distinct the agents are, not how many there are.

We also measured size on its own, holding subject separation roughly constant, at 50, 100 and
200 agents: top-1 went 83.8% → 83.3% → 79.5%, and "within the top three" went 97.2% → 95.7% →
92.7%. A four-fold increase in catalogue size costs a few points. Adding a near-duplicate agent
costs more.

---

## 5. One, two or three results — and sometimes none

Search2o decides how many results to show from how close the candidates are:

- **The scores are far apart** → one result, and the agent runs.
- **Two are close** → both are offered.
- **Three are close** → all three.
- **Nothing is close enough to the question** → no results, rather than a wrong answer.

Never more than three. This is what turns ambiguity from an error into a choice: on our hardest
material the right agent is in the offered set 95% of the time, against 86% if we always
insisted on a single answer.

The behaviour is tunable, and the trade is worth stating plainly. Showing one result more often
means being confidently wrong more often. Measured over 15,180 questions:

| how often one result is shown | right agent is in the results | confidently wrong |
|---|---|---|
| 88% | 90.2% | 7.2% |
| 78% | 92.4% | 3.6% |
| 69% | 93.6% | 1.8% |
| **58% (shipped)** | **94.3%** | **0.77%** |
| 42% | 94.7% | 0.23% |

We ship the setting that keeps confidently-wrong answers under 1%. On a well-separated
catalogue this dial stops mattering at all — every setting in the range behaves the same,
because the best candidate is nearly always far ahead of the second.

---

## 6. Refusing questions that nothing covers

A search engine that always answers is easy to embarrass. We measured this separately, because
the accuracy tests only ever asked questions that *did* have an answer.

Against questions with no covering agent at all — general knowledge, other domains, unrelated
subjects — **100% are refused in every language tested**, and 99.6% across a larger
English-only set. The cost is **under 0.5% of genuine questions** wrongly turned away.

There is a middle category that is deliberately handled the other way: questions that sit
*beside* the catalogue's territory without being covered by it. Roughly a third to two thirds
of those are refused, and the rest get an answer. That is a chosen bias — showing a plausible
neighbouring agent is better for a user than a blank refusal, whereas answering "what is the
capital of France" from a payments catalogue is not.

---

## 7. Languages

Tested in **Spanish, German, French, Mandarin and Japanese**, at the 40-agent level, 400
questions per language. Agent descriptions were translated; the search code and settings were
identical.

**Descriptions and questions in the same language:**

| language | top match is correct | right agent is within the top three |
|---|---|---|
| English | 94.0% | 98.2% |
| Spanish | 92.8% | 98.2% |
| German | 92.5% | 98.0% |
| French | 92.0% | 98.0% |
| Mandarin | 91.8% | 98.2% |
| Japanese | 91.2% | 98.2% |

**"Within the top three" is flat at 98% in all six languages.** The right agent is
found just as reliably whatever the language; the small differences are only in how often it is
confident enough to answer with one result. Part of even that gap is method rather than
capability — the English text is the original and the others are translations of it.

**Descriptions in one language, questions in another** — ten pairs, 400 questions each:

| | top match is correct | right agent is within the top three |
|---|---|---|
| across all ten language pairs | 88.2% – 90.8% | 92.0% – 97.5% |

Cross-language search works. A German description answers a French question; a Mandarin
description answers a Japanese one. The cost is about three points against staying in one
language. Notably, **Mandarin ↔ Japanese was the strongest pair of all (97.5% / 97.0%)** —
different scripts with no shared vocabulary, so this is genuine understanding of meaning rather
than word matching.

The no-match behaviour also transfers: 100% of unrelated questions refused in every language,
and **zero genuine questions wrongly refused in any of the five non-English ones**.

---

## 8. Speed and capacity

A search is **one request to the search service**. The question is turned into a vector inside
the database, next to the data, so nothing large crosses the network and there is no second
round trip.

| | |
|---|---|
| Server-side time, catalogues up to ~120 agents | **~70–130 ms** |
| Server-side time, 1,000-agent catalogue | **~400 ms** |
| Typical end-to-end from a browser at low load | **~230–260 ms** (median), under 600 ms at the 95th percentile |
| Throughput | scales linearly with provisioned capacity |

**Caution for the page: the "responds within 300 ms" claim on the current home page holds at
the 100-agent scale and does NOT hold at 1,000 agents**, where a search takes around 400 ms.
Either qualify the claim by catalogue size or use a looser phrase such as "typically under half
a second".

Latency is flat right up to the capacity limit and then degrades sharply — there is no gradual
slowdown to warn you — so capacity is provisioned to the expected rate rather than to the
average.

---

## 9. Why these numbers are believable

Worth a short section on the page, because accuracy claims are cheap and method is what makes
them credible.

- **Measured against the live system.** Every figure comes from the real search index and the
  production code with its shipped settings. We previously used a faster offline approximation
  and it was wrong by 14 points at the 1,000-agent scale, so we deleted it and adopted a rule:
  no accuracy number that was not measured live.
- **More than 20,000 labelled questions**, each with a known correct answer, across catalogues
  from 40 to 1,000 agents.
- **Settings were tuned on two catalogues and judged on four others they had never seen.** The
  tuned settings were then applied unchanged to a catalogue ten times larger, with no
  re-tuning, and held up.
- **Ideas that did not survive were dropped.** A cleverer rule for deciding when to show one
  result looked 7 points better on the data it was fitted to and vanished on held-out data; it
  was not shipped. Several other candidate signals were measured and rejected the same way.
- **The test catalogues are adversarially hard on purpose.** Some are packed with near-synonym
  agent pairs precisely so we measure the difficult case. The pooled figures are close to a
  worst case, not a typical one.

---

## 10. What we can say — and how to phrase it

**Safe claims, in the words to use:**

- "When your agents describe different things and the question is clear, Search2o finds the
  right one **more than 99% of the time**."
- "Tested at **40, 100 and 1,000 agents**, with more than 20,000 real questions."
- "At 1,000 agents, every agent was tested and **none was unfindable**."
- "Going from 100 to 1,000 agents costs almost nothing. What costs accuracy is two agents that
  do the same thing."
- "Where two agents genuinely overlap, Search2o offers both rather than guessing — and the
  right agent is among the results **94% of the time even on our hardest test catalogues**."
- "If nothing matches, Search2o says so. **Unrelated questions are refused essentially every
  time** — 100% in our multi-language test, 99.6% across a larger English set."
- "Works in **English, Spanish, German, French, Mandarin and Japanese**, including a question
  in one language against agents described in another."
- "Fewer than **1 in 100** searches returns a confident but wrong single answer, on our hardest
  material."

**Framing advice:**

- Lead with the conditional 99%, then explain the condition — it puts the customer in control
  rather than sounding like a hedge.
- Describe overlap with a concrete example (two agents that both handle "escalations"). It is
  immediately obvious and it makes the ambiguity feel like the catalogue's property, which it
  is.
- The 1,000-agent result is the credibility anchor. "Every agent tested, none unfindable" is
  worth more than any percentage.
- Do not present the pooled 86% as *the* accuracy figure without saying it comes from
  deliberately hard catalogues. It understates what a careful customer will see.

---

## 11. What must NOT be published

- **No corpus names.** Never "campus", "bigcorp", "wide1000", "heir", "clinic", "retail".
  Say "a 40-agent catalogue", "a 1,000-agent catalogue", "six test catalogues".
- **No internal settings or thresholds.** No distance values, no weights, no parameter names.
  Describe behaviour, never the dial.
- **No technology or vendor names** — not the embedding model, not the database, not the cloud
  provider. What search does is publishable; how it does it is not.
- **No per-agent or per-domain breakdowns** that would let the test data be reconstructed.
- **Nothing about the test data being machine-generated** beyond the honest caveat below, if it
  is mentioned at all.

---

## 12. Caveats to keep us honest

If a sceptical reader asks, these are true and we should not pretend otherwise:

- The test catalogues and questions were generated rather than collected from live customers.
  They were built to be hard, and the questions for the largest catalogue were written without
  reference to the agent descriptions, so they are not tuned to flatter us — but they are not
  production traffic.
- The "better than 99%" case is a **constructed** well-separated catalogue: 50 agents from 50
  different industries. It is a fair model of a focused deployment and it is not an average of
  our test material.
- Non-English results come from translated descriptions in one 40-agent catalogue, not from
  natively authored catalogues at every size.
- English is the strictest language on the no-match behaviour: it refuses the most borderline
  questions and is the only language that wrongly refuses any genuine ones (0.5%).
- Accuracy figures assume the agent has been indexed and its description has been accepted.
  A description that says only how an agent works, rather than what it does for a user, is
  rejected at publish time and never reaches search.
