<!-- Source: html/search.html -->

<!-- Key: "Kicker:" is the small label above a heading. "> **Figure.**" gives the figure's description, then its visible labels, top to bottom; edit the wording, not the drawing. "> **Annotated code.**" is a code sample; its numbered notes are the callouts. -->

Title: Search — Search2o

Meta description: Users do not choose agents; they say what they need. Search reads a request written in plain language and returns the agent built to handle it, by meaning rather than by keywords.

---

Kicker: Search

# Users do not choose agents. They say what they need.

Search reads a request in plain language and returns the agent built to handle it. The exchange below is the same whether the bundled UI, a chat bot or your own interface makes it.

> **Annotated code.** A search call and its response, annotated

File: POST /api/exec/search

```jsonc
// the request
{ "query": "Book a trip to New York" }

// the response
{
  "success": true,
  "searchResults": [
    {
      "agentName": "travel_desk",
      "agentTitle": "Travel desk"
    }
  ]
}
```

Notes:

1. The user’s words, as typed. No agent name, no keyword, no menu.
2. Zero, one or two agents, best first. One when the request clearly belongs to it, two when the request is ambiguous or two descriptions overlap, none when nothing fits. Then nothing runs.
3. Search only matches. The interface calls `execAgent` with the agent name and the same request, at once or after offering the user the choice.

Search works from meaning, not words. A request and a description do not need to share a word or a language. A search takes about 200 milliseconds in Search2o Cloud, and a thousand agents are searched as quickly as a hundred.

## The description is what search matches against

When an agent is published, its developer describes it in plain language. Search indexes the description within half a minute. This is the description the request above matched.

> **Figure.** The description of the Travel desk agent
>
> - travel_desk · Travel desk
> - Arranges air travel and hotel stays for business travel. Books flights and hotel nights for the dates and the city the traveler names, holds a booking when the traveler is not ready to confirm, and answers questions about an existing booking. It does not file expenses and does not approve travel.

A description is written for the person who will type the request. It says what the agent does for the user: the questions it answers, the actions it takes, what it leaves to others. A typical description has two to five sentences. A description that names only the mechanism, such as “calls the travel API and summarizes the JSON”, matches poorly, because users do not ask for a mechanism; search returns it to the developer with an explanation of what to change. When two agents overlap by accident, a request in the shared territory returns both, and sharper descriptions separate them. See [describing an agent](docs/search/describing-an-agent.html).

[Tags](docs/search/tags.html) split an account’s agents into pools, one for the help desk and one for finance, and a search names a pool or searches them all.

Kicker: Live demo

## Ask for something, in your own words

The [search and conversation demo](demo-search.html) runs in a live Search2o account with 200 agents, from human resources and finance to engineering and sales. Ask for something, and the matched agent runs and answers with mock data.

Kicker: Search quality

## Measured on 15,000 questions, against the live service

Six catalogs of agents, from a university to a thousand agents across fifty business areas. 15,000 questions, each with a known right agent. Every question went through the production search service.

The right agent comes first 84% to 91% of the time, depending on the catalog, and is one of the first two 92% to 97% of the time. A request about something else entirely is always refused; a request about the customer’s own world that no agent covers is refused 82% to 86% of the time. A search takes about 200 milliseconds in Search2o Cloud. A catalog of a thousand agents scores within one percentage point of a catalog of a hundred. What separates the easy catalogs from the hard ones is how distinct their agents are, and the descriptions determine that. The [search quality](docs/search/search-quality.html) page has every table and the conditions behind each number.

## Where to read more

The [search](docs/search/index.html) section of the documentation covers [how matching behaves](docs/search/how-matching-works.html), [describing an agent](docs/search/describing-an-agent.html), [tags](docs/search/tags.html), [search behavior](docs/search/search-settings.html) and [search quality](docs/search/search-quality.html). The REST API’s [search call](docs/rest-api/search.html) is the search box as an API call.
