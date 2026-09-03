# Using Search2o from Slack, Teams and Google Chat

This page describes how to let people use Search2o agents from a chat application. A small
program, usually called a bot, sits between the chat application and the agent server. The
person types a question in a chat thread. The bot finds the right agent, runs it, and posts
the answer back in that thread.

Search2o does not ship a bot. A company writes its own. Everything a bot needs is in the API
today, including the part that lets a person connect their Search2o account to the chat
application without handing over a password.

This page describes what the bot has to do and which calls it makes. The last section gives
prompts you can paste into an AI assistant to have most of the bot written for you.

## What the bot does

A chat integration needs four things.

It authenticates as the person who is chatting. Every call the bot makes is made as that
person, so their conversations, their memories and their usage are their own.

It finds an agent for each question, using search.

It runs the agent and posts the answer.

It keeps the chat thread and the Search2o conversation together, so that a follow-up question
in the same thread continues the same conversation.

## Connecting a person to the bot

The bot acts as a person, so it needs a token for that person. A token is created by the
person themselves. Their password is never given to the bot.

There are two ways to do this. Both produce the same kind of token.

### Pasting a token

The person signs in to the GUI and creates an integration token. The GUI shows the token once.
They copy it into the bot, usually with a slash command in a private message.

This is simple and needs nothing from the bot beyond a place to store the token. It suits a
small team. It is not suitable for a large one, because a token pasted into a public chat
message stays in that workspace's history.

### The connect flow

The bot sends the person a button. The button opens a page on the agent server. The person
signs in if they are not signed in already, approves the request, and returns to the chat
application. The bot collects the token by itself. Nothing is copied by hand.

The calls are:

1. The bot calls `startConnect` with a name to display, such as the name of the chat
   workspace. The call returns an identifier, a secret, a short code and an address.
2. The bot posts a button pointing at that address, and shows the short code beside it.
3. The person opens the page. The page shows what is asking for access and the same short
   code. The person checks that the two codes match before approving.
4. The person approves. A token is created for them.
5. The bot calls `getConnectToken` with the identifier and the secret until the answer says
   the request was approved. The token is returned once.

The short code is what protects the person. A link on its own is not enough to get a request
approved, because a request started by somebody else displays a code the person has never
seen. Tell people to compare the two codes. Do not let the bot display a code it did not get
from `startConnect`.

The secret from step 1 belongs to the bot. It must never be shown to the person or put in a
link.

The address comes from a setting on the agent server. Leave it empty when the agent server serves
the GUI, and the address follows wherever the GUI is served. Set a page for a GUI of your own, or
a full address for a GUI hosted somewhere else. The agent server does not have to serve the GUI at
all, and the GUI is a set of static pages that can be hosted anywhere, so a GUI hosted elsewhere
needs its address set here.

The agent server adds the request to whatever address is set, as a query parameter. A page that
reads that parameter works whichever way the GUI is built.

The address a bot receives is therefore either a full address or a path. Use a full address as
it is. Join a path to the address of the agent server.

## What an integration token can do

An integration token acts as its owner, limited to what any user may do. It can search, run
agents, and manage that person's own conversations. It cannot read or change configuration,
manage users, or read reports, whatever role its owner has.

A token can be created without an expiry, if the account allows it. Otherwise it expires after
a period the account sets.

## Managing tokens

A person sees their own tokens in the GUI. Each one shows the name they gave it, when it was
created and when it was last used. The last-used date is what tells a live integration from
one that was set up and forgotten.

A person can revoke any of their own tokens. Revoking one stops that token immediately and
affects nothing else, including their own sign-in.

A person may hold a limited number of tokens. Ten is the usual limit.

Two other events end a token. Resetting a password revokes that person's tokens, because
account recovery exists to remove credentials that somebody else may hold. Deleting a person
ends their tokens with their account.

## Finding an agent

The bot calls `search` with the person's question. The call returns up to three agents, and
two values that tell the bot what to do with them.

