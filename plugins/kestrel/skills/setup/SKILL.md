---
name: setup
description: Install, configure, upgrade, verify, or repair the Kestrel CLI and Local Core. Use only when the user explicitly invokes /kestrel:setup or explicitly approves setup after another Kestrel skill reports that Kestrel is unavailable or incompatible.
disable-model-invocation: true
---

# Set Up Kestrel

Read [the shared lifecycle contract](../../references/lifecycle.md) and [the writing guide](references/plain-language-writing.md).

Run `kestrel-plugin setup` without `--approve-install` first. Report detected Node, platform, executable, required package, resolved stable version, exact install command, and destination.

Require Node.js 22 on macOS arm64 or Linux x64 and Kestrel 0.8.8 or newer. Do not install Node or change the user's version manager. Treat explicit `--kestrel-bin` as authoritative; report `COMPATIBILITY_ERROR` instead of installing a different executable.

If installation or upgrade is required for a missing, persisted, or PATH selection, obtain explicit approval and rerun with `--approve-install`. Setup resolves the npm-installed binary from `npm prefix -g`, persists its absolute realpath, and configures the `kestrel` profile with the `dev` approval pack unless the user supplied overrides. Verify the real V2 job preflight and Local Core health under the selected `KESTREL_HOME`. Report the exact installed version, realpath, and any remaining blocker.
