---
name: review-work
description: Independently review an initial implementation broadly or a repair for closure, update issue dependencies, and gate completion. Use when the user explicitly invokes /review-work after /work-on-issues has marked issues Implemented.
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

Classify each reviewed issue by its existing history. An original implementation issue receives an **initial review**. A repair issue created by an earlier Review Work finding receives a **closure review**. A mixed wave can contain both, but keep their review boundaries separate. Do not create a new state or artifact for this classification.

If the authoritative graph cannot be read or updated, stop before review state changes.

## 2. Build a change-specific risk view

For an initial review, identify the failures the change can introduce. Base the risk view on changed behavior and affected boundaries, not a fixed checklist. Include ordinary correctness, integration, regression, and test risks. Add low-frequency concerns only when the change introduces them. Trace each relevant workflow from its trigger through the affected components to its observable result.

For a closure review, use the repair issue's failed behavior, named guarantee, established affected flow, done conditions, required validation, and directly changed shared boundaries as the complete review boundary. Verify that the repair closes that boundary without materially regressing it. Do not rebuild a broad risk view or expand into adjacent behavior merely because it is reachable.

## 3. Run independent reviews

Invoke both packaged reviewers:

- `execution:change-reviewer` checks intended behavior, ordinary correctness, integration, regressions, and test quality.
- `execution:adversarial-reviewer` searches relevant uncommon states involving ordering, retries, concurrency, partial state, stale data, migrations, authorization, outside outages, and recovery.

Give each reviewer the issue text, exact change range, affected workflows, relevant risk focus, and whether each issue is under initial or closure review. For closure, also give the named repair guarantee, established trigger-to-failure path, implicated components, done conditions, required validation, and directly changed shared boundaries. Do not give reviewers worker reasoning or conclusions. Invoke extra reviewer instances only for distinct risks an initial change actually introduces or an unresolved risk already inside a closure boundary.

The reviewers are read-only. Do not modify product code during review.

## 4. Reconcile and file defects

Reconcile all reviewer results before editing the issue graph. Trace or reproduce a reported failure before treating it as a defect. Establish the complete affected flow from the permitted trigger through each implicated component to the observable failure. A complete static trace is enough when runtime reproduction is impractical, but it must establish every link. Do not assume an input, caller, deployment state, or contract that the code and issue context do not establish. Exclude style preferences, speculative concerns, and requests that change settled outcomes or design.

During initial review, combine findings when restoring the intended behavior requires the same repair. Create one coherent repair issue for each distinct taskable repair needed to satisfy an acceptance condition, required validation, settled constraint, or regression caused by the reviewed change.

During closure review, extend the active graph only when the named repair still fails, required validation fails, a settled constraint within the repair boundary is violated, or the repair materially regresses the established affected flow or a shared boundary it changed. A material regression changes that flow's observable result, integrity, authorization, durability, or recoverability. Report other concrete observations in the final synthesis only, even when they are reachable or caused by the repair. Do not restart broad discovery or add low-impact adjacent edge cases to the Ready frontier.

For every admitted defect, use [the defect issue template](assets/defect-issue-template.md). Record the failed behavior, trigger, complete affected flow, components that must change, relevant constraints, observable completion conditions, and genuine dependencies. State the guarantee the repair must restore. Do not prescribe the implementation unless the settled design already does.

A blocking defect keeps the affected implementation issue `Implemented` and adds the repair issue as its blocker. During initial review, a non-blocking regression caused by the reviewed change becomes an independent `Ready` issue and does not hold an already completed outcome. During closure review, only a material regression admitted under the closure rule can become an independent `Ready` issue; other observations remain in the synthesis. Report a confirmed pre-existing or unrelated non-blocking defect in the final synthesis only; do not add it to the active issue graph. If the defect exposes an invalid product outcome or design commitment, mark the affected work `Blocked` and route it back to Planning or Design.

## 5. Gate completion

When no blocking defect remains, move the reviewed implementation issues to `Done` and recompute the `Ready` frontier. When blockers remain, keep affected implementation issues `Implemented` and make the repair path visible in the authoritative graph.

Commit local issue-state and defect-issue changes separately from the implementation commit. Do not include product-code changes. If an external tracker is authoritative, update it in place; create a local commit only when tracked local issue artifacts changed.

Finish with a short synthesis that names:

- the reviewed issues and change range
- the initial or closure posture applied to each issue
- the review result and confirmed defects
- new repair issue identifiers and blocking relationships
- resulting issue states and ready frontier
- the separate local review-state commit, when created

Do not fix the defects in this invocation. Return them to `/execution:work-on-issues`.
