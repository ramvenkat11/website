<!-- Source: html/search.html -->

<!-- Key: "Kicker:" is the small label above a heading. "> **Figure.**" gives the figure's description, then its visible labels, top to bottom; edit the wording, not the drawing. "> **Annotated code.**" is a code sample; its numbered notes are the callouts. -->

Title: Search — Search2o

Meta description: Users do not choose agents; they say what they need. Search reads a request written in plain language and returns the agent built to handle it, based on meaning rather than keywords.

---

Kicker: Search

# Users do not choose agents. They say what they need.

Search reads a request in plain language and returns the agent built to handle it. The exchange below is the same whether it comes from the bundled UI, a chatbot, or your own interface.

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

1. The user’s words exactly as typed. No agent name, keyword, or menu.
2. Zero, one, or two agents, with the best match first. Search returns one when the request clearly belongs to a single agent, two when the request is ambiguous or two descriptions overlap, and none when nothing fits. If nothing fits, no agent runs.
3. Search only finds matches. The interface calls `execAgent` with the agent name and the same request, either immediately or after asking the user to choose.

Search works from meaning, not specific words. A request and a description do not need to share any words or even a language. A search takes about 200 milliseconds in Search2o Cloud, and searching a thousand agents is as fast as searching a hundred.

## The description is what search matches against

When an agent is published, its developer describes it in plain language. Search indexes the description within 30 seconds. The request above matched this description.

> **Figure.** The description of the Travel desk agent
>
> - travel_desk · Travel desk
> - Arranges air travel and hotel stays for business travel. Books flights and hotel nights for the dates and the city the traveler names, holds a booking when the traveler is not ready to confirm, and answers questions about an existing booking. It does not file expenses and does not approve travel.

A description is written for the person who will type the request. It explains what the agent does for the user: the questions it answers, the actions it takes, and what it leaves to other agents. A typical description is two to five sentences long. A description that names only the mechanism, such as “calls the travel API and summarizes the JSON,” matches poorly because users do not ask for a mechanism. Search returns it to the developer with an explanation of what to change. When two agents accidentally overlap, a request in their shared area returns both. More precise descriptions separate them. See [describing an agent](docs/search/describing-an-agent.html).

[Tags](docs/search/tags.html) divide an account’s agents into pools, such as one for the help desk and another for finance. A search can name one pool or search all of them.

Kicker: Live demo

## Ask for something, in your own words

The [search and conversation demo](demo-search.html) runs in a live Search2o account with 200 agents, from human resources and finance to engineering and sales. Ask for something, and the matched agent runs and answers with mock data.

Kicker: Search quality

## Measured on 15,000 questions, against the live service

The test used six agent catalogs, ranging from a university catalog to one with a thousand agents across fifty business areas. It included 15,000 questions, each with a known correct agent. Every question went through the production search service.

The correct agent ranks first 84% to 91% of the time, depending on the catalog, and appears in the first two results 92% to 97% of the time. A request about something completely unrelated is always refused. A request related to the customer’s enterprise that no agent covers is refused 82% to 86% of the time. A search takes about 200 milliseconds in Search2o Cloud. A catalog of a thousand agents scores within one percentage point of a catalog of a hundred. The difference between easy and difficult catalogs is how distinct their agents are, which depends on their descriptions. The [search quality](docs/search/search-quality.html) page includes every table and the conditions behind each number.

## Where to read more

The [search](docs/search/index.html) section of the documentation covers [how matching works](docs/search/how-matching-works.html), [describing an agent](docs/search/describing-an-agent.html), [tags](docs/search/tags.html), [search behavior](docs/search/search-settings.html), and [search quality](docs/search/search-quality.html). The REST API’s [search call](docs/rest-api/search.html) provides the search box as an API call.
