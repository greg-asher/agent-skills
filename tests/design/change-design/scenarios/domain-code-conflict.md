# Cancellation conflict

The participant says customers may cancel one line from a multi-line order. Current code and tests expose only whole-order cancellation. Existing documentation uses `cancellation` for both behaviors. The design has not settled whether partial cancellation is a new requirement or a terminology mistake.
