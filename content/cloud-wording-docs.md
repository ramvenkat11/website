# Docs paragraphs that name Search2o Cloud

Current text, 2026-11-14. Edit each paragraph in place.

## docsrc/introduction/parts-of-the-system.html

Line 4, figure description for screen readers:

Your organization runs the agent servers and four clients, a browser chat, the chat applications, an agent harness and your own REST client, which all connect to the agent server cluster. The agent servers keep no state of their own: an encrypted link connects them to the cloud, which keeps the conversations and memories, encrypted by default.

Line 40, figure tag:

Search2o Cloud

Line 47, heading:

The cloud service

Line 48:

The cloud service runs as Search2o Cloud, hosted by Search2o, or as a private cloud, hosted in your own cloud account. The rest of the docs call either one "the cloud".

## docsrc/introduction/what-is-search2o.html

Line 13:

**Nothing to host for state.** The agent server holds no state. Everything is stored in the cloud, so agent servers can be started, stopped and scaled freely. Conversations, queries and memories are encrypted.

## docsrc/getting-started/registering-and-downloading.html

Line 4:

Search2o is in open beta, and anyone is welcome to try it. Creating an account is one step. It opens a free account with you as its first user and owner, and shows the account's license key once. The key connects an agent server to your account in Search2o Cloud, so store it with your other secrets as soon as it is shown. You are not asked for a password; you choose one the first time you open the UI.

## docsrc/getting-started/running-the-server.html

Line 23:

At startup the server validates the license and downloads the account's configuration from the cloud. It checks every entry of the expression allowlist against its own Python environment and builds its connection pools. Then it serves:

## docsrc/search/how-matching-works.html

Line 1:

A search takes about 200 milliseconds in the cloud and returns zero, one or two agents, depending on how confident the match is.

## docsrc/search/search-quality.html

Line 54:

A search compares the question against everything in the catalog and returns the best matches in about 200 milliseconds in the cloud. A catalog of a thousand agents takes about the same, a little over 200 milliseconds. Search does not get slower as the catalog grows. End to end, with the network hops, a user can expect an answer in well under a second. Search2o Cloud is served from the US East region today.

## docsrc/skill-integration/what-search2o-provides.html

Line 21:

The Search2o skill takes one entry. Behind it, search matches the request against every published agent's description in about 200 milliseconds in the cloud, with no model call. Adding an agent changes nothing in the skill or on any laptop.

## docsrc/security/data-privacy.html

Line 40:

Search2o Cloud runs on Google Cloud Platform. Search2o staff, and Google as the provider of the underlying infrastructure, can in principle see the data stored in plain form. With the default setting the account's key is managed by Search2o, so Search2o and Google can in principle read the encrypted data as well. With end-to-end encryption the key never leaves your organization, and neither Search2o nor Google can read what is stored encrypted. The [privacy policy](../../legal/privacy.html) is authoritative.

## docsrc/security/license-rotation.html

Line 1:

The license key connects an agent server to the account. Every request an agent server makes to Search2o Cloud carries the key, and an agent server without a valid key cannot start. An administrator can replace the key at any time, without downtime.  (License key rotation is not applicable to private cloud)

## docsrc/support-licensing/license.html

Line 13:

Search2o operates Search2o Cloud. Only the agent server uses the cloud's API; the license prohibits calling the API directly.

Line 14:

Search2o Cloud currently operates from the US East region, so an agent server in US East sees the lowest latency. Other regions will follow.

## docsrc/system-management/agent-server-sizing.html

Line 37:

Every agent run makes three requests to Search2o Cloud, which is 0.17s of the 0.28s that the quickest possible run takes. A run that continues an existing conversation makes a fourth request to load the state. That floor follows the distance rather than the speed of the machine.
