# <Failed behavior>

## Failed behavior

Describe what goes wrong, who or what is affected, and the conditions that trigger it.

## Affected work

Link the affected implementation issue, change range, and relevant code path.

## Repair requirements

State the behavior and constraints the repair must preserve. Do not prescribe a mechanism unless the settled design requires it.

## Done when

- The triggering scenario produces the expected observable behavior.
- A focused regression check covers the failure path.
- The affected issue's original outcome and constraints still hold.

## Depends on

List only genuine prerequisites. Write `None` when the repair can start immediately.