`searchBehavior` says whether to run the best match, run the only match, or show the list and
let the person choose. `followupBehavior` says the same for a question asked inside an
existing conversation, and can also say to continue with the agent already in use.

When the search returns nothing, no agent covers that question. Say so. There is no directory
of agents for end users, and none is needed. People ask, and the answer tells them whether an
agent exists.

A question must be at least eight characters. Treat a shorter one as a greeting rather than
showing the error.

## Letting the person choose

When the behaviour says to show the results, show them as buttons. One button per agent,
labelled with the agent title. Search returns at most three, so they fit in a single row.

Four things make a picker work properly.

Carry the question, not only the choice. Running an agent needs the question, and a click only
says which agent. Put a short identifier in the button and keep the question in your own store.
A chat application limits how much a button can carry, and a question can be longer than that.

Replace the message once somebody has chosen. Otherwise the buttons stay live, and a second
click starts a second conversation on the same question. Show which agent was chosen instead.

Accept the click only from the person who asked. In a channel anybody can click. A click from
somebody else would run that question under their account and put it in their history.

Let the behaviour decide whether to show a picker at all. Do not invent a rule of your own.

## Running an agent

The bot calls `execAgent` with the agent name and the person's question.

Leave the conversation identifier out to start a new conversation. The response carries the
new identifier. Pass that identifier on every later call to continue the same conversation.

The response also carries a result code that says how the run ended. A bot needs to handle
four cases. The run finished. The agent is asking for more input. The conversation is no
longer known, so start a new one. Anything else is a failure to report to the person.

## Threads and conversations

A chat application identifies a thread in its own way. Slack uses a workspace, a channel and
the timestamp of the first message. Teams and Google Chat each have their own identifiers.

The bot keeps its own record of which thread belongs to which Search2o conversation. It writes
the record when a conversation is created and reads it on every later message in that thread.

Conversations expire. When a stored identifier is no longer known, the response says so.
Start a new conversation and carry on. Do not treat it as an error.

## When an agent asks a question

An agent can pause and ask the person for input. The response then carries the message to show
and the list of inputs to collect. Each input has a type: a line of text, a password, a longer
block of text, a choice of one, or a choice of several. Every chat application can render all
five in a form.

Collect the answers and call `execAgent` again, with the same conversation identifier and the
answers as inputs. The agent continues from where it paused.

Slack needs one extra step. A form there can only be opened in response to a click, and the
answer arrives while the bot is replying to a message. So post a message with an Answer button,
and open the form when that button is pressed.

An input marked as hidden is not shown to the person. Send it back unchanged.

## Showing the answer

An answer is a list of parts. A part is text, HTML or an image.

Text is written as Markdown. Every chat application uses its own dialect, so convert it. Slack
and Google Chat need bold and links rewritten. Teams accepts a wider subset.

An image arrives as data, with its type. Upload it using the chat application's own file API.

HTML has no equivalent in any of the three chat applications. Convert it to text, or tell the
person the answer is available in the GUI. Agents written for a chat audience should produce
text and images.

## Slow answers

Every chat application expects the app to acknowledge an event quickly. Slack allows about
three seconds. Microsoft Teams allows longer, and Google Chat longer still. Check the current
figure for the one you are building against, because each vendor changes it.

Do not build against the figure. An agent that calls a model usually answers in about five
seconds, and sometimes takes a minute or more. No window covers that.

So the pattern is the same on all three. Acknowledge the event at once. Post a short message
saying the answer is coming. Post or edit the real answer when it arrives.

Each application has its own way to send that later message. In Slack, post a message and
edit it with `chat.update`. In Teams, keep the conversation reference and send a proactive
message, or update the activity. In Google Chat, create a message in the space with the Chat
API. All three also have a typing or progress indicator worth using while the person waits.

When a conversation turns out to have expired, the bot starts a new one and runs the question
again. Reuse the message already posted rather than posting another. Otherwise the person sees
two messages saying an answer is coming, for one question.

