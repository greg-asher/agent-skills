---
name: deep-discovery
description: Deeply investigate whatever already exists in a folder—software, documents, designs, data, or a mixture—using coordinated source investigators, workflow tracing, source reconciliation, an evidence-linked knowledge base, and adaptive reports, visuals, onboarding, and briefing assets. Use for application discovery, document-corpus analysis, technical onboarding, inherited systems, MVP handoffs, architecture reconstruction, mixed intent-versus-implementation reviews, or requests to understand an unfamiliar body of product or system material.
disable-model-invocation: true
---

# Deep Discovery

Explain the product, process, or system that exists now. Start broad. Find the workflows that create its value, trace them in depth, and connect the sources into one coherent account.

Use the current folder as the main boundary. Follow direct references to adjacent repositories, systems, schemas, or supporting artifacts when they materially shape the subject. State what was outside reach. Treat the invocation context as additional guidance:

`$ARGUMENTS`

Write for the named reader. If none is named, write for a technically literate teammate who does not know the subject. Keep current-state discovery separate from target architecture, migration planning, redesign, roadmapping, requirements, and implementation.

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before you write the report, knowledge-base pages, atlas, presentations, onboarding material, or final session synthesis. Apply its core rules to all prose. Apply its technical rules when you explain the system or give navigation instructions. Apply its editorial rules when you report findings, evidence, significance, or uncertainty.

In every response and artifact:

- Put the main finding first.
- Use short sentences, active voice, familiar words, and consistent terms.
- Explain a technical term when it first appears, unless the intended reader will know it.
- Name the actor when responsibility matters.
- Distinguish observed facts from source claims, corroboration, participant confirmation, inference, estimates, and unknowns.
- Put a source location, attribution, or code reference next to the claim it supports.
- Give exact dates, counts, units, and comparisons when the evidence supports them.
- Remove filler, slogans, jargon, decorative metaphors, and ceremonial conclusions.

## Lead the investigation

Remain in the main session. Own scope, workspace classification, path selection, synthesis, output selection, and follow-up decisions. Use the packaged `source-investigator` agent for bounded source groups. Do not give the full investigation to one agent.

Read [the source investigation guide](../../references/source-investigation.md) before inventorying the folder or assigning investigators.

## 1. Classify and inventory the workspace

Inventory meaningful local material before interpreting it. Classify the workspace as:

- **Software:** implemented application or operational automation is present.
- **Document corpus:** documents, designs, images, or data describe the subject without implemented application evidence.
- **Mixed:** documentary intent and implemented behavior are both material.
- **Sparse:** the folder cannot support a useful product or system account.

Git history and runnable workflows are optional evidence. Their absence is not a blocker. Source code without Git remains software.

Build a source manifest with the bundled corpus tool when Python 3 is available. Exclude generated Discovery outputs, dependencies, temporary material, lock files, and byte-identical duplicates from review. Keep duplicates, unreadable files, and partial reviews visible in coverage.

For Office files, use the bundled extractor from the source investigation guide. Read PDFs and images with native tools. Inspect long PDFs in page ranges. Render Office material with an already installed renderer when possible. Never install one automatically. Record layout limitations when rendering is unavailable.

If the workspace is sparse, report the evidence boundary, inaccessible material, and the few questions the folder cannot answer. Do not invent a product, workflow, or architecture.

## 2. Get oriented

Form a provisional view of:

- what the material appears to describe
- the actors and outcomes involved
- the workflows that may create value
- the important business rules, data, systems, dependencies, and design concepts
- the age, authority, and relationship of the sources
- the areas that need deeper investigation

In software or mixed mode, also scan product surfaces, tests, configuration, deployment material, build paths, and available history. Run or observe a representative product workflow when feasible. A build, typecheck, test, or help screen proves only that check. If the workflow cannot run, state the blocker and limit runtime claims.

Keep the initial view provisional. Use it to shape the scout wave.

## 3. Launch the scout wave

Launch source investigators with different bounded questions at the same time where useful. Match the number to the corpus. Useful groups include:

- product narrative, prior proposals, and design direction
- users, research, and current process
- business rules, business model, and operating responsibility
- data concepts, systems, and dependencies
- design concepts, prototypes, and unresolved alternatives

