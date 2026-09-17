# Sizing an agent server

This page reports what one agent server handled under load, and how much a second and a fourth
added. It is here so that a company can size a deployment from measurements rather than from
guesswork.

Everything below is about the agent server, which is the part a company runs.

## What was measured

One hundred agents were published, each mocking a different business domain. Every agent validates
a reference, branches on the result, builds a short list of notes and returns an answer. Each one
can also call a backend service or a language model, chosen by an input, so the same agents
produced all three workloads below.

| workload | what each run does | why it is here |
|---|---|---|
| **logic** | validation, branching, a loop of four steps, one function call | the agent server with nothing to wait for |
| **waiting** | the same, plus a call to a backend that takes 200 ms or 1 s | the common case, where a run waits on something |
| **language model** | the same, plus one model call, spread across three vendors | the realistic case, measured rather than assumed |

Every level ran three times and the tables give the median. A separate caller measured two other
requests throughout, so the tables also show what somebody else felt. The load generator was
measured too, and never used more than 0.26 of a core, so it was never the constraint.

The agent server ran on a laptop with 8 cores. One agent server uses one core. Measurements come
from one session on one day, with 62,492 executions behind them.

### The network

Every figure is a function of this distance, so it is stated first.

| measurement | median |
|---|---|
| one round trip to Search2o Cloud | 0.056s |
| one request the agent server answers alone | 0.0037s |

Each execution makes exactly three requests to Search2o Cloud. One registers the run, one records
the execution, one saves the conversation state. Three round trips are 0.17s of every execution,
and that floor moves with distance rather than with processor speed.

## One agent server, agents with nothing to wait for

| concurrent runs | runs per second | p50 | p90 | cores | memory | local call | browse |
|---|---|---|---|---|---|---|---|
| 1 | 3.5 | 0.282s | 0.312s | 0.07 | 107 MB | 0.0039s | 0.057s |
| 5 | 19.8 | 0.247s | 0.281s | 0.23 | 109 MB | 0.0038s | 0.057s |
| 10 | 37.0 | 0.265s | 0.302s | 0.45 | 112 MB | 0.0040s | 0.082s |
| 25 | 49.0 | 0.493s | 0.569s | 0.97 | 118 MB | 0.0047s | 0.145s |
| 50 | 47.3 | 1.019s | 1.129s | 0.98 | 120 MB | 0.0073s | 0.321s |
| 100 | 39.7 | 2.425s | 2.617s | 0.96 | 124 MB | 0.0093s | 0.830s |
| 150 | 33.7 | 4.206s | 4.484s | 0.92 | 131 MB | 0.0144s | 1.336s |
| 250 | 26.1 | 7.956s | 10.050s | 0.90 | 141 MB | 0.0367s | 3.095s |
| 400 | 20.9 | 14.415s | 18.890s | 0.75 | 165 MB | 0.0383s | 5.358s |

There were no failed runs at any level, including 400 at once.

**One agent server peaks at about 49 runs per second, and it reaches one full core to do it.** The
processor is the limit here, and the limit arrives at 25 concurrent runs. Past that, adding callers
adds queueing and nothing else.

Memory is not a constraint. The process held 107 MB idle and 165 MB with 400 runs in flight.
Conversation state is saved to Search2o Cloud rather than accumulated in the process.

## One agent server, agents that wait

A run that waits holds its place without using the processor. This is what most real agents do.

| concurrent runs | 200 ms backend | cores | 1 s backend | cores |
|---|---|---|---|---|
| 10 | 20.9 | 0.33 | 7.7 | 0.13 |
| 25 | 38.9 | 0.85 | 17.7 | 0.34 |
| 50 | 38.6 | 1.03 | 30.1 | 0.67 |
| 100 | 34.8 | 0.98 | 39.9 | 0.94 |
| 150 | 31.1 | 0.96 | 35.3 | 1.00 |
| 250 | 26.0 | 0.91 | 29.4 | 0.93 |

The slower the backend, the more runs one agent server carries before its processor fills. With a
200 ms backend the core fills at 50 concurrent runs. With a 1 s backend it takes 150.

## One agent server, agents that call a language model

Three vendors were used together, so no single vendor's rate limit set the result.

