---
name: start-design
description: Turn a settled greenfield product discovery into a coherent new solution design through research, alternative exploration, modeling, targeted prototypes, and an adaptive design conversation. Use for new applications with no existing codebase when the user explicitly invokes /start-design.
license: MIT
disable-model-invocation: true
---

# Start Design

Turn a settled greenfield discovery into a coherent new solution design. Work with the participant to explore credible alternatives and resolve the decisions that hold the solution together.

Treat this invocation context as a starting point:

`$ARGUMENTS`

Do not repeat product discovery. Do not turn design into a feature backlog, delivery plan, or implementation project.

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before writing the notebook, final design, or session synthesis.

Read and apply [the domain-modeling discipline](../../references/domain-modeling.md) when terms, relationships, invariants, scenarios, or source evidence expose a material conceptual conflict. Keep resolved domain state in the design notebook and keep implementation decisions in the design views.

Read [the local decision-map protocol](../../references/decision-map.md). Keep the ordinary design frontier by default. Escalate only when consequential uncertainty must remain coherent across sessions, contains real blocking relationships, supports independent work, or no longer fits a compact frontier. Return every resolution to the design notebook before continuing this workflow.

In every response and artifact:

- Put the design conclusion first.
- Use short sentences, active voice, familiar words, and stable terms.
- Explain an unfamiliar product, domain, or technical term when it first appears.
- Distinguish discovery findings, external facts, participant choices, assumptions, inference, and unknowns.
- Put attribution or a source next to the claim it supports.
- Avoid consultant language, generic architecture advice, exhaustive checklists, and ceremonial conclusions.

## Lead the design

Remain in the main session. Lead the conversation, design state, frontier, synthesis, and final report.

Use subagents for bounded external research, independent solution directions, focused models, or isolated prototypes. Give each subagent the smallest relevant context, one clear question, and the expected result. Do not ask a subagent to design the whole solution.

Ask for participant judgment when the choice depends on product intent, business priorities, risk tolerance, operating responsibility, or organizational preference. Find current public facts yourself.

## Keep durable design state

If a design notebook is supplied or obvious, read and resume it. Otherwise, create:

`.design/<initiative-slug>/notebook.md`

Use [the design notebook template](assets/design-notebook-template.md). Keep it current and compact. Replace outdated interpretations. Record the current position, active frontier, and best next move so another session can resume naturally.

Maintain these linked views as they become useful:

`outcomes and constraints <-> experience <-> domain <-> information and state <-> integrations <-> system responsibilities`

Let the views mature at different rates. Update every affected view when one decision changes another.

## Work the design frontier

The design frontier is the small set of consequential questions whose prerequisites are understood. A useful frontier question can change the solution, unlock other design work, or retire an important uncertainty.

Use this loop throughout the design:

1. Read the current design state.
2. Select the next consequential question.
3. Choose the best next move: conversation, external research, alternative generation, modeling, or a prototype.
4. Develop meaningfully different options.
5. Compare them against the outcomes and constraints that matter for this decision.
6. Resolve the uncertainty that separates the strongest options.
7. Decide, revise, or deliberately defer.
8. Update the design state and recompute the frontier.

Do not pursue every unanswered question. Leave reversible details open until they matter.

## Research as the design develops

Search supplied artifacts and notes first. Then search current primary internet sources.

Research when a current fact could change:

- the available solution directions
- an experience, domain, data, integration, or system boundary
- a platform or technology choice
- an important quality or constraint
- confidence in a major decision
- the need for a prototype

At the start and end of each broad design envelope:

1. Read the notebook and reconstruct the current position.
2. Identify new dependencies, unfamiliar concepts, and material unknowns.
3. Research only what can improve the next design questions or change the emerging synthesis.
4. Integrate the findings into the design and update the frontier.

Give a research subagent:

1. The smallest relevant design context.
2. One bounded factual question.
3. Why the answer matters.
4. A request for the finding, direct sources, uncertainty, design implications, and questions unlocked.

Do not give a separate research presentation. Use the result to improve the design conversation.

## Use models and prototypes selectively

Choose the representation that best resolves the current question. This may be a journey, service blueprint, state model, domain map, data flow, sequence, context diagram, interface sketch, or decision comparison.

Use the lowest fidelity that exposes the uncertainty. Use realistic data, integrations, or code when a simplified model would hide it.

Before creating a prototype, state:

- the question
- the assumption being tested
- the observation that would change the design
- the prototype boundary
- whether the code is disposable

Keep prototype code isolated from production work.

## 1. Establish the solution frame

Read the greenfield discovery brief, discovery notebook, supplied research, and current conversation.

Extract:

- the target opportunity and desired change
- users and other actors
- the product promise and smallest value loop
- defining experiences
- domain and system context
- business and technical drivers
- meaningful non-goals
- assumptions that still affect design

Translate these into the initial design state. Identify the first consequential questions. Research dependencies already visible in the discovery when current facts will improve the first options.

If discovery is incomplete, ask only for the product judgment needed to continue. Record the gap instead of restarting discovery.

## 2. Develop coherent solution directions

Create a small set of meaningfully different whole-solution directions. Each direction should connect:

- the defining user experiences
- domain responsibilities and boundaries
- important information and state changes
- external systems and organizations
- major system responsibilities
- qualities and constraints that shape the solution

Keep each direction coarse enough to preserve choice. Explain what truly distinguishes the directions and what evidence would weaken each one.

## 3. Resolve the consequential design

Work the frontier. Move between experience, domain, information, integration, and system design as dependencies emerge.

For each consequential question:

1. Decide whether it needs conversation, research, modeling, or a prototype.
2. Develop credible options.
3. Compare the options against the relevant outcomes and constraints.
4. Resolve the uncertainty that separates the strongest options.
5. Decide, revise, or leave the choice open with a reason.
6. Update every affected design view.

Periodically trace each defining experience through the emerging solution:

`actor and trigger -> interaction -> domain behavior -> information and state -> integrations -> outcome`

Use the trace to find missing responsibilities, awkward handoffs, and boundaries that no longer fit. Research or prototype only gaps that could change the design.

## 4. Publish the solution design

Finish when:

- the defining experiences can be explained through the solution
- the main domain, data, integration, and system boundaries work together
- important qualities and constraints have shaped the design
- major alternatives and decisions are understood
- consequential dependencies have been researched at the needed depth
- remaining uncertainty is explicit and does not prevent a coherent design

Do not wait for every reversible implementation detail.

Write a durable report using [the solution design template](assets/solution-design-template.md). Adapt its sections to the solution. Follow an existing documentation convention when obvious; otherwise write:

`docs/design/<initiative-slug>-solution-design.md`

Use diagrams only when they make a relationship or flow easier to understand. Cite important external sources near the claims they support.

Finish the session with a short synthesis covering:

- the proposed solution
- the defining experience and value flow
- the main domain and system boundaries
- the decisions that most shaped the solution
- important research or prototype findings
- remaining design questions
- the notebook and report paths

If the participant pauses, update the notebook and return only the current position, active frontier, recommended next move, and notebook path.

## Do not cross the boundary

Do not produce a Product Brief, roadmap, backlog, task breakdown, implementation plan, production code, or delivery workflow. Do not present a reversible implementation preference as a settled architectural decision.
