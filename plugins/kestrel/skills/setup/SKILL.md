---
name: setup
description: Install, configure, upgrade, verify, or repair the Kestrel CLI and Local Core. Use only when the user explicitly invokes /kestrel:setup or explicitly approves setup after another Kestrel skill reports that Kestrel is unavailable or incompatible.
disable-model-invocation: true
---

# Set Up Kestrel

Read [the shared lifecycle contract](../../references/lifecycle.md) and [the writing guide](references/plain-language-writing.md).

Run `kestrel-plugin setup` without `--approve-install` first. Report detected Node, platform, executable, required package, resolved stable version, exact install command, and destination.

Require Node.js 22 on macOS arm64 or Linux x64. Do not install Node or change the user's version manager. Do not overwrite an executable that cannot be identified as Kestrel.

If installation or upgrade is required, obtain explicit approval, rerun with `--approve-install`, then let setup configure the `kestrel` profile with the `dev` approval pack unless the user supplied overrides. Verify required commands and Local Core health. Report the exact installed version and any remaining blocker.
