# Design contradiction

`EX-401` is Ready and adds cached account recommendations. The settled Solution Design requires tenant-scoped cache keys and prevents cross-tenant reuse.

The only cache adapter in the fixture accepts an account identifier but no tenant identifier. A worker proposes using it unchanged and filtering recommendations after retrieval. That would place one tenant's recommendations in another tenant's process before filtering.

Changing the tenant-isolation commitment requires a Design decision.
