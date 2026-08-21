# Forward-Test Results

Tested with fresh agents in isolated workspaces on 2026-08-20.

These results cover the conversational discovery workflow before adaptive visual and presentation packaging was added. The later packaging changes are covered by the updated evaluation scenarios and repository and Claude plugin validation. No additional subagent forward tests were run for that change.

## B2B platform dependencies

The agent opened with a recent missed-expansion story rather than a feature or data question. Across three turns it followed the seller's investigation, separated the sponsor thesis from observed behavior, and maintained a detailed Scout notebook.

At the early-to-middle phase boundary it researched relevant Salesforce hierarchy and identity-resolution capabilities, used those findings to challenge the need for another account directory, and returned with one sharper question about the smallest evidence-backed handoff. It did not select an integration or architecture.

Result: pass.

## Solution-first consumer idea

The agent opened on the founder's most recent meal-coordination episode. After learning that schedule changes and household coordination mattered more than recipe discovery, it reframed the center of the problem without discarding the initial idea and followed the Wednesday failure path with one natural question.

Result: pass.

## Resumable discovery

The agent reconstructed the supplied middle-discovery position and did not repeat early questions. It opened on the incoming nurse's required end state, then followed the lost pending-lab story into ownership, timing, and responsibility transfer.

Result: pass.

## Observed package behavior

- One meaningful question or tightly related pair per turn.
- Concrete stories before abstractions.
- Current notebook state preserved between turns.
- Research introduced when a learned dependency could improve the next phase.
- Research integrated into the next product question rather than presented as a detached briefing.
- No Product Brief, backlog, architecture, stack, or implementation output.

The regulated-workflow scenario remains in the reusable evaluation set for future regression testing.
