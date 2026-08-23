---
name: manage-memory
description: Diagnose and reduce RAM or swap pressure from Codex, Claude Code, Kestrel, development servers, containers, and repository tooling without disrupting active work. Use when the user explicitly invokes /utilities:manage-memory or asks this plugin to investigate process memory.
disable-model-invocation: true
---

# Manage Memory

Diagnose process-memory pressure first, then take only the smallest explicitly authorized action that preserves active work.

Read [the plain-language writing guide](references/plain-language-writing.md).

## Diagnose

Capture current physical memory, swap or pressure state, and the largest resident processes using platform-native read-only tools. Group related process trees and identify their command, parent, owner, working directory when available, elapsed time, and whether they are tied to Codex, Claude Code, Kestrel, a dev server, test runner, language server, container, or repository.

Do not label ordinary filesystem cache as a leak. Distinguish sustained process growth, many abandoned duplicate processes, intentional build/test load, container allocation, and operating-system cache. Sample again when one snapshot cannot establish the pattern.

## Act safely

Read-only diagnosis is automatic. Before stopping or restarting anything, name the exact process tree, its repository or session association, current memory, likely user impact, and expected recovery. Require explicit approval unless the user already named that exact process or service for termination.

Prefer graceful, native shutdown. Stop children before parents only when the application requires it. Escalate signals gradually and verify exit. Never kill the Codex or Claude host serving the current conversation, an active Kestrel job, an editor with unsaved state, a database, or an unidentified process merely because it is large.

Do not change persistent runtime limits, container allocations, startup configuration, or operating-system settings without a separate explicit request.

## Report

Report the pressure diagnosis, largest relevant process trees, evidence for suspected leaks or abandonment, actions taken, memory recovered, and anything intentionally left running. If no safe action is justified, say so and give the next observation needed.
