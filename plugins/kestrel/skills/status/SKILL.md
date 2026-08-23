---
name: status
description: Inspect and explain an active, recent, or identified Kestrel lifecycle run from durable state and runtime evidence. Use only when the user explicitly invokes /kestrel:status to check installation readiness, progress, waiting work, failure, integration, or cleanup state.
disable-model-invocation: true
---

# Check Kestrel Status

Read [the shared lifecycle contract](../../references/lifecycle.md) and [the writing guide](references/plain-language-writing.md).

Run `kestrel-plugin status`, supplying `--session` or `--run` when named. Otherwise use the most recent relevant run. Reconcile the manifest with durable output rather than relying on a live process.

Distinguish not installed, no runs, running, waiting, failed, interrupted, completed-isolated, integrated, and cleaned. Report the evidence directory, identifiers, worktree, result revision, and one safest next action. Do not mutate or recover the run.
