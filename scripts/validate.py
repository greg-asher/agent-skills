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
    "analysis": {"blast-radius", "game-show", "map-workspace", "narrate", "teach-me"},
    "discovery": {"deep-discovery", "start-discovery"},
    "design": {"change-design", "start-design"},
    "planning": {"create-issues", "create-product-brief"},
    "execution": {"goal-mode", "guided-operator", "review-work", "work-on-issues"},
    "kestrel": {"assign"},
    "productivity": {"to-questionnaire"},
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


def validate_skill(skill_dir: Path, require_claude_manual_invocation: bool = True) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        fail(f"Missing {skill_file.relative_to(ROOT)}")

    metadata = frontmatter(skill_file)
    if metadata.get("name") != skill_dir.name:
        fail(f"Skill name does not match directory: {skill_dir.relative_to(ROOT)}")
    if not metadata.get("description"):
        fail(f"Missing skill description: {skill_file.relative_to(ROOT)}")
    if (
        require_claude_manual_invocation
        and metadata.get("disable-model-invocation") != "true"
    ):
        fail(f"Skill must remain manually invoked: {skill_file.relative_to(ROOT)}")
    if not require_claude_manual_invocation and "disable-model-invocation" in metadata:
        fail(
            "Cross-platform Analysis skills must use agents/openai.yaml invocation policy: "
            f"{skill_file.relative_to(ROOT)}"
        )
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


def validate_analysis_contracts() -> None:
    analysis = ROOT / "plugins" / "analysis"
    skills = analysis / "skills"

    required_skill_text = {
        "map-workspace": (
            ".analysis/workspace-model.json",
            "Static reachability does not prove runtime use.",
        ),
        "blast-radius": (
            "A downstream execution harness decides whether to enforce",
            "ready",
            "caution",
            "not-ready",
        ),
        "narrate": (
            "latest completed substantive work run",
            "full available thread",
            "tool-call transcript",
        ),
        "game-show": (
            "Ask exactly one question at a time",
            "does not require Narrate",
            ".analysis/learner-model.json",
        ),
        "teach-me": (
            "Persist history only within the current workspace.",
            "inspect, dispute, correct, or remove signals",
            "Persist a learning goal only when the user intends to learn across sessions.",
            ".analysis/learning/<slug>-reference.md",
        ),
    }
    for skill_name, required_phrases in required_skill_text.items():
        text = (skills / skill_name / "SKILL.md").read_text()
        for phrase in required_phrases:
            if phrase not in text:
                fail(f"Analysis {skill_name} contract is missing: {phrase}")

    schemas = {
        "workspace-model.schema.json": {
            "workspace",
            "analysis",
            "boundaries",
            "components",
            "relationships",
            "evidence",
            "findings",
            "unknowns",
        },
        "blast-radius.schema.json": {
            "change",
            "workspaceRevision",
            "readiness",
            "directImpacts",
            "indirectImpacts",
            "unknowns",
            "requiredValidation",
            "contextPack",
        },
        "learner-model.schema.json": {"workspace", "updatedAt", "concepts"},
        "run-model.schema.json": {
            "thread",
            "objective",
            "boundary",
            "coverage",
            "events",
            "outcome",
            "unresolved",
        },
    }
    for filename, expected_required in schemas.items():
        schema = read_json(analysis / "assets" / filename)
        if not expected_required.issubset(set(schema.get("required", []))):
            fail(f"Analysis schema is missing required fields: {filename}")

    learner_schema = read_json(analysis / "assets" / "learner-model.schema.json")
    learning_goals = learner_schema.get("properties", {}).get("learningGoals", {})
    goal_items = learning_goals.get("items", {})
    if not {"purpose", "desiredCapability", "status", "updatedAt"}.issubset(
        set(goal_items.get("required", []))
    ):
        fail("Analysis learner model is missing optional learning-goal fields")


def validate_supporting_contracts() -> None:
    domain_paths = [
        ROOT / "plugins" / plugin / "references" / "domain-modeling.md"
        for plugin in ("discovery", "design")
    ]
    decision_paths = [
        ROOT / "plugins" / plugin / "references" / "decision-map.md"
        for plugin in ("discovery", "design")
    ]
    for label, paths in (
        ("Domain-modeling", domain_paths),
        ("Decision-map", decision_paths),
    ):
        if any(not path.is_file() for path in paths):
            fail(f"{label} shared reference is missing")
        hashes = {hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
        if len(hashes) != 1:
            fail(f"{label} references differ between Discovery and Design")

    for plugin_name, skill_name in (
        ("discovery", "start-discovery"),
        ("design", "start-design"),
        ("design", "change-design"),
    ):
        text = (
            ROOT / "plugins" / plugin_name / "skills" / skill_name / "SKILL.md"
        ).read_text()
        if "../../references/decision-map.md" not in text:
            fail(f"{skill_name} does not reference the decision-map protocol")

    for plugin_name, skill_name in (
        ("discovery", "start-discovery"),
        ("discovery", "deep-discovery"),
        ("design", "start-design"),
        ("design", "change-design"),
    ):
        text = (
            ROOT / "plugins" / plugin_name / "skills" / skill_name / "SKILL.md"
        ).read_text()
        if "../../references/domain-modeling.md" not in text:
            fail(f"{skill_name} does not reference the domain-modeling discipline")

    repair_phrase = "Repair a conversation that did not land"
    for path in ROOT.glob("plugins/*/skills/*/references/plain-language-writing.md"):
        if repair_phrase not in path.read_text():
            fail(f"Conversation-repair contract is missing: {path.relative_to(ROOT)}")

    for plugin_name, skill_name in (
        ("productivity", "to-questionnaire"),
        ("execution", "guided-operator"),
    ):
        metadata_path = (
            ROOT
            / "plugins"
            / plugin_name
            / "skills"
            / skill_name
            / "agents"
            / "openai.yaml"
        )
        metadata = metadata_path.read_text()
        if "allow_implicit_invocation: false" not in metadata:
            fail(f"{skill_name} must disable implicit Codex invocation")

    productivity_codex = read_json(
        ROOT / "plugins" / "productivity" / ".codex-plugin" / "plugin.json"
    )
    if productivity_codex.get("skills") != "./skills/":
        fail("Productivity Codex manifest does not expose its skills")

    if not (ROOT / "THIRD_PARTY_NOTICES.md").is_file():
        fail("Missing THIRD_PARTY_NOTICES.md")


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
            validate_skill(
                skills / skill_name,
                require_claude_manual_invocation=plugin_name != "analysis",
            )
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
    validate_analysis_contracts()
    validate_supporting_contracts()

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
