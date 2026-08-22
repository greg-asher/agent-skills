# Agent Skills

Reusable Claude Code skills for workspace analysis, discovery, solution design, implementation planning, coordinated execution, independent review, and Kestrel delegation.

## Discovery plugin

The `discovery` plugin contains two skills:

| Skill | Purpose |
| --- | --- |
| `/discovery:start-discovery` | Develop a greenfield product idea through context-rich interviews, local source intake, and focused research. When meaningful material exists, it synthesizes it before asking the first unanswered question. |
| `/discovery:deep-discovery` | Investigate software, documents, designs, data, or a mixed folder. Produces an evidence-linked knowledge base and only the report, source, architecture, onboarding, visual, and briefing assets the material supports. |

Both skills are manually invoked. They keep discovery separate from Product Brief writing, target architecture, roadmaps, and implementation.

## Design plugin

The `design` plugin contains two skills:

| Skill | Purpose |
| --- | --- |
| `/design:start-design` | Turn a settled greenfield discovery into a coherent new solution design through conversation, current research, alternatives, models, and focused prototypes. |
| `/design:change-design` | Design an enhancement, integration, migration, or structural change through focused code investigation and current external research. |

Both design skills maintain a living design notebook. They adapt their next move to the current design question instead of following a fixed architecture checklist.

## Planning plugin

The `planning` plugin contains two skills:

| Skill | Purpose |
| --- | --- |
| `/planning:create-product-brief` | Compile settled discovery and design into one canonical Product Brief across Business and Process, Technology, and People. |
| `/planning:create-issues` | Turn a delivery-ready Product Brief into a small set of vertical, agent-ready implementation issues. |

Planning is convergent. It packages settled discovery and design decisions into one canonical delivery brief, then turns that brief into implementation issues without restarting discovery or design.

## Execution plugin

The `execution` plugin contains three skills and three model-neutral agents:

| Skill | Purpose |
| --- | --- |
| `/execution:goal-mode` | Drive an approved issue plan through alternating implementation and independent review until it reaches a verified end state or a proven blocker. |
| `/execution:work-on-issues` | Select and implement one coherent wave from the ready issue frontier, update the graph, and create one local integration commit. |
| `/execution:review-work` | Independently review implemented issues, create repair issues for confirmed defects, and gate completion. |

Execution uses the tracker supplied for the invocation or Planning's local implementation queue. The active Claude Code model orchestrates the work, and packaged agents inherit that model.

## Kestrel plugin

The `kestrel` plugin contains one skill:

| Skill | Purpose |
| --- | --- |
| `/kestrel:assign` | Assign a bounded repository task to Kestrel for autonomous implementation and validation in an isolated managed worktree. |

The skill accepts an implementation issue or a direct task. It submits Kestrel's supported job contract, waits for a terminal result, and returns the result with durable run and replay details.

It requires a locally installed Kestrel CLI with `kestrel job run` support.

## Analysis plugin

The `analysis` plugin contains five skills:

| Skill | Purpose |
| --- | --- |
| `/analysis:map-workspace` | Build a revision-scoped evidence model of workspace boundaries, components, interfaces, dependencies, runtime services, state, configuration, tests, and unknowns. |
| `/analysis:blast-radius` | Trace the direct and indirect impact of one proposed change and report execution readiness without modifying product code or enforcing execution. |
| `/analysis:narrate` | Turn the latest completed run in the current thread into a short, engaging account of the objective, turning points, changes, proof, and unresolved work. |
| `/analysis:game-show` | Host live adaptive repository trivia one grounded question at a time, with optional topic, difficulty, tone, and round-length instructions. |
| `/analysis:teach-me` | Teach the workspace through an adaptive path based on current evidence, the user's goal, recent work, and workspace-scoped learner history. |

Analysis keeps workspace evidence, agent activity, and learner history distinct but compatible. The human-facing skills can run independently. Game Show does not require Narrate, and Teach Me owns direct correction of inaccurate learner signals.

## Install in Claude Code

Add this repository as a marketplace:

```text
/plugin marketplace add greg-asher/agent-skills
```

Install the discovery plugin:

```text
/plugin install discovery@greg-asher-skills
```

Install the design plugin:

```text
/plugin install design@greg-asher-skills
```

Install the planning plugin:

```text
/plugin install planning@greg-asher-skills
```

Install the execution plugin:

```text
/plugin install execution@greg-asher-skills
```

Install the Kestrel plugin:

```text
/plugin install kestrel@greg-asher-skills
```

Install the Analysis plugin:

```text
/plugin install analysis@greg-asher-skills
```

The plugins use Git commit versions. Updating the marketplace and a plugin picks up the latest published commit.

## Use the skills

Start a greenfield product discovery:

```text
/discovery:start-discovery Explore an application that helps account teams investigate commercial whitespace.
```

Investigate an existing application or source corpus:

```text
/discovery:deep-discovery Focus on what this material establishes about the product, its workflows, data, systems, decisions, and current state.
```

