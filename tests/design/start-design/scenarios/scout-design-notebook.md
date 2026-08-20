# Scout Design Notebook

## Current Position

Scout will help an account owner investigate evidence of possible expansion. It will not score or declare opportunities. Two solution directions remain open: a Salesforce-centered investigation experience and a separate investigation workspace that writes selected outcomes back to Salesforce.

## Outcomes and Constraints

- Sellers must understand why evidence was surfaced.
- Salesforce remains authoritative for account ownership and opportunities.
- The first release cannot depend on a complete enterprise customer master.

## Working Design Views

### Experience

The seller opens a surfaced signal, reviews evidence and account context, records a disposition, and can start an existing Salesforce opportunity workflow.

### Domain responsibilities

Current concepts include Account, Signal, Evidence, Investigation, Disposition, and Opportunity. Ownership of Investigation is unsettled.

### External systems and integrations

Salesforce supplies account and opportunity context. Snowflake supplies usage signals. The join between their customer identifiers is incomplete.

## Solution Directions

1. Salesforce-centered: surface and investigate inside Salesforce.
2. Scout workspace: manage investigation state in Scout and write selected results to Salesforce.

## Decisions

- Scout will expose evidence, not an unexplained score.
- Scout will not own opportunity records.

## Active Design Frontier

- Determine the minimum trustworthy identity link needed for the defining experience.
- Decide where investigation state should live after the identity question is better understood.

## Best Next Move

Research current Salesforce identity and integration capabilities relevant to a bounded account-investigation workflow. Use the result to sharpen the identity boundary rather than select a full platform architecture.
