# Change-specific review strategy

## Start from intended behavior

Review the implementation against the selected issue text and observable done conditions. Trace the affected workflows through the diff and surrounding system. Treat tests as evidence, not as the definition of correctness.

## Ordinary review

Check the expected path, input and output handling, state changes, integration contracts, regressions, compatibility, error handling, and test quality. Look for code that satisfies a unit test but breaks the end-to-end outcome.

## Adversarial review

Choose rare-state probes from the actual change. Relevant risks can include:

- duplicate, delayed, reordered, or retried work
- concurrency and lost updates
- partial writes and interrupted workflows
- stale caches, replicas, sessions, or external data
- migration order and mixed-version compatibility
- authorization at alternate entry points
- dependency outages, timeouts, and recovery
- cleanup, rollback, replay, and restart behavior

Do not force every category onto every change.

## Confirm and classify

A defect needs a permitted input or reachable state, a complete path through the actual code, and an observable failure. Reproduce it when practical. A static trace is enough when every link is established by the issue, contract, caller, or code. Do not invent an input contract, deployment condition, or external behavior to complete the path.

Reconcile every reviewer result before editing the issue graph. Merge duplicate symptoms into one repair issue when they share a cause and repair boundary. Describe the guarantee the repair must restore without choosing an implementation mechanism that the settled design does not require.

A blocking defect prevents the reviewed issue's promised outcome, violates a settled constraint, risks data or authorization integrity, or makes operation unsafe. A non-blocking defect is real but does not prevent the completed outcome and can be repaired independently.

Do not file style preferences, speculative hardening, or a different product or architecture choice as defects.
