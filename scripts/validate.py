#!/usr/bin/env python3
"""Validate the marketplace, plugins, skills, and evaluation fixtures."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGINS = {
    "discovery": {"deep-discovery", "start-discovery"},
    "design": {"change-design", "start-design"},
    "planning": {"create-issues", "create-product-brief"},
    "execution": {"goal-mode", "review-work", "work-on-issues"},
    "kestrel": {"assign"},
}
EXPECTED_AGENTS = {
    "discovery": {"source-investigator"},
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


def validate_discovery_contracts() -> None:
    discovery = ROOT / "plugins" / "discovery" / "skills"
    start_text = (discovery / "start-discovery" / "SKILL.md").read_text()
    for required_text in (
        "Run an interview, not a turn-by-turn Q&A.",
        "Add two to four related prompts",
        "participant using voice mode",
    ):
        if required_text not in start_text:
            fail(f"Start Discovery interview contract is missing: {required_text}")
    if "Ask one meaningful question or one closely related pair at a time." in start_text:
        fail("Start Discovery reverted to a single-question interaction contract")

    notebook_text = (
        discovery
        / "start-discovery"
        / "assets"
        / "discovery-notebook-template.md"
    ).read_text()
    if "## Next Interview Opening" not in notebook_text:
        fail("Start Discovery notebook must preserve the next interview opening")

    schema_path = (
        discovery
        / "deep-discovery"
        / "assets"
        / "application-model.schema.json"
    )
    schema = read_json(schema_path)
    required_model_fields = {
        "schemaVersion",
        "generatedAt",
        "application",
        "scope",
        "analysis",
        "capabilities",
        "nodes",
        "relationships",
        "flows",
        "evidence",
        "findings",
        "unknowns",
    }
    if not required_model_fields.issubset(set(schema.get("required", []))):
        fail("Deep Discovery application model is missing knowledge-base fields")

    definitions = schema.get("$defs", {})
    support_values = set(definitions.get("support", {}).get("enum", []))
    expected_support = {
        "observed-runtime",
        "demonstrated-test",
        "static-analysis",
        "declared",
        "inferred",
        "unknown",
    }
    if support_values != expected_support:
        fail("Deep Discovery application model has unexpected support values")

    status_values = set(definitions.get("capabilityStatus", {}).get("enum", []))
    if not {"observed-working", "partial", "documented-but-not-found"}.issubset(
        status_values
    ):
        fail("Deep Discovery application model is missing capability statuses")


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

        if plugin_name == "discovery":
            for skill_name in expected_skills:
                skill_text = (skills / skill_name / "SKILL.md").read_text()
                if "`source-investigator`" not in skill_text:
                    fail(f"{skill_name} does not reference the packaged source-investigator")
                if "../../references/source-investigation.md" not in skill_text:
                    fail(f"{skill_name} does not reference the shared source guide")

    hashes = {hashlib.sha256(path.read_bytes()).hexdigest() for path in style_files}
    if len(hashes) != 1:
        fail("Plain-language writing references differ between skills")

    validate_discovery_contracts()

    source_model = read_json(
        ROOT / "plugins" / "discovery" / "assets" / "source-model.schema.json"
    )
    required_source_fields = {
        "subject",
        "corpusType",
        "coverage",
        "actors",
        "workflows",
        "decisions",
        "claims",
        "conflicts",
        "gaps",
        "unresolvedQuestions",
    }
    if not required_source_fields.issubset(set(source_model.get("required", []))):
        fail("Discovery source-model schema is missing required evidence fields")

    source_guide = ROOT / "plugins" / "discovery" / "references" / "source-investigation.md"
    if "${CLAUDE_PLUGIN_ROOT}/scripts/source-corpus.py" not in source_guide.read_text():
        fail("Discovery source guide does not reference the bundled corpus tool")

    source_corpus = ROOT / "plugins" / "discovery" / "scripts" / "source-corpus.py"
    if not source_corpus.is_file():
        fail("Missing plugins/discovery/scripts/source-corpus.py")
    if not os.access(source_corpus, os.X_OK):
        fail("plugins/discovery/scripts/source-corpus.py must be executable")
    try:
        ast.parse(source_corpus.read_text(), filename=str(source_corpus))
    except SyntaxError as error:
        fail(f"Discovery source corpus tool has invalid Python: {error}")

    source_corpus_tests = (
        ROOT / "tests" / "discovery" / "source-corpus" / "test_source_corpus.py"
    )
    if not source_corpus_tests.is_file():
        fail("Missing Discovery source corpus tests")

    kestrel_assign = ROOT / "plugins" / "kestrel" / "bin" / "kestrel-assign"
    if not kestrel_assign.is_file():
        fail("Missing plugins/kestrel/bin/kestrel-assign")
    if not os.access(kestrel_assign, os.X_OK):
        fail("plugins/kestrel/bin/kestrel-assign must be executable")

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
