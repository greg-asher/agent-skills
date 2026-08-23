---
name: cleanup
description: Safely remove a completed or explicitly discarded Kestrel managed worktree while retaining durable evidence by default. Use only when the user explicitly invokes /kestrel:cleanup for an identified or recent run.
disable-model-invocation: true
---

# Clean Up Kestrel Work

Read [the shared lifecycle contract](../../references/lifecycle.md) and [the writing guide](references/plain-language-writing.md).

Inspect the manifest, Git worktree registration, worktree status, lifecycle, and integration evidence. Run `kestrel-plugin cleanup` only when ownership is proven, the worktree is clean, and the result is integrated. Use `--discard-result` only after explicit discard approval.

Retain the run manifest, input, output, identifiers, and recovery evidence by default. Deleting evidence requires the user to explicitly request it, a second confirmation using the exact session identifier, and `--delete-evidence --confirm <session>`.

Report exactly what was removed, what evidence remains, and whether recovery is possible.
