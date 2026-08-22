# Latest completed run contract

Narrate analyzes the latest substantive work run in the current thread.

The run begins with the user request or durable goal that initiated the latest coherent objective. It ends with the terminal response immediately before Narrate was invoked. It may span automatic continuations, compaction, waits, retries, subagents, tool calls, additive user steering, and several internal turns.

Include relevant:

- user intent and later refinements that did not replace it
- investigation, implementation, and validation activity
- delegated work and reconciliation
- failed attempts, reversals, blockers, and consequential decisions
- files, commits, artifacts, external results, and terminal evidence

Exclude earlier completed objectives, unrelated task history, and Analysis-only invocations. Narrate, Game Show, and Teach Me do not advance the latest substantive work-run boundary.

Prefer explicit goal or run metadata when available. Otherwise infer the boundary from the initiating request, objective continuity, activity, and terminal result. When the boundary or coverage is materially ambiguous, state what was included and what could not be reconstructed.
