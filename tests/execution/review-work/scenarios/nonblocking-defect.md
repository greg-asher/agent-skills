# Pre-existing non-blocking defect

`EX-1001` is Implemented by commit `abc1001`. It promises that sellers can view a report's evidence, generation time, and source links. The change touches only the seller report assembler. All seller paths and permissions pass review.

Review also confirms an existing defect in a separate administrator diagnostics formatter that `abc1001` did not change or call. For administrators in a negative UTC offset, a timestamp near midnight displays the prior calendar date while the raw instant remains correct. Repository history establishes that the defect predates `abc1001`. It does not affect seller reporting, stored data, authorization, or the issue's done conditions.
