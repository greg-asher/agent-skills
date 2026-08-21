# Show the last successful synchronization in account status

## Useful outcome

An operator can tell whether account data is current without reading service logs.

## What changes

Add the last successful synchronization time to the existing account-status response and status view. Preserve the current state and error fields. When no synchronization has completed, show `Never synchronized`.

## Requirements and delivery context

Use the existing synchronization record as the source. Do not add a second timestamp or change synchronization scheduling.

## Done when

- A completed synchronization shows its recorded completion time in the API response and status view.
- An account with no completed synchronization shows `Never synchronized`.
- Existing status and error behavior remains unchanged.
- Focused API and view tests pass.
