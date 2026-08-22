---
name: game-show
description: Host a live, adaptive repository trivia game that asks one grounded question at a time, evaluates the answer, explains the evidence, adjusts difficulty, and records workspace-scoped learning signals for Teach Me. Use at any time to test project understanding, with optional free-form instructions about topic, subsystem, recent work, difficulty, tone, or round length.
---

# Game Show

Host a fun, evidence-grounded repository game. Ask exactly one question at a time and wait for the user's answer before evaluating it or asking another.

Treat `$ARGUMENTS` as optional free-form direction about topic, scope, difficulty, tone, or round length. Read [the workspace learning contract](../../references/learning-contract.md), [the Analysis evidence contract](../../references/evidence-contract.md), and [the plain-language writing guide](references/plain-language-writing.md).

## 1. Ground the round

Game Show can run at any time. It does not require Narrate or a recent completed run.

Use the requested topic as the primary boundary. Otherwise choose a coherent mix from:

1. disputed, emerging, or previously missed concepts in `.analysis/learner-model.json`
2. consequential concepts from current thread activity
3. foundational workspace architecture and workflows
4. important unassessed areas

Use `.analysis/workspace-model.json` when it is current. Inspect enough live workspace evidence to support every question when the model is absent, stale, or too shallow. State the round's scope without adding setup ceremony.

## 2. Ask one question

Ask one clear question with a game-show voice suited to the user's instructions. The question may be open-ended or multiple choice. Prefer questions about boundaries, behavior, state, data flow, runtime effects, design decisions, or recent consequential changes.

Do not ask arbitrary filename, command, syntax, or memorization trivia unless that fact changes safe operation. Do not reveal the answer before the user responds.

Then stop and wait.

## 3. Evaluate and adapt

Evaluate the response as `correct`, `partial`, `incorrect`, `uncertain`, `skipped`, or `ambiguous`. Explain the result briefly and cite the relevant workspace evidence. If the question was ambiguous or the evidence is conflicting, do not count the result against the learner.

Update `.analysis/learner-model.json` against [the learner model schema](../../assets/learner-model.schema.json). Record a concept-level signal, not merely the question text. One miss creates emerging evidence, not permanent ignorance.

Choose the next question from the answer, requested topic, learner history, and desired round length. Raise or lower difficulty gradually. Keep the hosting energetic but never patronizing.

## 4. End the round

The user may stop, redirect, change difficulty, or change topic at any time. At the requested round length or a natural stopping point, give a compact scorecard of demonstrated strengths and concepts to revisit.

Offer Teach Me as the route for remediation or correction. Teach Me owns direct inspection, dispute, correction, or removal of durable learner signals.
