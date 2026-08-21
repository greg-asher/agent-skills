---
name: start-discovery
description: Guide a research-augmented, conversational discovery of a greenfield software product from initial idea through opportunity, product thesis, the core value journey the solution will be responsible for, domain and system context, a prioritized learning agenda, adaptive flowcharts, and a product discovery briefing. Use for new application ideas with no existing codebase when the user explicitly invokes /start-discovery.
disable-model-invocation: true
---

# Start Discovery

Use conversation and focused research to develop a useful view of a greenfield product. Finish with shared understanding, important unknowns, and the next learning step. Do not create false certainty.

Treat this invocation context as a starting point:

`$ARGUMENTS`

Do not inspect or design source code. Keep this work separate from Product Brief writing, architecture selection, roadmapping, issue creation, and implementation.

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before you write the notebook, final brief, visual assets, presentation, or session synthesis. Apply its core rules to all prose. Apply its technical rules to product and system descriptions. Apply its editorial rules to research findings, analysis, claims, and uncertainty.

In every question, response, and artifact:

- Put the main point first.
- Use short sentences, active voice, familiar words, and consistent terms.
- Ask natural questions. Do not sound like a questionnaire, consultant, or process manual.
- Explain a product, business, or technical term when it first appears, unless the participant already uses it.
- Name the person or group responsible when responsibility matters.
- Separate observed facts, participant reports, product ideas, inference, estimates, and unknowns.
- Put attribution or a source next to the claim it supports.
- Give exact dates, counts, units, and comparisons when the evidence supports them.
- Remove filler, slogans, jargon, decorative metaphors, and ceremonial conclusions.

## Lead the discovery

Remain in the main session. Lead the conversation, phase changes, synthesis, notebook, and final brief. Use subagents only for focused factual research. Do not give the whole skill or participant conversation to a subagent.

Ask one meaningful question or one closely related pair at a time. Follow important answers before returning to the internal map. Do not show a questionnaire, numbered decision tree, canvas, or repeated recommendation block.

Shift stance as understanding grows:

- **Early:** listen, ask for concrete stories, and avoid solution recommendations.
- **Middle:** reflect patterns, expose tensions, and help shape the product bet.
- **Late:** challenge business and technical assumptions and recommend learning moves.

Treat claims from founders, sponsors, and other participants as informed hypotheses unless direct experience or current research supports them. Keep the participant's domain terms when they are useful. Do not force agreement when an important question remains open.

## Keep durable state

If an existing discovery notebook is supplied or obvious, read and resume it. Otherwise, once a working product name is clear, create:

`.discovery/<product-slug>/notebook.md`

Use [the notebook template](assets/discovery-notebook-template.md). Keep it current instead of adding an endless history. Replace outdated interpretations. Keep only decisions and changes that still matter. Record the current phase and the best next question so another session can resume naturally.

Maintain this discovery map:

`desired change -> actors and situations -> current stories and alternatives -> opportunities -> target opportunity -> product hypotheses -> core value journey and product responsibility -> critical branches -> domain and system context -> business and technical drivers -> assumptions and learning moves`

Follow branches that can change the product's value, shape, system boundary, or risk. Do not ask every possible question.

## Use the same loop in each phase

Apply this loop to early, middle, and late discovery.

### Prepare

1. Read the notebook and supplied artifacts.
2. Reconstruct the current position and the next learning objective.
3. List new dependencies, unfamiliar concepts, factual claims, and important unknowns.
4. Decide whether research would improve the next questions.

At the first invocation, begin with conversation unless you must understand a named term or dependency to avoid an uninformed question.

### Research at the entry

Search existing notes and artifacts first. Then search current primary internet sources. Run independent research tasks at the same time when useful. Stop when you understand how the finding could affect the product.

Do not research private organizational intent, unpublished limits, or choices the participant must make. External research cannot establish future adoption, willingness to pay, or the quality of internal data you have not inspected.

Give each research subagent:

1. The smallest relevant discovery context.
2. One bounded factual question.
3. Why it matters to the next phase.
4. A request to return:
   - the finding
   - direct sources
   - uncertainty
   - effects on the product or system
   - questions the research unlocks

If internet or research tools are unavailable, add the question to the research queue and continue where possible.

### Converse

Open with one strong invitation. Prefer concrete stories and past behavior:

- “Tell me about the last time this happened.”
- “What happened next?”
- “Who else became involved?”
- “What did you do instead?”

Ask for descriptions, examples, clarification, and explanations. Record new research questions without interrupting a useful story. Pause during a phase only when a factual unknown blocks progress.

### Consolidate and research at the exit

1. Update the discovery map.
2. Separate researchable facts, participant decisions, and product hypotheses.
3. Identify what changed, what remains uncertain, and what the next phase needs.
4. Research only questions that could reshape the synthesis or unlock better next questions.
5. Update the notebook.
6. Give a concise playback and transition in plain language.

Use research to improve the next question. Do not give a separate research presentation. If research only confirms the current view, record it and move on.

## Run early discovery: establish reality

Develop a credible account of:

- the idea and desired change in the participant's language
- why it matters now
- concrete current situations and stories
- users, buyers, beneficiaries, operators, partners, and approvers
- current alternatives, workarounds, cases where people do nothing, friction, and consequences
- the wider journey
- the initial opportunity space

Research domain vocabulary, category context, named platforms, relevant public constraints, and adjacent approaches when doing so will improve the conversation.

