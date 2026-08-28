# Shared complete-flow defect

`EX-1201` is Implemented by commit `abc1201`. It promises that resumed and retried exports preserve one stable artifact identity and publish one downloadable result.

Reviewers report three symptoms:

- `src/export-producer.ts` omits `artifactIdentity` when a suspended export resumes.
- `src/export-event.ts` permits the identity to be absent from the completion DTO.
- `src/export-store.ts` generates a new identity when the field is absent, while `src/downloads.ts` publishes every stored completion.

The permitted resume path crosses all four components. The missing identity propagates from the producer through the DTO and persistence layer to duplicate downloadable results. The findings share one violated identity guarantee and require one coordinated repair across the affected flow.
