# <Failed behavior>

## Failed behavior

Describe what goes wrong, who or what is affected, and the conditions that trigger it.

## Affected flow

Link the affected implementation issue and change range. Trace the failure from its trigger through the participating components to the observable result, and name every component that must change.

## Repair requirements

State the behavior and constraints the repair must preserve. Do not prescribe a mechanism unless the settled design requires it.

## Done when

- The triggering scenario produces the expected observable behavior.
- A focused regression check covers the failure path.
- Complete-flow validation proves the intended behavior end to end.
- The affected issue's original outcome and constraints still hold.

## Depends on

List only genuine prerequisites. Write `None` when the repair can start immediately.
