---
name: deep-discovery
description: Deeply investigate an existing software application or unfamiliar codebase using coordinated subagents, end-to-end workflow tracing, AST-backed architecture modeling, an evidence-linked knowledge base, adaptive diagrams, and discovery and onboarding presentations. Use for application discovery, technical onboarding, inherited systems, MVP handoffs, architecture reconstruction, or requests to understand what a repository does, how it works, how data moves, and what state the build is in.
disable-model-invocation: true
---

# Deep Discovery

Explain an existing application as it works now. Start broad. Find the workflows that create its value, trace them in depth, and connect them into one account of the product and system.

Use the current repository as the main boundary. Follow direct references to related repositories, deployment files, shared schemas, or supporting artifacts when the application uses them. State what you could not inspect. Treat the invocation context below as additional guidance:

`$ARGUMENTS`

Use the arguments and repository context to identify the intended reader. If no reader is named, write for a technically literate teammate who does not know the application. Explain internal terms on first use. Do not assume the reader knows the repository structure.

Keep this discovery separate from migration planning, target architecture, redesign, or implementation.

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before you write the report, knowledge-base pages, atlas, presentations, onboarding material, or final session synthesis. Apply its core rules to all prose. Apply its technical rules when you explain the system or give navigation instructions. Apply its editorial rules when you report findings, evidence, significance, or uncertainty.

In every response and artifact:

- Put the main finding first.
- Use short sentences, active voice, familiar words, and consistent terms.
- Explain a technical term when it first appears, unless the intended reader will know it.
- Name the actor when responsibility matters.
- Distinguish observed facts from repository claims, inference, estimates, and unknowns.
- Put attribution or a code reference next to the claim it supports.
- Give exact dates, counts, units, and comparisons when the evidence supports them.
- Remove filler, slogans, jargon, decorative metaphors, and ceremonial conclusions.

## Lead the investigation

Remain in the main session and lead the investigation. Do not give the whole skill to a subagent. Use subagents for focused repository searches and workflow traces. Keep orientation, path selection, synthesis, and follow-up decisions in the main session.

Subagents do not share the lead's full context. Give each subagent the relevant working view, one specific question, and the expected result. Do not ask a subagent to summarize the whole repository.

## 1. Get oriented

Experience the application if it can be run or observed. Scan the repository structure, product surfaces, documentation, tests, configuration, and recent history.

Run or observe at least one representative user workflow when feasible. A build, typecheck, test suite, or help screen proves only that check. It does not prove the product workflow. If the workflow cannot run, state the exact blocker and limit later claims accordingly.

Form a working view of:

- what the application does
- who appears to use it
- which capabilities appear central
- which workflows may create its value
- which parts of the system need deeper investigation

Use this view to shape the scout assignments. Do not treat it as settled.

## 2. Launch the scout wave

Launch scouts with different questions at the same time. Match the number of scouts to the repository. Cover these perspectives:

- product behavior, users, capabilities, and candidate workflows
- components, services, runtime, and application structure
- data models, sources, transformations, and integrations
- current build, tests, recent evolution, ownership, and operating context

Give every scout a compact assignment containing:

1. The provisional application context relevant to its work.
2. One bounded investigation question.
3. A request to identify or challenge likely workflows that create value.
4. A request to return what it learned, how the pieces connect, and what remains unclear.

Let scouts follow useful connections they find. These perspectives organize the search. They do not define the application's architecture.

## 3. Choose the value paths

Combine the scout findings into an updated view of the application. Select the two or three end-to-end workflows that best explain its purpose and value.

Prefer workflows that cross several parts of the application and produce a meaningful result. They should also reveal important data or integrations. State why you selected each path.

Select workflows that represent distinct user outcomes. Do not choose local, hosted, or provider-specific versions of the same outcome as separate paths unless their differences explain an important product boundary. Model those versions as branches within one trace when possible.

## 4. Launch the trace wave

Launch one subagent per selected value path, concurrently where the paths are independent.

Ask each trace agent to follow its workflow through the actual application:

`trigger or input -> entry point -> processing and decisions -> data and integrations -> resulting system, user, or business outcome`

Have the agent explain meaningful branches, handoffs, and incomplete portions without turning the trace into a file-by-file tour.

## 5. Assemble the application model

