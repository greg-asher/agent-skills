---
name: to-questionnaire
description: Turn missing knowledge or authority into a focused Markdown questionnaire for the person who holds it. Use when the user explicitly invokes /to-questionnaire to collect facts, constraints, preferences, or approvals without inventing the answers.
license: MIT
disable-model-invocation: true
---

# To Questionnaire

Create a questionnaire for knowledge the current participant cannot supply. Interview the sender about the handoff, not about subject matter they do not know.

Treat `$ARGUMENTS` and the current conversation as the starting context.

Read [the plain-language writing guide](references/plain-language-writing.md) before asking questions or writing the artifact.

## 1. Establish the recipient

Learn the recipient's role, relevant expertise, relationship to the sender, and what context they already have. Ask one focused question only when the conversation does not establish this.

Complete this step when the tone and necessary background are clear.

## 2. Establish the required return

Identify what the sender must know, decide, or receive. Classify each requested answer as:

- **Fact:** an observable or documented truth
- **Constraint:** a limit delivery must respect
- **Preference:** a choice the recipient is entitled to make
- **Approval:** explicit authorization from the responsible person

Mark an answer **Blocking** only when work cannot safely continue without it. Ask for supporting evidence when a policy, system state, contract, approval, or other primary artifact should substantiate the answer.

Complete this step when every requested return has a type, blocking status, and intended use.

## 3. Write the questionnaire

Read [the questionnaire template](assets/questionnaire-template.md). Write the artifact to:

- `docs/questionnaires/<slug>.md` in a repository
- `questionnaires/<slug>.md` in an ordinary folder

Order blocking and highest-value questions first. Use one idea per question. Put an answer space directly below each question. Explain why an answer matters only when the recipient could otherwise misread the request or give an unusably shallow answer.

State that partial answers and explicit uncertainty are useful. End with a catch-all for important information the questionnaire did not anticipate.

Complete this step when every required return is covered by an atomic question and the artifact exists.

## Boundaries

- Do not ask the sender to answer subject-matter questions they have already said they cannot answer.
- Do not invent or pre-fill the recipient's answers.
- Do not send the questionnaire, contact the recipient, publish it to a tracker, or create external records.
- Do not turn the questionnaire into a broad discovery exercise.
- Do not treat an unanswered preference as approval.

Finish with the artifact path, the blocking answers, and the decision or workflow that can resume when they arrive.
