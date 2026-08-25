---
name: narrate
description: Turn the latest completed agent work run in the current thread into a short, engaging, easy-to-read narrative that explains the objective, turning points, decisions, changes, validation, failures, and remaining work. Use immediately after a large or long-running turn, goal, or multi-agent run when the user wants to catch up without rereading the transcript or tool log.
license: MIT
---

# Narrate

Tell the story of the latest completed substantive work run in this thread. Treat `$ARGUMENTS` as optional guidance about audience, emphasis, or tone.

Read [the latest completed run contract](../../references/thread-run-contract.md), [the Analysis evidence contract](../../references/evidence-contract.md), and [the plain-language writing guide](references/plain-language-writing.md).

## 1. Reconstruct the run

Infer the latest completed run across the full available thread, not only the final assistant message. Follow explicit goal or run metadata when available. Include relevant continuations, tool activity, subagents, retries, failures, user steering, validation, artifacts, and terminal results.

Use current diffs, commits, generated artifacts, test output, or provider results to corroborate the thread when useful. Do not expand into unrelated repository analysis.

If compaction or inaccessible activity prevents full reconstruction, state the exact coverage limit. Never invent missing steps or motivations.

Organize the reconstructed activity against [the completed run schema](../../assets/run-model.schema.json) before writing. Keep this model in working context unless the user explicitly asks to save it.

## 2. Find the story

Identify:

- what the user needed and why the run mattered
- the central tension or hard problem
- the two or three turning points that changed the direction
- what actually changed or was established
- how the result was verified
- what remains unresolved or consequential

Separate intended work, attempted work, completed work, and validated outcomes. Include a failed attempt only when it explains a decision, constraint, or result.

## 3. Write the narrative

Write a strong title followed by a short post, usually four to eight compact paragraphs. Lead with the outcome. Use chronological order when the evolution matters; otherwise organize around the main idea and consequence.

Make the writing lively, concrete, and easy to read without becoming promotional, theatrical, or cute. Explain unfamiliar technical terms. Mention exact files, tests, commits, counts, and limitations only when they help the reader understand the story.

Do not produce:

- a tool-call transcript
- a commit-by-commit changelog
- a generic status template
- invented dialogue or internal reasoning
- a long checklist disguised as prose

End with the meaningful current state, not a ceremonial conclusion. Return the narrative in the thread. Do not create or modify workspace files unless the user explicitly asks to save it.
