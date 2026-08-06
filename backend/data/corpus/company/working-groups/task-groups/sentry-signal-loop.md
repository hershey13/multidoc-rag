---
title: "Sentry Signal Loop"
description: "A Task Group restoring frontend Sentry as a useful triage tool: cutting noise at source, and prototyping a Sentry-to-GitLab-issue automation with Duo Developer doing the triage."
---

## Attributes

| Property        | Value                                                                                                          |
| --------------- | -------------------------------------------------------------------------------------------------------------- |
| Date Created    | 2026-05-19                                                                                               |
| Target End Date | 2026-08-15                                                                                                     |
| Slack           | [#tg_sentry_signal_loop](https://gitlab.enterprise.slack.com/archives/C0B41EVB4J3) (only accessible from within the company)       |

## Context

GitLab's frontend Sentry project (`gitlabcom-clientside`) accepts approximately 25 million events every 30 days. The signal-to-noise ratio has degraded to the point where the project is functionally unused for triage: the loudest issues are not bugs, and the bugs that *do* exist are buried and unowned.

![Sentry baseline — gitlabcom-clientside, March 2026 (~24.8M error events)](/images/company/working-groups/task-groups/sentry-signal-loop/baseline-march-2026.png)

Baseline: ~24.8M error events in March 2026.

A meaningful share of that volume is not "our application is broken 25 million times" — it is events that should never have been reported in the first place. Browser-extension CSP reports (for example, ad-blockers blocking our own Snowplow endpoint, third-party browser telemetry) and expected `4xx` responses from the application correctly enforcing its rules dominate the top of the list. **Sentry should report unexpected failures of our code, and nothing more than that.**

On top of the volume problem, there is no triage process. Every event already carries a `feature_category` tag, and the canonical `feature_category` → owning group mapping (see [`/handbook/product/categories/features/`](/handbook/product/categories/features/)) lives in [`stages.yml`](https://gitlab.com/gitlab-com/www-gitlab-com/-/blob/master/data/stages.yml). Ownership is declared. What's missing is anyone or anything looking at the data — a real bug affecting hundreds of thousands of users sits unassigned not because we don't know whose it is, but because nothing is looking.

The [Frontend Observability Working Group](/handbook/company/working-groups/frontend-observability/) (2021–2023) built the technical instrumentation and exited cleanly. The framework works. What was never built is the operating loop on top of it — the signal loop this Task Group sets out to close.

### Goals

The work splits into two phases that together form the loop:

1. **Primary Goal — Reduce noise at the source.** Update the Sentry SDK configuration and Sentry inbound filters so that the project reports unexpected failures of our code, and nothing more. The exit criterion is a ≥50% drop in 30-day event volume from the ~26M baseline (see [Exit Criteria](#exit-criteria) for the cited measurement). The exact filters are decided iteratively as MRs land and Sentry data updates.

2. **Secondary Goal — Build a Sentry → GitLab issue → Duo Developer triage automation, and run it.** Once the noise floor is lowered, we build the system that keeps us on top of the events. The automation runs on a daily schedule, fetches the latest Sentry issues, opens corresponding GitLab issues routed to the owning group through `feature_category`, and uses Duo Developer to produce triage on each. The unifying pattern: an agent separates noise from signal, and on each side produces a proposal that a human acts on. No MRs are opened autonomously — the handoff to the human is part of the design, not a limitation of it.

### Challenges

- **Agent-assisted work on signal is genuinely hard.** Frontend errors are often symptoms of root causes elsewhere in the stack, so the agent's output has to be a useful starting point for a human, not a finished answer. Calibrating that bar is part of the experiment, not a precondition for it.
- **Routing depends on signals we don't fully control.** The automation routes Sentry issues to owning groups through `feature_category`, and relies on CODEOWNERS for human collaboration on the resulting GitLab issues. Both signals exist today, but it is not yet known how cleanly they map to "a human who can actually act on this issue." Some routing failures are expected; how we handle them is part of what the experiment surfaces.
- **Deduplication across daily runs.** The automation runs on a 24-hour cadence. A Sentry issue that exists today will, in most cases, still exist tomorrow — the underlying problem won't be resolved overnight. The automation must reliably recognise a Sentry issue it has already opened a GitLab issue for and skip it, rather than producing a duplicate every day. Getting this wrong floods owning groups with copies of the same issue and immediately destroys trust in the automation. The mapping from Sentry issue identity to GitLab issue is one of the first design decisions we need to get right.
- **Finding a long-term owner is not guaranteed.** The automation only survives the Task Group if a group accepts it as their permanent responsibility (see [Exit Criteria](#exit-criteria)). If no owner is found, the automation is sunset at the end of the quarter, and that is itself a valid outcome — it tells us the value isn't sufficient for any group to invest in.
- **Deploy and rollup latency.** In order to test if our changes are effective, we need to wait for more events to roll in. This will cause the work to take longer than it would if we were seeing results in real time. 

These are the known challenges, but there may be additional issues that have yet to be identified.

## Exit Criteria

1. **Noise reduced at source (primary outcome).** Sentry SDK configuration and inbound filters are updated such that 30-day event volume in `gitlabcom-clientside` is reduced by ≥50% to less then 12.4M events in total from the March 2026 baseline of ~24.8M error events (see [Context](#context) for the screenshot and live view).
2. **Automation exists and has run on real issues.** The automation runs on a daily schedule, fetches Sentry issues, opens corresponding GitLab issues routed through `feature_category`, and produces Duo Developer triage (root cause, code references, proposed fix) on each. The automation has run for at least 2 weeks against real owning groups, with results recorded somewhere reviewable (issue link, Duo's output, owning-group action taken).
3. **The automation is useful enough to keep running.** The main thing we look at: when the automation opens a GitLab issue, does the owning group actually do something with it within 14 days — pick it up, assign it, put it on a milestone, fix it — or do they just close it and move on? That tells us whether Duo's triage is helping or just adding noise. Two extra checks back this up: we read through a handful of Duo's analyses by hand to see if they actually point at the real bug, and we look at how many issues got opened in total (a few good ones is a very different result from a flood of mediocre ones). At the end, the Task Group writes down a clear yes-or-no call with the reasoning. **"No, this didn't work, and here's what we learned" is a fine answer** — we don't pick a target percentage up front, because figuring out what "useful" looks like is the whole point of trying this.
4. **Long-term ownership is resolved.** Either a long-term owner has been identified for the automation, has been involved in the last 4 weeks of the Task Group, and has accepted a documented handover **or** no owner has been found and the automation is sunset at Task Group end with the rationale documented.

## Roles and Responsibilities

| Task Group Role | Person          | Title                                                        |
| --------------- | --------------- | ------------------------------------------------------------ |
| DRI             | [Jannik Lehmann](https://gitlab.com/jannik_lehmann)  | Senior Frontend Engineer, AI-Powered:AI Catalog              |