Design a new solution from a greenfield discovery:

```text
/design:start-design Use the current Scout discovery brief and help us design the solution.
```

Design a change in an existing application:

```text
/design:change-design Design how this application should move into our standard AWS tenancy. Stay grounded in the code and research current AWS capabilities as they become relevant.
```

Create a Product Brief from settled discovery and design:

```text
/planning:create-product-brief Use the current discovery and design reports to create the canonical Product Brief.
```

Create implementation issues from the Product Brief:

```text
/planning:create-issues Turn the delivery-ready Product Brief into durable, agent-ready issue files.
```

Implement one coherent ready wave:

```text
/execution:work-on-issues Work the current ready frontier. Keep coupled contract changes sequential.
```

Complete an approved issue plan through a durable goal:

```text
/goal Use /execution:goal-mode to complete the approved local issue plan. Preserve unrelated changes and stop only at a verified end state or proven blocker.
```

Review the implemented wave:

```text
/execution:review-work Review every Implemented issue that has not reached Done.
```

Assign one of those issues to Kestrel:

```text
/kestrel:assign Complete docs/planning/scout/issues/02-qualify-opportunity.md
```

Build or refresh the workspace model:

```text
/analysis:map-workspace Focus on runtime, state, and cross-package boundaries.
```

Assess a proposed change before execution:

```text
/analysis:blast-radius Rename the shared InvoiceCreated event without changing external behavior.
```

Catch up after a long agent run:

```text
/analysis:narrate Emphasize the turning points and what the validation established.
```

Start an adaptive repository game at any time:

```text
/analysis:game-show Focus on queue ownership. Five difficult questions with a playful tone.
```

Learn a workspace or correct learner history:

```text
/analysis:teach-me Help me understand retry ownership before I change it.
```

Arguments are optional. Each skill can establish its starting context from the current session and workspace.

## What the skills produce

`start-discovery` maintains `.discovery/<product>/notebook.md` during the conversation. When meaningful local material exists, it also maintains a hashed source manifest and machine-readable source model there. The first pass synthesizes the material without creating a preliminary report, then opens with the first question the sources cannot answer. On resume, it reads only new and changed material. When discovery is complete, it writes a Greenfield Discovery Brief, an editable core value journey, useful supporting visuals, and a product discovery briefing.

`deep-discovery` classifies the current folder as software, a document corpus, mixed, or sparse. In repositories it defaults to `docs/discovery/`; in ordinary folders it defaults to `discovery/`. Document-only investigations produce a canonical report, source guide, source model, evidence-linked knowledge base, useful visuals, and one briefing. Software investigations preserve the revision-scoped application model, evidence catalog, AST and runtime analysis, architecture atlas, onboarding, and presentation flow. Mixed investigations reconcile documented intent with implemented behavior. Sparse folders get an honest evidence boundary instead of manufactured artifacts.

The artifact packages expand and contract with the application. Small systems use combined views and a compact presentation. Large systems gain linked subsystem, flow, data, runtime, and cross-cutting views only where the overview would lose important distinctions.

Both skills use the included plain-language writing rules. Reports lead with the main finding, explain unfamiliar terms, and separate facts from claims, inference, and unknowns.

`start-design` maintains `.design/<initiative>/notebook.md` and writes `docs/design/<initiative>-solution-design.md` unless another documentation convention is clear.

`change-design` maintains `.design/<change>/notebook.md` and writes `docs/design/<change>-change-design.md`. Its report connects external research to the actual code paths, contracts, data, and system boundaries affected by the change.

`create-product-brief` writes `docs/planning/<initiative>-product-brief.md` unless another documentation convention is clear. It combines the product narrative with Business and Process, Technology, and People requirements.

`create-issues` writes an implementation queue and individual issue files under `docs/planning/<initiative>/issues/`. It creates tracker issues only when explicitly requested.

`work-on-issues` advances selected issues from `Ready` through `In progress` to `Implemented`, updates dependencies when the code reveals them, and creates one local integration commit for a successful wave. It does not push or open a pull request.

`review-work` reviews the wave without modifying product code. It advances clean issues to `Done`, creates repair issues for confirmed defects, updates blocking relationships, and makes a separate local issue-state commit when local issue files change.

`goal-mode` keeps a compact ledger of authoritative, implementation, validation, protected, external, and evidence surfaces. It alternates the two execution workflows until all in-scope issues are `Done` or the remaining work is genuinely blocked. It does not authorize pushes, pull requests, deployments, or other external mutations.

`map-workspace` writes `.analysis/workspace-model.json` and `.analysis/workspace-map.md`. The machine-readable model uses stable evidence IDs and distinguishes observation, tests, static analysis, declarations, inference, and unknowns. It records environment-variable names and roles, never values.

`blast-radius` writes paired JSON and Markdown results under `.analysis/blast-radius/`. Each result states `ready`, `caution`, or `not-ready`, traces direct and indirect effects, names required validation, and includes a minimal task context pack only when the evidence supports one. Analysis reports readiness; a separate execution harness decides whether to enforce it.

