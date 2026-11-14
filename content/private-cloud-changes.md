# Adding the private cloud to the docs and the website

Written 2026-11-13, updated the same day after the easy changes were made. Line numbers are those of the source
files on that date.

## Where things stand

The home page says the agent server uses Search2o Cloud **or** the organization's private cloud. This document
tracks bringing the rest of the website and the docs in line.

I searched the 147 docs source pages in `docsrc/`, the 14 site pages in `html/`, the 4 legal pages in
`html/legal/`, and the generators in `gen/`.

| Part | What it is | Entries | Status |
|---|---|---|---|
| A | Easy changes | 31 edits in 24 files | **Done.** Review the wording |
| B | Needs a fact or a decision from you | 22 places | **Waiting for you** |
| C | More complicated: legal text, figures, another project, a new page | 14 places | **Not started** |
| D | No change needed | about 85 | Nothing to do |

Nothing has been uploaded. The docs were rebuilt after part A: 27 built pages changed, and every changed line is one
of the edits listed below.

## The three terms used in part A

Part A was written with these terms. If you want different ones, tell me and I will change all 31 edits to match.

- **Search2o Cloud**: the cloud service hosted by Search2o.
- **Private cloud**: the same cloud service, hosted in the organization's own cloud account.
- **The cloud**: whichever of the two the account uses.

The docs already wrote "the cloud" about 60 times as shorthand. Those stay correct without an edit.

---

## Part A: done

### A1. The definition, in one place

`docsrc/introduction/parts-of-the-system.html`

- Line 47, heading: "Search2o Cloud" → "**The cloud service**". The heading's anchor changes from `#search2o-cloud`
  to `#the-cloud-service`. No page in the docs or the site linked to the old anchor.
- Line 48, new paragraph at the top of that section: "**The cloud service runs as Search2o Cloud, hosted by
  Search2o, or as a private cloud, hosted in your own cloud account. The rest of the docs call either one "the
  cloud".**"

This is the only sentence in the docs that mentions the private cloud so far. Everything else in part A relies on
it.

### A2. "Search2o Cloud" → "the cloud", where the sentence is true for either cloud

Only the name changed. "The cloud" is capitalised at the start of a sentence.

| File and line | Now reads |
|---|---|
| `docsrc/agent-definition/const.html:31` | …before it leaves for the cloud, the same way it encrypts an agent's description. |
| `docsrc/agent-definition/namespaces.html:4` | The object is encrypted on its way to and from the cloud, which never reads it. |
| `docsrc/agent-definition/python-expressions.html:40` | The cloud reads each expression and refuses the agent if… |
| `docsrc/agent-execution/conversation-state.html:1` | …the conversation state is encrypted and stored in the cloud, or handed to your own code… |
| `docsrc/agent-execution/error-handling.html:63` | …a stop by the person, and an error from the cloud. |
| `docsrc/commands/log.html:1` | Logs stay in your environment and are never sent to the cloud. |
| `docsrc/commands/memory.html:30` | …makes a round trip to the cloud, where memories are kept and searched. |
| `docsrc/development/publishing.html:15` | The cloud produces a merged definition from the draft and the new version… |
| `docsrc/development/trace-and-validation.html:1` | …it must validate: the cloud checks the definition, and the agent server runs it… |
| `docsrc/hooks/conversation-state.html:1` | …and stores the ciphertext in the cloud. |
| `docsrc/hooks/conversation-state.html:9` | The cloud does not check who continues a conversation whose state your code holds… |
| `docsrc/introduction/how-it-fits-together.html:7` | The cloud checks the definition and every Python expression in it. |
| `docsrc/reports/index.html:14` | The agent server could not complete a call to the cloud during the run. |
| `docsrc/rest-api/automating-with-an-llm.html:25` | …the cloud checks it against the role, records it against the service account… |
| `docsrc/rest-api/overview.html:15` | The cloud checks the role on every call. |
| `docsrc/runtime/compile-rules.html:1` | The cloud applies the rules when a draft is validated or published. |
| `docsrc/runtime/connection-pools.html:1` | …the calls to the cloud, the LLM calls, and the calls made by api commands… |
| `docsrc/runtime/controlled-execution.html:8` | The cloud checks every expression when the agent is validated… |
| `docsrc/runtime/controlled-execution.html:29` | The cloud receives the search request and the conversation state… |
| `docsrc/runtime/overview.html:18` | The cloud stores the change, stamped with the time. |
| `docsrc/security/secret-vault.html:4` | Agent definitions, prompts and profiles are stored in the cloud in plain form… |
| `docsrc/skill-integration/what-search2o-provides.html:84` | Requests pass through the cloud. |
| `docsrc/skill-integration/what-search2o-provides.html:85` | Definitions and state are stored in the cloud. |
| `docsrc/system-management/agent-server-sizing.html:30` | The cloud pool is the one the agent server uses to reach the cloud… |
| `docsrc/system-management/agent-server-sizing.html:33` | …conversation state is saved to the cloud rather than accumulated in the process. |
| `docsrc/system-management/agent-server-sizing.html:36` | Heading: "Putting the agent server near the cloud". Its anchor changes with it; nothing linked to the old one. |
| `docsrc/system-management/single-sign-on.html:51` | The exchange with your identity provider happens in the cloud; your agent server never holds the secret… |
| `html/runtime.html:169` | The cloud stores it with a timestamp. |
| `html/runtime.html:190` | The cloud receives the search request and conversation state… |

