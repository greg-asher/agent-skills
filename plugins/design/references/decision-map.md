# Local decision-map protocol

A decision map is an escalation artifact for uncertainty that no longer fits a compact notebook frontier. It resolves decisions; it does not plan or execute implementation.

## Escalation test

Keep the ordinary notebook frontier when the remaining questions can be resolved coherently in the current session.

Escalate when one or more of these conditions materially affects the work:

- the uncertainty must remain coherent across multiple sessions
- decisions have real blocking relationships
- independent research or participant decisions can proceed in parallel
- the notebook frontier can no longer summarize the open decisions without losing dependencies or context

Do not create a map merely because several questions exist.

## Storage

Create a `decisions/` directory beside the owning notebook:

- Discovery: `.discovery/<slug>/decisions/`
- Design: `.design/<slug>/decisions/`

Use `map.md` as the index. Store each decision as `<NN>-<decision-slug>.md`. Keep all artifacts local. Do not create or update tracker issues.

## Map contract

The map contains:

- **Destination:** the settled state the map must reach
- **Ready frontier:** decisions with no unresolved blockers
- **Blocked decisions:** decisions and the unresolved decisions blocking them
- **Unresolved fog:** important uncertainty that cannot yet be expressed as a decision
- **Resolved decisions:** a one-line result linked to the authoritative decision file
- **Return condition:** what the owning notebook can do when the map is complete

The map is an index. A decision's evidence, alternatives, and full resolution live only in its decision file.

## Decision contract

Each decision file contains:

- status: `ready`, `blocked`, or `resolved`
- the decision question
- why it matters to the destination
- blockers by linked decision name
- relevant evidence and uncertainty
- credible options and distinguishing tradeoffs
- the resolution, rationale, and confidence when settled
- effects on the owning notebook and other decisions
- the condition that would justify reopening it

## Work the map

1. Name the destination and return condition.
2. Create only decisions that can be stated precisely now.
3. Add blocking links after the decision files exist.
4. Keep unformed uncertainty in fog until another resolution makes it precise.
5. Resolve one coherent decision or tightly coupled decision cluster at a time.
6. Update affected blockers, frontier, fog, and notebook views immediately.
7. Run independent evidence gathering in parallel only when it cannot change another task's question.
8. When the destination is reached, synthesize the resolved decisions into the owning notebook and continue its normal workflow.

Never turn decision files into implementation tickets, publish them to a tracker, or proceed directly from the map to implementation. The Product Brief and issue-planning boundaries remain unchanged.
