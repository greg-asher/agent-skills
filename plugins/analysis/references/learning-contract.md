# Workspace learning contract

Game Show and Teach Me share `.analysis/learner-model.json`.

## Learning goals

Persist a learning goal only when the user intends to learn across sessions. Record its purpose, the capability the user wants to gain, its active, paused, or completed status, and current trusted resource links. Keep a one-session request in the current conversation rather than adding durable state.

Learning goals are optional so existing learner models remain valid. Do not turn the learner model into a curriculum or infer a long-term mission from one request.

## Concept state

Track understanding by concept, not by isolated question text. Use these states:

- `unassessed`: no useful evidence yet
- `emerging`: partial or inconsistent understanding
- `practiced`: correct understanding demonstrated once with meaningful reasoning
- `demonstrated`: correct understanding demonstrated repeatedly or applied successfully
- `disputed`: the user challenged the assessment or its evidence needs review

Record whether evidence came from Game Show, Teach Me, observed work, or a user correction. Distinguish correct, partial, incorrect, uncertain, skipped, and ambiguous outcomes. An ambiguous question does not count against the learner.

One meaningful success can establish `practiced`. Reserve `demonstrated` for repeated correct reasoning or successful application across time or different workflows. Use retrieval after intervening material and application in a changed context when they advance the user's goal; do not manufacture repetitive quizzes.

## Persistence and correction

Persist learner history across threads and tasks in the same workspace. Do not carry it to another workspace automatically.

Teach Me owns direct correction. A user may inspect, dispute, correct, or remove a learner signal in natural language. Preserve the correction and its reason. Do not treat one incorrect answer as permanent ignorance, and do not infer mastery from a guessed answer without supporting reasoning.

## Grounding

Every assessed or taught concept must trace to current workspace evidence. Prefer consequential architecture, workflow, boundary, state, and change concepts. Avoid incidental filename, command, or syntax trivia unless the detail changes safe operation.

Use current primary sources when an external concept, platform, standard, or practice materially affects the lesson. Workspace behavior still requires workspace evidence. Save trusted resource links on a persistent learning goal only when they are useful across sessions.
