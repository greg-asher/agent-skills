# Closure review finds a material regression

`REPAIR-1601` was created by the initial review of `EX-1601`. It restores stable identity for resumed and retried exports. The established affected flow includes the resume producer, completion DTO, shared completion persistence, and download consumer.

The repair is Implemented. Its focused identity checks and resume-and-retry complete-flow scenario pass. To preserve one row, the repair changes the shared `saveCompletion` conflict path used by resumed and ordinary exports.

For an ordinary export without resume metadata, the new conflict update writes a null download URL over the completed row. The export remains marked complete but its download returns not found. The permitted ordinary path crosses the shared persistence boundary changed by the repair, and the repository's ordinary-export integration check now fails.