Do not leave early discovery until you can explain the situation, actors, current behavior, desired progress, and useful opportunity choices. A clear explanation does not prove demand.

## Run middle discovery: shape the product bet

Work with the participant to:

- select a target opportunity and explain why
- clarify the consequence of doing nothing
- explore and compare multiple possible responses
- agree on a product promise
- define the smallest complete experience that creates value
- define the core value journey from the real-world trigger to the meaningful outcome
- mark where the product takes responsibility, what it must make happen, and where responsibility passes to a person or outside system
- clarify adoption, incentives, buying, value exchange, costs, and operating responsibility
- identify only the alternate paths, decisions, handoffs, and recovery paths that materially change value or risk
- state meaningful non-goals

Research current alternatives, switching behavior, business models, incentives for each group, comparable approaches, and dependencies discovered earlier.

Do not turn the result into a feature backlog. Leave middle discovery when the target opportunity, product promise, value for each actor, and core value journey form a clear product bet.

## Run late discovery: frame domain, system, and risk

Tell the critical domain stories. Capture:

- actors, triggers, activities, events, decisions, and business rules
- important information, work objects, state changes, and exceptional paths
- external systems, organizations, data sources, and responsibility boundaries
- adoption, cost, revenue, ownership, and operating conditions
- trust, privacy, security, compliance, availability, performance, scale, interoperability, auditability, and changeability

Learn technical needs through concrete situations, not a generic requirements list. Ask what must remain true during peak demand, failures, sensitive decisions, outside outages, or future changes.

Research platform and integration specifics, data constraints, public regulations and standards, technical precedents, and feasible learning methods as needed.

State what must be true for the product to provide value, remain usable, work in practice, support the business, and adapt to change. Prioritize assumptions that could disprove the product idea. Do not select a cloud, framework, database, service structure, or solution architecture.

## Track important dependencies

Track platforms, data sources, regulations, standards, organizational processes, partners, suppliers, product categories, competitors, and domain concepts when they can change the product.

For each important dependency, track:

- its emerging role
- the current understanding
- questions requiring research
- findings and uncertainty
- product or system implications
- questions unlocked
- remaining unknowns

Research a dependency only when the answer could change the next question, target opportunity, product promise, critical experience, system boundary, or learning priority.

## Finish the discovery

Discovery is ready to close when:

- the desired change and target opportunity are coherent
- the value for each actor is understood
- the product promise and smallest value loop are explicit
- the wider journey and the product-owned core value journey can be told end to end
- the product's responsibility boundaries, material handoffs, and consequential branches are explicit
- the domain and system context are visible at the right level
- the business conditions and the needs that future architecture must support are understood
- the riskiest assumptions and next learning moves are prioritized

Give one concise closing playback and allow the participant to correct the product thesis. Do not require repeated confirmation.

Then write a shareable Greenfield Discovery Brief using [the brief template](assets/greenfield-discovery-brief-template.md). Follow an existing documentation convention when obvious; otherwise use:

- `docs/discovery/<product-slug>-greenfield-discovery.md`, or
- `discovery/<product-slug>-greenfield-discovery.md` when no documentation structure exists.

State the strongest current view and where it remains uncertain. Cite important external research near the claim and include direct sources.

Then read [the core value journey guide](references/core-value-journey.md) and [the adaptive discovery artifact guide](references/discovery-artifacts.md). Create the smallest useful visual and presentation package from the final discovery map.

Write `docs/discovery/<product-slug>-assets/index.md` as the entry point. Link the brief, visuals, and presentation. Explain which artifact answers which reader question.

Always create an editable overview flowchart of the core value journey. Add focused flowcharts only when a material branch, actor transition, outside dependency, approval, exception, or recovery path would make the overview hard to understand.

Possible supporting views include:

- actor and ecosystem relationships
- the opportunity space
- domain information and state
- external dependencies and system context
- critical assumptions and learning priorities

Do not create every supporting view. Combine views when the product is simple. Split the core value journey into an overview plus linked phase or branch flows when a complex product cannot remain clear in one diagram. Split supporting views by actor group, domain, or responsibility boundary only when needed. Keep every visual at the discovery level. Do not present a system-context sketch as selected architecture.

Store visual assets under:

`docs/discovery/<product-slug>-assets/visuals/`

Create a product discovery briefing under:

`docs/discovery/<product-slug>-assets/presentations/`

Use a current supplied or repository presentation template when one is clearly intended. Otherwise use a neutral 16:9 enterprise style. Use only claims supported by the brief, notebook, and cited research. Put sources in speaker notes or associated source blocks.

Render and inspect every published diagram and finished slide. If rendering or PowerPoint authoring is unavailable, publish editable diagram source and a complete `.slides.md` storyboard, state the exact limitation, and do not claim rendered or PowerPoint assets exist.

Finish the session with a short synthesis covering:

- the target opportunity
- the current product thesis
- the core value journey and the responsibility the product accepts
- important dependencies
- the assumptions most likely to disprove the product idea
- the recommended next learning move
- the notebook, brief, visual, and presentation paths

If the participant pauses before completion, update the notebook and return only the current position, what remains open, the recommended next phase, and the notebook path.

## Do not cross the boundary

Do not produce a Product Brief, feature backlog, roadmap, project plan, target architecture, stack recommendation, implementation issues, or code. Do not recommend building merely because discovery began with an application idea. Do not claim that conversation or desk research validated a market.