The agent server can stream progress while an agent runs, and a bot can use it to update the
placeholder message. Do not close a stream that has not finished. Closing it stops the agent.

## Notes for each chat application

### Slack

Use Socket Mode where possible. The bot then needs only outgoing connections, so it can run
inside a private network beside the agent server, with nothing exposed to the internet. This
matters when the agent server is not reachable from outside the company.

Verify Slack's request signature on every event.

Post answers in a thread, so that a conversation in Search2o matches a thread in Slack.

The connect flow uses an ordinary link button. Slack has no masked input, so never collect a
password or a token in a Slack form.

### Microsoft Teams

Teams bots are registered in Azure and receive events over HTTPS. The bot needs a public
endpoint, or a tunnel into the company network.

Use Adaptive Cards for the connect button and for the input form when an agent asks a question.

Teams identifies a conversation and a reply chain. Use both to key the record of which thread
belongs to which Search2o conversation.

### Google Chat

A Google Chat app receives events over HTTPS or through Pub/Sub. Pub/Sub suits a bot inside a
private network, for the same reason as Socket Mode in Slack.

Use card messages for the connect button and for input forms.

Google Chat identifies a space and a thread. Key the record on both.

## Building the bot with an AI assistant

The API is small enough that an assistant can write most of a bot in one pass. What it cannot
do is guess the contract, and a wrong guess produces code that looks right and fails in
testing. So give it the contract first.

Paste the reference prompt below, then the prompt for your chat application, then let it work.
Both are written to be pasted as they are.

### The reference prompt

