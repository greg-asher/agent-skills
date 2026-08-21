# Adaptive architecture artifacts

Use this guide after the primary value paths are understood. Build architectural assets from one connected application model. Do not create unrelated diagrams from separate interpretations of the repository.

## Build the application model

Combine three evidence sources:

1. **Static source structure:** abstract syntax trees, compiler indexes, language servers, imports, calls, routes, events, data access, inheritance, and generated dependency information.
2. **Runtime structure:** processes, services, jobs, stores, queues, providers, deployment configuration, environment boundaries, and observed behavior.
3. **Product behavior:** actors, triggers, decisions, state changes, integrations, and outcomes from the selected value-path traces.

Use [the application model schema](../assets/application-model.schema.json) as the durable interchange shape. Adapt optional fields to the application, but preserve evidence, status, and uncertainty.

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

Record the analysis tools, included source roots, exclusions, parse failures, and important coverage limits in the application model. Do not imply complete call coverage in a dynamic or partially parsed system.

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

Store the atlas under:

`docs/discovery/<application-slug>-assets/architecture/`

Create:

- `application-model.json`
- `atlas.md` using [the atlas index template](../assets/architecture-atlas-template.md)
- editable diagram sources such as Mermaid or DOT
- rendered SVG or PNG versions when rendering tools are available

Use stable names and consistent node labels across diagrams. Put code references and evidence beside the relevant model entries. Keep labels short inside diagrams and move explanations into the atlas.

Render and inspect each published diagram. Split, collapse, or relayout a view when labels are unreadable, edges obscure relationships, or separate runtime instances appear merged.

If no rendering tool is available, publish the editable source and state which rendered formats remain unavailable. Do not claim that an unrendered asset was visually inspected.
