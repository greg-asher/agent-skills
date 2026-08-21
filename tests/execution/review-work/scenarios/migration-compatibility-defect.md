# Migration compatibility defect

`EX-901` is Implemented by commit `abc901`. It changes `jobs.state` from a string to a structured object. The deployment design permits old and new workers to overlap during rolling deployment.

The migration rewrites every existing string value to a JSON object. The new worker reads both formats. The old worker still compares the database value directly with string literals and fails after any rewritten row is leased. No mixed-version test exists.
