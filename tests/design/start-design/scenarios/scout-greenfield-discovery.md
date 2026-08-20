# Scout Greenfield Discovery Brief

## Executive Summary

Commercial leaders want account teams to recognize credible expansion opportunities inside existing enterprise customers. Useful signals are scattered across systems and interpreted differently. Scout should help a seller move from a weak signal to a focused investigation. It should not declare that an opportunity exists or replace seller judgment.

## Target Opportunity

Help an account owner recognize why an existing customer may have unmet demand, understand the supporting evidence, and decide whether to investigate.

## Actors and Value

- Account executives investigate and act on opportunities.
- Sales managers coach sellers and need a consistent basis for reviewing possible whitespace.
- Revenue operations manages account hierarchy, ownership, and commercial definitions.
- Data teams maintain product-usage and customer-behavior data.

## Defining Experience

A seller notices a possible expansion signal, sees why it was surfaced, reviews the supporting account and usage context, records whether it is worth investigating, and carries the useful context into the existing sales workflow.

## Domain and System Context

- Salesforce contains account ownership, account hierarchy, opportunities, and seller activity.
- Snowflake contains product usage and customer behavior.
- A third-party provider supplies firmographic data, but its reliability is unknown.
- The organization has not established a durable identity rule across these sources.

## Design Drivers

- Evidence must be explainable to sellers and managers.
- Account ownership and opportunity activity remain authoritative in Salesforce.
- The design must tolerate incomplete and conflicting source data.
- Data access must respect existing commercial and customer-data permissions.
- The first useful experience should not require an enterprise-wide canonical customer model.

## Non-goals

- Fully automated opportunity qualification
- Replacing Salesforce
- Producing a complete sales analytics platform

## Important Unknowns

- Which identity links are reliable enough to show without manual review?
- Should Scout persist investigation state or write all durable state into Salesforce?
- Which signals create enough value to justify their data and operating cost?