```
You are writing a chat bot that connects a chat application to Search2o. Use only the
API described here. Do not invent endpoints, fields or values.

BASE URL
  The address of the customer's agent server. Call it BASE. Every call is a POST with a
  JSON body. Every response is JSON.

AUTHENTICATION
  Calls made on behalf of a person carry that person's integration token:
      Authorization: Bearer <token>
  Three calls need no token at all: startConnect, getConnectRequest, getConnectToken.

ERRORS
  A failure is HTTP 4xx with a body of:
      { "success": false, "error": { "message": "...", "cause": "...", "data": {} } }
  Show error.message. There is no error code to branch on.

CONNECTING A PERSON  (run once per person, no password is ever handled by the bot)
  1. POST BASE/api/auth/startConnect
       in : { "clientName": "Slack - Acme workspace" }
       out: { "success": true, "connectId": "...", "connectSecret": "...",
              "connectUrl": "...", "userCode": "ZUEZFA",
              "expiresIn": 600, "pollIntervalSeconds": 5 }
     Keep connectSecret private to the bot. Never show it or put it in a link.
  2. Show the person a button opening connectUrl, and show userCode next to it.
     Tell them to check that the code on the page matches this one.
  3. POST BASE/api/auth/getConnectToken every pollIntervalSeconds
       in : { "connectId": "...", "connectSecret": "..." }
       out: { "status": "pending" | "approved" | "denied" | "expired",
              "token": "...", "tokenType": "Bearer", "expiresIn": 31536000,
              "userEmail": "...", "userName": "..." }
     token is set only when status is approved, and only once. Store it against the
     person's chat-application user id. Stop polling on denied or expired.

FINDING AN AGENT
  POST BASE/api/exec/search
    in : { "query": "the person's question" }        at least 8 characters
    out: { "success": true,
           "searchResults": [ { "agentName": "...", "agentTitle": "..." } ],
           "searchBehavior": "executeTopMatch" | "executeOnlyMatch" | "showResults",
           "followupBehavior": "executeTopMatch" | "executeOnlyMatch" | "showResults"
                               | "executePrevious" }
  Up to three results. searchBehavior tells you what to do with them for a new question,
  followupBehavior for a question inside a conversation that already exists.
      executeTopMatch   run the first result
      executeOnlyMatch  run it when there is one result, otherwise show the list
      showResults       show the list and let the person choose
      executePrevious   keep using the agent already in this conversation
  An empty searchResults means no agent covers that question. Say so.

RUNNING AN AGENT
  POST BASE/api/exec/execAgent
    in : { "agentName": "...", "inputs": { "query": "the person's question" },
           "stream": false, "convid": "..." }
         Leave convid out to start a conversation. Pass it to continue one.
    out: { "success": true, "convid": "...", "agentName": "...",
           "resultCode": "...", "askInput": null,
           "output": { "agentName": "...", "parts": [ ... ] } }

  resultCode is one of:
      success                     finished; show output.parts
      ask                         it needs input; see ASKING below
      unknownAgentOrConversation  the conversation is gone; start a new one
      failCommand, errorInAgent, callFailed, timedOut, stopped, unexpected, mustLogin
                                  failed; tell the person, using error.message when present

  output.parts is a list. Each part is one of:
      { "contentType": "text",  "text": "markdown" }
      { "contentType": "html",  "text": "<p>...</p>" }
      { "contentType": "image", "text": "<base64>", "mimeType": "image/png" }

ASKING THE PERSON FOR INPUT
  When resultCode is "ask", askInput is:
      { "message": "shown above the fields",
        "inputs": [ { "name": "...", "type": "...", "label": "...",
                      "description": "...", "options": [], "default": null,
                      "hidden": false } ] }
  type is one of str, password, text, chooseOne, chooseMany.
  A hidden input is not shown to the person. Send it back unchanged.
  Collect the answers and call execAgent again with the same convid and
  inputs set to { "<name>": "<answer>", ... }.

CONVERSATIONS
  POST BASE/api/exec/getConversation        { "convid": "..." }
  POST BASE/api/user/getUnpinnedConversations { "nextCursor": null, "limit": 25 }
  POST BASE/api/user/getPinnedConversations   { }
  POST BASE/api/user/setConversationTitle     { "convid": "...", "title": "..." }
  POST BASE/api/user/setPinned                { "convid": "...", "pinned": true }
  POST BASE/api/user/deleteConversation       { "convid": "..." }

RULES YOU MUST FOLLOW
  - Store one integration token per chat-application user. Never share one between people.
  - Keep your own record of which chat thread belongs to which convid. Search2o holds no
    link to the chat application.
  - When execAgent returns unknownAgentOrConversation, forget the stored convid, start a
    new conversation and carry on. It is not an error to report.
  - Never log a token, never put one in a URL, never post one into a channel.
  - An answer is markdown. Convert it to the chat application's own format.
  - html parts cannot be shown in any chat application. Convert them to text, or tell the
    person the answer is in the Search2o GUI.
  - image parts are base64. Upload them using the chat application's file API.
  - When searchBehavior or followupBehavior says to show the results, show one button per
    agent. Put a short id in the button and keep the question in your own store, because a
    button carries little and a question can be long. Replace the message once somebody
    chooses, so a second click cannot start a second conversation. Accept the click only
    from the person who asked.
  - When a run returns unknownAgentOrConversation, reuse the message you already posted for
    the retry. Do not post a second one.
```

### The prompt for Slack

```
Write a Slack bot in <your language> using the reference above.

  - Use Socket Mode, so the bot needs no public address and can run inside a private
    network next to the agent server.
  - Verify Slack's request signature on every event.
  - Respond to app mentions and direct messages.
  - Reply in a thread. Key the conversation record on team id, channel id and thread_ts.
  - On first use by a person, run the connect flow. Post the button and the code in a
    direct message, never in a channel.
  - Acknowledge the event within three seconds. Post a short "working on it" message, then
    edit it with chat.update when the answer arrives. An agent can take a minute, so never
    hold the acknowledgement open waiting for it.
  - An ask cannot open a modal directly. A modal needs a trigger_id, and a message event
    does not carry one. Post a message with an Answer button, and open the modal from the
    button click.
  - Map the input types to Slack blocks: str to plain text, password to plain text, text to
    a multiline input, chooseOne to a static select, chooseMany to a multi select.
  - Show search results as buttons in a message, one per agent, and update that message once
    somebody chooses.
  - Convert markdown to Slack mrkdwn. Bold is *text*, links are <url|label>.
  - Upload image parts with files.upload and post them in the thread.
```

