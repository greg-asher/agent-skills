#!/usr/bin/env python3
"""Bounded, read-only inventory of common developer storage."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


NAMES = {
    "node_modules": ("dependencies", "review-required"),
    ".next": ("build-output", "regenerable"),
    "dist": ("build-output", "regenerable"),
    "build": ("build-output", "regenerable"),
    ".turbo": ("build-cache", "regenerable"),
    ".cache": ("cache", "regenerable"),
    ".pytest_cache": ("test-cache", "regenerable"),
    "__pycache__": ("language-cache", "regenerable"),
}


def size(path: Path) -> int:
    total = 0
    try:
        for root, dirs, files in os.walk(path, followlinks=False):
            dirs[:] = [name for name in dirs if not (Path(root) / name).is_symlink()]
            for name in files:
                try:
                    total += (Path(root) / name).stat(follow_symlinks=False).st_size
                except OSError:
                    pass
    except OSError:
        pass
    return total


def candidates(home: Path) -> list[tuple[Path, str, str]]:
    values = [
        (home / ".npm" / "_cacache", "npm-cache", "regenerable"),
        (home / "Library" / "pnpm" / "store", "pnpm-store", "review-required"),
        (home / ".cache" / "pnpm", "pnpm-cache", "regenerable"),
        (home / ".cache" / "yarn", "yarn-cache", "regenerable"),
        (home / ".codex" / "worktrees", "codex-worktrees", "review-required"),
        (home / ".codex" / "plugin-data", "codex-plugin-data", "review-required"),
        (home / ".claude" / "projects", "claude-project-data", "protected"),
        (home / ".claude" / "plugins" / "cache", "claude-plugin-cache", "regenerable"),
    ]
    return [item for item in values if item[0].exists()]


def scan_root(root: Path, max_depth: int) -> list[tuple[Path, str, str]]:
    found = []
    base_depth = len(root.parts)
    for current, dirs, _ in os.walk(root, followlinks=False):
        path = Path(current)
        depth = len(path.parts) - base_depth
        dirs[:] = [name for name in dirs if name != ".git" and not (path / name).is_symlink()]
        for name in list(dirs):
            if name in NAMES:
                category, safety = NAMES[name]
                found.append((path / name, category, safety))
                dirs.remove(name)
        if depth >= max_depth:
            dirs.clear()
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", default=[], help="Project root to scan; repeatable")
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--project-only", action="store_true", help="Skip Codex, Claude, and package-manager homes")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    roots = [Path(value).expanduser().resolve() for value in args.root]
    if not roots:
        roots = [Path.cwd().resolve()]
    home = Path.home().resolve()
    items = [] if args.project_only else candidates(home)
    for root in roots:
        if root.exists() and root.is_dir():
            items.extend(scan_root(root, max(1, args.max_depth)))
    unique = {}
    for path, category, safety in items:
        canonical = path.resolve()
        unique[str(canonical)] = {
            "path": str(canonical), "category": category, "safety": safety, "bytes": size(canonical)
        }
    results = sorted(unique.values(), key=lambda item: item["bytes"], reverse=True)
    document = {"roots": [str(root) for root in roots], "totalBytes": sum(i["bytes"] for i in results), "items": results}
    if args.json:
        print(json.dumps(document, indent=2))
    else:
        print(f"Measured {document['totalBytes']} bytes across {len(results)} targets")
        for item in results:
            print(f"{item['bytes']:>14}  {item['safety']:<15}  {item['category']:<20}  {item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
