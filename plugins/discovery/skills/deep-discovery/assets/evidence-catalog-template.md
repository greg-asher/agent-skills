# <Application> Evidence Catalog

## Snapshot and Scope

Record when the investigation ran, the repository revisions and dirty state, included and excluded boundaries, unavailable material, and the application model this catalog supports.

## Analysis Coverage

For each runtime, test, AST, configuration, documentation, history, or external research method, record:

- stable method ID, tool, and version when available
- purpose and languages or surfaces covered
- included source roots and important exclusions
- parse failures and unresolved relationships
- coverage limits, including dynamic dispatch, generated code, reflection, dependency injection, aliases, build variants, or unavailable environments

## Runtime Observations

List `runtime-observation` evidence by stable evidence ID. State what was attempted, when, where, the result, and which capabilities, flows, nodes, relationships, or findings it supports. Include commands when they help another engineer reproduce the observation.

## Test Results

List `test-result` evidence. Name the exact test or check, its result, and what it demonstrates. State what it does not prove when that distinction matters.

## Source Analysis

List retained `source-analysis` evidence. Give the method ID, qualified symbol or relationship, exact source location, and the application behavior or boundary it helps explain. Summarize source facts; do not reproduce a raw symbol or call graph.

## Configuration and Documentation

Separate declared runtime or product behavior from observed behavior. Link conflicts to the affected finding or unknown.

## Repository History and Ownership

Include history and ownership evidence only when it changes the current model, explains evolution, or identifies a supported operating responsibility.

## External Sources

List direct sources for relevant outside systems, standards, or public facts. Record access dates when the source can change.

## Conflicts, Gaps, and Limits

Summarize contradictory evidence, material coverage gaps, unavailable adjacent systems, and the prioritized unknown IDs they create.

Omit empty evidence sections. Keep each evidence item concise and use the same stable ID, support level, source, location, method, and result recorded in `application-model.json`.
