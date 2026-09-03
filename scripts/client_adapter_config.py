#!/usr/bin/env python3
"""Test non-destructive, idempotent client adapter configuration updates."""

from __future__ import annotations

import copy
from typing import Any


START = "[Mind Palace adapter: start]"
END = "[Mind Palace adapter: end]"


def append_unique(values: list[str], value: str) -> list[str]:
    return values.copy() if value in values else [*values, value]


def configure_opencode(config: dict[str, Any], skill_path: str) -> dict[str, Any]:
    result = copy.deepcopy(config)
    skills = result.setdefault("skills", {})
    skills["paths"] = append_unique(skills.get("paths", []), skill_path)
    return result


def upsert_managed_block(existing: str, body: str) -> str:
    start_count = existing.count(START)
    end_count = existing.count(END)
    if start_count != end_count or start_count > 1:
        raise ValueError("ambiguous Mind Palace adapter markers")
    block = f"{START}\n{body.strip()}\n{END}"
    if start_count == 0:
        separator = "\n\n" if existing else ""
        return f"{existing}{separator}{block}"
    start = existing.index(START)
    end = existing.index(END, start) + len(END)
    return f"{existing[:start]}{block}{existing[end:]}"


def configure_claude_project(settings: dict[str, Any], body: str) -> dict[str, Any]:
    result = copy.deepcopy(settings)
    existing = result.get("project_instructions", "")
    result["project_instructions"] = upsert_managed_block(existing, body)
    return result


def run_scenario() -> None:
    original_config = {
        "$schema": "https://opencode.ai/config.json",
        "model": "example/model",
        "instructions": ["existing.md", "team/*.md"],
        "skills": {"paths": ["existing-skills"], "urls": ["https://example.test/skills"]},
        "permission": {"edit": "ask"},
    }
    configured = configure_opencode(original_config, "mind-palace-skills")
    if original_config["skills"]["paths"] != ["existing-skills"]:
        raise ValueError("adapter mutated the input OpenCode config")
    if configured["instructions"] != original_config["instructions"]:
        raise ValueError("adapter changed existing OpenCode instructions")
    if configured["skills"]["urls"] != original_config["skills"]["urls"]:
        raise ValueError("adapter changed existing OpenCode skill URLs")
    if configured["permission"] != original_config["permission"]:
        raise ValueError("adapter changed existing OpenCode permissions")
    if configure_opencode(configured, "mind-palace-skills") != configured:
        raise ValueError("OpenCode adapter reinstall was not idempotent")

    existing = "Keep this user instruction.\n\nKeep this second instruction."
    installed = upsert_managed_block(existing, "Resolve release 0.1.0 from common memory.")
    if not installed.startswith(existing) or installed.count(START) != 1:
        raise ValueError("managed block replaced existing instructions")
    if upsert_managed_block(installed, "Resolve release 0.1.0 from common memory.") != installed:
        raise ValueError("managed block reinstall was not idempotent")
    upgraded = upsert_managed_block(installed, "Resolve release 0.2.0 from common memory.")
    if not upgraded.startswith(existing) or "release 0.1.0" in upgraded:
        raise ValueError("managed block upgrade changed unrelated instructions")
    try:
        upsert_managed_block(f"{existing}\n{START}", "candidate")
    except ValueError:
        pass
    else:
        raise ValueError("malformed managed block was not refused")

    claude_settings = {
        "account_instructions": "Keep this account-wide preference.",
        "project_instructions": "Keep this Claude Project instruction.",
        "enabled_skills": ["existing-skill"],
        "enabled_connectors": ["existing-connector"],
    }
    claude_installed = configure_claude_project(
        claude_settings, "Resolve release 0.1.0 from common memory."
    )
    if claude_settings["project_instructions"] != "Keep this Claude Project instruction.":
        raise ValueError("adapter mutated the input Claude settings")
    for field in ("account_instructions", "enabled_skills", "enabled_connectors"):
        if claude_installed[field] != claude_settings[field]:
            raise ValueError(f"adapter changed existing Claude {field}")
    if not claude_installed["project_instructions"].startswith(
        claude_settings["project_instructions"]
    ):
        raise ValueError("adapter replaced existing Claude Project instructions")
    if configure_claude_project(
        claude_installed, "Resolve release 0.1.0 from common memory."
    ) != claude_installed:
        raise ValueError("Claude adapter reinstall was not idempotent")
    claude_upgraded = configure_claude_project(
        claude_installed, "Resolve release 0.2.0 from common memory."
    )
    if "release 0.1.0" in claude_upgraded["project_instructions"]:
        raise ValueError("Claude adapter upgrade retained the old managed block")


def main() -> int:
    try:
        run_scenario()
    except ValueError as exc:
        print(f"client adapter configuration failed: {exc}")
        return 1
    print("Client adapter configuration scenario passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
