# Manual production cutover

The release is locally validated. Company policy requires a release manager to promote the protected branch, enter production credentials in the provider dashboard, run the production deployment, and approve an irreversible schema cutover. A pre-cutover backup and a compatibility rollback are available before the schema cutover. Afterward, containment is possible but schema rollback is not. Completion requires provider deployment status, production version, migration status, health checks, and a user-visible smoke test. Evidence must not contain credential values.
