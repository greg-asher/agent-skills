---
name: review-work
description: Independently review an implemented issue wave against its intended behavior and actual change, find ordinary and low-frequency defects, update issue dependencies, and gate completion. Use when the user explicitly invokes /review-work after /work-on-issues has marked issues Implemented.
license: MIT
disable-model-invocation: true
---

# Review Work

Review implemented work without changing product code. Keep the main session in control of scope, risk analysis, finding reconciliation, issue state, and the review-state commit.

Treat this invocation context as the starting point:

`$ARGUMENTS`

Read [the plain-language writing guide](references/plain-language-writing.md) before writing findings or issues. Read [the issue graph contract](references/issue-graph.md) and [the review strategy](references/review-strategy.md) before delegating review.

## 1. Resolve the review scope

Use an explicitly supplied tracker, issue set, issue URL, commit, or change range as authoritative. Otherwise, review every issue marked `Implemented` but not `Done` and the local integration commit that delivered it. Never create a second execution manifest.

Read the full issue text, done conditions, Product Brief and design commitments needed to judge the work. Establish the exact diff. Inspect both the change and the surrounding code paths, data, contracts, tests, and affected workflows.

If the authoritative graph cannot be read or updated, stop before review state changes.

## 2. Build a change-specific risk view

Identify the failures this change can introduce. Base the risk view on changed behavior and affected boundaries, not a fixed checklist. Include ordinary correctness, integration, regression, and test risks. Add low-frequency concerns only when the change introduces them. Trace each relevant workflow from its trigger through the affected components to its observable result.

## 3. Run independent reviews

Invoke both packaged reviewers:

- `execution:change-reviewer` checks intended behavior, ordinary correctness, integration, regressions, and test quality.
- `execution:adversarial-reviewer` searches relevant uncommon states involving ordering, retries, concurrency, partial state, stale data, migrations, authorization, outside outages, and recovery.

Give each reviewer the issue text, exact change range, affected workflows, and relevant risk focus. Do not give reviewers worker reasoning or conclusions. Invoke extra reviewer instances only for distinct risks the change actually introduces.

The reviewers are read-only. Do not modify product code during review.

## 4. Reconcile and file defects

Reconcile all reviewer results before editing the issue graph. Trace or reproduce a reported failure before treating it as a defect. Establish the complete affected flow from the permitted trigger through each implicated component to the observable failure. A complete static trace is enough when runtime reproduction is impractical, but it must establish every link. Do not assume an input, caller, deployment state, or contract that the code and issue context do not establish. Exclude style preferences, speculative concerns, and requests that change settled outcomes or design.

Combine findings when restoring the intended behavior requires the same repair. Create one coherent repair issue for each distinct taskable repair needed to satisfy an acceptance condition, required validation, settled constraint, or regression caused by the reviewed change. Use [the defect issue template](assets/defect-issue-template.md). Record the failed behavior, trigger, complete affected flow, components that must change, relevant constraints, observable completion conditions, and genuine dependencies. State the guarantee the repair must restore. Do not prescribe the implementation unless the settled design already does.

A blocking defect keeps the affected implementation issue `Implemented` and adds the repair issue as its blocker. A non-blocking regression caused by the reviewed change becomes an independent `Ready` issue and does not hold an already completed outcome. Report a confirmed pre-existing or unrelated non-blocking defect in the final synthesis only; do not add it to the active issue graph. If the defect exposes an invalid product outcome or design commitment, mark the affected work `Blocked` and route it back to Planning or Design.

## 5. Gate completion

When no blocking defect remains, move the reviewed implementation issues to `Done` and recompute the `Ready` frontier. When blockers remain, keep affected implementation issues `Implemented` and make the repair path visible in the authoritative graph.

Commit local issue-state and defect-issue changes separately from the implementation commit. Do not include product-code changes. If an external tracker is authoritative, update it in place; create a local commit only when tracked local issue artifacts changed.

Finish with a short synthesis that names:

- the reviewed issues and change range
- the review result and confirmed defects
- new repair issue identifiers and blocking relationships
- resulting issue states and ready frontier
- the separate local review-state commit, when created

Do not fix the defects in this invocation. Return them to `/execution:work-on-issues`.