`narrate` returns its post in the current thread. It reconstructs the latest substantive run across long-running continuations, tool activity, delegated work, retries, failures, and validation. It does not save a file unless the user asks.

`game-show` asks one live question at a time and updates `.analysis/learner-model.json` with concept-level evidence. It can run without recent activity or accept free-form topic, scope, difficulty, tone, and round-length instructions.

`teach-me` creates a dynamic learning path and teaches one grounded concept at a time. Learner history persists across threads and tasks in the same workspace. Users inspect, dispute, correct, or remove inaccurate signals directly through Teach Me.

The complete lifecycle is:

```text
Discover -> Design -> Plan -> Goal Mode
                              |        |
                              v        |
                       Work on Issues  |
                              |        |
                              v        |
                         Review Work --+
```

`kestrel:assign` writes the submitted job input and Kestrel's durable output under the plugin data directory. Kestrel implements and validates the task in a session-isolated managed worktree; the skill reports the terminal result, identifiers, artifact paths, and replay command.

Analysis sits beside the lifecycle. Its workspace model can ground discovery, design, planning, and execution, while Narrate, Game Show, and Teach Me turn work from any phase into durable human understanding.

## Repository structure

```text
.claude-plugin/marketplace.json       Marketplace catalog
plugins/discovery/                    Installed Claude Code plugin
  .claude-plugin/plugin.json
  agents/source-investigator.md
  assets/source-model.schema.json
  references/source-investigation.md
  scripts/source-corpus.py
  skills/start-discovery/
  skills/deep-discovery/
plugins/design/                       Installed Claude Code plugin
  .claude-plugin/plugin.json
  skills/start-design/
  skills/change-design/
plugins/planning/                     Installed Claude Code plugin
  .claude-plugin/plugin.json
  skills/create-product-brief/
  skills/create-issues/
plugins/execution/                    Installed Claude Code plugin
  .claude-plugin/plugin.json
  skills/goal-mode/
  skills/work-on-issues/
  skills/review-work/
  agents/issue-worker.md
  agents/change-reviewer.md
  agents/adversarial-reviewer.md
plugins/kestrel/                      Installed Claude Code plugin
  .claude-plugin/plugin.json
  bin/kestrel-assign
  skills/assign/
plugins/analysis/                     Claude Code and Codex plugin
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  assets/                             Workspace, run, learner, and blast-radius schemas
  references/                         Shared evidence, run, and learning contracts
  skills/map-workspace/
  skills/blast-radius/
  skills/narrate/
  skills/game-show/
  skills/teach-me/
tests/discovery/                      Evaluation prompts and fixtures
  source-corpus/                      Dependency-free corpus and OOXML extractor tests
tests/design/                         Design evaluation prompts and scenarios
tests/planning/                       Planning evaluation prompts and scenarios
tests/execution/                      Execution evaluation prompts and scenarios
tests/kestrel/                        Kestrel assignment evaluation and wrapper contract test
tests/analysis/                       Analysis evaluation prompts and scenarios
scripts/validate.py                   Dependency-free repository validation
```

Tests stay outside the plugin, so users install only the runtime skill files.

## Develop and validate

Run the dependency-free repository checks:

```bash
python3 scripts/validate.py
```

Validate with Claude Code:

```bash
claude plugin validate .
claude plugin validate ./plugins/discovery
claude plugin validate ./plugins/design
claude plugin validate ./plugins/planning
claude plugin validate ./plugins/execution
claude plugin validate ./plugins/kestrel
claude plugin validate ./plugins/analysis
```

Test the Kestrel job wrapper without starting a live Kestrel run:

```bash
node --test tests/kestrel/assign-script.test.mjs
```

Test source inventory and Office extraction:

```bash
python3 -m unittest discover -s tests/discovery/source-corpus -p 'test_*.py' -v
```

Load the plugin directly during development:

```bash
claude --plugin-dir ./plugins/discovery
claude --plugin-dir ./plugins/design
claude --plugin-dir ./plugins/planning
claude --plugin-dir ./plugins/execution
claude --plugin-dir ./plugins/kestrel
claude --plugin-dir ./plugins/analysis
```

## Security

The plugins include no hooks, Model Context Protocol servers, or preapproved tools. Discovery includes a model-neutral source investigator and a dependency-free Office extractor that rejects unsafe archive paths and bounded-expansion limits. Analysis is read-only with respect to product code and external systems; its default writes are limited to `.analysis/` evidence and learner artifacts, and it records environment-variable names rather than values. Execution includes model-neutral packaged agents; the reviewer agents cannot write files. The Kestrel plugin includes one executable wrapper that invokes a locally installed `kestrel job run`. It requests a managed worktree and does not merge or publish by default. Review skill and agent instructions before installation, as you would with any agent extension.

## License

MIT
