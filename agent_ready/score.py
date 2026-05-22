from __future__ import annotations

from dataclasses import asdict, dataclass

from .scanner import ProjectSummary


@dataclass
class ReadinessScore:
    score: int
    grade: str
    checks: dict[str, bool]
    recommendations: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def calculate_score(summary: ProjectSummary) -> ReadinessScore:
    checks = {
        "languages_detected": bool(summary.languages),
        "package_manager_detected": bool(summary.package_managers),
        "test_command_detected": bool(summary.test_commands),
        "build_or_lint_detected": bool(summary.build_commands or summary.lint_commands),
        "ci_detected": bool(summary.ci_workflows),
        "important_files_detected": bool(summary.important_files),
        "risk_areas_detected": bool(summary.risk_areas),
    }
    weights = {
        "languages_detected": 10,
        "package_manager_detected": 15,
        "test_command_detected": 20,
        "build_or_lint_detected": 15,
        "ci_detected": 20,
        "important_files_detected": 10,
        "risk_areas_detected": 10,
    }
    score = sum(weights[name] for name, passed in checks.items() if passed)
    recommendations = recommendations_for(checks)
    return ReadinessScore(score=score, grade=grade_for(score), checks=checks, recommendations=recommendations)


def grade_for(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def recommendations_for(checks: dict[str, bool]) -> list[str]:
    messages = {
        "languages_detected": "Add source files or supported extensions so agents can identify the stack.",
        "package_manager_detected": "Add package metadata such as package.json, pyproject.toml, go.mod, or Cargo.toml.",
        "test_command_detected": "Add a test command or test directory so agents know how to verify changes.",
        "build_or_lint_detected": "Expose build or lint commands in package scripts, Makefile, or project config.",
        "ci_detected": "Add a CI workflow that runs tests and agent-ready --check.",
        "important_files_detected": "Add README or contribution docs that explain the repository.",
        "risk_areas_detected": "Document safety-sensitive areas such as env files, deploys, auth, or migrations.",
    }
    return [message for name, message in messages.items() if not checks[name]]
