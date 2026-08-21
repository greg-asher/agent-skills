# Agent Skills

Reusable Claude Code skills for discovery, solution design, implementation planning, coordinated execution, independent review, and Kestrel delegation.

## Discovery plugin

The `discovery` plugin contains two skills:

| Skill | Purpose |
| --- | --- |
| `/discovery:start-discovery` | Develop a greenfield product idea through context-rich interviews and focused research. Produces a living notebook, discovery brief, core value journey flowcharts, adaptive supporting visuals, and a product discovery briefing. |
| `/discovery:deep-discovery` | Investigate an existing application through repository analysis and end-to-end workflow traces. Produces a report, evidence-linked knowledge base, AST-backed architecture atlas, onboarding material, and adaptive presentation package. |

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

The `execution` plugin contains two skills and three model-neutral agents:

| Skill | Purpose |
| --- | --- |
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

The plugins use Git commit versions. Updating the marketplace and a plugin picks up the latest published commit.

## Use the skills

Start a greenfield product discovery:

```text
/discovery:start-discovery Explore an application that helps account teams investigate commercial whitespace.
```

Investigate an existing application:

```text
/discovery:deep-discovery Focus on what the application does, its main workflows, data movement, architecture, and build status.
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

Review the implemented wave:

```text
/execution:review-work Review every Implemented issue that has not reached Done.
```

Assign one of those issues to Kestrel:

```text
/kestrel:assign Complete docs/planning/scout/issues/02-qualify-opportunity.md
```

Arguments are optional. Each skill can establish its starting context from the current session and workspace.

## What the skills produce

`start-discovery` maintains `.discovery/<product>/notebook.md` during the conversation. When discovery is complete, it writes a Greenfield Discovery Brief and an editable flowchart of the core value journey the product will be responsible for. It adds focused branch flows and supporting opportunity, actor, domain, dependency, or learning-priority visuals only when they improve understanding. It also creates a product discovery briefing.

`deep-discovery` writes `docs/discovery/<application>-deep-discovery.md` and a companion asset package. It combines AST and static analysis with runtime, deployment, and value-path evidence to build a revision-scoped application model with stable IDs and a central evidence catalog. That model powers a navigable discovery knowledge base and is projected into a multi-resolution architecture atlas, onboarding guide, and discovery and onboarding presentations.

The artifact packages expand and contract with the application. Small systems use combined views and a compact presentation. Large systems gain linked subsystem, flow, data, runtime, and cross-cutting views only where the overview would lose important distinctions.

Both skills use the included plain-language writing rules. Reports lead with the main finding, explain unfamiliar terms, and separate facts from claims, inference, and unknowns.

`start-design` maintains `.design/<initiative>/notebook.md` and writes `docs/design/<initiative>-solution-design.md` unless another documentation convention is clear.

`change-design` maintains `.design/<change>/notebook.md` and writes `docs/design/<change>-change-design.md`. Its report connects external research to the actual code paths, contracts, data, and system boundaries affected by the change.

`create-product-brief` writes `docs/planning/<initiative>-product-brief.md` unless another documentation convention is clear. It combines the product narrative with Business and Process, Technology, and People requirements.

`create-issues` writes an implementation queue and individual issue files under `docs/planning/<initiative>/issues/`. It creates tracker issues only when explicitly requested.

`work-on-issues` advances selected issues from `Ready` through `In progress` to `Implemented`, updates dependencies when the code reveals them, and creates one local integration commit for a successful wave. It does not push or open a pull request.

`review-work` reviews the wave without modifying product code. It advances clean issues to `Done`, creates repair issues for confirmed defects, updates blocking relationships, and makes a separate local issue-state commit when local issue files change.

The complete lifecycle is:

```text
Discover -> Design -> Plan -> Work on Issues -> Review Work
                                      ^              |
                                      |--- defects ---|
```

`kestrel:assign` writes the submitted job input and Kestrel's durable output under the plugin data directory. Kestrel implements and validates the task in a session-isolated managed worktree; the skill reports the terminal result, identifiers, artifact paths, and replay command.

## Repository structure

```text
.claude-plugin/marketplace.json       Marketplace catalog
plugins/discovery/                    Installed Claude Code plugin
  .claude-plugin/plugin.json
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
  skills/work-on-issues/
  skills/review-work/
  agents/issue-worker.md
  agents/change-reviewer.md
  agents/adversarial-reviewer.md
plugins/kestrel/                      Installed Claude Code plugin
  .claude-plugin/plugin.json
  bin/kestrel-assign
  skills/assign/
tests/discovery/                      Evaluation prompts and fixtures
tests/design/                         Design evaluation prompts and scenarios
tests/planning/                       Planning evaluation prompts and scenarios
tests/execution/                      Execution evaluation prompts and scenarios
tests/kestrel/                        Kestrel assignment evaluation and wrapper contract test
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
```

Test the Kestrel job wrapper without starting a live Kestrel run:

```bash
node --test tests/kestrel/assign-script.test.mjs
```

Load the plugin directly during development:

```bash
claude --plugin-dir ./plugins/discovery
claude --plugin-dir ./plugins/design
claude --plugin-dir ./plugins/planning
claude --plugin-dir ./plugins/execution
claude --plugin-dir ./plugins/kestrel
```

## Security

The plugins include no hooks, Model Context Protocol servers, or preapproved tools. Execution includes model-neutral packaged agents; the reviewer agents cannot write files. The Kestrel plugin includes one executable wrapper that invokes a locally installed `kestrel job run`. It requests a managed worktree and does not merge or publish by default. Review skill and agent instructions before installation, as you would with any agent extension.

## License

MIT
