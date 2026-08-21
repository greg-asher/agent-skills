# <Application> Architecture Atlas

## How to Use This Atlas

Explain the levels and the questions each view answers. Link to the canonical discovery report and discovery knowledge base. State that the atlas is a projection of `knowledge-base/application-model.json` and identify the model IDs used by each view.

## Application Overview

List the smallest set of views that orients every reader.

## Primary Application Flows

Link each value-path view to its outcome, entry point, important boundaries, and evidence.

## Subsystem Views

Create this section only when the application has meaningful subsystems. For each subsystem, explain its responsibility, parent context, public relationships, owners when known, and linked diagrams.

## Data and State Views

Include only views that explain important ownership, movement, transformation, or lifecycle behavior.

## Runtime and Operational Views

Include deployment, environment, event, identity, or observability views only when they explain the current application.

## Codebase Navigation

Link AST-backed module or repository views that help an engineer move from architecture into source code.

## Evidence and Limits

Explain which relationships were observed, demonstrated by tests, established statically, declared, inferred, or left unknown. Link the evidence catalog, analysis methods, source coverage, parse failures, and material limits rather than repeating them incompletely.

Omit empty sections. Split a view when it becomes hard to read. Link every focused view back to its parent context.
