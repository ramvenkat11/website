# Search2o Launch Pricing

2026-09-19

# Part 1 — Motivation and decisions

## Principles

Every pricing decision below satisfies three rules.

1. No hindrance to trying the product. Anyone can sign up, build, publish and run agents without a card, and the Claude Code skill works on the free tier.
2. Every limit has a visible cost reason. Only indexing, AI assistance and search capacity cost Search2o money, so only those are limited. Nothing that costs nothing (integration tokens, drafts, profiles, memory labels) is limited or charged, because users know it costs nothing.
3. Priced as an enterprise application, not a developer tool. The search is for end users, so end users are the paying unit. More agents is the goal, so developers pay no premium over anyone else.

## Pricing model

One price, one unit: $30 per member per month, where a member is a person, a developer, or a service account.

- The value unit is executions, and searches count as executions. Each member brings 300 executions per month into a pool shared by the whole workspace.
- Nothing stops at the limit. Beyond the pool, overage is $30 per additional 300 executions — the same as a seat, so adding usage and adding a person cost the same and routing traffic through one seat gains nothing.
- No platform fee. Enterprise pricing is not yet decided; any revenue floor belongs there, not in Paid.
- Named seats at low volume. Active-user billing (pay only for people who used it that month) arrives with Enterprise as the volume incentive.
- Customers bring their own model keys, so Search2o's cost per execution is small; the seat carries the revenue and executions stay a fairness-safe meter.

## Behavior at the seams

No one meets a limit or a bill they were not told about first.

- A Free workspace cannot add an eleventh member; upgrading to Paid converts the whole workspace, all members. Not stated on the page.
- Free stops at its limits — executions, indexes, AI assistance — until the month resets. No overage on Free, and the page does not say so.
- On Paid, indexing beyond 10 per member per month fails. There is no index overage; the remedy is more members.
- Downgrade from Paid to Free keeps all data; Free limits apply after a 30-day grace. Nothing is deleted the day a card is cancelled.
- The execution meter is visible to every admin. Alerts go out at 80% and 100% of the pool. Admins may set a monthly spend cap; the default is uncapped and nothing stops.
- Overage is never cheaper than a seat, so the only remedies on the page are "add members" or pay $30 per 300.
- Nothing pinned disappears without notice. At Enterprise, a user gets a week's warning before org policy deletes a pinned conversation, with a prompt to export.
- Version age counts from when a version was superseded. The current version, and any version live in an environment, never expires.
- Free workspaces dormant for 1 month are deleted.
- Sanity caps that exist only to stop runaway scripts return "contact us", never "upgrade".

## Beta terms and what to measure

The beta is free with the limits on, Paid is available from day one, and the beta end date is on the page.

- Members paid for during the beta keep the $30 price for 24 months; members added to the same account after the beta pay the price current at that time. No discount: the freeze is the founding incentive.
- The page states the structure now so the eventual pricing is not a surprise: per member, pooled executions. No commitment to a permanent free tier.
- Around day 45, ask the ten most active workspaces what they would budget. Usage at $0 is not a price signal.

Track from day one:

1. Free workspaces hitting the 300 pool, and how many of those convert.
2. Executions per paid member per month, by percentile. Revisit the index and execution allowances against the 90th percentile of paid usage so only power users ever see a limit.
3. Which workspaces use service accounts, SSO, and reports — this is the gate-placement data for Enterprise.
4. Who asks about SSO, audit, or dedicated hosting — the Enterprise pipeline.

Benchmark: the median free-to-paid rate across products is about 8%. If under 2% of active free workspaces convert at $30, the problem is activation or value, not price.

## Enterprise scope

Enterprise launches at general availability, not in the beta, and its pricing is not yet decided. Scope is set by one rule: an Enterprise gate is something only a company with a procurement process needs.

- Active-user billing: the customer pays for people who used Search2o that month, not for provisioned seats.
- Deployment choice: multi-tenant SaaS, dedicated cloud for an industry group, or the customer's own cloud, with an SLA.
- SSO (OIDC now; SAML and SCIM when built), audit trail (1 year default, configurable to 7 years, immutable), support contract with a named contact.
- Org-wide retention settings, legal hold per conversation or user, per-user erasure, export on demand.
- Retention beyond Paid: reports 1 year with export; conversation, version-history and memory retention admin-configurable.
- Pooled execution volume in place of per-seat overage; terms to be set with the pricing.