Every assignment must include the provisional context relevant to that group, the files or source area, one investigation question, and the required return shape from the source investigation guide.

In software and mixed modes, add focused software scouts for:

- product behavior, users, capabilities, and candidate workflows
- components, services, runtime, and application structure
- data models, transformations, integrations, and state
- build, tests, recent evolution, ownership, and operating context

Use AST-capable tooling supported by the workspace when it explains application-owned modules, symbols, imports, calls, routes, events, data access, interfaces, or extension points. Do not analyze generated code or dependency internals. Do not treat an AST graph as the architecture.

## 4. Choose and trace the value paths

Combine the scout findings. Select the two or three end-to-end workflows that best explain the subject's purpose and value. A value path may come from implemented behavior, documented workflow, or both.

Prefer distinct actor outcomes that cross meaningful boundaries and reveal important data, decisions, integrations, or operating responsibilities. State why each was selected.

Launch one bounded trace per path when the paths are independent. Follow:

`trigger or input -> actor and entry point -> activities and decisions -> data, systems, and handoffs -> meaningful outcome`

In software mode, follow the actual application path. In document mode, follow the documented process across sources. In mixed mode, trace documented intent and implemented behavior separately, then state where they align or diverge.

## 5. Assemble the current-state model

Create a source model using `${CLAUDE_PLUGIN_ROOT}/assets/source-model.schema.json`. Reconcile vocabulary, actors, workflows, business rules, operating context, product, data, system, and design concepts, decisions, claims, conflicts, gaps, and unresolved questions.

Classify document decisions as settled, proposed, superseded, or unclear. Classify claims as source-stated, corroborated, participant-confirmed, inferred, or unknown. Do not treat a newer date as proof that one source supersedes another. Surface conflicts instead of choosing silently.

For software or mixed mode, also maintain the existing application model using [the application-model schema](assets/application-model.schema.json). Reconcile static relationships with processes, deployment units, configuration, tests, integrations, and primary flows. Preserve these capability statuses:

- **Observed working**
- **Demonstrated by test**
- **Implemented and connected**
- **Declared operational**
- **Partial**
- **Stubbed or mocked**
- **Documented but not found**
- **Outside boundary**

Use **active** only when direct usage, runtime, deployment, or telemetry evidence supports it.

Build one connected explanation of the product or process and its actors, its main capabilities and value paths, business rules and operating responsibility, data concepts and ownership, systems and dependencies, design direction and decisions, current build where software exists, and conflicts or gaps that change the account.

Give the three to five most consequential findings more weight than inventories and counts.

Build the model as the investigation proceeds. Use stable IDs for capabilities, nodes, relationships, flows, evidence, findings, and unknowns. Record evidence once in the central evidence catalog and refer to it by ID from supported claims. Preserve repository revisions, analysis methods, source locations, exclusions, parse failures, and coverage limits. Do not wait until the end to recreate evidence from memory.

## 6. Fill material gaps

Launch the smallest follow-up investigation that can resolve a gap that would materially change the product, workflow, system, or operating account. Stop when further inspection would only add completeness.

Keep open questions about current state. Group them as evidence gaps, source conflicts, ownership questions, or adjacent systems outside the boundary. Exclude future design and remediation choices.

## 7. Build the discovery package

Treat the models and evidence catalog as the canonical knowledge layer. Derive the report, visuals, onboarding, and presentations from it so the package does not contain competing accounts. Follow an existing documentation convention. Otherwise use:

- `docs/discovery/` when the folder is a repository
- `discovery/` in an ordinary folder

Create `<subject-slug>-assets/index.md` as the package entry point. Link every published artifact and state the reader question it answers. Do not copy original sources.

### Document corpus

Always publish:

- `<subject-slug>-deep-discovery.md`, the canonical report
- `<subject-slug>-assets/source-guide.md`
- `<subject-slug>-assets/source-model.json`
- `<subject-slug>-assets/index.md`
- editable workflow, actor, dependency, or conflict visuals that materially improve understanding
- one discovery briefing under `<subject-slug>-assets/presentations/`

Create `<subject-slug>-assets/knowledge-base/index.md` using [the knowledge-base template](assets/knowledge-base-template.md) and `<subject-slug>-assets/knowledge-base/evidence-catalog.md` using [the evidence catalog template](assets/evidence-catalog-template.md). Make the index useful to product, operations, technical readers, and future agents. Lead with outcomes, value paths, decision state, consequential findings, and the best evidence entry points. Reuse stable source-model and evidence IDs instead of duplicating claims.

