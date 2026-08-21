# Common functional regression

`EX-701` is Implemented by commit `abc701`. It promises safe, readable download names for every export.

The diff removes the existing fallback for an empty normalized account name. The route passes the returned value directly into `Content-Disposition`. An account name made only of slashes now produces an empty filename. Existing tests cover ordinary names but not an empty normalized value.
