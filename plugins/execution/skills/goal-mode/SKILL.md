---
name: goal-mode
description: Drive an approved dependency-aware issue plan to a verified end state by alternating the packaged work-on-issues and review-work workflows, preserving a compact surface ledger, and stopping only when all in-scope work is Done or genuinely blocked. Use when the user explicitly invokes /execution:goal-mode, normally inside /goal, for long-running implementation work with settled issues and testable completion criteria.
license: MIT
disable-model-invocation: true
---

# Goal Mode

Complete one approved issue plan through a convergent implementation and review loop. Keep the main session responsible for the durable objective, scope, surface ledger, progress, and stopping decision.

When the host supports durable Goal Mode, use this skill within `/goal` so the loop can continue across turns. The skill remains usable in one continuous session when Goal Mode is unavailable.

Treat this invocation context as the starting point:

`$ARGUMENTS`

Read [the plain-language writing guide](references/plain-language-writing.md). Read and follow the packaged [work-on-issues workflow](../work-on-issues/SKILL.md) and [review-work workflow](../review-work/SKILL.md) rather than recreating either workflow here. Read the packaged [guided-operator workflow](../guided-operator/SKILL.md) only when completion reaches a multi-stage human gate with sensitive inputs, consequential mutations, recovery requirements, or human-assessed evidence.

## 1. Establish the contract

Resolve one authoritative issue graph and the Product Brief, design, repository instructions, and acceptance criteria that govern it. A good goal is larger than one issue wave but smaller than an open-ended backlog. If the objective or completion criteria are not settled, stop and route the work back to Planning instead of inventing them.

Record a concise surface ledger in the goal's working context:

- **Source of truth:** authoritative plan, graph, specifications, and instructions
- **Implementation:** code, data, configuration, documentation, and runtime surfaces the issues may change
- **Validation:** tests, commands, builds, scenarios, and artifacts that prove the outcome
- **Protected:** unrelated changes, deferred work, stable behavior, and explicit non-goals
- **External:** publication, deployment, provider, customer, destructive, or other separately authorized actions
- **Evidence:** current observations that justify the open issues

Discover unknown surfaces from the issue graph and repository before broad edits. Keep the ledger short and update it only when evidence changes the known contract. Do not create a separate planning artifact unless the repository already requires one.

## 2. Work and review

Repeat this sequence without waiting for another user prompt:

1. Follow `work-on-issues` for the next coherent ready wave.
2. Preserve its local integration commit and validation evidence.
3. Follow `review-work` for every newly Implemented issue and its exact change range.
4. Reconcile confirmed repair issues into the authoritative graph.
5. Continue from the recomputed Ready frontier.

Treat the user's invocation of this skill as authorization for local implementation, validation, issue-state updates, and the local commits required by the two packaged workflows. It does not authorize pushing, opening or merging pull requests, deployment, provider changes, customer mutations, destructive actions, or other external effects.

## 3. Keep review convergent

Accept a review finding only when it:

- identifies an observable failure
- maps to an unmet acceptance condition, regression, or required validation failure
- cites concrete evidence and the owning surface
- is not already represented by an open or completed issue
- defines a testable completion condition

Reject style preferences, speculative hardening, optional refactors, unrelated baseline failures, and changes to settled outcomes or design. Do not reopen a completed issue without new evidence that its completion condition fails.

Resolve defects at the earliest surface where behavior becomes incorrect. Recheck current implementation and tests before carrying forward claims from old plans, issues, or incident history.

After each cycle, record only:

- issues advanced, added, blocked, or completed
- current Ready frontier
- validation and review evidence
- material surface-ledger changes

Each cycle must reduce unresolved in-scope defects or materially strengthen the evidence for a blocker. If the same defect survives two attempted repairs, stop repeating patches: perform one focused root-cause pass across its documented surfaces and update its completion condition. If the next repair still makes no measurable progress, mark the affected work `Blocked` with the proven reason and smallest action needed to resume.

## 4. Stop at the verified end state

Complete the goal only when:

- every in-scope issue is `Done`
- every acceptance criterion has current passing evidence
- required validation passes
- the final review finds no actionable in-scope defect
- protected surfaces remain intact
- no unauthorized external action occurred

Do not call unrelated baseline failures goal failures. Record them as out of scope unless the implementation caused or exposed them as blockers to an acceptance criterion.

If completion requires missing information, permission, an external dependency, or a product or design decision, stop as blocked rather than guessing or weakening the goal.

When the remaining work is a qualifying human operation, complete safe local preparation, write the Guided Operator runbook, link it from the owning issue, and record the exact evidence required to resume. Keep the issue `Blocked`. The runbook does not authorize the external action. On resume, recheck current external state and evidence before moving the issue to `Implemented` or Review Work.

Finish with a short outcome-first report naming the issues resolved, surfaces changed, validation evidence, number of work-review cycles, and any exact blocker or authorized follow-up that remains.