Enterprise gates are things only a company with a procurement process needs. Anything a team needs to use the product — service accounts, tokens, priority capacity — stays in Paid.

## Unlimited everywhere

Everything that costs Search2o nothing is unlimited on every tier, with abuse ceilings in code only — never on the pricing page.

| Item | Treatment |
| --- | --- |
| Integration tokens per user | Unlimited; abuse ceiling in code |
| Drafts per user | Unlimited; abuse ceiling in code |
| Profiles (llm, mcp, prompt, api, db) | Unlimited; abuse ceiling in code |
| Memory labels per agent | Unlimited; abuse ceiling in code |
| Pinned conversations per user | Unlimited; exempt from the inactivity timer |
| Conversations per user | Unlimited; retention handles storage |
| Long-term memory | Bounded by count per user (100 Free, 500 Paid), never by time |
| Agents (drafts) | Unlimited; only indexing is limited |

An abuse ceiling is set far above any real use, and hitting one says "contact us", not "upgrade".

## Open decisions

Two decisions remain before GA; one of them before the beta page goes live.

- [ ] The beta end date, shown on the page (beta page).
- [ ] Enterprise pricing (GA): price per user, volume bands, minimum commitment, and whether active-user billing changes the rate.

Decided and not to be reopened: $30 per member for people, developers and service accounts, billed monthly for now; 300 executions per member pooled with $30 per additional 300; 30 indexes per month on Free and 10 per member per month on Paid, with indexing failing beyond that; AI assistance 100 per month on Free and 50 per member per month on Paid; memory 100 per user on Free and 500 on Paid; Free stops at its limits with no overage; no platform fee; no agent versioning on Free; dormant free workspaces deleted after 1 month; no commitment to a permanent free tier; Enterprise post-beta.

# Part 2 — Pricing page

## Plans

Two plans during the public beta. A member is a person, a developer, or a service account. Enterprise arrives at general availability.

- **Price** — Free: $0 · Paid: $30 / member / month, billed monthly
- **Members** — Free: up to 10 · Paid: unlimited
- **Agents** — Free: unlimited drafts; 30 indexes / month · Paid: unlimited drafts; 10 indexes / member / month
- **Executions (incl. searches)** — Free: 300 / workspace / month, pooled · Paid: 300 / member / month, pooled; $30 per extra 300
- **AI assistance** (drafting, doc questions, description validation) — Free: 100 / month · Paid: 50 / member / month
- **Capacity** — Free: shared, best-effort · Paid: priority
- **Reports** — Free: performance and errors with details, 7 days retention · Paid: all four reports with details, 90 days retention
- **Conversations** — Free: 7 days inactive; pins never expire · Paid: 90 days inactive; pins never expire
- **Agent version history** — Free: none · Paid: last 90 days
- **Support** — Free: community · Paid: email

Pay during the beta and each paid member keeps the $30 price for 24 months. Members added after the beta pay the then-current price.

## Limits and retention by tier

Retention is a fair gate because storage costs; features whose absence changes behavior (memory) are bounded by count, not time.

- **Indexed agents** — Free: 30 indexes / month · Paid: 10 indexes / member / month
- **Executions (incl. searches)** — Free: 300 / workspace / month · Paid: 300 / member / month; $30 per extra 300
- **AI assistance** — Free: 100 / month · Paid: 50 / member / month
- **Agent performance report (with details)** — Free: 7 days · Paid: 90 days
- **Agent errors report (with details)** — Free: 7 days · Paid: 90 days
- **LLM cost report** — Free: not included · Paid: 90 days
- **User usage report** — Free: not included · Paid: summary, 90 days
- **Inactive conversations** — Free: 7 days · Paid: 90 days
- **Pinned conversations** — never expire on either plan
- **Agent version history** — Free: none · Paid: last 90 days
- **Long-term memory** — Free: 100 memories / user · Paid: 500 memories / user
- **Dormant workspace** — Free: deleted after 1 month of inactivity · Paid: not applicable

## Enterprise

Available at general availability. Includes SSO, an audit trail, flexible retention, and a support contract with an SLA. Pricing will be announced at GA.
