# Agent Skills

Reusable Claude Code skills for product and technical discovery.

The first plugin, `discovery`, contains two skills:

| Skill | Purpose |
| --- | --- |
| `/discovery:start-discovery` | Develop a greenfield product idea through a guided conversation and focused research. Produces a living discovery notebook and a shareable Greenfield Discovery Brief. |
| `/discovery:deep-discovery` | Investigate an existing application with coordinated subagents and end-to-end workflow traces. Produces a short session synthesis and a durable technical discovery report. |

Both skills are manually invoked. They keep discovery separate from PRD writing, target architecture, roadmaps, and implementation.

## Install in Claude Code

Add this repository as a marketplace:

```text
/plugin marketplace add greg-asher/agent-skills
```

Install the discovery plugin:

```text
/plugin install discovery@greg-asher-skills
```

The plugin uses Git commit versions. Updating the marketplace and plugin picks up the latest published commit.

## Use the skills

Start a greenfield product discovery:

```text
/discovery:start-discovery Explore an application that helps account teams investigate commercial whitespace.
```

Investigate an existing application:

```text
/discovery:deep-discovery Focus on what the application does, its main workflows, data movement, architecture, and build status.
```

Arguments are optional. Each skill can establish its starting context from the current session and workspace.

## What the skills produce

`start-discovery` maintains `.discovery/<product>/notebook.md` during the conversation. When discovery is complete, it writes a Greenfield Discovery Brief using the repository's documentation conventions.

`deep-discovery` writes `docs/discovery/<application>-deep-discovery.md` unless the repository has another clear documentation convention.

Both skills use the included plain-language writing rules. Reports lead with the main finding, explain unfamiliar terms, and separate facts from claims, inference, and unknowns.

## Repository structure

```text
.claude-plugin/marketplace.json       Marketplace catalog
plugins/discovery/                    Installed Claude Code plugin
  .claude-plugin/plugin.json
  skills/start-discovery/
  skills/deep-discovery/
tests/discovery/                      Evaluation prompts and fixtures
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
```

Load the plugin directly during development:

```bash
claude --plugin-dir ./plugins/discovery
```

## Security

The discovery plugin includes no hooks, Model Context Protocol servers, executable skill scripts, or preapproved tools. Review skill instructions before installation, as you would with any agent extension.

## License

MIT