### A3. Done earlier the same day, on the home page

- `html/index.html:185` — the section 4 subtitle: "The agent server is stateless and uses the cloud for state, search
  and reports."
- `html/index.html:215` — the figure's cloud box names both: "Search2o Cloud OR Your private cloud".
- `html/index.html:188` — the figure's description for screen readers says "Search2o Cloud or to your private
  cloud".

### A4. Rebuilt pages

`python3 gen/build.py` rebuilt the docs. 27 pages under `html/docs/` changed: the 23 docs pages above, plus four
index pages that repeat an opening sentence (`agent-execution/index.html`, `development/index.html`,
`hooks/index.html`, `runtime/index.html`).

---

## Part B: waiting for you

Each of these states a fact about Search2o's hosted service. Swapping the name would make the sentence wrong or
unverified for a private cloud, so I left them all unchanged.

### The seven questions

1. How does an agent server point at a private cloud? The license text names a setting, `SEARCH2O_CLOUD_URL`. Is
   that the one?
2. Where is the account registered and the license key checked when the cloud is private?
3. Which cloud platforms can host a private cloud? Search2o Cloud runs on Google Cloud Platform.
4. Who holds the per-account encryption key when `encryptionSource` is `cloud` and the cloud is private?
5. Is the 200 ms search time a claim for Search2o Cloud only, or also a target for a private cloud?
6. What does a private cloud cost, and is it part of the beta?
7. Does any data go to Search2o when the cloud is private (license checks, usage counts)?

### B1. "Nothing to host" [your call on the wording]

- `docsrc/introduction/what-is-search2o.html:13` — "**Nothing to host for state.** The agent server holds no state.
  Everything is stored in Search2o Cloud, so agent servers can be started, stopped and scaled freely." With a private
  cloud the organization does host the state. The bullet's title needs your wording, not just a name swap.

### B2. Search speed [question 5]

- `docsrc/search/how-matching-works.html:1` — "A search takes about 200 milliseconds in Search2o Cloud…"
- `docsrc/search/search-quality.html:54` — "…in about 200 milliseconds in Search2o Cloud."
- `docsrc/skill-integration/what-search2o-provides.html:21` — "…in about 200 milliseconds in Search2o Cloud, with no
  model call."
- `html/search.html:90` and `html/search.html:130` — "A search takes about 200 milliseconds in Search2o Cloud…"

