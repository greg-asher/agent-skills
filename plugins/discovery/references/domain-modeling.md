# Domain-modeling discipline

Use this discipline while the owning Discovery or Design skill leads the work. Its purpose is to keep the product language coherent, not to start a second discovery or design process.

## When to apply it

Apply the discipline when:

- one term appears to name different concepts
- different terms appear to name the same concept
- a relationship or invariant remains vague
- a concrete scenario exposes an unclear domain boundary
- participant language conflicts with supplied evidence, code, tests, or runtime behavior

Do not interrupt merely to polish wording. Intervene when the ambiguity could change product behavior, responsibility, system boundaries, requirements, or design.

## Work the model

1. State the conflicting or unclear meanings and why the distinction matters.
2. Use one or more concrete scenarios, including an important edge case, to test the distinction.
3. Check the relevant sources or implementation when the claim is externally discoverable.
4. Ask the participant to settle only the intent, policy, or meaning that evidence cannot settle.
5. Record the resolved term, relationship, invariant, or conflict in the owning notebook immediately.
6. Use the resolved language consistently in later conversation and artifacts.

Keep implementation mechanisms out of the domain model. Record implementation and architecture decisions in the owning Design view.

## Durable decisions

Offer an architecture decision record only when the workspace already uses ADRs and the decision is all three of:

- costly to reverse
- surprising without its rationale
- the result of a genuine tradeoff between credible alternatives

Otherwise, keep the decision in the owning notebook or design artifact. Never create `CONTEXT.md`, an ADR directory, or another domain artifact by default.
