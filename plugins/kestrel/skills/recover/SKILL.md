---
name: recover
description: Diagnose and safely continue a failed, waiting, or interrupted Kestrel run without duplicating live work. Use only when the user explicitly invokes /kestrel:recover and names or implies a Kestrel run needing recovery.
license: MIT
disable-model-invocation: true
---

# Recover Kestrel Work

Read [the shared lifecycle contract](../../references/lifecycle.md) and [the writing guide](references/plain-language-writing.md).

Run `kestrel-plugin recover` for the named or latest run without `--replay`. Read the manifest, output, doctor evidence, replay pointer, blocker, and current lifecycle.

Never replay a running or completed run and never create a replacement while the original may be active. If evidence establishes an ordinary interruption and no prior automatic replay occurred, rerun with `--replay`. Permit one automatic replay only.

Stop for credentials, authority, semantic decisions, environmental repair, or a second failure. Report the diagnosis, action, final lifecycle, identifiers, and durable evidence paths.
