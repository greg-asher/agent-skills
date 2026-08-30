---
name: work-on-issues
description: Select and implement one coherent ready wave from a dependency-aware issue graph through coordinated implementation agents, then update the graph and create one local integration commit. Use when the user explicitly invokes /work-on-issues after implementation issues exist.
license: MIT
disable-model-invocation: true
---

# Work on Issues

Implement one coherent wave from the ready frontier. Keep the main session in control of selection, delegation, integration, issue state, and the wave commit.

Treat this invocation context as the starting point:

`$ARGUMENTS`

Read [the plain-language writing guide](references/plain-language-writing.md) before editing issue text or the implementation queue. Read [the issue graph contract](references/issue-graph.md) and [the orchestration guide](references/orchestration.md) before selecting work.

## 1. Resolve the execution basis

Use an explicitly supplied tracker, issue set, or issue URL as authoritative. Otherwise, use the repository's `implementation-queue.md` and linked issue files. If both sources could be authoritative and the user's intent is unclear, ask which one to use. Never create a second execution manifest or mirror an external tracker into local Markdown.

Read the complete authoritative queue and the full text of candidate issues. Load the Product Brief and design context needed to preserve settled outcomes and constraints. Inspect repository instructions, status, current changes, relevant code, and real dependencies before selecting a wave.

If the authoritative graph cannot be read or updated, stop before implementation. Preserve unrelated working-tree changes. Do not select an issue whose likely files or behavior overlap unresolved existing edits.

## 2. Select one coherent wave

Honor explicitly named issues when they are ready. Otherwise, choose a coherent subset of the `Ready` frontier.

Choose issues that can be implemented and reviewed together. Consider dependency readiness, shared contracts, file contention, integration order, risk, and the size of the combined review surface. Do not add dependencies only to make coordination easier.

Move selected issues to `In progress` before delegation.

For a repair issue, inspect the complete affected flow before delegation. Keep every component required to restore the intended behavior in one coherent wave. Map every required component to an assignment and make cross-component contracts and integration order explicit. Components may have bounded owners; the union of assignments must cover the complete repair. Do not split the repair into separate issues merely by file or component boundary.

## 3. Delegate bounded assignments

Invoke one or more `execution:issue-worker` agents. Give each worker:

- the complete issue text and observable done conditions
- the relevant Product Brief and design commitments
- the complete affected flow, the behavior, seams, and files it owns, and the named owners of other required components
- integration expectations and overlap constraints
- repository instructions and the checks it must run

Before delegation, verify that the assignments collectively cover every component required for the repair. Assign focused checks with their component owners and assign the complete-flow validation to one worker. The lead remains responsible for running that validation after integrating the whole wave.

If a required component has no owner in the wave, a cross-owner seam is unspecified, or an assignment requires an unplanned change inside another worker's ownership, the worker must stop that part and report the incomplete boundary instead of applying a local patch. A bounded assignment is not incomplete merely because another named worker owns other required components.

Use concurrent workers only when their assignments are merge-safe and ownership is disjoint. Sequence work that touches the same contracts, state, migrations, generated artifacts, or files.

Workers implement and test their assignments. They must not edit the issue graph, commit, push, open a pull request, or spawn more agents.

## 4. Integrate the wave

Inspect every worker result and working-tree change. Resolve cross-issue seams in the main session. Run the repository checks and the wave-level scenarios needed to establish that the combined behavior works.

Apply implementation findings to the authoritative graph. Update an existing repair issue when a finding belongs to its affected flow. Clarify, split, combine, add, or rewire issues only when the code reveals a genuinely distinct delivery shape. Preserve the settled product outcome and design commitments. If implementation invalidates either, mark the affected work `Blocked` and route the decision back to Planning or Design.

When every issue's done conditions and wave checks pass, move it to `Implemented` and recompute the `Ready` frontier. Leave failed or unresolved issues `In progress` or `Blocked`, with the reason and genuine dependency recorded.

## 5. Commit and stop

For a successful wave, create one local integration commit containing the complete wave and its local issue-graph updates. Follow repository commit conventions and reference the issue identifiers. Stage explicit paths so unrelated changes remain untouched. Do not push or open a pull request.

If an external tracker is authoritative, update its issues and relationships in place. Add the local commit reference after the commit exists. If the tracker update fails, report the graph as unsynchronized.

Finish with a short synthesis that names:

- the implemented wave and issue identifiers
- the behavior delivered and checks run
- issue or dependency changes discovered during implementation
- the local integration commit
- the next `/execution:review-work` invocation

Stop after the integration commit so review remains independent.
