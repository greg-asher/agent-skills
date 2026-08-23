---
name: reclaim-storage
description: Safely reclaim reviewed disk usage from coding-agent caches, stale Git worktrees, node_modules, package-manager caches, and build artifacts. Use only when the user explicitly invokes /utilities:reclaim-storage or asks this plugin to perform cleanup after reviewing targets.
disable-model-invocation: true
---

# Reclaim Storage

Reclaim disk from exact reviewed targets while preserving source work, credentials, active sessions, and recoverability.

Read [the plain-language writing guide](references/plain-language-writing.md). Begin with `/utilities:audit-storage` evidence from the current turn or refresh it before deletion when paths, sizes, activity, or Git state could have changed.

## Authorization boundary

The user's request to clean authorizes ordinary regenerable caches in the named scope. Obtain explicit confirmation before removing:

- any worktree or repository;
- `node_modules` or another dependency installation;
- Kestrel run evidence, Codex/Claude conversation data, logs, or downloads;
- anything classified Review required or Unknown;
- more than the reviewed scope.

Confirmation must name the category or exact targets and show the estimated reclaimable size. Never bundle protected data into a broad “clean all” operation.

## Safety checks

Resolve every target to an absolute canonical path. Refuse filesystem roots, home directories, workspace roots, unresolved variables, symlinks escaping the reviewed target, and paths that changed identity after review.

Before removing a Git worktree, prove it is registered, clean, inactive, and has no unique unpushed commits. Check remote pull-request state when available. Use `git worktree remove` and then `git worktree prune`; do not directly erase a registered worktree. For Kestrel-managed worktrees, invoke `/kestrel:cleanup` and preserve evidence by default.

Prefer native cache commands when they preserve current installs. Remove build outputs only when their owning project and regeneration path are known. Never delete credentials, configuration, databases, lockfiles, source, current-session state, or active process files.

## Execution and proof

Recheck free space immediately before and after. Execute the smallest coherent category first, stop on unexpected state, and do not force past a failed safety check. Report exact targets removed, bytes reclaimed, commands used, skipped targets and reasons, and whether each removal is regenerable or recoverable.
