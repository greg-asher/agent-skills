# Shared event refactor

The intended change renames the public `InvoiceCreated` event to `BillingEvent`. The shared type is exported from `packages/contracts`; the API publishes it; two workers consume it; billing fixtures serialize the old event name; and production queue configuration references a topic whose compatibility is not established. External provider changes and deployment are protected.
