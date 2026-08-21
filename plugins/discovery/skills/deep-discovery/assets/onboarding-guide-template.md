# <Application> Engineering Onboarding Guide

## Start Here

Explain what the application does, who uses it, and which value paths organize the guide. Link the canonical discovery report and architecture atlas.

## Product and Domain Orientation

Describe the user outcomes, important domain terms, responsibilities, and business rules an engineer needs before reading code.

## Primary Application Flows

For each defining flow, explain the trigger, entry point, decisions, state changes, integrations, branches, outcome, and linked diagrams.

## System and Runtime Model

Explain how repositories, modules, processes, services, jobs, stores, queues, providers, and environments relate. Distinguish shared implementation from separate runtime instances.

## Codebase Navigation

Organize useful entry points by product behavior and subsystem. Give a reading path that moves from a primary flow into its supporting modules, data, contracts, and tests.

## Data and State

Explain the important records, ownership, lifecycle, transformations, and persistence boundaries.

## Integrations and Contracts

Describe external systems, public interfaces, events, generated contracts, dependencies, and known failure behavior.

## Build, Run, and Test

Document supported commands and environments. State what each check or workflow demonstrates and what it does not establish.

## Capability State

Summarize observed, tested, connected, declared, partial, stubbed, documented-but-absent, and outside-boundary behavior.

## Ownership and Operations

Name users, sponsors, maintainers, operational responsibilities, environments, and adjacent teams only when the investigation supports them.

## Important Unknowns

List current-state gaps that could materially change the engineer's mental model.

Omit irrelevant sections. For a large system, keep a core guide and link focused subsystem guides. Preserve the same vocabulary and parent context across every guide.