These five are accurate as written, because they name the cloud the figure was measured on. If the answer is
"Search2o Cloud only", leave them and add one sentence on the search quality page that a private cloud's speed
depends on how it is sized.

### B3. Region and hosting [question 3]

- `docsrc/search/search-quality.html:54` — "Search2o Cloud is served from the US East region today…" Keep, and add
  that a private cloud runs in the region the organization chooses.
- `docsrc/support-licensing/license.html:14` — "Search2o Cloud currently operates from the US East region…" Same.
- `docsrc/system-management/agent-server-sizing.html:37` — "Every agent run makes three requests to Search2o Cloud,
  which is 0.17s of the 0.28s…" The request count holds for both; the timing was measured against Search2o Cloud.
- `docsrc/security/data-privacy.html:40` — "Search2o Cloud runs on Google Cloud Platform." Keep, and add what a
  private cloud runs on.

### B4. Who operates it and who can read the data [question 7]

- `docsrc/support-licensing/license.html:13` — "Search2o operates Search2o Cloud." Keep, and add that the
  organization operates its private cloud.
- `docsrc/support-licensing/license.html:13` — "Only the agent server uses the cloud's API; the license prohibits
  calling the API directly." Confirm this also holds for a private cloud.
- `docsrc/security/data-privacy.html:1` to `:25` — the whole page answers "what leaves your organization and who can
  read it". With a private cloud the data leaves the agent server but stays in the organization's own account. The
  page needs a short section saying so, and its "Who can read it" column needs a check.

### B5. Encryption keys [question 4]

- `docsrc/security/encryption.html:6` — "With encryptionSource set to cloud, Search2o keeps one key per account in a
  key management service." With a private cloud, say who keeps the key.

### B6. Account, registration and license [questions 1 and 2]

- `docsrc/getting-started/registering-and-downloading.html:4` — "The key connects an agent server to your account in
  Search2o Cloud…"
- `docsrc/getting-started/running-the-server.html:23` — "At startup the server validates the license and downloads
  the account's configuration from Search2o Cloud."
- `docsrc/security/license-rotation.html:1` — "Every request an agent server makes to Search2o Cloud carries the
  key…"

The getting started pages describe the Search2o Cloud path. The simplest edit is to leave them as that path and link
from each to the private cloud page, once it exists.

### B7. Pricing [question 6]

- `html/pricing.html:7` and `:9` — the page description: "Search2o Cloud is free during beta and becomes a paid
  service at general availability."
- `html/pricing.html:60` — the figure's description: "An encrypted link connects it to Search2o Cloud, which keeps
  the state and is free during the beta."
- `html/pricing.html:76` — the figure's label "Search2o Cloud".
- `html/pricing.html:92` — the heading "Search2o Cloud is free during beta".
- `html/pricing.html:93` — "The agent server stores state in Search2o Cloud. The cloud service is in beta and free
  to use."

These are true for Search2o Cloud. The page says nothing about a private cloud, so a reader who saw it on the home
page will look for its price here.

---

## Part C: more complicated

### C1. The license forbids it as written [counsel]

- `html/legal/license.html:108`, section 4(f) — forbids running the software with `SEARCH2O_CLOUD_URL` set to
  anything other than a Search2o-authorized endpoint on search2o.com or a domain Search2o designates. **As written,
  this prohibits pointing an agent server at a private cloud** unless Search2o designates that endpoint in writing.
  This is the most important item in this document.
- `html/legal/license.html:119` — explains that 4(f) applies to the Search2o Cloud endpoint. Changes with 4(f).
- `html/legal/license.html:78` to `:81` — the definitions of "Search2o Cloud", "Search2o Cloud APIs",
  "Search2o-Controlled Systems" and "Search2o Services" all mean systems operated by or for Search2o. A private cloud
  is operated by the customer, so it is none of these, and the license has no term for it.
