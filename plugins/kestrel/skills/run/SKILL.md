---
name: run
description: Autonomously deliver one bounded repository task through Kestrel assignment, monitoring, local integration, validation, and safe managed-worktree cleanup. Use only when the user explicitly invokes /kestrel:run and wants an end-to-end local result.
disable-model-invocation: true
---

# Run Work Through Kestrel

Read [the shared lifecycle contract](../../references/lifecycle.md) and [the writing guide](references/plain-language-writing.md).

Resolve the current Git root. Read a named issue completely or compile the direct request into a temporary task file containing outcome, boundaries, completion conditions, and validation. Stop if required work exists only in uncommitted source changes.

Write known validation commands as a JSON array of argument arrays, for example `[["pnpm","test","--","focused"]]`. Run `kestrel-plugin run --workspace <root> --task-file <file> --validation-file <file>`. Omit the validation file only when the durable Kestrel result already contains sufficient task-specific proof. If the command returns `SETUP_REQUIRED`, explain and obtain one-time installation approval, use Setup, then resume the same request without asking the user to repeat it.

Let the runtime reuse a matching active or completed run. It assigns, monitors, integrates the exact result commit into the local branch, and removes only a proven-clean managed worktree while retaining evidence. Stop on changed intent, overlapping dirty files, ambiguous conflicts, failed validation, missing authority, or production impact.

Report the completed changes, validation, integrated revision, session/run identifiers, evidence directory, and cleanup result. Do not push, publish, merge remotely, or deploy.
