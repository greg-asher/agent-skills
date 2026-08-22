# Ambiguous Game Show answer

The question asks which component owns retries. Application code declares a worker-local retry count, while current deployment configuration declares platform retries. The evidence does not establish which setting wins in production. A later unambiguous question asks which package owns the shared event type; the learner answers `apps/api`, but current exports establish `packages/contracts`.
