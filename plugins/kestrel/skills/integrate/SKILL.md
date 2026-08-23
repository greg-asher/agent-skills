---
name: integrate
description: Verify and integrate a completed isolated Kestrel result into the current local branch while preserving unrelated changes. Use only when the user explicitly invokes /kestrel:integrate for a completed run.
disable-model-invocation: true
---

# Integrate a Kestrel Result

Read [the shared lifecycle contract](../../references/lifecycle.md) and [the writing guide](references/plain-language-writing.md).

Inspect the named or latest completed run, its assignment, source revision, worktree, changed files, validation, and target working tree. Run `kestrel-plugin integrate` only when ownership and completion are proven.

Preserve unrelated dirty files. Stop on overlapping files or ambiguous conflicts. The runtime creates one scoped worktree result commit when needed, cherry-picks the exact result, aborts a failed cherry-pick, and records the integrated revision.

Run any task-specific validation not already represented in durable evidence before claiming success. Report the result and target revisions. Do not push or publish.
