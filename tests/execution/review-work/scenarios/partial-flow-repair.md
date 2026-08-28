# Local repair leaves the flow broken

`EX-1301` is Implemented by commit `abc1301`. It promises that a resumed export reaches one downloadable completion.

The change adds a DTO guard that rejects completion events without `artifactIdentity`, and its focused DTO tests pass. The permitted resume producer still emits events without that field. Those events now stop at the guard, the persistence row remains pending, and the download consumer times out.

The local guard changes the first observed failure but does not restore the promised end-to-end behavior. Review must trace the producer, DTO, persistence, and consumer flow before defining one blocking repair.
