---
name: change-design
description: Design an enhancement, integration, migration, modernization, or structural change in an existing application through focused code and runtime investigation, current external research, alternative comparison, and targeted prototypes. Use when the user explicitly invokes /change-design for a code-aware design of a proposed change.
disable-model-invocation: true
---

# Change Design

Design a coherent change in an existing application. Keep the design centered on the requested behavior and the affected slice of the real system.

Treat this invocation context as a starting point:

`$ARGUMENTS`

Combine code investigation with current external research. Do not redesign or document the whole application by default. Do not turn the design into a delivery plan.

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before writing the notebook, final design, or session synthesis.

In every response and artifact:

- Put the proposed change first.
- Use short sentences, active voice, familiar words, and stable terms.
- Explain an unfamiliar product, domain, or technical term when it first appears.
- Distinguish code and runtime facts, documented intent, external findings, participant choices, assumptions, inference, and unknowns.
- Put code references and external sources next to the claims they support.
- Avoid consultant language, generic architecture advice, exhaustive checklists, and ceremonial conclusions.

## Lead the design

Remain in the main session. Own the changed scenarios, design state, frontier, synthesis, and final report.

Use subagents for bounded code or runtime traces, external research questions, independent change options, focused models, or isolated prototypes. Give each subagent the smallest relevant context, one clear question, and the expected result. Do not ask a subagent to redesign the whole application.

Run code tracing and external research together when they are independent. Ask the participant only for product intent, business priorities, risk tolerance, organizational constraints, or facts unavailable from the supplied environment.

## Keep durable design state

If a design notebook is supplied or obvious, read and resume it. Otherwise, create:

`.design/<change-slug>/notebook.md`

Use [the change design notebook template](assets/design-notebook-template.md). Keep it current and compact. Replace outdated interpretations. Record the current position, affected slice, active frontier, and best next move so another session can resume naturally.

Maintain these connected views:

`requested behavior <-> current executing path <-> affected surface <-> candidate seams <-> proposed delta <-> transition states`

## Work the change frontier

The change frontier is the small set of consequential questions whose prerequisites are understood. A useful frontier question can change the proposed delta, reveal another affected boundary, distinguish credible seams, or retire an important uncertainty.

Use this loop throughout the design:

1. Read the current change state.
2. Select the next consequential question.
3. Choose the best next move: code inspection, runtime inspection, external research, participant judgment, modeling, or a prototype.
4. Develop meaningfully different options.
5. Compare them against the desired behavior and actual system constraints.
6. Resolve the uncertainty that separates the strongest options.
7. Decide, revise, or deliberately defer.
8. Update the affected slice and recompute the frontier.

Expand the investigation only when the changed path exposes another meaningful boundary.

## Keep external research connected to the code

Search supplied artifacts and repository material first. Then search current primary sources.

Use the affected slice to form external research questions about:

- current framework and platform capabilities
- supported integration paths
- compatibility and versioning rules
- data evolution and migration patterns
- relevant standards
- known limitations and failure modes
- credible alternatives to the emerging design

Every external idea must return to the application:

- Where would it attach?
- What existing responsibility would change?
- Which contracts or data would it affect?
- Does the current stack support it?
- What temporary state would it create?

Current vendor guidance does not establish an organization's internal platform standard. When the change targets a named cloud tenancy, platform, or operating environment, inspect the supplied platform material first. If it is unavailable, use external research to frame provisional options and ask the participant for the internal constraint before settling the service choice.

At the start and end of each broad design envelope:

1. Read the notebook and reconstruct the current position.
2. Identify what the latest code trace revealed.
3. Research only facts that can improve the options or change the emerging design.
4. Integrate the findings into the affected slice and frontier.

Give a research subagent:

1. The relevant stack, dependency, or proposed seam.
2. One bounded factual question.
3. Why the answer matters to this application.
4. A request for the finding, direct sources, uncertainty, code implications, and questions unlocked.

Do not recommend a pattern because it is common. Show how it fits this codebase.

## Use models and prototypes selectively

Choose the representation that best explains the current question. This may be a current-and-proposed flow, dependency map, state model, contract diff, data flow, sequence, context diagram, interface sketch, or decision comparison.

Use the lowest fidelity that exposes the uncertainty. Use realistic code, data, or integrations when a simplified model would hide it.

