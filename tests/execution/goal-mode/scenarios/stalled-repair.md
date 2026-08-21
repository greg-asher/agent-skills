# Repair history

REPAIR-21 restores provider retry recovery. Two implementation cycles changed retry timing, but the same recovery scenario still fails. The evidence ledger points to the provider adapter and its unavailable signed fixture. A third repair cannot validate the acceptance condition without that fixture.
