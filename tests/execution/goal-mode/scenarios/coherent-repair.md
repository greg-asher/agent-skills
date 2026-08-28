# Coherent repair reconciliation

Review of `EX-1401` confirms that resumed exports can produce duplicate downloadable artifacts. The reviewers report an omitted identity in the resume producer, an optional completion DTO field, and fallback identity generation in persistence. The download consumer publishes both stored results.

No repair issue exists yet. All findings belong to the same resume transaction and violate the same stable-artifact guarantee. Restoring the promised outcome requires one coordinated repair across the producer, DTO, persistence, and consumer flow. Separate component-level patches would only move the failure to the next surface.
