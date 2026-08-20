---
name: deep-discovery
description: Deeply investigate an existing software application or unfamiliar codebase using coordinated subagents, end-to-end workflow tracing, and synthesis. Use for application discovery, technical onboarding, inherited systems, MVP handoffs, architecture reconstruction, or requests to understand what a repository does, how it works, how data moves, and what state the build is in.
disable-model-invocation: true
---

# Deep Discovery

Explain an existing application as it works now. Start broad. Find the workflows that create its value, trace them in depth, and connect them into one account of the product and system.

Use the current repository as the main boundary. Follow direct references to related repositories, deployment files, shared schemas, or supporting artifacts when the application uses them. State what you could not inspect. Treat the invocation context below as additional guidance:

`$ARGUMENTS`

Keep this discovery separate from migration planning, target architecture, redesign, or implementation.

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before you write the report or final session synthesis. Apply its core rules to all prose. Apply its technical rules when you explain the system or give navigation instructions. Apply its editorial rules when you report findings, evidence, significance, or uncertainty.

In every response and artifact:

- Put the main finding first.
- Use short sentences, active voice, familiar words, and consistent terms.
- Explain a technical term when it first appears, unless the intended reader will know it.
- Name the actor when responsibility matters.
- Distinguish observed facts from repository claims, inference, estimates, and unknowns.
- Put attribution or a code reference next to the claim it supports.
- Give exact dates, counts, units, and comparisons when the evidence supports them.
- Remove filler, slogans, jargon, decorative metaphors, and ceremonial conclusions.

## Lead the investigation

Remain in the main session and lead the investigation. Do not give the whole skill to a subagent. Use subagents for focused repository searches and workflow traces. Keep orientation, path selection, synthesis, and follow-up decisions in the main session.

Subagents do not share the lead's full context. Give each subagent the relevant working view, one specific question, and the expected result. Do not ask a subagent to summarize the whole repository.

## 1. Get oriented

Experience the application if it can be run or observed. Scan the repository structure, product surfaces, documentation, tests, configuration, and recent history.

Form a working view of:

- what the application does
- who appears to use it
- which capabilities appear central
- which workflows may create its value
- which parts of the system need deeper investigation

Use this view to shape the scout assignments. Do not treat it as settled.

## 2. Launch the scout wave

Launch scouts with different questions at the same time. Match the number of scouts to the repository. Cover these perspectives:

- product behavior, users, capabilities, and candidate workflows
- components, services, runtime, and application structure
- data models, sources, transformations, and integrations
- current build, tests, recent evolution, ownership, and operating context

Give every scout a compact assignment containing:

1. The provisional application context relevant to its work.
2. One bounded investigation question.
3. A request to identify or challenge likely workflows that create value.
4. A request to return what it learned, how the pieces connect, and what remains unclear.

Let scouts follow useful connections they find. These perspectives organize the search. They do not define the application's architecture.

## 3. Choose the value paths

Combine the scout findings into an updated view of the application. Select the two or three end-to-end workflows that best explain its purpose and value.

Prefer workflows that cross several parts of the application and produce a meaningful result. They should also reveal important data or integrations. State why you selected each path.

## 4. Launch the trace wave

Launch one subagent per selected value path, concurrently where the paths are independent.

Ask each trace agent to follow its workflow through the actual application:

`trigger or input -> entry point -> processing and decisions -> data and integrations -> resulting system, user, or business outcome`

Have the agent explain meaningful branches, handoffs, and incomplete portions without turning the trace into a file-by-file tour.

## 5. Assemble the application model

Combine the workflow traces with the scout findings. Build one connected explanation of:

- the product and its users
- its main capabilities
- its core value paths
- the major application and runtime pieces
- its data model and data movement
- external integrations and dependencies
- the current state of the build
- ownership and operating context
- how the application has evolved and where it appears to be heading

Resolve different descriptions of the same behavior into one shared vocabulary.

For each main capability or value path, state whether it is:

- implemented and active
- implemented but apparently unused
- partial or incomplete
- stubbed or mocked
- described in documentation but not found in the build

Do not infer that a capability is operational merely because supporting code exists.

## 6. Fill important gaps

Identify missing information that prevents a clear explanation of the application. Launch the smallest follow-up search that can answer each important question. Then update the application model.

Repeat only when the answer changes your understanding of the product, its workflows, or the supporting system. Do not inspect the repository only for completeness.

## 7. Publish the discovery

Write a durable Markdown report. Follow an existing documentation convention when one is obvious; otherwise write:

`docs/discovery/<application-slug>-deep-discovery.md`

Use this structure:

```markdown
# <Application> Deep Discovery

## Executive Summary

## Product and Users

## Core Value Paths

## System Architecture

## Data Model and Data Flow

## Integrations and Dependencies

## Current Build and Evolution

## Ownership and Operating Context

## Open Questions

## Codebase Guide
```

Use a simple diagram only when it makes a system relationship or workflow easier to understand. Cite useful code locations so another engineer can move from the report into the application. Include owners, maintainers, users, environments, and operating duties only when the evidence identifies them. State what remains unknown.

Finish the session with a concise executive synthesis covering:

- what the application is
- why it matters
- the workflows that define it
- how the system works at a high level
- the most important current-state observations
- the durable report path

Keep the session synthesis short. Put the detail in the report.
