#!/usr/bin/env python3
"""Validate the marketplace, plugins, skills, and evaluation fixtures."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGINS = {
    "discovery": {"deep-discovery", "start-discovery"},
    "design": {"change-design", "start-design"},
    "planning": {"create-issues", "create-product-brief"},
    "execution": {"review-work", "work-on-issues"},
}
EXPECTED_AGENTS = {
    "execution": {"adversarial-reviewer", "change-reviewer", "issue-worker"},
}


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
    for model_key in ("model", "effort"):
        if model_key in metadata:
            fail(f"Skill must remain model-neutral: {skill_file.relative_to(ROOT)}")

    for markdown in skill_dir.rglob("*.md"):
        relative_markdown = markdown.relative_to(skill_dir)
        if relative_markdown.parts[0] == "assets":
            continue
        text = markdown.read_text()
        for raw_target in re.findall(r"\]\(([^)]+)\)", text):
            if raw_target.startswith(("http://", "https://", "#")):
                continue
            target = raw_target.split("#", 1)[0]
            if not target:
                continue
            resolved = (markdown.parent / target).resolve()
            if not resolved.is_file():
                fail(
                    "Broken skill reference: "
                    f"{markdown.relative_to(ROOT)} -> {raw_target}"
                )


def validate_agent(agent_file: Path) -> None:
    metadata = frontmatter(agent_file)
    if metadata.get("name") != agent_file.stem:
        fail(f"Agent name does not match file: {agent_file.relative_to(ROOT)}")
    if not metadata.get("description"):
        fail(f"Missing agent description: {agent_file.relative_to(ROOT)}")
    for model_key in ("model", "effort"):
        if model_key in metadata:
            fail(f"Agent must remain model-neutral: {agent_file.relative_to(ROOT)}")

    if agent_file.stem in {"change-reviewer", "adversarial-reviewer"}:
        allowed = {tool.strip() for tool in metadata.get("tools", "").split(",")}
        if allowed != {"Read", "Grep", "Glob"}:
            fail(f"Review agent must be read-only: {agent_file.relative_to(ROOT)}")


def validate_evals(plugin_name: str, skill_name: str) -> None:
    test_dir = ROOT / "tests" / plugin_name / skill_name
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
    entries = {entry.get("name"): entry for entry in marketplace.get("plugins", [])}
    if set(entries) != set(EXPECTED_PLUGINS):
        fail(f"Unexpected marketplace plugins: {sorted(entries)}")

    style_files: list[Path] = []
    for plugin_name, expected_skills in EXPECTED_PLUGINS.items():
        entry = entries[plugin_name]
        if entry.get("source") != f"./plugins/{plugin_name}":
            fail(f"Marketplace {plugin_name} entry is invalid")

        plugin = ROOT / "plugins" / plugin_name
        skills = plugin / "skills"
        manifest = read_json(plugin / ".claude-plugin" / "plugin.json")
        if manifest.get("name") != plugin_name:
            fail(f"Plugin manifest name must be {plugin_name}")

        actual_skills = {path.name for path in skills.iterdir() if path.is_dir()}
        if actual_skills != expected_skills:
            fail(f"Unexpected {plugin_name} skill folders: {sorted(actual_skills)}")

        for skill_name in sorted(expected_skills):
            validate_skill(skills / skill_name)
            validate_evals(plugin_name, skill_name)
            style_files.append(
                skills / skill_name / "references" / "plain-language-writing.md"
            )

        expected_agents = EXPECTED_AGENTS.get(plugin_name, set())
        agent_dir = plugin / "agents"
        actual_agents = (
            {path.stem for path in agent_dir.glob("*.md")} if agent_dir.is_dir() else set()
        )
        if actual_agents != expected_agents:
            fail(f"Unexpected {plugin_name} agents: {sorted(actual_agents)}")
        for agent_name in sorted(expected_agents):
            validate_agent(agent_dir / f"{agent_name}.md")

    hashes = {hashlib.sha256(path.read_bytes()).hexdigest() for path in style_files}
    if len(hashes) != 1:
        fail("Plain-language writing references differ between skills")

    read_json(
        ROOT
        / "plugins"
        / "discovery"
        / "skills"
        / "deep-discovery"
        / "assets"
        / "application-model.schema.json"
    )

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
