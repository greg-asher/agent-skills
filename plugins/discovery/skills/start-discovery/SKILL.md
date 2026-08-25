---
name: start-discovery
description: Guide a research-augmented, conversational discovery of a greenfield software product, beginning with a quiet investigation of meaningful local documents, designs, data, or software when present. Use for new application ideas, artifact-led product discovery, or resuming a living discovery notebook when the user explicitly invokes /start-discovery.
license: MIT
disable-model-invocation: true
---

# Start Discovery

Use local sources, conversation, and focused research to develop a useful view of a greenfield product. Finish with shared understanding, important unknowns, and the next learning step. Do not create false certainty.

Treat this invocation context as a starting point:

`$ARGUMENTS`

Keep this work separate from Product Brief writing, architecture selection, roadmapping, issue creation, and implementation.

## Write in plain language

Read [the plain-language writing guide](references/plain-language-writing.md) before writing or asking questions. Put the main point first. Use short sentences, active voice, familiar words, and consistent terms. Ask natural questions. Name the responsible actor when it matters. Separate source claims, participant reports, research, inference, and unknowns. Remove filler and ceremony.

Read and apply [the domain-modeling discipline](../../references/domain-modeling.md) when language, relationships, invariants, scenarios, or supplied evidence expose a material conceptual conflict. Keep resolved domain state in the discovery notebook; do not create a separate glossary by default.

Read [the local decision-map protocol](../../references/decision-map.md). Keep the ordinary notebook frontier by default. Escalate only when consequential uncertainty must remain coherent across sessions, contains real blocking relationships, supports independent work, or no longer fits a compact frontier. The decision map remains part of Discovery and returns its resolutions to this notebook.

## Lead the discovery

Remain in the main session. Own the source intake, conversation, phase changes, synthesis, notebook, and final brief. Use the packaged `source-investigator` agent only for bounded local source groups. Use research agents only for bounded factual questions. Do not hand the participant conversation to an agent.

Run an interview, not a turn-by-turn Q&A. Use fewer, richer turns that give the participant enough context and room to think aloud. Follow important answers before returning to the internal map. Do not show a questionnaire, numbered decision tree, canvas, or repeated recommendation block.

Shape each substantial interview turn around one learning objective:

1. Briefly play back the relevant understanding, tension, or uncertainty.
2. Explain why exploring it matters now.
3. Offer one broad invitation that can elicit a story, explanation, or point of view.
4. Add two to four related prompts that suggest useful angles, examples, contrasts, or edge cases.
5. Invite the participant to answer freely, skip prompts, correct the framing, and go wherever the story is most useful.

Present the invitation and prompts as a natural spoken passage, not a numbered list the participant must complete. Keep every prompt within the same topic. A participant using voice mode should be able to respond with a several-minute narrative without having to remember a form. Treat partial answers, digressions, and corrections as useful evidence. Do not repeat an unanswered prompt unless it remains important after synthesis.

Shift stance as understanding grows:

- **Early:** listen, ask for concrete stories, and avoid solution recommendations.
- **Middle:** reflect patterns, expose tensions, and help shape the product bet.
- **Late:** challenge business and technical assumptions and recommend learning moves.

Treat imported product claims and participant beliefs as hypotheses unless direct experience, participant confirmation, or current evidence supports them.

## Choose the entry mode

Read [the source investigation guide](../../references/source-investigation.md). At every entry, detect the notebook and source state, then inventory meaningful local material.

Use one of three modes:

- **Idea-led:** no meaningful source material exists. Begin the conversational flow.
- **Artifact-led:** material exists but no source state exists. Run a quick source investigation first.
- **Resume:** a notebook or source manifest exists. Reconstruct the learning objective and inspect only new or changed material before continuing.

Arguments, attached files, and meaningful content in the current folder are source material. Generated Discovery outputs, dependencies, lock files, temporary files, and byte-identical duplicates are not.