- `html/legal/license.html:107`, section 4(e) — forbids calling the Search2o Cloud APIs directly. Decide whether the
  same applies to a private cloud's APIs.
- `html/legal/license.html:110`, section 4(h) — forbids building a substitute for Search2o Cloud. Decide how a
  licensed private cloud relates to this.
- `html/legal/terms.html:64`, `:78`, `:146`, `:155` — the Terms govern "Search2o's cloud services". A private cloud
  is software the customer runs, so it likely needs license terms of its own.
- `html/legal/privacy.html:107` — "Those communications originate from the customer's agent server rather than
  Search2o Cloud." Still true; check it once question 7 is answered.

I have not proposed wording for any legal text.

### C2. Figures [a drawing change, and your choice of label]

Changing these is a visual change that needs rendering and checking, and the label is a design choice: "The cloud",
or both names as on the home page.

- `gen/figures.py:154` — the docs architecture figure draws a box "Search2o Cloud" with "search · state · reports".
  The box is 200 wide, so both names do not fit on one line.
- `gen/figures.py:254` — the configuration sync figure draws a box "Search2o Cloud" with "stores it, stamps the
  time".
- `docsrc/introduction/parts-of-the-system.html:40` — the label "Search2o Cloud" inside that page's figure.
- `docsrc/introduction/parts-of-the-system.html:4` — the same figure's description for screen readers: "…an
  encrypted link connects them to Search2o Cloud, which keeps the conversations and memories…"
- `html/pricing.html:76` — the pricing figure's label (also listed under B7).

### C3. Text generated from the s2oserver project [another project]

These sentences appear in the built docs but come from `../s2oserver/models/systemconfig.py`. **They belong to the
s2oserver project and cannot be changed from the website repository.** Change them there, then rebuild the docs
here.

- `html/docs/system-management/agent-servers.html` — "How this agent server connects to Search2o Cloud." and "…so
  nothing configured for an agent can change how this server reaches Search2o Cloud."
- `html/docs/hooks/overview.html` — "…ownership is not checked by Search2o Cloud." and "Validation runs keep their
  state in Search2o Cloud."

### C4. A page that does not exist yet [new writing]

- A docs page for the private cloud: what it is, what it runs on, how to point an agent server at it. You said you
  will write this.
- Until it exists, "Your private cloud" in the home page figure has no link, and the definition sentence in A1 has
  nothing to point to.

---

## Part D: no change needed

- About 60 uses of "the cloud" across the docs, for example "The cloud stores and returns only the encrypted value"
  (`docsrc/agent-definition/const.html:31`).
- Setting names and values: `cloudPool` and "the cloud connection pool" (`docsrc/gui/operations.html:4`,
  `docsrc/system-management/agent-server-sizing.html:29`), and the `encryptionSource` value `cloud`
  (`docsrc/security/encryption.html:6`, `:22`). These are identifiers.
- Other meanings of the word: "Google Cloud console" (`docsrc/system-management/single-sign-on.html:36`), "cloud
  systems" in the founder's line (`html/about.html:75`), "cloud hosting and infrastructure"
  (`html/legal/privacy.html:111`).
- `html/about.html:70` — "A hybrid cloud architecture… Encryption protects sensitive information in the cloud." True
  for both.
- `html/conversation.html:134` — "…the cloud never decrypts it. An account can keep the state in its own enterprise
  instead of storing it in the cloud." True for both.
- The social card and the LinkedIn banner do not mention the cloud.

## Suggested order for what is left

1. Resolve license section 4(f) with counsel (C1), since it decides whether the feature can be offered as described.
2. Answer the seven questions in part B.
3. Write the private cloud docs page (C4).
4. I make the part B edits as each answer arrives, and update `html/pricing.html`.
5. Choose the figure label (C2); I redraw and check the figures.
6. Ask the s2oserver session to change the strings in `models/systemconfig.py` (C3), then rebuild the docs here.
