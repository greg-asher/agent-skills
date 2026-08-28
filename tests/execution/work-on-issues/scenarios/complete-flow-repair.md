# Complete-flow repair wave

`REPAIR-601` is Ready. It restores the guarantee that resumed and retried exports preserve one stable artifact identity and publish one downloadable result.

The confirmed affected flow crosses `src/export-producer.ts`, `src/export-event.ts`, `src/export-store.ts`, and `src/downloads.ts`. The producer must emit the identity on resume, the DTO must require it, persistence must preserve one record for it, and the consumer must publish that stable record. These components share the event contract and cannot be repaired as independent local issues.

Focused checks cover each component. The required complete-flow scenario resumes an export, retries its completion event, and asserts one stable stored and downloadable artifact. The repository check is `npm test`.
