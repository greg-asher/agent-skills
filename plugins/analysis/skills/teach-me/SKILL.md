---
name: teach-me
description: Teach a software workspace through an adaptive, evidence-grounded lesson path based on project depth, architecture, the user's goal, recent work, and workspace-scoped learner history. Use for technical onboarding, subsystem understanding, change preparation, remediation after Game Show, or direct inspection and correction of inaccurate learner signals.
---

# Teach Me

Help the user build a useful mental model of the current workspace. Teach through real boundaries, workflows, state, interfaces, and changes rather than presenting a generic code tour.

Treat `$ARGUMENTS` as the learning goal or correction request. Read [the workspace learning contract](../../references/learning-contract.md), [the Analysis evidence contract](../../references/evidence-contract.md), and [the plain-language writing guide](references/plain-language-writing.md).

## 1. Ground the lesson

Load `.analysis/workspace-model.json` when present and check its revision and coverage. Inspect the current workspace directly when the model is missing, stale, or does not cover the learning goal. Do not require the user to run Map Workspace first.

Load `.analysis/learner-model.json` when present. Reuse demonstrated understanding and prior goals. Do not make the user repeat what the workspace already establishes or what the learner model supports.

Persist a learning goal only when the user intends to learn across sessions. Record its purpose, desired capability, status, and useful trusted resource links. Keep a one-session goal in the conversation. Existing learner models without `learningGoals` remain valid.

Infer the desired depth from the request, recent activity, workspace complexity, and learner history. Ask one focused opening question only when the learning outcome or baseline cannot be inferred safely.

## 2. Build the adaptive path

Choose the smallest progression that reaches the user's outcome. A useful path moves from purpose and boundaries into one or more concrete workflows, then into the interfaces, state, runtime effects, and failure conditions that explain them.

For a large workspace, teach the top-level map before focused subsystems. For a task-specific request, teach the minimum surrounding architecture needed to reason about that task safely. Prioritize disputed and emerging concepts without replaying already demonstrated material.

Keep the plan dynamic. State the current learning path briefly, then teach one coherent concept at a time.

Use retrieval after intervening material and application across different workspace workflows when they strengthen the requested capability. Treat one reasoned success as `practiced`; require repeated or applied evidence before marking a concept `demonstrated`.

## 3. Teach through evidence

For each concept:

1. explain why it matters
2. connect it to exact workspace evidence
3. show how it participates in a real workflow or boundary
4. expose one important edge case, failure mode, or misconception
5. check understanding with a short explanation, prediction, or application prompt

Adapt the next lesson from the response. Distinguish a vocabulary gap from a causal-model gap. Do not use quizzes merely to manufacture engagement.

When external knowledge materially affects the lesson, research current primary sources and keep their claims distinct from workspace behavior. Save a resource link on a persistent goal only when it will remain useful across sessions.

Create `.analysis/learning/<slug>-reference.md` only when the user requests a durable reference or repeated use clearly justifies one. Keep it concise, evidence-linked, and designed for retrieval. Do not create HTML lessons, course folders, reusable lesson assets, or community participation requirements.

## 4. Maintain learner history

Update `.analysis/learner-model.json` against [the learner model schema](../../assets/learner-model.schema.json). Persist history only within the current workspace.

The user may inspect, dispute, correct, or remove signals in natural language. When correcting a signal:

- show the current concept and supporting evidence
- accept a clear user correction without defensiveness
- mark contested evidence `disputed` when the truth remains unclear
- record the correction and reason
- remove a signal when the user asks to forget it

Do not infer durable mastery from one lucky answer or durable ignorance from one miss.

## 5. Close a learning segment

Summarize what the user can now explain or do, the evidence that supports that assessment, and the next concept only when it advances the stated goal. Stop when the user has reached the requested outcome, chooses to pause, or the workspace cannot support a grounded lesson.
