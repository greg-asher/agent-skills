#!/usr/bin/env python3
"""Validate the marketplace, plugin, skills, and evaluation fixtures."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "discovery"
SKILLS = PLUGIN / "skills"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Cannot read valid JSON from {path.relative_to(ROOT)}: {error}")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"Missing YAML frontmatter in {path.relative_to(ROOT)}")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip()
    return values


def validate_skill(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        fail(f"Missing {skill_file.relative_to(ROOT)}")

    metadata = frontmatter(skill_file)
    if metadata.get("name") != skill_dir.name:
        fail(f"Skill name does not match directory: {skill_dir.relative_to(ROOT)}")
    if not metadata.get("description"):
        fail(f"Missing skill description: {skill_file.relative_to(ROOT)}")
    if metadata.get("disable-model-invocation") != "true":
        fail(f"Skill must remain manually invoked: {skill_file.relative_to(ROOT)}")

    text = skill_file.read_text()
    for target in re.findall(r"\]\((assets|references)/([^)]+)\)", text):
        relative = Path(target[0]) / target[1]
        if not (skill_dir / relative).is_file():
            fail(f"Broken skill reference: {skill_dir.name}/{relative}")


def validate_evals(skill_name: str) -> None:
    test_dir = ROOT / "tests" / "discovery" / skill_name
    document = read_json(test_dir / "evals.json")
    if document.get("skill_name") != skill_name:
        fail(f"Wrong skill_name in {test_dir.relative_to(ROOT)}/evals.json")
    for evaluation in document.get("evals", []):
        for relative in evaluation.get("files", []):
            if not (test_dir / relative).is_file():
                fail(f"Missing evaluation fixture: {test_dir.relative_to(ROOT)}/{relative}")


def main() -> None:
    marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")
    if marketplace.get("name") != "greg-asher-skills":
        fail("Unexpected marketplace name")
    if len(marketplace.get("plugins", [])) != 1:
        fail("Marketplace must contain one discovery plugin")

    entry = marketplace["plugins"][0]
    if entry.get("name") != "discovery" or entry.get("source") != "./plugins/discovery":
        fail("Marketplace discovery entry is invalid")

    manifest = read_json(PLUGIN / ".claude-plugin" / "plugin.json")
    if manifest.get("name") != "discovery":
        fail("Plugin manifest name must be discovery")

    expected_skills = {"deep-discovery", "start-discovery"}
    actual_skills = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    if actual_skills != expected_skills:
        fail(f"Unexpected skill folders: {sorted(actual_skills)}")

    for skill_name in sorted(expected_skills):
        validate_skill(SKILLS / skill_name)
        validate_evals(skill_name)

    style_files = [
        SKILLS / "deep-discovery" / "references" / "plain-language-writing.md",
        SKILLS / "start-discovery" / "references" / "plain-language-writing.md",
    ]
    hashes = {hashlib.sha256(path.read_bytes()).hexdigest() for path in style_files}
    if len(hashes) != 1:
        fail("Plain-language writing references differ between skills")

    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            if path.resolve() == Path(__file__).resolve():
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            if "TODO" in text or "[Insert" in text:
                fail(f"Placeholder text remains in {path.relative_to(ROOT)}")

    print("Validation passed")


if __name__ == "__main__":
    main()