### Run the artifact-led quick pass

1. Establish a working product slug without asking if the material makes it clear.
2. Save `.discovery/<product-slug>/source-manifest.json` with the bundled inventory tool.
3. Inspect the meaningful sources. Use the Office extractor, native PDF and image reading, and installed renderers as described in the source guide.
4. Assign bounded source groups to `source-investigator` agents when the corpus benefits from parallel review.
5. Reconcile the results into `.discovery/<product-slug>/source-model.json` using `${CLAUDE_PLUGIN_ROOT}/assets/source-model.schema.json`.
6. Create or update `.discovery/<product-slug>/notebook.md` with source coverage, material findings, conflicts, currency, and inaccessible sources.

Create no standalone Deep Discovery report, source guide, asset index, visual, or presentation during this pass.

The first artifact-led response contains only:

- what the material appears to describe
- the most important conflict, gap, or uncertainty
- one natural question the sources cannot answer

Do not ask the participant to repeat facts already in the sources.

If the source corpus reveals an implemented application, say so and ask whether the initiative is truly greenfield or whether it should be understood as a change to that application. Do not continue under a false greenfield frame.

### Resume incrementally

Generate a new manifest with the saved manifest as `--previous`. Inspect files marked `new` or `changed`, account for removed sources, and carry forward unaffected findings. Update only the affected source-model findings and notebook sections. Do not reread the full corpus or repeat settled early questions.

## Keep durable state

If an existing discovery notebook is supplied or obvious, read and resume it. Otherwise, once a working product name is clear, create:

`.discovery/<product-slug>/notebook.md`

Use [the notebook template](assets/discovery-notebook-template.md). Keep it current instead of adding an endless history. Replace outdated interpretations. Keep only decisions and changes that still matter. Record the current phase, learning objective, source currency, and best next interview opening so another session can resume naturally.

Maintain this discovery map:

`desired change -> actors and situations -> current stories and alternatives -> opportunities -> target opportunity -> product hypotheses -> core value journey and product responsibility -> critical branches -> domain and system context -> business and technical drivers -> assumptions and learning moves`

Follow branches that can change value, product shape, system boundary, or risk. Do not ask every possible question.

## Use the same loop in each phase

### Prepare

1. Read the notebook, source manifest, source model, and supplied artifacts.
2. Reconstruct the current position and next learning objective.
3. List changed dependencies, unfamiliar concepts, factual claims, and important unknowns.
4. Decide whether local inspection or external research would improve the next question.

Search local material before the internet. Never place confidential source text in an external search query.

### Research at entry

Search current primary sources only for bounded facts that could improve the conversation. Research named platforms, public constraints, categories, alternatives, standards, and precedents when they matter. Do not research private organizational intent, unpublished limits, or decisions the participant must make.

Give each research agent the smallest relevant context, one factual question, why it matters, and a request for the finding, direct sources, uncertainty, product or system effects, and questions unlocked. If internet tools are unavailable, add the question to the research queue and continue.

### Converse

Open with enough context for the participant to understand the topic and then give one strong, open invitation. Add a small cluster of optional prompts that helps them tell a complete story. Prefer concrete stories and past behavior:

- “Tell me about the last time this happened.”
- “What happened next?”
- “Who else became involved?”
- “What did you do instead?”

For example: “I want to understand the last real episode before we talk about a product. Walk me through what triggered it, who became involved, where the work became difficult, and what happened in the end. Use whichever parts are useful, and correct any assumptions in that framing.”

Ask for descriptions, examples, clarification, comparisons, and explanations. Do not require the participant to answer every prompt. Record new research questions without interrupting a useful story. Pause during a phase only when a factual unknown blocks progress.

### Consolidate at exit

1. Update the discovery map.
2. Separate researchable facts, participant decisions, and product hypotheses.
3. Identify what changed, what remains uncertain, and what the next phase needs.
4. Research only questions that could reshape the synthesis or unlock better next questions.
5. Update the notebook.
6. Give a concise playback and transition in plain language. Use the transition to frame the next interview topic, not merely to append another question.

