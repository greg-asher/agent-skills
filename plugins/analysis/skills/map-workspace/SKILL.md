---
name: map-workspace
description: Build or refresh a revision-scoped, evidence-linked model of an unfamiliar software workspace, including boundaries, components, interfaces, dependencies, runtime services, configuration, state, tests, and material unknowns. Use before agentic changes, architectural analysis, technical teaching, or blast-radius assessment when the workspace lacks a current trusted map.
license: MIT
---

# Map Workspace

Build the deterministic workspace model that other Analysis skills can trust. Treat `$ARGUMENTS` as focus guidance, not permission to ignore important cross-boundary relationships.

Read [the Analysis evidence contract](../../references/evidence-contract.md) and [the plain-language writing guide](references/plain-language-writing.md).

## 1. Establish the snapshot

Resolve the workspace root, repository identity, current revision, working-tree state, repository instructions, and existing `.analysis/workspace-model.json`. If a model exists, check its revision, covered sources, methods, and limitations before reusing it.

Inventory application-owned source, package and build metadata, configuration, tests, deployment material, schemas, scripts, and current documentation. Exclude dependencies, generated code, build output, secrets, and generated Analysis artifacts.

## 2. Extract structure

Use the strongest safe tools already available in the workspace. Prefer AST-capable analysis for symbols, exports, imports, calls, types, routes, events, and data access. Do not install tooling automatically.

Identify:

- bounded contexts, packages, services, applications, and deployment units
- public interfaces and shared contracts
- state ownership, persistence, queues, events, and asynchronous handoffs
- runtime services and external systems
- environment-variable names and roles, never values
- build, test, release, and operating boundaries

Static reachability does not prove runtime use.

## 3. Reconcile runtime evidence

Trace the workflows that best expose cross-boundary behavior. Run only safe, read-only, or repository-standard diagnostic checks. Distinguish direct observation, demonstrated tests, static analysis, declarations, inference, and unknowns.

Compare current code and tests with documentation. Preserve material conflicts. Prefer current implementation and direct evidence over stale narrative claims without erasing the documented intent.

## 4. Build the model

Write `.analysis/workspace-model.json` against [the workspace model schema](../../assets/workspace-model.schema.json). Use stable IDs for boundaries, components, relationships, evidence, findings, and unknowns.

Write `.analysis/workspace-map.md` as a compact human projection containing:

1. the workspace purpose and revision
2. the important boundaries and responsibilities
3. the main runtime and state relationships
4. the best code and workflow entry points
5. the most consequential conflicts and unknowns
6. coverage and freshness limits

Do not create a target architecture, migration plan, refactor proposal, or backlog.

## 5. Verify and report

Parse the JSON and confirm every referenced evidence ID exists. Check that no secret values or raw environment dumps entered either artifact. Report the artifact paths, revision, methods, strongest findings, and exact coverage limitations.
