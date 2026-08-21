# Agent Skills

Reusable Claude Code skills for discovery, solution design, and implementation planning.

## Discovery plugin

The `discovery` plugin contains two skills:

| Skill | Purpose |
| --- | --- |
| `/discovery:start-discovery` | Develop a greenfield product idea through a guided conversation and focused research. Produces a living discovery notebook and a shareable Greenfield Discovery Brief. |
| `/discovery:deep-discovery` | Investigate an existing application with coordinated subagents and end-to-end workflow traces. Produces a short session synthesis and a durable technical discovery report. |

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

Arguments are optional. Each skill can establish its starting context from the current session and workspace.

## What the skills produce

`start-discovery` maintains `.discovery/<product>/notebook.md` during the conversation. When discovery is complete, it writes a Greenfield Discovery Brief using the repository's documentation conventions.

`deep-discovery` writes `docs/discovery/<application>-deep-discovery.md` unless the repository has another clear documentation convention.

Both skills use the included plain-language writing rules. Reports lead with the main finding, explain unfamiliar terms, and separate facts from claims, inference, and unknowns.

`start-design` maintains `.design/<initiative>/notebook.md` and writes `docs/design/<initiative>-solution-design.md` unless another documentation convention is clear.

`change-design` maintains `.design/<change>/notebook.md` and writes `docs/design/<change>-change-design.md`. Its report connects external research to the actual code paths, contracts, data, and system boundaries affected by the change.

`create-product-brief` writes `docs/planning/<initiative>-product-brief.md` unless another documentation convention is clear. It combines the product narrative with Business and Process, Technology, and People requirements.

`create-issues` writes an implementation queue and individual issue files under `docs/planning/<initiative>/issues/`. It creates tracker issues only when explicitly requested.

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
tests/discovery/                      Evaluation prompts and fixtures
tests/design/                         Design evaluation prompts and scenarios
tests/planning/                       Planning evaluation prompts and scenarios
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
```

Load the plugin directly during development:

```bash
claude --plugin-dir ./plugins/discovery
claude --plugin-dir ./plugins/design
claude --plugin-dir ./plugins/planning
```

## Security

The plugins include no hooks, Model Context Protocol servers, executable skill scripts, or preapproved tools. Review skill instructions before installation, as you would with any agent extension.

## License

MIT
