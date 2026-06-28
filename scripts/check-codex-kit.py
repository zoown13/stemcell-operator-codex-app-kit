#!/usr/bin/env python3
"""Validate the repository-scoped Codex app kit without network access."""

from __future__ import annotations

import os
import pathlib
import re
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    ".github/pull_request_template.md",
    ".gitignore",
    ".worktreeinclude",
    "AGENTS.md",
    "Instructions.md",
    "KIT_VERSION",
    "README.md",
    "README.ko.md",
    ".codex/config.toml",
    "docs/SPEC.md",
    "docs/ARCHITECTURE.md",
    "docs/BACKLOG.md",
    "docs/OPERATING_MODEL.md",
    "docs/CODEX_APP_SETUP.md",
    "docs/CLOUD_PLAYBOOK.md",
    "docs/LOCAL_VALIDATION.md",
    "docs/AUTOMATIONS.md",
    "docs/GITHUB_INTEGRATION.md",
    "docs/MIGRATION_FROM_API_KIT.md",
    "docs/REFERENCES.md",
    "docs/DELIVERABLE_MAP.md",
    "prompts/cloud/01-m0-scaffold.md",
    "prompts/cloud/02-m1-crd-contract.md",
    "prompts/cloud/03-m2-expression-engine.md",
    "prompts/cloud/04-m3-universal-runtime.md",
    "prompts/cloud/05-m4-controller.md",
    "prompts/cloud/06-independent-review.md",
    "prompts/cloud/07-overnight-batch.md",
    "prompts/local/01-integrate-cloud-change.md",
    "prompts/local/02-kind-e2e.md",
    "prompts/local/03-final-milestone-review.md",
    "prompts/automation/nightly-bounded-iteration.md",
    "scripts/bootstrap.sh",
    "scripts/check-codex-kit.py",
    "scripts/codex-cloud-setup.sh",
    "scripts/codex-worktree-setup.sh",
    "scripts/kind-e2e-preflight.sh",
    "scripts/verify-cloud.sh",
    "scripts/verify-local.sh",
    "scripts/validate-repo.sh",
}

REQUIRED_EXECUTABLES = {
    "scripts/bootstrap.sh",
    "scripts/check-codex-kit.py",
    "scripts/codex-cloud-setup.sh",
    "scripts/codex-worktree-setup.sh",
    "scripts/kind-e2e-preflight.sh",
    "scripts/verify-cloud.sh",
    "scripts/verify-local.sh",
    "scripts/validate-repo.sh",
}

REQUIRED_AGENTS = {
    "architect",
    "implementer",
    "code_reviewer",
    "test_engineer",
    "security_reviewer",
    "deployment_validator",
}

READ_ONLY_AGENTS = {"architect", "code_reviewer", "security_reviewer"}
WRITE_AGENTS = {"implementer", "test_engineer", "deployment_validator"}

REQUIRED_SKILLS = {
    "stemcell-plan",
    "stemcell-scaffold",
    "stemcell-crd",
    "stemcell-expression-engine",
    "stemcell-runtime-role",
    "stemcell-cloud-task",
    "stemcell-local-integration",
    "stemcell-review",
    "stemcell-test",
    "stemcell-deploy-validate",
    "stemcell-overnight",
}

FORBIDDEN_PATHS = {
    ".github/codex/prompts",
    "scripts/run-overnight.sh",
    "scripts/notify_email.py",
    "scripts/codex-api.py",
    "scripts/codex_api.py",
}

NAME_RE = re.compile(r"^[a-z][a-z0-9_-]*$")