Use research to improve the next question. Do not give a separate research presentation. If research only confirms the current view, record it and move on.

## Run early discovery: establish reality

Develop a credible account of the idea, desired change, why it matters now, concrete current situations, actors, current alternatives, friction, consequences, wider journey, and initial opportunity space.

Research domain vocabulary, category context, named platforms, public constraints, and adjacent approaches only when it improves the conversation. Leave early discovery when you can explain the situation, actors, current behavior, desired progress, and useful opportunity choices. This does not prove demand.

## Run middle discovery: shape the product bet

Work with the participant to select a target opportunity, clarify the consequence of doing nothing, compare possible responses, agree on a product promise, define the smallest complete experience, and trace the core value journey from real-world trigger to meaningful outcome.

Mark where the product accepts responsibility and where responsibility passes to a person or outside system. Clarify adoption, incentives, buying, value exchange, costs, operating responsibility, consequential branches, and non-goals. Do not turn the result into a feature backlog.

## Run late discovery: frame domain, system, and risk

Capture actors, triggers, activities, events, decisions, business rules, important information and state changes, exceptional paths, external systems and organizations, data sources, responsibility boundaries, and operating conditions.

Learn technical needs through concrete situations. Ask what must remain true during peak demand, failures, sensitive decisions, outside outages, or future changes. Cover trust, privacy, security, compliance, availability, performance, scale, interoperability, auditability, and changeability only where the product context makes them material.

State conditions future architecture must support. Do not select a cloud, framework, database, service structure, or target architecture.

## Track important dependencies

Track platforms, data sources, regulations, standards, organizational processes, partners, suppliers, categories, competitors, and domain concepts when they can change the product.

For each, record its role, current understanding, research questions, findings and uncertainty, product or system implications, questions unlocked, and remaining unknowns. Research only when the answer could change the next question, target opportunity, product promise, critical experience, system boundary, or learning priority.

## Finish the discovery

Close when the desired change, target opportunity, actor value, product promise, smallest value loop, core value journey, responsibility boundaries, material handoffs, domain and system context, business conditions, future-architecture needs, riskiest assumptions, and next learning moves form one coherent account.

Give one concise closing playback and allow correction. Then write a shareable Greenfield Discovery Brief using [the brief template](assets/greenfield-discovery-brief-template.md). Follow an existing documentation convention; otherwise use:

- `docs/discovery/<product-slug>-greenfield-discovery.md` in a repository
- `discovery/<product-slug>-greenfield-discovery.md` in an ordinary folder

Separate supplied source material from external research. Cite important claims near the text they support.

Read [the core value journey guide](references/core-value-journey.md) and [the adaptive discovery artifact guide](references/discovery-artifacts.md). Create the smallest useful visual package and one product discovery briefing. Always create editable source for the core value journey. Add focused actor, opportunity, domain, dependency, branch, or learning-priority views only when they materially improve understanding. Keep every visual at the discovery level.

Use a supplied presentation template when clearly intended. Otherwise use a neutral 16:9 style. Render and inspect published diagrams and slides when tooling is available. If PowerPoint authoring is unavailable, create a complete `.slides.md` storyboard and do not claim a `.pptx` exists.

Finish the session with the target opportunity, current product thesis, core value journey and product responsibility, important dependencies, assumptions most likely to disprove the idea, recommended next learning move, and durable paths.

If the participant pauses early, update the notebook and return only the current position, what remains open, the recommended next phase, and the notebook path.

## Do not cross the boundary

Do not produce a Product Brief, feature backlog, roadmap, project plan, target architecture, stack recommendation, implementation issues, or code. Do not recommend building merely because discovery began with an application idea. Do not claim that source material, conversation, or desk research validated a market.
