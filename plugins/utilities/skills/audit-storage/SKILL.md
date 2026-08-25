---
name: audit-storage
description: Inventory and explain disk usage from Codex, Claude Code, Kestrel, Git worktrees, repositories, node_modules, package-manager caches, and build artifacts without deleting anything. Use when the user explicitly invokes /utilities:audit-storage or asks this plugin for a disk or memory cleanup assessment.
license: MIT
disable-model-invocation: true
---

# Audit Storage

Build a read-only, evidence-backed storage inventory and reclaim plan. Treat “memory” as disk storage unless the user clearly asks about RAM or process memory.

Read [the plain-language writing guide](references/plain-language-writing.md). Run `${CLAUDE_PLUGIN_ROOT}/scripts/storage-audit.py` in Claude Code or resolve the same script relative to this skill in other hosts.

## Scope

Start with the locations the user names. Otherwise inspect the current repository, its registered worktrees, and relevant agent/package-manager homes that exist. Use `--root` for additional project parents and `--project-only` when agent homes are outside scope. Do not scan an entire home directory or filesystem by default.

Classify findings as:

- **Regenerable:** caches and build output reproducible from durable sources.
- **Review required:** dependencies, inactive worktrees, old logs, downloads, and retained run evidence.
- **Protected:** dirty or active worktrees, unpushed commits, credentials, configuration, current sessions, source repositories, databases, and user-authored artifacts.
- **Unknown:** ownership, activity, or recoverability cannot be established.

For Git worktrees, inspect registration, working-tree status, branch reachability, and associated pull-request state when available. For Kestrel-managed worktrees, defer to `/kestrel:cleanup`; do not bypass its lifecycle evidence. Never infer safety from age or size alone.

## Output

Report total measured bytes, largest categories and targets, confidence, exclusions, and a ranked reclaim plan. Distinguish immediately reclaimable space from space requiring review. Include exact paths, but never expose secret values.

Do not delete, prune, uninstall, kill processes, modify configuration, or write outside a temporary report requested by the user.
