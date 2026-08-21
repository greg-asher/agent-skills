# Wave orchestration

## Form a coherent wave

Start from the ready frontier. A wave is coherent when its issues share an outcome or integration boundary and the combined change can be reviewed as one unit.

Prefer a smaller wave when issues create a broad review surface, interact through unstable contracts, or compete for the same files. Include multiple issues when their ownership is disjoint and landing them together proves a useful combined behavior.

## Assign work

Give each `execution:issue-worker` a complete, bounded assignment. Name the worker's owned behavior, files, interfaces, and tests. State what another worker may change and how the results must integrate.

Run workers concurrently only when their edits are disjoint or safely composable. Sequence work that changes shared types, schemas, migrations, state machines, generated files, or public contracts. File contention can require sequencing without becoming an issue dependency.

## Integrate results

Require each worker to report changed files, behavior delivered, checks run, failures, assumptions, and graph discoveries. The lead inspects the actual changes, resolves seams, and runs combined checks.

Do not mark an issue `Implemented` because a worker reports success. Mark it only after the integrated wave satisfies the issue's observable done conditions.

## Commit the wave

Create one commit only after the complete successful wave is integrated. Include code, tests, and local graph changes for that wave. Stage explicit paths and leave unrelated edits untouched. Follow repository conventions and include the issue identifiers in the commit message.

Do not commit a failed wave. Leave its issues `In progress` or `Blocked` and explain what remains.
