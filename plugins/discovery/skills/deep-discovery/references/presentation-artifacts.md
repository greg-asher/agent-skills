# Discovery and onboarding presentations

Create presentations from the completed discovery report, discovery knowledge base, and the models and visuals supported by the workspace. Do not rediscover or reinterpret the subject while building slides.

## Select the package

Choose the smallest package that serves the readers:

- **Document corpus:** one discovery briefing grounded in the source model and useful workflow or relationship visuals.
- **Compact application:** one combined discovery and onboarding presentation with a technical appendix.
- **Larger application:** one executive discovery briefing and one engineering onboarding presentation.
- **Large or federated system:** add subsystem or cross-cutting deep-dive presentations only when the core onboarding deck cannot explain them clearly.

Do not split decks only to appear comprehensive. Do not place every generated diagram into a presentation.

## Find the visual direction

Search the repository and supplied artifacts for a current PowerPoint template, brand guide, logo, fonts, or recent internal presentation. Use a clear current source when one exists. Otherwise use a neutral 16:9 enterprise style with restrained color, strong typography, and simple compositions.

Use an installed presentation-authoring tool that can create PowerPoint files. If none is available, ask before adding a dependency. When the environment cannot create PowerPoint, produce a complete `.slides.md` storyboard, state the exact blocker, and do not claim a `.pptx` exists.

## Build the discovery briefing

Use [the discovery briefing storyboard](../assets/discovery-briefing-storyboard.md) as a narrative pattern, not a mandatory slide list.

The briefing should help a sponsor or technical leader understand:

- what the product, process, or application is and why it matters
- who uses it and which outcomes define its value
- the workflows, business rules, systems, and responsibilities that shape it
- what the sources or investigation establish
- the findings that most change the current understanding
- important decisions, conflicts, dependencies, ownership, and unknowns

Keep the main deck concise. Move code detail, inventories, and secondary diagrams into an appendix only when they help discussion.

## Build engineering onboarding

Use [the engineering onboarding storyboard](../assets/engineering-onboarding-storyboard.md) as a narrative pattern. Expand it by subsystem or primary flow when the application needs more depth.

The onboarding presentation should help an engineer build a useful mental model before reading files. Connect product purpose to runtime, code, data, integrations, and ownership. Include code entry points and repository navigation without turning the deck into a file listing.

## Preserve traceability

Use only claims supported by the report and source or application model in the discovery knowledge base. Put source locations, code references, and external sources in speaker notes or a clearly associated source block. Label source-stated claims, corroboration, participant confirmation, observations, static findings, declared behavior, inference, and unknowns accurately.

## Inspect the finished presentations

Render every slide. Inspect the full deck and each slide at readable size. Fix clipped text, crowded layouts, unintended overlap, broken connectors, tiny labels, inconsistent terminology, and diagrams that are illegible at presentation scale.

Use one main point per slide. Shorten copy or split a slide before shrinking text. Use takeaway titles that state what the audience should understand.

Store finished presentations under the selected discovery output root:

`<discovery-output>/<subject-slug>-assets/presentations/`

Keep temporary builders, renders, and working files outside the published asset package.
