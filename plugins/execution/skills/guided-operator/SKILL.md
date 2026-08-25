---
name: guided-operator
description: Prepare a safe, resumable runbook for a multi-stage operation that requires human authority or action. Use when the user explicitly invokes /execution:guided-operator for credentials, dashboards, protected promotions, deployments, migrations, cutovers, or physical or visual verification.
license: MIT
disable-model-invocation: true
---

# Guided Operator

Prepare the human to complete a consequential operation without expanding the agent's authority. Produce the runbook and safe local helpers; do not perform the complete external procedure.

Treat `$ARGUMENTS`, the current issue, and the current workspace as the operation boundary.

Read [the plain-language writing guide](references/plain-language-writing.md) and [the runbook template](assets/operator-runbook-template.md).

## 1. Confirm that a runbook is warranted

Use this workflow only when the remaining operation has multiple ordered actions, sensitive inputs, consequential mutations, recovery requirements, or evidence that a human must assess.

Use the host's ordinary approval mechanism for one safe command or one simple approval. Return unresolved product or design decisions to their owning workflow. Use a questionnaire when another person holds missing knowledge.

## 2. Establish current state and authority

Inspect the repository and available read-only external state before asking the user. Identify:

- current and target state
- the human authority or action required
- safe preparation the agent can complete locally
- external, destructive, protected, or irreversible actions
- sensitive input names and where the human obtains them
- proof required to recognize success

Never read, request, record, or display a secret value. The runbook may instruct the human to enter it directly into an authorized destination. Refer to sensitive inputs by variable or credential name only.

## 3. Design the operation

Break the operation into focused stages. For each stage define:

- preconditions
- actor and exact action
- command or current authoritative URL when needed
- confirmation before a consequential mutation
- expected result
- evidence to retain without sensitive values
- stop condition and recovery action

Include rollback for every reversible mutation. For an irreversible action, state that fact before its confirmation and give the safest available containment or recovery path.

Record a resume checkpoint after every completed stage. A resumed run must recheck current state rather than trust a stale checkbox.

## 4. Write and verify the runbook

Write `docs/operations/<operation-slug>-runbook.md`. Include the authority boundary, prerequisites, stages, stop conditions, rollback, evidence, resume state, and completion criteria from the template.

Add a helper script only when deterministic local behavior reduces risk. Keep human-authorized actions gated. Never embed or print secrets, weaken confirmation gates, or automatically run the complete procedure. Validate a shell helper with `bash -n` and ShellCheck when available.

Statically trace every input, action, output, evidence item, stop condition, and rollback path. Finish with the runbook path, safe preparation completed, human action required, and exact evidence needed to resume the owning workflow.

## Goal Mode handoff

When Goal Mode reaches this workflow, it may complete safe local preparation and write the runbook. Link the runbook from the owning issue, record the exact resume condition, and leave the issue `Blocked`. On resume, recheck current external state and evidence before moving the issue to `Implemented` or sending it to Review Work.
