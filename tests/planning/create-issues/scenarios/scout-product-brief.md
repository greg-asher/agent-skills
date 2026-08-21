# Scout Product Brief

## Product Narrative

Enterprise account executives spend hours reconciling customer records, product usage, and market information before they can identify credible whitespace. Scout turns an assigned account into a small set of evidence-backed opportunity hypotheses. The seller remains responsible for choosing a hypothesis and deciding what enters Salesforce.

## Outcomes and Delivery Boundary

The seller can reach one defensible opportunity hypothesis and a usable account brief faster than through manual research. Scout does not create opportunities, send outreach, recommend pricing, change opportunity stages, or cover accounts outside the seller's Salesforce assignment.

## Defining Scenarios

### Investigate an assigned account

The seller opens the Account Queue and selects an assigned account. Scout shows whether analysis is ready, refreshing, unavailable, or has never run. The Account Brief presents up to three hypotheses with supporting evidence, conflicting evidence, sources, freshness, and confidence limits.

### Select and act on a hypothesis

The seller inspects claims in the Evidence Panel, selects one hypothesis, edits its summary, previews the Salesforce note, and explicitly saves it. Scout confirms success. If the response is uncertain or fails, Scout preserves the draft and lets the seller retry without creating duplicate notes.

### Work with incomplete evidence

Scout can show a partial brief when a noncritical source is unavailable and identifies the missing source. Material stale evidence is marked stale. Scout never hides conflicting evidence.

## Business and Process Requirements

- Sellers can investigate only accounts assigned to them in Salesforce.
- A brief contains no more than three ranked hypotheses.
- Every material claim shows its source and freshness.
- Sellers can dismiss a hypothesis and optionally state why.
- Scout writes to Salesforce only after the seller previews and approves the note.
- The pilot measures preparation time, brief usage, and hypothesis acceptance without imposing an unsettled numeric threshold.

## Technology Requirements

- Scout is a company web application using enterprise single sign-on.
- The identity boundary maps the signed-in seller to Salesforce account assignments and prevents access to other accounts.
- Salesforce owns account identity, assignments, opportunities, and saved notes. Snowflake owns product-usage facts. The approved third-party provider owns firmographic records.
- Scout owns derived hypotheses, evidence links, dismissals, and generated brief drafts.
- Account analysis can complete asynchronously. The queue exposes its current state.
- An account is never analyzed until its first request, refreshing while analysis runs, ready after success, and unavailable after a failed first analysis. A failed refresh preserves the last usable brief and shows the failure.
- Scout preserves the source, retrieval time, and analysis version for every material claim.
- Salesforce account and opportunity data is stale after 24 hours, Snowflake usage data after 48 hours, and third-party firmographic data after 30 days.
- The Salesforce integration reads account context and writes only seller-approved notes. Retrying an uncertain save cannot create a duplicate note.
- The experience remains usable when one noncritical source is unavailable and makes stale, missing, and conflicting evidence visible.

## People and Operating Requirements

- The seller owns hypothesis selection, edits, dismissal feedback, and the final decision to save a note.
- Revenue Operations owns approved data access and source quality and investigates missing or stale source data during the pilot.
- Revenue Operations owns the freshness policy and the decision to disable an unreliable source.
- Enterprise Application Support owns Scout availability, failed analyses, Salesforce write failures, and seller support. It escalates source incidents to Revenue Operations.
- Sales leaders review pilot adoption and hypothesis acceptance without gaining permission to write notes on a seller's behalf.

## Success and Readiness

Pilot sellers reach an accepted hypothesis and usable brief faster than with manual research. Preparation time, brief usage, and hypothesis acceptance are observable pilot measures.

`Ready for issue creation`

## Source Artifacts

- Scout Greenfield Discovery Brief
- Scout Solution Design