Do not manufacture an architecture atlas or engineering onboarding guide without software or operational-system evidence.

### Software

Preserve the current software package:

- canonical report
- asset index
- evidence-linked discovery knowledge base
- application model using [the application-model schema](assets/application-model.schema.json)
- evidence catalog
- adaptive architecture atlas with editable diagram source
- onboarding material suited to the technical reader
- a compact combined discovery/onboarding presentation or separate discovery and engineering onboarding presentations when scale requires them

Read [the adaptive architecture guide](references/architecture-artifacts.md) before creating the atlas. Use one readable overview plus focused views only where runtime, domain, ownership, contract, data, or value-path boundaries would otherwise be lost.

### Mixed

Publish the source guide and source model alongside the software package. Make documented intent versus implemented behavior a first-class part of the report and visuals. Do not privilege either automatically.

### Sparse

Publish only the canonical report and the smallest useful source guide or index. Do not create empty visuals, onboarding, architecture, or presentations.

### Canonical report

Use this adaptable structure:

```markdown
# <Subject> Deep Discovery

## Executive Summary
## Product, Process, and Actors
## Core Value Paths
## Business Rules and Operating Context
## Data, Systems, and Dependencies
## Design Direction and Decision State
## Current Build and Evolution
## Conflicts, Gaps, and Open Questions
## Source Guide | Codebase Guide
```

Omit sections the evidence cannot support. Use **Source Guide** when no codebase exists and **Codebase Guide** when software is present. In mixed mode, use both where they answer different navigation questions.

Make the Executive Summary stand alone. State what exists, the outcome it creates, the broad shape, what the investigation established, and the most important current-state findings.

Embed or link only the knowledge-base and atlas views that materially improve the report. In software views, distinguish shared implementation from shared runtime infrastructure and show separate runtime instances when one shared node would mislead the reader.

### Visuals and presentations

Create only visuals that make a material relationship easier to understand. Preserve editable source. Render and inspect published diagrams when rendering is available; otherwise state the limitation.

For software or mixed mode, follow [the adaptive architecture guide](references/architecture-artifacts.md). Read the canonical application model from the knowledge base. Write the atlas index, diagram sources, and rendered diagrams under:

`<discovery-output>/<subject-slug>-assets/architecture/`

Choose views that answer important reader questions. Typical families include system context, runtime topology, subsystem responsibilities, module dependencies, primary flows, data movement, state, events, deployment, and codebase navigation. Do not produce every family.

Prefer one readable overview plus linked deep dives over one dense diagram. Split models by logical boundaries when a large codebase, several runtime units, multiple domains, or many cross-cutting relationships cannot remain legible in one view. Preserve parent context and important cross-boundary relationships.

Render and inspect every published diagram. If rendering is unavailable, publish editable source and state the exact limitation.

Create onboarding material only for software or operational-system evidence. Write `<discovery-output>/<subject-slug>-assets/onboarding-guide.md` using [the onboarding guide template](assets/onboarding-guide-template.md). Treat the template as a learning progression, not a mandatory section list. Link to the report, knowledge base, atlas, code entry points, and supported build or run paths.

Then read [the presentation guide](references/presentation-artifacts.md). For software, create either:

- one combined discovery and onboarding presentation for a compact application, or
- an executive discovery briefing and an engineering onboarding presentation for a larger application.

Add focused deep-dive presentations only when the core onboarding presentation cannot explain a complex subsystem or cross-cutting concern at readable density.

For a document corpus, create the one discovery briefing required above. Use a current supplied presentation template when one is clearly intended. Otherwise use a neutral 16:9 style. Use only claims supported by the report and discovery knowledge base. Put source locations, code references, and external sources in speaker notes or associated source blocks.

Render and inspect every finished slide. If PowerPoint authoring is unavailable, create complete `.slides.md` storyboards, state the exact blocker, and do not claim that `.pptx` files exist.

Finish the session with a short executive synthesis covering what the subject is, why it matters, its defining workflows, its broad shape, the most important conflicts or current-state findings, and the durable artifact paths.
