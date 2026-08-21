# Reliable Daily Export Product Brief

## Product Narrative

Finance needs one trustworthy usage export for each business date. The current scheduled job can upload a file and fail before advancing its checkpoint, causing the next run to export the same source rows again. The change makes each date a durable, visible export run that operators can recover without creating duplicate finance output.

## Outcomes and Delivery Boundary

Each business date has at most one completed export artifact. Operators can understand and recover failures without reading application logs. The change does not alter ingestion, normalization, aggregation, or downstream finance reconciliation rules.

## Defining Scenarios

### Automatic daily delivery

The schedule creates or resumes the durable run for the business date. The run progresses through pending, running, retrying, and completed. A completed date links to one stable current artifact. Transient failures retry automatically.

### Exhausted retries

After automatic retries are exhausted, the date remains failed with its latest failure information. A finance operator can start a manual retry. The retry uses the same logical run and artifact identity and cannot create a second completed artifact.

### Compatibility transition

The existing schedule first creates durable run records while the current export remains readable. Finance then moves to the stable artifact link. The old checkpoint-only path is removed only after completed and failed dates are visible through the new model.

## Business and Process Requirements

- Finance receives one completed export for each business date.
- A completed date is not automatically rerun.
- Finance operators can distinguish pending, running, retrying, completed, and failed dates.
- Failed dates preserve enough information for an operator to understand the latest failure and start a safe retry.
- Finance reconciliation continues to consume the same business data throughout the transition.

## Technology Requirements

- Each business date and export type has one durable run identity.
- The business date is the UTC calendar date of `usage_events.recorded_at`. The 05:00 UTC schedule targets the previous UTC date.
- The run stores attempt history, source range, stable artifact identity, state, and failure details.
- CSV creation uses durable staging and publication uses the stable artifact key for the run.
- The source checkpoint advances in the same database transaction that marks the run completed.
- Automatic and manual attempts reuse the run identity at the artifact boundary.
- The job claims one run at a time through a database lease.
- Automatic retry allows three attempts in total, waiting five minutes and then fifteen minutes. Network timeouts, temporary database unavailability, and temporary artifact-service errors are transient. Authentication, authorization, invalid source data, and exhausted attempts require operator action.
- Delivery follows expand, migrate, and contract phases and preserves the readable current export until finance has moved to the stable link.

## People and Operating Requirements

- Finance analysts continue the existing downstream reconciliation process.
- Finance operators use an internal Export Runs page protected by company single sign-on to review runs, open completed artifacts, and retry failed dates after automatic retries are exhausted.
- The `finance-export-operator` role controls retry access. The Finance Systems owner grants or removes it.
- Data Engineering owns the Export Runs page, job operation, and escalation for persistent failures.
- The delivery team must make the new run states and stable artifact link available before the old checkpoint-only path is removed.

## Success and Readiness

One business date cannot produce two completed finance artifacts. A retry after upload or checkpoint failure completes without duplicate output. Operators can identify and retry failed dates without reading application logs.

`Ready for issue creation`

## Source Artifacts

- Daily Exporter Current-State Discovery
- Reliable Daily Export Change Design
