---
name: assign
description: Assign a bounded repository task to Kestrel for autonomous implementation and validation in a managed worktree. Use when the user explicitly invokes /kestrel:assign with an issue, task, or implementation outcome they want Kestrel to complete.
disable-model-invocation: true
---

# Assign Work to Kestrel

Hand one implementation assignment to Kestrel and stay with it until Kestrel returns a terminal result. Do not implement the same task yourself.

Treat this invocation context as the starting point:

`$ARGUMENTS`

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before writing the assignment or reporting the result.
Read [the shared Kestrel lifecycle contract](../../references/lifecycle.md).

## 1. Establish the assignment

Use the current Claude project unless the user names another repository. Resolve its Git root.

If the arguments name an issue file, read the complete issue. Follow its linked Product Brief or design only when the issue does not contain enough context to execute correctly. Treat the issue as the assignment authority.

If the arguments describe the work directly, compile a concise self-contained assignment containing:

- the useful outcome
- the behavior or repository change to make
- settled constraints and boundaries
- observable completion conditions
- the validation that proves completion

Preserve exact paths, commands, requirements, and exclusions supplied by the user. Do not add a new planning phase, redesign the solution, or pad the assignment with generic engineering advice.

Kestrel receives the committed `HEAD` through a managed worktree. If the assignment depends on uncommitted local changes that are not captured in the task, stop and identify that dependency instead of handing Kestrel an incomplete repository state.

## 2. Submit the work

Write the complete assignment to a unique temporary Markdown file. Keep user content out of shell arguments.

Run the plugin executable:

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/kestrel-plugin" assign \
  --workspace "<absolute-git-root>" \
  --task-file "<absolute-task-file>" \
  --state-dir "${CLAUDE_PLUGIN_DATA}/kestrel"
```

Use `--profile <id>` only when the user supplies an override. The wrapper always requires the resolved `cli_dev_local` preset and `dev` approval pack for managed repository work.

Before it creates an assignment, the wrapper runs the read-only Kestrel job preflight. A missing `exec_command`, wrong preset, or incompatible Kestrel returns `SETUP_REQUIRED` or `COMPATIBILITY_ERROR` without creating a managed worktree. The wrapper submits `job_input_v2` with:

- build interaction mode
- full-auto execution
- noninteractive completion
- a session-isolated managed worktree
- durable input and output files
- the immutable profile identity returned by preflight
- host `exec_command` for repository implementation; never sandbox `code.execute`
- any validation argument arrays rendered exactly into the assignment

Let the command reach a terminal result. If the shell moves a long-running process into the background, continue monitoring that process instead of starting another assignment.

## 3. Report the result

Read the durable output JSON named by the wrapper.

For a completed assignment, report:

- what Kestrel completed
- the validation Kestrel reports
- the session, thread, and run identifiers
- the assignment directory
- the managed worktree or changed-files location when the output identifies it
- the replay command

For a failed or waiting assignment, report the specific blocker or failure, the durable manifest and output paths, and the replay and doctor commands. Do not describe a started process as completed work.

Do not merge, push, publish, or continue implementing locally unless the user separately asks for that action.
