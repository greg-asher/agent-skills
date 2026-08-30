# Change-specific review strategy

## Start from intended behavior

Review the implementation against the selected issue text and observable done conditions. Trace each affected workflow from its trigger through the participating components to its observable result. Treat tests as evidence, not as the definition of correctness.

Classify an original implementation issue as an initial review and a repair issue created by an earlier review as a closure review. Initial review examines the change-specific risk surface broadly. Closure review verifies the repair's named guarantee, established affected flow, done conditions, required validation, and directly changed shared boundaries. It does not restart broad risk discovery.

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

During closure review, choose ordinary and adversarial probes only when they can falsify the named repair guarantee, required validation, or behavior of the established affected flow or a directly changed shared boundary. Do not expand into adjacent edge cases merely because they are reachable.

## Confirm and classify

A defect needs a permitted input or reachable state, a complete path through the actual code, and an observable failure. Reproduce it when practical. A static trace is enough when every link is established by the issue, contract, caller, or code. Do not invent an input contract, deployment condition, or external behavior to complete the path. The first incorrect component starts the investigation; it does not by itself define the repair boundary.

Reconcile every reviewer result before editing the issue graph. During initial review, combine findings into one repair issue when restoring the intended behavior requires the same coordinated change. During closure review, extend the active graph only when the named repair still fails, required validation fails, a settled constraint within the repair boundary is violated, or the repair materially regresses the established affected flow or a shared boundary it changed. A material regression changes that flow's observable result, integrity, authorization, durability, or recoverability. Report other concrete closure observations in the synthesis only, even when they are reachable or caused by the repair.

For every admitted finding, identify each component that must change across the complete affected flow. Describe the guarantee the repair must restore without choosing an implementation mechanism that the settled design does not require.

A blocking defect prevents the reviewed issue's promised outcome, violates a settled constraint, risks data or authorization integrity, or makes operation unsafe. During initial review, a non-blocking regression caused by the reviewed change can be repaired independently. During closure review, only a material regression admitted under the closure rule can enter the active graph independently. Report other closure observations and pre-existing or unrelated non-blocking defects without adding them to the active issue graph.

Do not file style preferences, speculative hardening, or a different product or architecture choice as defects.
