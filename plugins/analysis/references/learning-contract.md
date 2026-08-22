# Workspace learning contract

Game Show and Teach Me share `.analysis/learner-model.json`.

## Concept state

Track understanding by concept, not by isolated question text. Use these states:

- `unassessed`: no useful evidence yet
- `emerging`: partial or inconsistent understanding
- `practiced`: correct understanding demonstrated once with meaningful reasoning
- `demonstrated`: correct understanding demonstrated repeatedly or applied successfully
- `disputed`: the user challenged the assessment or its evidence needs review

Record whether evidence came from Game Show, Teach Me, observed work, or a user correction. Distinguish correct, partial, incorrect, uncertain, skipped, and ambiguous outcomes. An ambiguous question does not count against the learner.

## Persistence and correction

Persist learner history across threads and tasks in the same workspace. Do not carry it to another workspace automatically.

Teach Me owns direct correction. A user may inspect, dispute, correct, or remove a learner signal in natural language. Preserve the correction and its reason. Do not treat one incorrect answer as permanent ignorance, and do not infer mastery from a guessed answer without supporting reasoning.

## Grounding

Every assessed or taught concept must trace to current workspace evidence. Prefer consequential architecture, workflow, boundary, state, and change concepts. Avoid incidental filename, command, or syntax trivia unless the detail changes safe operation.
