# Adaptive greenfield discovery artifacts

Create visual and presentation assets from the settled discovery brief and notebook. Do not turn discovery artifacts into a target architecture, feature plan, or unsupported market claim.

## Select the package

Always create the core value journey flow described in [the core value journey guide](core-value-journey.md). Then choose the smallest supporting set that helps the intended readers understand the product opportunity:

- actor and ecosystem map
- opportunity map
- domain and information lifecycle view
- external dependency and system-context sketch
- assumptions and learning-priority view
- product discovery briefing presentation

Do not produce every supporting view. Contract when the core value journey and one supporting visual already explain the product. Expand when a complex ecosystem, several actor groups, multiple journey branches, or distinct responsibility boundaries become unreadable in one view.

For a simple product, the brief, two or three visuals, and one concise briefing may be enough. For a complex enterprise product, split ecosystem, experience, domain, and dependency views into linked diagrams and use an appendix for deeper material.

## Keep the evidence honest

Build each asset from the final discovery map:

`desired change -> actors and situations -> opportunities -> product thesis -> core value journey and product responsibility -> critical branches -> domain and system context -> assumptions and learning moves`

Distinguish participant reports, external research, product hypotheses, choices, inference, and unknowns. Do not draw an integration or application boundary as settled architecture.

Use editable Mermaid, DOT, or another suitable source format. Render to SVG or PNG when tools are available. Inspect each published diagram and split or simplify it when labels, branches, or relationships become difficult to follow.

Store visual assets under:

`docs/discovery/<product-slug>-assets/visuals/`

If no rendering tool is available, publish the editable source and state which rendered formats remain unavailable.

## Build the product discovery briefing

Use [the product discovery storyboard](../assets/product-discovery-briefing-storyboard.md) as a narrative pattern, not a mandatory slide list.

The presentation should help sponsors, product leaders, and technical partners understand:

- the current situation and desired change
- the target opportunity and product thesis
- value for each important actor
- the core value journey and the responsibility the product accepts
- domain and system context without selecting architecture
- important dependencies and research
- assumptions most likely to disprove the idea
- the next learning move

Search supplied material for a current PowerPoint template, brand guide, logo, fonts, or recent internal presentation. Use a clear current source when one exists. Otherwise use a neutral 16:9 enterprise style.

Use an installed presentation-authoring tool that can create PowerPoint files. If none is available, ask before adding a dependency. When the environment cannot create PowerPoint, create a complete `.slides.md` storyboard, state the exact blocker, and do not claim a `.pptx` exists.

Use only claims supported by the brief, notebook, and cited research. Put sources in speaker notes or a clearly associated source block.

Render every finished slide. Inspect the deck and each slide at readable size. Fix clipped text, crowded layouts, unintended overlap, inconsistent terms, and diagrams that are illegible at presentation scale.

Store the finished presentation under:

`docs/discovery/<product-slug>-assets/presentations/`

Keep temporary builders, renders, and working files outside the published asset package.
