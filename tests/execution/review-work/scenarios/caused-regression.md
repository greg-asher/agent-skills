# Non-blocking regression caused by the wave

`EX-1101` is Implemented by commit `abc1101`. It promises that sellers see report generation times in their selected time zone.

The change updates the shared `formatTimestamp` helper used by both seller reports and the administrator diagnostics page. Seller scenarios pass. The new offset calculation makes an administrator timestamp near midnight display the prior calendar date for negative UTC offsets. The raw instant remains correct, and the administrator defect does not block the seller outcome, but the diff establishes that `abc1101` caused the regression.
