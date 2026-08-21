# Failed integration check

`EX-501` is In progress. Its worker added retry support and all focused unit tests pass.

The issue promises that a retried export returns the same artifact identity and never creates two downloadable artifacts for one run. The wave-level scenario sends the same completion event twice. The second event creates a new artifact identifier, so the scenario fails.

No external dependency or design contradiction has been identified.
