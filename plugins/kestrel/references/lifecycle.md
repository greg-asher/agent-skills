# Kestrel lifecycle contract

Use `${CLAUDE_PLUGIN_ROOT}/bin/kestrel-plugin` in Claude Code. In Codex, resolve `bin/kestrel-plugin` from the installed Kestrel plugin root.

Pass task content through `--task-file`, or use `--task` when the plugin should persist the exact task content into durable evidence. Pass validation as a JSON file containing argument arrays through `--validation-file`; commands are spawned directly without a shell. Pass `--state-dir` when the host provides an explicit plugin-data directory. Otherwise the executable uses `${CLAUDE_PLUGIN_DATA}/kestrel` in Claude Code and `${CODEX_HOME:-~/.codex}/plugin-data/kestrel` in Codex.

`--state-dir` is the plugin evidence root and the exact value passed to Kestrel as `KESTREL_HOME`. The plugin never passes a Kestrel `--state-dir` flag. Its child environment overwrites inherited `KESTREL_HOME` and removes inherited `KESTREL_CORE_HOME` plus obsolete plugin-created `KESTREL_*_DIR` variables. Local Core derives its own canonical epoch-scoped paths; the wrapper does not provision worktrees itself.

`kestrel-plugin doctor --workspace <root> --state-dir <path>` checks the committed `HEAD`, Git metadata, Kestrel 0.8.8-or-newer compatibility, the plugin evidence root, actual Local Core health under `KESTREL_HOME`, worktree support, active sessions, and evidence health. Assignment performs the same preflight and a real `job preflight` for `job_input_v2`, `cli_dev_local`, `dev`, and `exec_command`. It returns `SETUP_REQUIRED` or `COMPATIBILITY_ERROR` before invoking `job run` when setup is not safe.

Executable selection is deterministic: explicit `--kestrel-bin`, then a compatible absolute realpath persisted in `setup.json`, then the first `kestrel` on `PATH`. An explicit incompatible selection is authoritative and is never replaced. Approved npm installation resolves the installed executable from `npm prefix -g`, verifies it, and persists that realpath, detected version, minimum version, V2 capability, and verification time. Later commands reuse the persisted realpath even when another package manager shadows `kestrel` on `PATH`.

Lifecycle states are `RUNNING`, `WAITING`, `FAILED`, `INTERRUPTED`, `SETUP_FAILED`, `COMPLETED_ISOLATED`, `INTEGRATED`, and `CLEANED`. Durable evidence lives under `runs/<session>/` as `manifest.json`, `input.json`, `task.json`, `output.json`, optional `daemon-error.txt`, and any doctor evidence. A structured `job_run_rejection_v1` is retained as a durable `COMPATIBILITY_ERROR`. Manifests record the state directory, source revision, binding evidence, failure phase/class, recovery command, worktree creation status, and cleanup safety.

Exit code 0 means the requested operation completed, 2 means approval or operator input is required, 3 means installation or platform setup is required, and 4 means incompatible Kestrel or binding evidence. Never report a terminal outcome from process existence alone.

No lifecycle command authorizes pushing, pull requests, remote merges, deployments, production changes, or deletion of durable evidence.
