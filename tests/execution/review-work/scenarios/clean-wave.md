# Clean implemented wave

`EX-601` is Implemented by commit `abc601`. It promises filesystem-safe export names while preserving a human-readable account name.

The diff changes only `src/export-name.ts` and its tests. It normalizes separators, rejects control characters, preserves Unicode letters, and supplies `export` when the normalized name is empty. The focused, integration, and compatibility tests pass. Surrounding callers use the returned name only as a download filename.

No working-tree product changes exist after `abc601`.
