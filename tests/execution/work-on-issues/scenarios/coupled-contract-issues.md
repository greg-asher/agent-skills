# Coupled contract issues

The local queue contains two Ready issues:

- `EX-201` Add `artifactVersion` to the public export-completed event in `src/events.ts` and migrate existing persisted events in `migrations/014-events.sql`.
- `EX-202` Make the notification consumer require `artifactVersion`. It changes `src/events.ts`, `src/notify.ts`, and the mixed-version compatibility tests.

Both issues are product-ready, but they share the event contract, compatibility window, migration order, and one source file. The consumer must continue to process events produced by the version deployed immediately before the migration. The combined check is `npm test`.
