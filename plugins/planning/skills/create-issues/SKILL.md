---
name: create-issues
description: Turn a delivery-ready Product Brief into a small dependency-aware set of standalone, agent-ready implementation issues. Use when the user explicitly invokes /create-issues after the canonical Product Brief is ready and wants durable issue files or an implementation queue.
license: MIT
disable-model-invocation: true
---

# Create Issues

Turn a delivery-ready Product Brief into the smallest useful set of implementation assignments. Make each issue coherent enough for an agent to complete without reconstructing the product from the full planning history.

Treat this invocation context as a starting point:

`$ARGUMENTS`

Do not reopen discovery, redesign the solution, estimate delivery, create another planning artifact, or publish to an issue tracker unless the user explicitly asks.

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before writing issue files, the queue, or the session synthesis.

In every issue:

- Lead with the useful behavior or enabling outcome.
- Name the user, system actor, process, surface, responsibility, and result when they matter.
- Use direct requirements and observable completion conditions.
- Include the Product Brief commitments and repository context needed for this assignment.
- Avoid ticket jargon, process metadata, exhaustive file lists, and repeated background.

## Lead the issue design

Remain in the main session. Own source selection, decomposition, dependency decisions, coverage, and the final queue.

Use subagents for focused repository traces or independent scenario decomposition when the work is broad. Give each subagent one bounded slice. Reconcile all suggestions into one issue graph in the main session.

## 1. Establish the delivery basis

Read the complete Product Brief. Treat it as the canonical source for product narrative and Business and Process, Technology, and People requirements.

If the Product Brief is marked `Not ready for issue creation`, stop and name the blocking decisions. Do not decompose around them.

Read linked Discovery or Design artifacts only when deeper rationale or context is needed for correct decomposition. Do not make readers reconstruct requirements from those sources. If a supporting source conflicts with the Product Brief, follow the Product Brief and make the mismatch visible when it affects delivery.

Inspect the repository when one exists. Identify current product surfaces, execution paths, ownership boundaries, contracts, data, integrations, operational paths, and tests that affect how work can be divided. For a greenfield product, use the responsibilities and boundaries in the Product Brief and linked Solution Design.

Do not settle a new product, architecture, or ownership decision inside an issue. State required guarantees without inventing an unsettled schema, API, algorithm, vendor, or operating model.

## 2. Find the vertical slices

Start with the Product Brief's defining scenarios. Divide the work into thin end-to-end increments that produce useful or visibly demonstrable behavior.

Keep the Business and Process, Technology, and People work needed for an outcome in the same product slice. Create a standalone process, technology, or people issue only when it has a distinct owner, prerequisite relationship, or independently useful deliverable.

Prefer an issue that crosses the necessary process, interface, behavior, data, integration, and operating boundaries over separate frontend, backend, database, integration, documentation, training, and testing tickets.

Keep the issue set small. Combine work when one agent or owner can deliver it coherently. Split work when an issue contains separate outcomes, unrelated ownership, or a dependency that should land independently.

For a broad replacement or data evolution, use expand, migrate, and contract slices. Preserve compatibility until the contract issue removes the old path.

## 3. Build the issue graph

For each issue, define:

- the useful outcome and where it fits in a defining scenario
- the behavior, process, technology, and responsibility changes needed for the slice
- the Product Brief requirements it must satisfy
- the existing seams, contracts, data, integrations, operational paths, and compatibility rules it must preserve
- observable completion conditions across every applicable lens
- real prerequisite issues

Embed the relevant requirements and context in the issue. Link the Product Brief for authority, but do not require the implementation agent to infer the assignment from it.

Add a dependency only when the downstream issue cannot be completed against the current system or a stable contract. Do not serialize independent work for convenience.

Classify every issue in the shared execution graph. Put issues with no unresolved prerequisite in `Ready`. Put issues with unresolved prerequisites in `Blocked` and name the issue that must reach `Done` before each can advance.

## 4. Check the complete plan

Trace every defining scenario and requirement through the issue set. Give each requirement one clear delivery home. Make sure each issue delivers a coherent slice and that the complete set produces the Product Brief's intended product and operating result.

Do not create a traceability matrix or another middle artifact. Perform the coverage check as part of issue design.

Do not add cleanup, infrastructure, testing, documentation, training, adoption, or operational issues by default. Include that work in the relevant vertical slice unless it meets the standalone-issue rule.

## 5. Publish the issue set

Write each issue using [the issue template](assets/issue-template.md). Follow an existing documentation convention when obvious; otherwise write:

```text
docs/planning/<initiative-slug>/issues/
  implementation-queue.md
  01-<issue-slug>.md
  02-<issue-slug>.md
```

Write `implementation-queue.md` using [the queue template](assets/implementation-queue-template.md). This file is the living issue graph used by implementation and review when no external tracker is authoritative. Put each issue in exactly one state and keep real dependency relationships in the issue files. Order issues within a state for comprehension, not to imply dependencies that do not exist.

Create or update external tracker issues only when the user explicitly requests that separate action.

Finish the session with a short synthesis covering:

- the delivery shape
- the number of issues
- the initial `Ready` frontier
- the important blocked dependency boundary
- the issue directory
