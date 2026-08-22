# Incremental refresh scenario

`.analysis/workspace-model.json` was generated at revision `abc123`. The current revision is `def456`. Only `packages/contracts` and its tests changed, but the saved model has relationships from that package to the API, worker, and billing package. The refresh must preserve evidence outside the affected relationship closure and state any surfaces it could not recheck.
