# Adaptive architecture artifacts

Use this guide after the primary value paths are understood. Build architectural assets from one connected application model. Do not create unrelated diagrams from separate interpretations of the repository.

## Build the application model

Combine three evidence sources:

1. **Static source structure:** abstract syntax trees, compiler indexes, language servers, imports, calls, routes, events, data access, inheritance, and generated dependency information.
2. **Runtime structure:** processes, services, jobs, stores, queues, providers, deployment configuration, environment boundaries, and observed behavior.
3. **Product behavior:** actors, triggers, decisions, state changes, integrations, and outcomes from the selected value-path traces.

Use [the application model schema](../assets/application-model.schema.json) as the durable interchange shape. It is the machine-readable core of the discovery knowledge base, not merely input for diagrams. Adapt optional fields to the application, but preserve stable IDs, repository revisions, analysis coverage, evidence links, capability status, findings, and uncertainty.

Record evidence once in the model's central `evidence` collection. Link capabilities, nodes, relationships, flows, and findings through `evidenceIds`. Use `sourceLocations` for navigation, not as a substitute for describing what the evidence establishes. A reader or future agent should be able to move from a consequential finding to the affected capability or flow, then to the supporting runtime observation, test, source location, configuration, documentation, or history.

An abstract syntax tree establishes code structure. It does not establish runtime activity, data ownership, product meaning, or deployment topology. Label each node and relationship by its support:

- observed at runtime
- demonstrated by a test
- statically established
- declared by configuration or documentation
- inferred
- unknown

## Use AST analysis intelligently

Identify the languages and use an AST-capable tool already supported by the repository or environment. Prefer compiler APIs, language servers, Tree-sitter, and language-native parsers. Do not introduce a large analysis dependency merely to produce a diagram.

Typical starting points include the TypeScript compiler or language server for JavaScript and TypeScript, Python's `ast` module, `go/ast` and `go/packages` for Go, Roslyn for .NET, compiler or language-server indexes for Java and Kotlin, and rust-analyzer or a Rust parser for Rust. Use repository-native tooling when it provides a more accurate project graph.

Exclude generated files, vendored dependencies, build outputs, and framework internals unless they explain an application boundary.

Use a two-pass analysis:

1. **Coverage pass:** inventory application-owned languages, project or workspace manifests, source roots, generated-code boundaries, parser choices, repository revisions, and files that cannot be parsed. Establish which static relationships each tool can and cannot recover.
2. **Value-path pass:** start from the selected workflow entry points and retain only the modules, symbols, calls, routes, events, jobs, contracts, and data access that explain the path, an important branch, or a system boundary.

Prefer the repository's resolved project graph over file-by-file parsing when it is available. Compiler configuration, module resolution, build tags, generated contracts, aliases, and workspace boundaries can materially change the source graph.

Collect only structure that helps explain the application:

- application-owned modules and symbols
- imports and dependency direction
- routes, commands, events, and jobs
- calls that form the primary value paths
- data access and serialization boundaries
- interfaces, implementations, and extension points
- cross-repository or generated contracts

Dynamic dispatch, dependency injection, reflection, code generation, and external configuration can hide runtime relationships. Combine static analysis with tests, configuration, and workflow traces. Keep unresolved links visible.

Do not publish a raw symbol or call graph as architecture.

Normalize retained facts into the application model as you investigate:

- give every retained module, symbol, route, event, job, contract, and relationship a stable ID
- record qualified names and exact source locations when the tool provides them
- link each static fact to a `source-analysis` evidence record and the analysis method that produced it
- connect static nodes to their runtime unit, subsystem, capability, and value-path steps only when repository or runtime evidence supports that connection
- preserve unresolved targets and contradictory evidence as unknowns instead of silently dropping them

Record the analysis tools and versions, included source roots, exclusions, parse failures, and important coverage limits in the application model. State whether call edges cover direct calls only, whether imports were fully resolved, and which dynamic or generated relationships remain opaque. Do not imply complete call coverage in a dynamic or partially parsed system.

Before publishing, check model integrity:

- IDs are unique and references resolve.
- Every static relationship has source-analysis evidence.
- Runtime and deployment claims do not rely only on AST evidence.
- Capability status uses the strongest status the investigation actually supports.
- Separate runtime instances remain separate even when they share code.
- Findings and unknowns link to the model entries they affect.
- Derived pages and diagrams identify the model entries they project.

## Partition the model

Split a large model using the strongest boundaries available, in this order:

1. runtime and deployment units
2. product or domain responsibilities
3. ownership boundaries
4. public contracts and integration seams
5. primary value paths
6. packages, namespaces, and import structure
7. structural clustering when the architecture is otherwise unclear

Directory structure alone does not define architecture.

Preserve a top-level application view. Add focused views for partitions that cannot remain legible or meaningful in the overview. A focused view must link back to its parent context and preserve important cross-boundary relationships.

## Choose useful projections

Treat each diagram as an answer to one reader question. Useful diagram families include:

- system context and actors
- runtime or deployment topology
- application and subsystem responsibilities
- AST-backed module dependencies
- primary-flow sequence or activity views
- data lineage and ownership
- domain state transitions
- event and integration topology
- cross-cutting identity, security, or observability paths
- repository navigation

Do not produce every family. Contract the set when one view already answers the question. Expand when a diagram mixes abstraction levels, hides meaningful runtime instances, crosses several domains, or becomes difficult to read.

Prefer one overview plus linked deep dives over one dense diagram. For a small application, a combined system/runtime view and a few primary-flow diagrams may be enough.

## Generate durable diagram assets

Store the canonical model and evidence catalog under:

`docs/discovery/<application-slug>-assets/knowledge-base/`

Create:

- `application-model.json`
- `evidence-catalog.md`
- `index.md` and any justified topic pages

Store the atlas derived from that model under:

`docs/discovery/<application-slug>-assets/architecture/`

Create:

- `atlas.md` using [the atlas index template](../assets/architecture-atlas-template.md)
- editable diagram sources such as Mermaid or DOT
- rendered SVG or PNG versions when rendering tools are available

Use stable names and consistent node labels across diagrams. Put code references and evidence beside the relevant model entries. Keep labels short inside diagrams and move explanations into the atlas.

Render and inspect each published diagram. Split, collapse, or relayout a view when labels are unreadable, edges obscure relationships, or separate runtime instances appear merged.

If no rendering tool is available, publish the editable source and state which rendered formats remain unavailable. Do not claim that an unrendered asset was visually inspected.