Read [the adaptive architecture guide](references/architecture-artifacts.md). Combine the workflow traces, scout findings, static source analysis, runtime and deployment material, and observed behavior into one connected application model.

Use AST-capable tooling supported by the repository or environment to establish useful source relationships. Analyze application-owned source, not generated files or dependency internals. Capture modules, symbols, imports, calls, routes, events, data access, interfaces, and extension points only when they explain the application or a primary value path.

Build the model as the investigation proceeds. Use stable IDs for capabilities, nodes, relationships, flows, evidence, findings, and unknowns. Record evidence once in the central evidence catalog and refer to it by ID from supported claims. Preserve repository revisions, analysis methods, source locations, exclusions, parse failures, and coverage limits. Do not wait until the end to recreate evidence from memory.

Build one connected explanation of:

- the product and its users
- its main capabilities
- its core value paths
- the major application and runtime pieces
- its data model and data movement
- external integrations and dependencies
- the current state of the build
- ownership and operating context
- how the application has evolved and where it appears to be heading

Resolve different descriptions of the same behavior into one shared vocabulary.

Do not treat the AST as the architecture. Reconcile static relationships with processes, deployment units, configuration, tests, integrations, and primary application flows. Distinguish observed, tested, statically established, declared, inferred, and unknown relationships. A static import or call edge is one fact in the model, not proof that a capability works or runs in a particular environment.

Partition a large model using runtime, domain, ownership, contract, value-path, and package boundaries. Keep a top-level application view and add focused subsystem views only where the overview loses meaningful distinctions.

Identify the three to five findings that most change how a new reader should understand the product or system. Give those findings more weight than component inventories, repository counts, or implementation detail.

Include a subsystem, schema detail, configuration value, or repository statistic only when it explains a value path, system boundary, capability state, important risk, or useful navigation point.

For each main capability or value path, use the strongest status supported by the investigation:

- **Observed working:** completed during this investigation.
- **Demonstrated by test:** covered by a test that passed, but not directly observed.
- **Implemented and connected:** the code path is wired together, but was not run.
- **Declared operational:** documentation or deployment configuration presents it as operational, but live state was not checked.
- **Partial:** required behavior is missing.
- **Stubbed or mocked.**
- **Documented but not found.**
- **Outside boundary:** relevant, but not inspected.

Use **active** only when runtime, deployment, telemetry, or direct usage evidence supports it. Do not infer activity from code, tests, manifests, or documentation alone.

## 6. Fill important gaps

Identify missing information that prevents a clear explanation of the application. Launch the smallest follow-up search that can answer each important question. Then update the application model.

Repeat only when the answer changes your understanding of the product, its workflows, or the supporting system. Do not inspect the repository only for completeness.

Keep only open questions that could materially change the current-state model. Group them as:

- evidence gaps
- repository or documentation conflicts
- ownership questions
- adjacent systems outside the investigation boundary

Prioritize questions within each group. Leave future product decisions, remediation choices, and redesign questions out.

## 7. Build the discovery package

Create an adaptive package from the application model. Treat the model and its evidence catalog as the canonical knowledge layer. Derive the report, atlas, onboarding material, and presentations from that layer so the package does not contain competing accounts of the application. The package should become deeper only when the application and audience require it.

Always produce:

- the canonical Markdown discovery report
- a navigable, evidence-linked discovery knowledge base
- a machine-readable application model and human-readable evidence catalog
- an asset index that explains the package and intended readers
- a navigable architecture atlas
- editable source for every published diagram
- an onboarding asset suited to the intended technical reader
- a presentation package suited to the application's size and audiences

For a compact application, combine related diagrams and use one discovery-and-onboarding presentation with a technical appendix. For a larger application, create a discovery briefing and a separate engineering onboarding presentation. Add subsystem or cross-cutting deep dives only when the core atlas or onboarding deck cannot explain them clearly.

Do not create diagrams or decks merely to increase the artifact count.

Write `docs/discovery/<application-slug>-assets/index.md` as the package entry point. Link the canonical report, discovery knowledge base, architecture atlas, onboarding guide, presentations, and focused deep dives. Explain which artifact answers which reader question.

### Create the discovery knowledge base

Write the canonical knowledge layer under:

`docs/discovery/<application-slug>-assets/knowledge-base/`

Always create:

