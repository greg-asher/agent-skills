# Core value journey

Use the core value journey as the central model of the proposed product. Show the end-to-end progress the product must make successfully happen, not a tour of screens or features.

## Define the journey

1. Name the real-world trigger that creates the need.
2. Name the meaningful user or business outcome. Do not end at a click, submission, notification, or other interface event unless that event is the actual outcome.
3. Describe the wider human or business journey around the product.
4. Mark where the proposed product accepts responsibility and where that responsibility ends.
5. Sequence the major actor actions, product responsibilities, decisions, handoffs, information movement, and state changes between trigger and outcome.
6. Mark outside systems and people at the points where they provide input, make a decision, perform work, or receive responsibility.
7. Add only branches that materially change value, ownership, trust, feasibility, or risk.

The journey may include work performed by people or external systems. Make ownership visible instead of implying that the product performs everything.

## Create the flowcharts

Always create one editable overview flowchart. Prefer five to nine meaningful stages that a product sponsor can read without narration. Use actor or responsibility lanes when they make ownership clearer. Mark the product responsibility boundary directly in the diagram.

Create focused supporting flows only when the overview would otherwise hide an important difference, such as:

- a distinct actor or entry path
- an approval, escalation, or human override
- an asynchronous or external handoff
- an exception or recovery path that changes the outcome
- a journey phase with enough decisions to become unreadable in the overview

For a complex product, keep one stable overview and split detail by journey phase or material branch. Link each detail flow back to the stage it expands. Do not create a separate flow for minor variants.

Use labels that describe progress and responsibility in domain language. Do not use component names, services, databases, queues, APIs, or proposed implementation details.

## Publish the journey

Store editable Mermaid source at:

`docs/discovery/<product-slug>-assets/visuals/core-value-journey.mmd`

Render it to SVG or PNG when tools are available. Store focused flows beside it with clear names such as:

- `core-value-journey-approval.mmd`
- `core-value-journey-recovery.mmd`
- `core-value-journey-phase-<name>.mmd`

Include a short note with the diagram that states:

- the outcome the journey creates
- where product responsibility begins and ends
- important handoffs
- unresolved journey questions

Use the overview in the discovery brief and the main presentation. Put focused flows in the relevant section or appendix.