Before creating a prototype, state:

- the question
- the assumption being tested
- the observation that would change the design
- the prototype boundary
- whether the code is disposable

Keep prototype code isolated from the application unless the user explicitly changes the scope.

## 1. Anchor on the changed scenario

Read the requested change, available deep-discovery report, repository documentation, tests, schemas, configuration, deployment definitions, and relevant recent history.

Express the change as one or more concrete user or system scenarios. Identify the current trigger, behavior, result, and desired difference.

Treat the repository and runtime as evidence of current behavior. Treat documentation as intended or reported behavior. Make disagreements visible.

Do not begin with a broad repository audit.

## 2. Trace the affected slice

Follow each changed scenario through the actual application:

`trigger -> entry point -> processing and decisions -> data and contracts -> integrations -> result`

Inspect the relevant code, tests, configuration, schemas, infrastructure, and runtime material. Follow direct and transitive effects on:

- modules and services
- users and system consumers
- interfaces, events, and jobs
- persisted data and state
- external integrations
- deployment and configuration
- performance, reliability, security, cost, and operations
- ownership boundaries

Use focused subagents for independent traces. Ask each agent to explain the behavior and relationships, not produce a file inventory.

Expand outward only when the trace crosses another meaningful boundary.

## 3. Research what the code reveals

Research the platform, framework, integration, compatibility, data, or migration questions exposed by the trace. Run independent code and research tasks together.

Integrate each finding back into the current-state slice. State whether it creates a new option, removes an option, changes a constraint, or exposes another question.

Keep a platform choice provisional when the repository and public sources cannot establish its fit with the organization's standards.

## 4. Find and compare change seams

Identify credible places to make the change. Consider only approaches relevant to the affected slice, such as:

- modify the existing responsibility
- extend an existing boundary
- integrate through a current contract
- introduce an isolating interface or adapter
- replace one responsibility incrementally
- use a temporary transition path

Compare options against:

- desired behavior
- actual coupling and ownership
- data and contract effects
- compatibility and coexistence
- relevant system qualities
- reversibility and temporary complexity
- cost and future change

Explain what truly distinguishes the options and what evidence would weaken each one.

## 5. Resolve the consequential design

Work the change frontier. For each consequential question:

1. Inspect the affected code or runtime path more deeply when needed.
2. Research current external options when the stack or problem warrants it.
3. Model the relevant behavior, structure, state, or data flow.
4. Prototype the uncertainty that separates credible options when inspection and research are not enough.
5. Discuss product, business, and risk tradeoffs with the participant.
6. Decide, revise, or defer.
7. Update the current slice, proposed delta, and affected surface.

Repeat until the proposed change remains coherent as the investigation expands.

## 6. Compose and publish the change design

Explain the design as a delta:

`relevant current behavior -> chosen seam -> proposed behavior -> affected contracts and data -> resulting behavior`

When old and new behavior must coexist, describe the meaningful transition states, compatibility rules, data ownership, and the condition for removing temporary paths. Do not add a migration narrative when the change does not need one.

Trace the changed scenarios through the proposed design. Resolve contradictions that affect the design. Leave unrelated application behavior outside the report.

Finish when:

- the relevant current behavior is understood from code and runtime evidence
- the affected surface is bounded
- the chosen seam fits the application
- current external knowledge has informed the important choices
- the proposed behavior, structure, contracts, and data changes agree
- coexistence or transition states are understood where needed
- major alternatives and decisions are explained
- remaining uncertainty is explicit and does not prevent a coherent design

Write a durable report using [the change design template](assets/change-design-template.md). Adapt its sections to the change. Follow an existing documentation convention when obvious; otherwise write:

`docs/design/<change-slug>-change-design.md`

Use diagrams only when they make the current-to-proposed change easier to understand.

Finish the session with a short synthesis covering:

- the proposed change and chosen seam
- the relevant current behavior
- the affected surface
- the external findings that most shaped the design
- the major design decisions
- transition states when relevant
- remaining design questions
- the notebook and report paths

If the participant pauses, update the notebook and return only the current position, active frontier, recommended next move, and notebook path.

## Do not cross the boundary

Do not produce a PRD, roadmap, backlog, task breakdown, implementation plan, production code, or delivery workflow. Do not broaden the work into a full application redesign unless the requested change genuinely crosses the whole system.
