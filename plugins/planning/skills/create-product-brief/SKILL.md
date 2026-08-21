---
name: create-product-brief
description: Turn settled product discovery and solution or change design into one canonical Product Brief covering the product narrative and Business and Process, Technology, and People requirements. Use when the user explicitly invokes /create-product-brief after discovery and design are complete and before implementation issues are created.
disable-model-invocation: true
---

# Create Product Brief

Compile settled discovery and design into the canonical requirements for delivery. Tell one coherent product story and state what must be true across Business and Process, Technology, and People.

Treat this invocation context as a starting point:

`$ARGUMENTS`

Do not repeat discovery, reopen settled design, or turn the Product Brief into a roadmap, issue list, architecture catalog, or collection of separate planning documents.

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before writing the Product Brief or session synthesis.

In every response and artifact:

- Put the intended outcome first.
- Use short sentences, active voice, familiar words, and stable product terms.
- Name real users, product surfaces, actions, systems, responsibilities, and results.
- State requirements as observable behavior, explicit constraints, or assigned responsibilities.
- Distinguish settled decisions, non-blocking unknowns, and delivery blockers.
- Remove filler, project-management language, repeated source material, and ceremonial conclusions.

## Lead the synthesis

Remain in the main session. Own source selection, reconciliation, product framing, readiness, and the final Product Brief.

Use subagents only when large source artifacts need independent scenario, technology, operating-model, or consistency analysis. Give each subagent one bounded question and the minimum relevant context. Do not ask a subagent to write the whole Product Brief.

## 1. Establish the planning basis

Locate the discovery and design artifacts for the same initiative. Use exact paths from the arguments when supplied. Otherwise use the current conversation and obvious repository conventions.

Use these handoffs:

- Greenfield product: Greenfield Discovery Brief plus Solution Design.
- Existing application change: Deep Discovery report when relevant plus Change Design.

Read the complete handoffs. Treat discovery as the source of product intent or current-state understanding. Treat design as the settled account of the proposed product and solution. Inspect the repository only when it helps confirm current names, seams, constraints, or operating reality.

Do not combine artifacts from unrelated initiatives. If a coherent design is missing, identify the missing handoff instead of inventing it.

The published Product Brief becomes the canonical delivery requirement. Discovery and Design remain the sources for deeper context and rationale.

## 2. Reconcile the product narrative

Build one consistent account of:

- the people affected
- the current problem or opportunity
- the intended change and why it matters
- the defining experience or value loop
- the outcomes and delivery boundary

Resolve wording differences into one product vocabulary. Preserve useful source links instead of copying exploratory analysis.

If the sources conflict about a requirement, architecture choice, or responsibility, make the conflict visible. Resolve it only from an explicit settled decision. Do not silently choose the most convenient source.

## 3. Compile the requirements

Organize settled commitments through three connected lenses.

### Business and Process

Capture the workflows, business rules, controls, exceptions, ownership boundaries, outcomes, and measures needed to produce the intended value.

### Technology

Capture settled architectural patterns, system responsibilities, data and state ownership, integrations, security, reliability, performance, observability, runtime, deployment, migration, and compatibility requirements that delivery must preserve.

Include the commitments needed to build and operate the product. Link to Design for detailed rationale, diagrams, component exploration, or alternatives.

### People

Capture actors, permissions, decision rights, operational ownership, support, escalation, training, adoption, and responsibilities introduced, removed, or transferred by the product.

Do not invent a requirement to fill a heading. State an absence only when it is a meaningful settled boundary.

## 4. Trace the defining scenarios

Use the scenarios to connect the three lenses. For each defining path, make clear:

`actor and trigger -> business process -> product and system behavior -> operating handoff -> result`

Include alternate and failure behavior when it changes the process, system obligation, human responsibility, or outcome. Check that requirements across the three lenses describe the same product rather than three independent workstreams.

## 5. Set readiness

The Product Brief is ready for issue creation only when:

- the product narrative and delivery boundary agree with the source decisions
- every defining scenario has a clear result
- the requirements across all three lenses are consistent
- architecture and ownership decisions needed for delivery are settled
- success can be observed
- no issue author would need to invent product behavior, a structural mechanism, or an owner

Record non-blocking unknowns with their expected impact.

If an unresolved decision could change requirements, architecture, or ownership:

- mark the brief `Not ready for issue creation`
- name the decision and the affected part of the brief
- keep the durable brief as the current canonical planning state
- do not disguise the gap with placeholders or proceed to issue creation

Otherwise mark the brief `Ready for issue creation`.

## 6. Publish the Product Brief

Write the durable document using [the Product Brief template](assets/product-brief-template.md). Adapt the content to the product while keeping the three lenses visible. Follow an existing documentation convention when obvious; otherwise write:

`docs/planning/<initiative-slug>-product-brief.md`

Link the relevant Discovery and Design artifacts when their locations are known.

Finish the session with a short synthesis covering:

- the product outcome
- the defining delivery shape
- the most important cross-lens commitment
- whether the Product Brief is ready for issue creation
- the Product Brief path

Do not create implementation issues in the same invocation.
