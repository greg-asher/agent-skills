# Kestrel lifecycle contract

Use `${CLAUDE_PLUGIN_ROOT}/bin/kestrel-plugin` in Claude Code. In Codex, resolve `bin/kestrel-plugin` from the installed Kestrel plugin root.

Pass task content through `--task-file`, or use `--task` when the plugin should persist the exact task content into durable evidence. Pass validation as a JSON file containing argument arrays through `--validation-file`; commands are spawned directly without a shell. Pass `--state-dir` when the host provides an explicit plugin-data directory. Otherwise the executable uses `${CLAUDE_PLUGIN_DATA}/kestrel` in Claude Code and `${CODEX_HOME:-~/.codex}/plugin-data/kestrel` in Codex.

`--state-dir` is authoritative for the whole runtime. The plugin derives `core/`, `core/logs/`, `sockets/`, `leases/`, `runtime/`, and `worktrees/` beneath it, passes `--state-dir` to Kestrel, and exports `KESTREL_STATE_DIR`, `KESTREL_CORE_STATE_DIR`, `KESTREL_CORE_LOG_DIR`, `KESTREL_SOCKET_DIR`, `KESTREL_LEASE_DIR`, `KESTREL_RUNTIME_DIR`, and `KESTREL_MANAGED_WORKTREE_DIR` to child processes. Local Core must consume this contract; the wrapper does not provision worktrees itself.

`kestrel-plugin doctor --workspace <root> --state-dir <path>` checks the committed `HEAD`, Git metadata, Kestrel capabilities, Node/platform compatibility, all derived state paths, Local Core availability, worktree support, active sessions, leases, and evidence health. Assignment performs the same writable-state preflight and returns `SETUP_FAILED` with `noMutation` evidence before invoking `job run` when setup is not safe.

Lifecycle states are `RUNNING`, `WAITING`, `FAILED`, `INTERRUPTED`, `SETUP_FAILED`, `COMPLETED_ISOLATED`, `INTEGRATED`, and `CLEANED`. Durable evidence lives under `runs/<session>/` as `manifest.json`, `input.json`, `task.json`, `output.json`, optional `daemon-error.txt`, and any doctor evidence. Manifests record the state directory, derived runtime configuration, source revision, failure phase/class, recovery command, worktree creation status, and cleanup safety.

Exit code 0 means the requested operation completed, 2 means approval or operator input is required, 3 means installation or platform setup is required, and other nonzero results are failures. Never report a terminal outcome from process existence alone.

No lifecycle command authorizes pushing, pull requests, remote merges, deployments, production changes, or deletion of durable evidence.
