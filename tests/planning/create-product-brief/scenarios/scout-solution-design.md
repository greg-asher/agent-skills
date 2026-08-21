# Scout Solution Design

## Proposed solution

Scout is a company web application accessed through enterprise single sign-on. It builds an evidence-backed account brief from approved internal and external sources. Salesforce remains the system of record for accounts and seller-authored notes.

## Defining experience

The seller starts in an Account Queue containing assigned accounts. Opening an account loads an Account Brief with up to three opportunity hypotheses. Each hypothesis states the opportunity, why it may matter now, supporting evidence, conflicting evidence, source dates, and confidence limits.

The seller can open the Evidence Panel to inspect individual claims. The seller can select one hypothesis, edit the generated summary, and use the Save to Salesforce action. Scout shows the exact note before writing it and reports whether the save succeeded.

## Important behavior

- The Account Queue distinguishes ready, refreshing, unavailable, and never-analyzed accounts.
- An Account Brief can display partial evidence when one source is unavailable, but it must identify the missing source.
- A hypothesis with stale material evidence is marked stale rather than silently refreshed in place.
- Conflicting evidence appears beside supporting evidence.
- Save to Salesforce requires an explicit seller action and is idempotent when retried after an uncertain response.
- A failed save preserves the edited note and offers a retry.
- Sellers can dismiss a hypothesis and give one optional reason. Dismissal affects later ranking for that account.

The Account Queue uses this state contract:

- An account is `never analyzed` until its first analysis is requested.
- Starting an analysis or refresh changes the account to `refreshing`.
- A successful analysis changes the account to `ready` and preserves its analysis version.
- A failed first analysis changes the account to `unavailable` and shows that no brief exists.
- A failed refresh preserves the last usable brief, marks its evidence state, and shows the refresh failure instead of replacing the brief.

Revenue Operations maintains the approved freshness policy. Salesforce account and opportunity data is stale after 24 hours, Snowflake usage data after 48 hours, and third-party firmographic data after 30 days.

## System responsibilities

An account analysis service coordinates source reads and hypothesis generation. An evidence store preserves claims, source references, retrieval time, and analysis version. A Salesforce adapter reads account context and writes only seller-approved notes. An identity layer maps the signed-in seller to assigned accounts.

Enterprise Application Support owns Scout availability, failed analyses, Salesforce write failures, and seller support. It escalates source access and source-quality incidents to Revenue Operations. Revenue Operations owns source approval, freshness policy, and the decision to disable an unreliable source.

## Data and integration boundaries

Salesforce owns account identity, assignments, opportunities, and saved notes. Snowflake owns product-usage facts. The third-party provider owns firmographic records. Scout owns derived hypotheses, evidence links, dismissals, and generated brief drafts.

## Important qualities

The product must preserve claim provenance, prevent unauthorized account access, and make partial or stale evidence visible. Analysis may complete asynchronously. The user experience should remain usable when one noncritical source is unavailable.

## Not part of the solution

The first release does not create opportunities, send outreach, recommend price, or support accounts outside the seller's Salesforce assignment.
