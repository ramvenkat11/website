# What Search2o Cloud keeps

Search2o Cloud stores what your agent servers need to run your agents and what your team needs to
manage them. This page lists what is saved. How long each item is kept, and how encryption works,
are covered on their own pages.

Like any service, the cloud also keeps the basics of an account: the account itself, its license
keys, its users and the details they sign in with.

## Audit log

A record of changes made in your account and of events from your agent servers. Each entry says
what happened, who did it and when. Entries are written for:

- **Agents:** a description indexed, an indexing failure, a description deleted, and a change of
  title, tag, or time and cost limits.
- **Configuration:** a change to any setting or profile. An entry names the fields that changed,
  not their values. Allowlist changes list the entries added and removed.
- **Sign-in:** repeated failed sign-ins for a user, and a password reset asked for an address that
  has no account.
- **Agent servers:** a server starting, a server picking up a configuration change, and events a
  server reports. Each entry names the server and its version.

Each entry also records the lowest role allowed to read it, so entries about administrator-only
settings are visible to administrators only.

## Configuration

Every setting your agent servers run with:

- **System settings:** sign-in, allowlist, operators, system variables, hooks, agent servers,
  secrets, encryption, connection pools, search and validation.
- **Profiles:** LLM, API, database, MCP and prompt profiles, and which agents use each one.

Profiles name secrets; they do not hold them. A value such as an API key is written as a
reference, `sys.secret['NAME']`, and the agent server looks up the value when it runs. Secrets
kept in the hosted vault, and the text of prompt profiles, are stored encrypted.

## Agents and drafts

For each agent:

- Its definition, as you wrote it and in its checked form.
- Its name, title, tag, version, and time and cost limits.
- What its definition refers to: the profiles it uses, the agents it invokes, the secrets it reads
  and the memory labels it stores. These are names only.
- The query used to test it.
- Its description, stored encrypted.
- Earlier versions of the agent.

A draft holds the same items while it is being written, plus whether it has been checked and run.

## Reports

A record of each agent run: the agent and version, the user, the conversation, when it ran, how
long it took, the result, the LLM cost and time, and, for a failure, the error message and where
in the agent it happened. The reports are calculated from these records when you open them.

The query that started a run is not saved here.

## Conversations

For each conversation:

- Who it belongs to, its title, whether it is pinned, and when it was last used. The title starts
  as the first query and is stored encrypted.
- Its state: the variables and messages the agents need to continue it. The state is encrypted on
  your agent server before it is sent, so the cloud stores it without being able to read it.

If your agent servers save conversation state through your own hook, the state stays with you and
the cloud keeps only the conversation's details above.

## Long-term memory

What agents remember about a user between conversations. Each memory is kept per user, per agent
and per label, and holds:

- The text, stored encrypted.
- A vector made from the text, which is what lets an agent find the memories relevant to a
  question.
- When it was saved and when it was last used.
