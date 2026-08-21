# Issue graph contract

The issue graph is the shared state between Planning, implementation, and review. Update it in place.

## Authority

Use the tracker, issue set, or issue URLs explicitly supplied for the invocation. Otherwise, use the local `implementation-queue.md` and linked issue files. Do not create a local mirror of an external tracker or a separate execution log.

If the tracker supports dependency or sub-issue relationships, use them. Otherwise, record explicit issue links in the issue body. Keep each issue in one state only.

## States

- `Ready`: All prerequisite issues are `Done`. The issue can enter an implementation wave now.
- `In progress`: The issue is selected for the current wave or has unresolved implementation work.
- `Blocked`: The issue cannot proceed because of a real prerequisite, external condition, or required Planning or Design decision.
- `Implemented`: The issue's implementation and wave checks passed. Independent review has not yet cleared it.
- `Done`: Independent review found no blocking defect, or all blocking repairs have passed review.

The `Ready` section is the current dependency-free frontier. Recompute it whenever a state or dependency changes.

## Graph changes

Implementation and review can clarify, split, combine, add, and rewire issues when the work reveals a more accurate graph. Preserve the original outcome, done conditions, and settled design commitments. Do not weaken an issue to declare success.

Add only genuine prerequisites. A dependency means the downstream issue cannot be completed correctly against the current system or a stable contract. Coordination preference and file contention do not create product dependencies.

When work contradicts a settled product outcome, block it and route the decision to Planning. When it contradicts a design commitment, block it and route the decision to Design.
