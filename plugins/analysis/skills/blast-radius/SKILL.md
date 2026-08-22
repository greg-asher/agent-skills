---
name: blast-radius
description: Analyze the direct and indirect impact of one proposed software change across files, packages, interfaces, state, configuration, environment variables, runtime services, events, tests, deployments, and protected surfaces. Use before an agent or engineer executes a consequential refactor, migration, integration, or multi-file change and needs grounded readiness evidence or a minimal task context pack.
---

# Blast Radius

Determine what one intended change can affect before anyone executes it. Analysis remains read-only. A downstream execution harness decides whether to enforce the readiness result.

Treat `$ARGUMENTS` and the current conversation as the change intent. Read [the Analysis evidence contract](../../references/evidence-contract.md) and [the plain-language writing guide](references/plain-language-writing.md).

## 1. Resolve the change contract

State the intended outcome, named targets, in-scope behavior, protected behavior, and separately authorized external effects. If a material ambiguity would change the impact boundary, ask one focused question before continuing.

Load `.analysis/workspace-model.json` when present. Check its revision and coverage. Refresh the affected model surfaces through direct inspection when the model is missing, stale, or incomplete. Do not treat the model as proof by itself.

## 2. Trace impact

Begin at the earliest changed contract and follow both direct and indirect relationships:

- callers, imports, exports, interfaces, shared types, and generated consumers
- configuration, feature flags, environment-variable names, and defaults
- state ownership, schemas, migrations, caches, queues, and events
- processes, services, jobs, deployments, and external integrations
- tests, fixtures, build tasks, release paths, documentation, and operating procedures

Trace runtime and event relationships separately from static code relationships. Identify where evidence stops.

## 3. Assess readiness

Use one result:

- `ready`: the material boundary is current and supported; unknowns do not threaten the stated outcome.
- `caution`: material uncertainty remains, but the change can be bounded with explicit constraints and validation.
- `not-ready`: unresolved targets, stale coverage, unknown runtime effects, missing authority, or contradictory evidence prevents a credible boundary.

This is an evidence-backed assessment, not an execution lock. Never weaken `not-ready` merely to produce a context pack.

## 4. Produce the outputs

Choose a short change slug. Write:

- `.analysis/blast-radius/<change-slug>.json` against [the Blast Radius schema](../../assets/blast-radius.schema.json)
- `.analysis/blast-radius/<change-slug>.md` as the readable report

The report leads with readiness and the main reason, then covers intent, direct impact, indirect impact, protected surfaces, evidence, unknowns, and required validation.

Include the smallest useful context pack only when evidence supports it. The pack contains the objective, relevant paths, interfaces, runtime constraints, evidence IDs, allowed actions, prohibited actions, and required validation. Prefer references and interface summaries to raw source bodies.

## 5. Verify and stop

Parse the JSON, resolve every evidence ID, and confirm the workspace revision. Do not modify product code, run destructive tests, deploy, change providers, or execute the proposed change. Report the result and the smallest evidence needed to move from `caution` or `not-ready` to `ready`.
