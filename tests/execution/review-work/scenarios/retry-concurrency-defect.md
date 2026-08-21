# Retry and concurrency defect

`EX-801` is Implemented by commit `abc801`. It promises that payment-provider retries never create more than one charge for an order.

The handler checks `charges` for the provider event identifier, calls the provider, then inserts the identifier. There is no uniqueness constraint or transaction around the check and insert. Two workers can read the missing row together, both call the provider, and only then record completion. Unit tests retry sequentially and pass.
