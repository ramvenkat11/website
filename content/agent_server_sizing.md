# Sizing an agent server

An agent server is the part of Search2o that a company runs. This page says how many to run and
how to configure them. The figures come from our own load tests, on an Intel i9 at 2.40 GHz. A
faster processor does proportionally more, so these are a conservative starting point.

## Run one agent server for every processor core

An agent server is a single Python process. Python holds a global interpreter lock, so one process
uses one core however many threads it has. A larger machine therefore does nothing for a single
agent server, and capacity comes from running more of them.

A machine with eight cores should run eight agent servers behind a load balancer. In our tests a
second agent server nearly doubled throughput, from 50 to 89 agent runs per second, and both
servers stayed near a full core.

## Plan about 50 agent runs per second for each agent server

Every agent run costs an agent server about 20 to 24 milliseconds of processor time, whatever the
agent does. One core is a thousand milliseconds per second, which is where the figure of 50 comes
from.

How many runs that allows at the same time depends on how long a run lasts.

    agent runs at the same time  =  50 per second  x  seconds per run

**Plan about 25 at the same time for agents that mostly compute.** A computing agent finishes in
around half a second and uses the processor for all of it.

**Plan 100 to 150 at the same time for agents that call a remote language model.** Such an agent takes a
few seconds and spends almost all of that waiting, which costs the agent server nothing. These
agents never fill a core. What gives out first is the agent server's responsiveness, so watch that
rather than the processor.

How long a model call takes belongs to the model rather than to Search2o, and it is the number that
decides how many runs fit. These are the medians we measured with small fast models.

| model | median run |
|---|---|
| claude-haiku-4-5 | 1.5s |
| gemini-3.6-flash | 3.9s |
| gpt-5-mini | 4.5s |


Agents that stream their answers hold a connection for the life of the run, so a deployment that
streams heavily holds fewer runs at the same time than these figures suggest.

## Raise the API connection pool if your agents call anything

This is the pool the agents themselves use, for calls to language models and to your own services.
The default of 20 connections suits an agent server that mostly computes. When agents call
anything, size the pool above the number of runs at once, because each waiting run holds a
connection for the whole call. Twenty connections serve about twenty runs.

In our tests, 100 model-calling runs at the same time gave **1 run per second and 82 failures** on
the default pool, and **24 runs per second with no failures** on a wide one. Size the pool above the
number of runs you expect at the same time.

## Leave the cloud connection pool alone

That is a different pool, used by the agent server to reach Search2o Cloud rather than by your
agents. Widening it from 20 to 200 gained nothing in our tests and made heavy load worse, because
it admits more work into one process.

## Treat 107 MB to 165 MB as base memory

An agent server held 107 MB idle and 165 MB with 400 runs in flight. It stays in that band because
conversation state is saved to Search2o Cloud rather than accumulated in the process.

That band covers agents that move short text. Everything else a run holds lives in the process
while the run lasts. An agent that handles images is the clear case, because an image travels as
text and a single one can be several megabytes. Large API responses, database results and long
documents count the same way. A run carrying 2 MB needs at least that much on top of the base, and
a hundred such runs need at least two hundred megabytes more.

## Put the agent server near Search2o Cloud

Every agent run makes three requests to Search2o Cloud, which is 0.17s of the 0.28s that the
quickest possible run takes. A run that continues an existing conversation makes a fourth request
to load the state. That floor follows the distance rather than the speed of the machine.

## Watching a deployment that is already busy

Two things tell you whether another agent server will help. Neither needs any extra load put on the
system.

The first is the processor use of each agent server, which ordinary monitoring reports.

The second is how long an agent server takes to answer a request it handles by itself. **`GET
/health` is the one to use.** It returns a fixed answer, it needs no sign in, and it reaches
nothing outside the agent server, so its response time reflects that server's own health and
nothing else. Any uptime monitor can poll it.

It answers in about 0.003s on a server with capacity to spare, and stays there while the server has
room. It passes 0.01s when the server is running out.

| what you see at a busy time | what it means | what to do |
|---|---|---|
| each server near a full core | the agent servers are doing the work | add another one |
| `/health` under 0.01s, servers well under a core | the runs are waiting on something else | another server will wait too |
| `/health` climbing above 0.01s | the agent server itself is saturated | add another one |

Add agent servers while each one is near a full core. A server at half a core is waiting rather
than working, and another one waits alongside it.