- `index.md` using [the knowledge-base template](assets/knowledge-base-template.md)
- `application-model.json` using [the application model schema](assets/application-model.schema.json)
- `evidence-catalog.md` using [the evidence catalog template](assets/evidence-catalog-template.md), organized by evidence type and linked to stable evidence IDs

Make the index useful to product, engineering, operations, and future agents. Lead with the application's outcomes, defining value paths, capability state, major boundaries, consequential findings, and the best places to enter the evidence. Include the repository revision and investigation scope so readers know which system state the knowledge describes.

Add focused Markdown pages for capabilities, value paths, runtime units, data, integrations, domain vocabulary, code navigation, or operations only when a single index would become dense. A focused page must link back to its parent topic and reuse model IDs, terms, statuses, and evidence IDs. Do not duplicate prose merely to create more pages.

The JSON model is the machine-readable source for entities and traceability. The Markdown pages are the human navigation layer. Update the model before regenerating a derived page or diagram when the understanding changes. Check that every consequential claim has direct evidence or is labeled inferred or unknown; every referenced ID resolves; every flow step resolves to modeled nodes when applicable; and every published asset records which model entries it derives from.

### Write the canonical report

Follow an existing documentation convention when one is obvious; otherwise write:

`docs/discovery/<application-slug>-deep-discovery.md`

Use this structure:

```markdown
# <Application> Deep Discovery

## Executive Summary

## Product and Users

## Core Value Paths

## System Architecture

## Data Model and Data Flow

## Integrations and Dependencies

## Current Build and Evolution

## Ownership and Operating Context

## Open Questions

## Codebase Guide
```

Make the Executive Summary stand alone. State what the application is, the user outcome it creates, the broad system shape, what the investigation demonstrated, and the most important current-state findings. Leave detailed timings, limits, component catalogs, and secondary observations in the report body.

Embed or link only the knowledge-base and atlas views that materially improve the report. Distinguish shared implementation from shared runtime infrastructure. Show separate process or service instances when the same code runs in several places. Do not use one shared node when it could imply one global service, database, or process.

Cite useful code locations so another engineer can move from the report into the application. Include owners, maintainers, users, environments, and operating duties only when the evidence identifies them. State what remains unknown.

### Create the architecture atlas

Follow [the adaptive architecture guide](references/architecture-artifacts.md). Read the canonical application model from the knowledge base. Write the atlas index, diagram sources, and rendered diagrams under:

`docs/discovery/<application-slug>-assets/architecture/`

Choose views that answer important reader questions. Typical families include system context, runtime topology, subsystem responsibilities, module dependencies, primary flows, data movement, state, events, deployment, and codebase navigation. Do not produce every family.

Prefer one readable overview plus linked deep dives over one dense diagram. Split models by logical boundaries when a large codebase, several runtime units, multiple domains, or many cross-cutting relationships cannot remain legible in one view. Preserve parent context and important cross-boundary relationships.

Render and inspect every published diagram. If rendering is unavailable, publish editable source and state the exact limitation.

### Create onboarding material and presentations

Write `docs/discovery/<application-slug>-assets/onboarding-guide.md` using [the onboarding guide template](assets/onboarding-guide-template.md). Treat the template as a learning progression, not a mandatory section list. Link to the report, knowledge base, atlas, code entry points, and supported build or run paths. Adapt its depth by subsystem and reader need.

Then read [the presentation guide](references/presentation-artifacts.md). Create either:

- one combined discovery and onboarding presentation for a compact application, or
- an executive discovery briefing and an engineering onboarding presentation for a larger application.

Add focused deep-dive presentations only when the core onboarding presentation cannot explain a complex subsystem or cross-cutting concern at readable density.

Use a current supplied or repository presentation template when one is clearly intended. Otherwise use a neutral 16:9 enterprise style. Use only claims supported by the report and application model in the discovery knowledge base. Put code references and external sources in speaker notes or associated source blocks.

Render and inspect every finished slide. If PowerPoint authoring is unavailable, create complete `.slides.md` storyboards, state the exact blocker, and do not claim that `.pptx` files exist.

Finish the session with a concise executive synthesis covering:

- what the application is
- why it matters
- the workflows that define it
- how the system works at a high level
- the most important current-state observations
- the durable report, knowledge-base, atlas, onboarding, and presentation paths

Keep the session synthesis short. Put the detail in the durable package.
