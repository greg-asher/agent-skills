# Daily Exporter Current-State Discovery

The Daily Exporter turns incoming usage rows into one finance export each day. A scheduled Python job reads rows after the last checkpoint, normalizes account identifiers, aggregates daily totals, uploads a CSV file, and then advances the checkpoint.

Finance analysts consume the exported file in a separate reconciliation process. The repository documents a daily schedule but contains no retry dashboard.

The current flow can duplicate output after a partial failure. If the upload succeeds but the process stops before the checkpoint advances, the next run reads and exports the same rows again. The export client has no idempotency key. The checkpoint records only the last source row.

The job has no durable run state visible to finance users. Operators learn about failure from logs outside the application boundary. Manual reruns use the same job command and have the same duplicate risk.
