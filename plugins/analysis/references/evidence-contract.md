# Analysis evidence contract

All Analysis skills share the same evidence vocabulary and workspace boundary.

## Evidence levels

- **Observed current:** directly inspected in the current workspace or run.
- **Demonstrated by test:** a current test or safe runtime observation establishes the behavior.
- **Static analysis:** code structure, symbols, imports, calls, types, or configuration establish a relationship but not runtime activity.
- **Declared:** documentation, configuration, or a participant states the claim.
- **Inferred:** the analysis connects evidence without direct proof.
- **Unknown:** available evidence does not establish the claim.

Put evidence next to the claim it supports. Include a relative path and the most precise useful locator. Never convert static reachability into a claim of runtime use.

## Shared workspace state

Use `.analysis/` at the workspace root:

- `.analysis/workspace-model.json`: revision-scoped machine-readable workspace model.
- `.analysis/workspace-map.md`: concise human navigation view derived from the model.
- `.analysis/learner-model.json`: workspace-scoped learning history.
- `.analysis/blast-radius/<change-slug>.json`: machine-readable change-impact result.
- `.analysis/blast-radius/<change-slug>.md`: readable impact report and context pack.

Follow another established workspace convention when it clearly owns analysis artifacts. Do not write generated analysis into application source folders.

## Freshness

Record the current Git revision when available. Otherwise record file fingerprints or modification evidence sufficient to describe the snapshot. Before reusing a model, compare its revision and covered sources with the current workspace. Refresh affected relationships instead of silently using stale evidence.

Current implementation, tests, runtime configuration, and direct observation outrank stale narrative documentation. Preserve conflicts rather than choosing silently.

## Safety and privacy

- Record environment-variable names and their roles, never secret values.
- Do not copy credentials, tokens, private keys, complete environment dumps, or sensitive terminal output into Analysis artifacts.
- Prefer interface summaries and evidence references to raw file bodies.
- Keep learner history inside its workspace. Do not transfer it to another workspace automatically.
- Analysis is read-only with respect to product code, runtime systems, providers, and deployments. Generated `.analysis/` artifacts are the only default workspace mutation.