def rel(path: pathlib.Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_front_matter(path: pathlib.Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("missing or malformed YAML front matter")

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"unsupported front-matter line: {line!r}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def validate_required_files(errors: list[str], warnings: list[str]) -> None:
    for relative in sorted(REQUIRED_FILES):
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")

    for relative in sorted(REQUIRED_EXECUTABLES):
        path = ROOT / relative
        if path.exists() and not os.access(path, os.X_OK):
            warnings.append(
                "helper is not directly executable; invoke it with an explicit "
                f"interpreter in Codex App Worktrees: {relative}"
            )

    for relative in sorted(FORBIDDEN_PATHS):
        path = ROOT / relative
        if path.exists():
            errors.append(f"legacy API automation asset must be removed: {relative}")

    for path in ROOT.rglob("*"):
        if path.is_symlink():
            errors.append(f"unexpected symlink in distributable kit: {rel(path)}")
        if path.name in {"__pycache__", ".DS_Store"}:
            errors.append(f"generated local artifact must be removed: {rel(path)}")
        if path.is_file() and path.suffix in {".zip", ".gz", ".tgz", ".pyc"}:
            errors.append(f"nested generated artifact must be removed: {rel(path)}")


def validate_text_format(errors: list[str]) -> None:
    text_extensions = {".md", ".toml", ".sh", ".py"}
    text_files = {
        ROOT / relative
        for relative in REQUIRED_FILES
        if pathlib.Path(relative).suffix in text_extensions
        or relative in {"KIT_VERSION", ".gitignore", ".worktreeinclude"}
    }

    for path in sorted(text_files):
        if not path.is_file():
            continue
        data = path.read_bytes()
        if b"\r\n" in data:
            errors.append(f"text file must use LF line endings: {rel(path)}")

    for relative in sorted(REQUIRED_EXECUTABLES):
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            first_line = read_text(path).splitlines()[0]
        except IndexError:
            errors.append(f"required helper is empty and missing shebang: {relative}")
            continue
        expected = "#!/usr/bin/env python3" if path.suffix == ".py" else "#!/usr/bin/env bash"
        if first_line != expected:
            errors.append(f"required helper has unexpected shebang: {relative}")


def validate_config(errors: list[str]) -> None:
    path = ROOT / ".codex/config.toml"
    if not path.is_file():
        return
    try:
        config = tomllib.loads(read_text(path))
    except Exception as exc:  # noqa: BLE001 - validation utility
        errors.append(f"invalid .codex/config.toml: {exc}")
        return

    agents_cfg = config.get("agents", {})
    if not isinstance(agents_cfg, dict):
        errors.append(".codex/config.toml [agents] must be a table")
        return

    max_threads = agents_cfg.get("max_threads")
    max_depth = agents_cfg.get("max_depth")
    if not isinstance(max_threads, int) or not 1 <= max_threads <= 16:
        errors.append(".codex/config.toml agents.max_threads must be an integer from 1 to 16")
    if max_depth != 1:
        errors.append(".codex/config.toml agents.max_depth must be 1 for bounded direct delegation")


def validate_agents(errors: list[str]) -> set[str]:
    agent_names: set[str] = set()
    directory = ROOT / ".codex/agents"

    for path in sorted(directory.glob("*.toml")):
        try:
            data = tomllib.loads(read_text(path))
        except Exception as exc:  # noqa: BLE001 - validation utility
            errors.append(f"invalid TOML {rel(path)}: {exc}")
            continue

        for key in ("name", "description", "developer_instructions"):
            value = data.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{rel(path)} missing non-empty string {key}")

        name = data.get("name")
        if not isinstance(name, str):
            continue
        if not NAME_RE.fullmatch(name):
            errors.append(f"invalid custom-agent name {name!r} in {rel(path)}")
        if path.stem != name:
            errors.append(f"custom-agent filename must match name: {rel(path)} vs {name}")
        if name in agent_names:
            errors.append(f"duplicate agent name: {name}")
        agent_names.add(name)

        sandbox = data.get("sandbox_mode")
        if name in READ_ONLY_AGENTS and sandbox != "read-only":
            errors.append(f"{rel(path)} must default to read-only sandbox")
        if name in WRITE_AGENTS and sandbox != "workspace-write":
            errors.append(f"{rel(path)} must default to workspace-write sandbox")

        nicknames = data.get("nickname_candidates", [])
        if nicknames:
            if not isinstance(nicknames, list) or not all(isinstance(item, str) and item for item in nicknames):
                errors.append(f"{rel(path)} nickname_candidates must be non-empty strings")
            elif len(nicknames) != len(set(nicknames)):
                errors.append(f"{rel(path)} nickname_candidates must be unique")

    missing = REQUIRED_AGENTS - agent_names
    if missing:
        errors.append(f"missing required agents: {', '.join(sorted(missing))}")
    return agent_names


def validate_skills(errors: list[str]) -> set[str]:
    skill_names: set[str] = set()
    directory = ROOT / ".agents/skills"

    for path in sorted(directory.glob("*/SKILL.md")):
        try:
            fields = parse_front_matter(path)
        except ValueError as exc:
            errors.append(f"{rel(path)}: {exc}")
            continue

        name = fields.get("name", "")
        description = fields.get("description", "")
        if not name or not description:
            errors.append(f"{rel(path)} requires name and description")
            continue
        if not NAME_RE.fullmatch(name):
            errors.append(f"invalid skill name {name!r} in {rel(path)}")
        if path.parent.name != name:
            errors.append(f"skill directory must match skill name: {rel(path)} vs {name}")
        if name in skill_names:
            errors.append(f"duplicate skill name: {name}")
        skill_names.add(name)

    missing = REQUIRED_SKILLS - skill_names
    if missing:
        errors.append(f"missing required skills: {', '.join(sorted(missing))}")
    return skill_names


def validate_no_api_automation(errors: list[str]) -> None:
    workflows = ROOT / ".github/workflows"
    if workflows.exists():
        for path in workflows.rglob("*"):
            if not path.is_file():
                continue
            text = read_text(path).lower()
            if "codex" in path.name.lower():
                errors.append(f"Codex-driving GitHub workflow is forbidden: {rel(path)}")
            forbidden_tokens = (
                "openai/codex-action",
                "secrets.openai_api_key",
                "api.openai.com/v1/responses",
            )
            if any(token in text for token in forbidden_tokens):
                errors.append(f"API-based Codex workflow is forbidden: {rel(path)}")

    for path in sorted((ROOT / "scripts").glob("*")):
        if not path.is_file() or path.name == "check-codex-kit.py":
            continue
        text = read_text(path).lower()
        forbidden_tokens = (
            "openai_api_key",
            "openai/codex-action",
            "api.openai.com/v1/responses",
        )
        if any(token in text for token in forbidden_tokens):
            errors.append(f"API-based Codex logic is forbidden in helper: {rel(path)}")


def validate_consistency(errors: list[str], agent_names: set[str], skill_names: set[str]) -> None:
    version_path = ROOT / "KIT_VERSION"
    if version_path.is_file() and read_text(version_path).strip() != "2.0.0-codex-app":
        errors.append("KIT_VERSION must be 2.0.0-codex-app")

    backlog = read_text(ROOT / "docs/BACKLOG.md") if (ROOT / "docs/BACKLOG.md").is_file() else ""
    if "## M2 — Pure expression engine" not in backlog:
        errors.append("backlog must define M2 as the pure expression engine")
    if "## M3 — Universal runtime" not in backlog:
        errors.append("backlog must define M3 as the universal runtime")

    agent_refs = "\n".join(
        read_text(path)
        for path in (ROOT / "AGENTS.md", ROOT / "Instructions.md")
        if path.is_file()
    )
    for name in sorted(agent_names):
        if f"`{name}`" not in agent_refs:
            errors.append(f"repository instructions do not reference custom agent: {name}")

    prompt_text = "\n".join(
        read_text(path) for path in sorted((ROOT / "prompts").rglob("*.md"))
    )
    for name in sorted(skill_names):
        # Domain skills can be selected implicitly, so only require every skill to
        # be discoverable through its own front matter, not explicitly named in prompts.
        if not (ROOT / ".agents/skills" / name / "SKILL.md").is_file():
            errors.append(f"skill path disappeared during consistency check: {name}")
    for required_marker in ("LOCAL_REQUIRED", "mode: Cloud", "mode: Worktree"):
        if required_marker not in prompt_text:
            errors.append(f"prompt library is missing required marker: {required_marker}")

    forbidden_absolute = str(ROOT)
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".toml", ".sh", ".py"}:
            continue
        if forbidden_absolute in read_text(path):
            errors.append(f"distributable file contains build-machine absolute path: {rel(path)}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    validate_required_files(errors, warnings)
    validate_text_format(errors)
    validate_config(errors)
    agent_names = validate_agents(errors)
    skill_names = validate_skills(errors)
    validate_no_api_automation(errors)
    validate_consistency(errors, agent_names, skill_names)

    if errors:
        print("Codex app kit validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        if warnings:
            print("Codex app kit validation warnings:", file=sys.stderr)
            for warning in warnings:
                print(f"- {warning}", file=sys.stderr)
        return 1

    if warnings:
        print("Codex app kit validation warnings:", file=sys.stderr)
        for warning in warnings:
            print(f"- {warning}", file=sys.stderr)

    print(
        "Codex app kit validation passed: "
        f"{len(agent_names)} agents, {len(skill_names)} skills, "
        f"{len(REQUIRED_FILES)} required files, no API-based Codex workflow"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
