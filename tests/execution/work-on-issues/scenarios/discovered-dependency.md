# Discovered dependency

`EX-301` is Ready and promises that a seller can resume an interrupted analysis without losing approved evidence. The settled design requires resume tokens to survive process restarts.

The current implementation trace shows that resume tokens exist only in an in-process map. No persistence adapter or durable token contract exists. Implementing the visible resume path before that capability would violate the done conditions.

The missing prerequisite can be delivered as a bounded issue: persist and retrieve opaque resume tokens through the existing repository boundary, including restart coverage. It has no unresolved prerequisite.
