# <Application> Discovery Knowledge Base

## Start Here

State what the application does, who this knowledge base is for, the revision and scope it describes, and the three to five findings that most affect understanding. Link the canonical discovery report, machine-readable application model, architecture atlas, onboarding guide, and presentation package.

## How to Navigate

Organize links by the questions a reader is likely to ask:

- What outcomes does the application create, and for whom?
- Which value paths make those outcomes happen?
- Which capabilities are observed, tested, connected, declared, partial, stubbed, absent, or outside the boundary?
- Which runtime units, modules, data, and integrations support each path?
- Where should an engineer enter the code?
- What evidence supports the current model, and what remains unknown?

## Product and Capability Map

Link the application outcomes, actors, capabilities, capability states, and defining value paths. Use stable IDs from `application-model.json` when referring to a modeled item.

## Value Paths

For each selected value path, link a focused page or report section that covers its trigger, actors, entry point, processing, decisions, state changes, runtime handoffs, integrations, branches, outcome, status, and supporting evidence.

## System and Runtime

Link the application overview and only the subsystem, runtime, deployment, event, identity, or operational views needed to explain the current system.

## Data and Integrations

Link important records, ownership, lifecycle, transformations, contracts, providers, and outside systems. Keep declared and inferred relationships distinct from observed or tested behavior.

## Codebase Guide

Link source entry points and AST-backed module, symbol, route, event, job, contract, and data-access relationships that help a reader follow the value paths. Do not publish an exhaustive symbol inventory.

## Evidence Catalog

Link `evidence-catalog.md`. Summarize the evidence types, analysis methods, repository revisions, included source roots, exclusions, parse failures, and coverage limits.

## Vocabulary

Define application and domain terms that a new reader needs. Reuse the canonical terms and aliases in `application-model.json`.

## Findings and Unknowns

Link consequential findings and prioritized current-state unknowns. Keep evidence gaps, repository conflicts, ownership questions, and adjacent systems outside the boundary separate.

Omit empty sections. Add topic pages only when they make the knowledge easier to navigate. Keep claims, IDs, terms, status, and evidence links consistent with `application-model.json`; update the model first when the understanding changes.
