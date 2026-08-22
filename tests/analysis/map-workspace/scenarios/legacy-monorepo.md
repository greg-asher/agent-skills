# Legacy monorepo scenario

The workspace has `apps/api`, `apps/worker`, `packages/contracts`, and `packages/billing`. The root architecture document says the API writes jobs directly to PostgreSQL. Current worker configuration declares `JOB_QUEUE_URL`, and tests publish `invoice.created` through a queue adapter. `packages/contracts` exports the shared event type. A checked-in `.env.example` names `JOB_QUEUE_URL` and `DATABASE_URL` without values.

The user wants a current workspace map, not a migration or refactor plan.
