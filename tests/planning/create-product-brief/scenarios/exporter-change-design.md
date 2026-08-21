# Reliable Daily Export Change Design

## Proposed change

Make each business-date export a durable run with one stable identity. Automatic retries and manual reruns must resume or reproduce the same logical export rather than create another finance artifact.

## Product behavior

Finance operators can see each business date as pending, running, retrying, completed, or failed. A completed date links to exactly one current export artifact. A failed date shows the last failure and offers a manual retry. A retry does not create a second completed artifact for the same date.

The scheduler retries transient failures automatically. After the retry limit, the run remains failed until an operator retries it. A completed run is not automatically rerun.

The business date is the UTC calendar date of `usage_events.recorded_at`. The 05:00 UTC schedule targets the previous UTC business date.

Automatic retry allows three attempts in total, with waits of five minutes and then fifteen minutes. Network timeouts, temporary database unavailability, and temporary artifact-service errors are transient. Authentication, authorization, invalid source data, and exhausted attempts leave the run failed for operator action.

Finance operators use an internal Export Runs page protected by company single sign-on. The `finance-export-operator` role can inspect runs, open completed artifacts, and retry failed runs. The Finance Systems owner grants or removes the role. Data Engineering owns the page, job operation, and escalation for persistent failures.

## Design delta

Add an export run record keyed by business date and export type. Store attempt history, source range, artifact identity, state, and failure details. Build the CSV in durable staging and publish it under a stable artifact key. Advance the source checkpoint in the same database transaction that marks the run completed.

Use the run identity as the idempotency key at the artifact boundary. A new attempt for an existing run reuses the stable artifact identity. The job claims one run at a time through a database lease.

## Compatibility

During expansion, the existing schedule creates run records but the current export remains readable. During migration, finance switches to the stable artifact link. The old checkpoint-only path is removed after completed and failed dates are visible through the new run model.

## Boundary

The change does not redesign incoming usage ingestion, account normalization, daily aggregation rules, or the downstream finance reconciliation process.