### The prompt for Microsoft Teams

```
Write a Microsoft Teams bot in <your language> using the reference above.

  - Use the Bot Framework. The bot needs a public HTTPS endpoint, or a tunnel into the
    network where the agent server runs.
  - Respond to messages in channels and in one to one chats.
  - Key the conversation record on the Teams conversation id and the reply chain id.
  - On first use by a person, run the connect flow. Send the button as an Adaptive Card,
    in a one to one chat rather than a channel.
  - Acknowledge the activity at once. Keep the conversation reference, and send the answer
    as a proactive message when it arrives, or update the activity. An agent can take a
    minute, which is longer than the connector will wait, so never answer inline.
  - Render an ask as an Adaptive Card with an input for each field, and a submit action
    that returns the answers.
  - Teams accepts a useful subset of markdown. Convert what it does not accept.
  - Attach image parts as card images or file attachments.
```

### The prompt for Google Chat

```
Write a Google Chat app in <your language> using the reference above.

  - Receive events over Pub/Sub, so the app needs no public address and can run inside a
    private network next to the agent server.
  - Respond to messages in spaces and in direct messages.
  - Key the conversation record on the space name and the thread name.
  - On first use by a person, run the connect flow. Send the button as a card, in a direct
    message rather than a space.
  - Reply in the same thread.
  - Acknowledge the event at once, then create the answer as a new message with the Chat API
    when it arrives. An agent can take a minute, which is longer than the wait allowed for a
    reply to the event itself.
  - Render an ask as a card with a section per field and a submit button.
  - Convert markdown to Google Chat formatting. Bold is *text*, links are <url|label>.
  - Upload image parts as card images.
```

### Check these before you trust the result

An assistant will produce something plausible. These are the points where a plausible answer
is wrong, so check each one against the running bot.

The connect flow never returns the token to the browser. If the generated code reads a token
from a redirect or from the page, it has invented that.

The token is returned once. If the code expects to fetch it again later, it is wrong.

`unknownAgentOrConversation` means start a new conversation. If the code treats it as a
failure and shows an error, people will see errors when a conversation simply expired.

The question goes in `inputs` under the name `query`. It is not a top level field.

`convid` is left out to start a conversation. It is not set to null or to an empty string.

An agent that asks needs the same `convid` on the next call, or it starts again from the
beginning.

In Slack, opening a form straight from a message event cannot work. If the generated code does
that, it will fail the first time an agent asks for anything.

## When single sign-on is available

Search2o will support signing people in through a company's own identity provider, using OIDC
or SAML.

Very little changes for a chat integration. A token still belongs to a person, is still
created by that person, and still works the same way. The connect flow is unchanged. The only
difference is in step 3: instead of a password form, the page sends the person to their
identity provider and brings them back.

Two points are worth planning for.

The pasted-token route becomes the only route for people who never open the GUI, unless the
connect flow is in place. Prefer the connect flow.

Resetting a password no longer applies, because passwords live with the identity provider. A
token is then ended by the person revoking it, or by the person being deleted in Search2o.
Disabling somebody at the identity provider does not end their Search2o tokens. Remove the
person in Search2o as well.

## What a company decides before starting

Who may connect a chat account. Every person who uses the bot needs a Search2o account.

Whether tokens expire. A token that never expires is convenient and has to be revoked by hand.

How the bot reaches the agent server. A bot outside the network needs the agent server to be
reachable, or a tunnel.

What happens to an agent that produces HTML. Either the agent is changed, or the bot converts
the HTML.
