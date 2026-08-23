# Kestrel lifecycle contract

Use `${CLAUDE_PLUGIN_ROOT}/bin/kestrel-plugin` in Claude Code. In Codex, resolve `bin/kestrel-plugin` from the installed Kestrel plugin root.

Pass task content through `--task-file`, never through a shell argument. Pass validation as a JSON file containing argument arrays through `--validation-file`; commands are spawned directly without a shell. Pass `--state-dir` when the host provides an explicit plugin-data directory. Otherwise the executable uses `${CLAUDE_PLUGIN_DATA}/kestrel` in Claude Code and `${CODEX_HOME:-~/.codex}/plugin-data/kestrel` in Codex.

Lifecycle states are `RUNNING`, `WAITING`, `FAILED`, `INTERRUPTED`, `COMPLETED_ISOLATED`, `INTEGRATED`, and `CLEANED`. Durable evidence lives under `runs/<session>/` as `manifest.json`, `input.json`, `output.json`, and any doctor evidence.

Exit code 0 means the requested operation completed, 2 means approval or operator input is required, 3 means installation or platform setup is required, and other nonzero results are failures. Never report a terminal outcome from process existence alone.

No lifecycle command authorizes pushing, pull requests, remote merges, deployments, production changes, or deletion of durable evidence.