| concurrent runs | runs per second | p50 | cores | local call | browse |
|---|---|---|---|---|---|
| 1 | 0.3 | 4.298s | 0.02 | 0.0036s | 0.058s |
| 10 | 4.0 | 1.235s | 0.09 | 0.0039s | 0.057s |
| 25 | 7.2 | 1.302s | 0.13 | 0.0037s | 0.056s |
| 50 | 16.9 | 1.297s | 0.32 | 0.0043s | 0.059s |
| 100 | 23.9 | 2.089s | 0.58 | 0.0058s | 0.105s |

**One hundred model-calling runs at the same time used 0.58 of a core, and browsing stayed at
0.105s.** The same agent server filled its core at 25 runs when there was nothing to wait for.

How long a run takes is a property of the vendor rather than of Search2o. At 100 concurrent runs
the medians were 1.47s, 3.90s and 4.53s for the three vendors. Use the figure for the vendor being
bought.

## The rule that covers all three

Each run costs the agent server about the same amount of processor time whatever it waits for.

| workload | runs per second | cores | processor time per run |
|---|---|---|---|
| logic | 49.0 | 0.97 | 20 ms |
| 1 s backend | 39.9 | 0.94 | 24 ms |
| language model | 23.9 | 0.58 | 24 ms |

**About 20 to 24 milliseconds per run, so one agent server sustains roughly 50 runs per second.**
That figure belongs to the agent server and transfers to another deployment.

The number of runs in flight then follows from how long a run lasts.

    runs at the same time  =  50 per second  x  seconds per run

A logic run of half a second gives 25 at the same time, which is what was measured. A model run of
two seconds gives 100, which is also what was measured. Put the duration of the real agents into
that line and it gives the number to plan for.

## More than one agent server

Each agent server is one process on one core, so a machine with eight cores runs eight of them.

| agent servers | peak runs per second | cores used | cores per server |
|---|---|---|---|
| 1 | 50.0 | 0.96 | 0.96 |
| 2 | 89.5 | 1.81 | 0.91 |
| 4 | 101.9 | 2.30 | 0.58 |

The second agent server nearly doubles throughput. The third and fourth add much less.

The reason is visible in the last column. At one and two servers each one is using nearly a full
core, so the agent servers are the limit and another one helps. At four servers each is at 0.58 of
a core, so they are waiting rather than working, and the limit has moved to the capacity behind
them.

That capacity was raised for these runs and is elastic in production, sized to the account. So the
ceiling of about 100 runs per second is a property of this test setup. **The last column is the
part that transfers.** Add agent servers while each is near a full core. Stop when they are not.

## What other people feel while the load runs

This is the number to plan against. The question is not how many agents an account holds. It is
how slow the product becomes for everybody else while agents are running.

| runs at the same time | browsing, logic agents | browsing, model agents |
|---|---|---|
| 10 | 0.082s | 0.057s |
| 25 | 0.145s | 0.056s |
| 50 | 0.321s | 0.059s |
| 100 | 0.830s | 0.105s |

Model-calling agents barely disturb anybody, because they spend their time waiting. Logic agents
compete for the same processor as everything else, and browsing passes 0.8s at 100 of them.

## Telling which side is constrained

Call a request that the agent server answers by itself. `getAccountName` is one, because it needs
nothing from anywhere else. Read the median while the load runs.

Under 0.01s means the agent server has capacity left. The waiting is elsewhere, and another agent
server will not help.

Rising well above that means the agent server is saturated, and another one will help. It reached
0.038s at 400 concurrent logic runs on one server.

The companion measurement is processor use per server, in the table above. Near one core means add
a server. Well under it means do not.

## Sizing guidance

These numbers count agent runs happening at the same time. They are not a limit on how many agents
an account holds. The account here held 100 agents, and any of them can run at any time.

Plan 25 agent runs at the same time per agent server for agents that mostly compute.

Plan 100 at the same time per agent server for agents that call a language model, and more if the
model is slow. Check the processor rather than the count.

Run one agent server per core. Two servers gave 1.8 times the throughput of one.

Give interactive users their own agent servers when the work is compute heavy. Browsing went from
0.082s to 0.830s as logic runs went from 10 to 100 on a shared process.

Stop adding agent servers when each is well under a full core. At that point the capacity behind
them is the limit, and more of them changes nothing.

## Keeping measurements comparable

The agents have to stay the same, and so does the work each run does.

The distance to Search2o Cloud has to stay the same, because three round trips sit inside every
run.

The levels, durations and number of repetitions have to stay the same. Each level here ran three
times, and the medians are reported.

The load generator has to be measured as well as the servers. It used 0.26 of a core at 95 runs per
second here, which is what makes these numbers the servers' own.
