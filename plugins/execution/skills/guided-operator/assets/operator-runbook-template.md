# <Operation> Operator Runbook

## Outcome

<Target state and why the operation is required.>

## Authority Boundary

- Agent may: <safe preparation and read-only verification>
- Human must: <authorized actions>
- Separately authorized external effects: <exact effects or none>

## Current State

<Verified state, evidence, and verification time.>

## Prerequisites

- [ ] <Required access, backup, maintenance window, or input name>

## Sensitive Inputs

List names and authorized destinations only. Never record values.

| Input name | Obtained from | Entered into | Persisted |
| --- | --- | --- | --- |
| `<NAME>` | <source> | <destination> | <yes, no, or destination-managed> |

## Stages

### 1. <Stage name>

- Preconditions: <verified conditions>
- Actor: <human or agent>
- Action: <one focused procedure>
- Confirmation gate: <required confirmation or none>
- Expected result: <observable state>
- Evidence: <nonsensitive proof to retain>
- Stop condition: <condition that prevents continuation>
- Recovery or rollback: <exact safe response>
- Resume checkpoint: <state to recheck after interruption>

## Completion Criteria

- [ ] <Observable target state>
- [ ] <Required verification>
- [ ] <Evidence recorded>
- [ ] <Temporary access, state, or resources removed where required>

## Owning Workflow Resume Condition

<Exact evidence and current-state check required before implementation or review resumes.>
