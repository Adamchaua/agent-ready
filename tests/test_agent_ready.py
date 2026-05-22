import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent_ready.cli import main
from agent_ready.generator import write_outputs
from agent_ready.scanner import scan
from agent_ready.score import calculate_score


class AgentReadyTest(unittest.TestCase):
    def make_repo(self, root: Path) -> Path:
        package_json = {
            "scripts": {"test": "vitest", "build": "vite build", "lint": "eslint ."},
            "dependencies": {"react": "latest", "vite": "latest"},
        }
        (root / "package.json").write_text(json.dumps(package_json))
        (root / "src").mkdir()
        (root / "src" / "main.tsx").write_text("console.log('ok')")
        (root / ".github" / "workflows").mkdir(parents=True)
        (root / ".github" / "workflows" / "ci.yml").write_text("name: ci")
        return root

    def test_scan_detects_stack_and_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            summary = scan(root)
            self.assertIn("TypeScript/React", summary.languages)
            self.assertIn("React", summary.frameworks)
            self.assertIn("Vite", summary.frameworks)
            self.assertIn("npm test", summary.test_commands)
            self.assertIn("npm run build", summary.build_commands)
            self.assertIn(".github/workflows/ci.yml", summary.ci_workflows)

    def test_scan_respects_extra_ignores(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            (root / "fixtures").mkdir()
            (root / "fixtures" / "generated.py").write_text("print('skip me')")
            (root / "examples" / "generated").mkdir(parents=True)
            (root / "examples" / "generated" / "demo.py").write_text("print('skip me too')")
            summary = scan(root, extra_ignores=["fixtures", "examples/generated"])
            self.assertNotIn("Python", summary.languages)
            self.assertNotIn("fixtures", summary.top_directories)
            self.assertNotIn("examples", summary.top_directories)

    def test_scan_detects_pyproject_only_python_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text("[project]\nname = 'demo'\n")
            (root / "demo").mkdir()
            (root / "demo" / "__init__.py").write_text("")
            summary = scan(root)
            self.assertIn("Python", summary.languages)
            self.assertIn("Python/pyproject", summary.package_managers)
            self.assertIn("python -m pytest", summary.test_commands)

    def test_scan_skips_python_packaging_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            (root / "agent_ready.egg-info").mkdir()
            (root / "agent_ready.egg-info" / "PKG-INFO").write_text("Metadata-Version: 2.1")
            summary = scan(root)
            self.assertNotIn("agent_ready.egg-info", summary.top_directories)

    def test_write_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            summary = scan(root)
            written = write_outputs(root, summary)
            names = {p.relative_to(root).as_posix() for p in written}
            self.assertIn("AGENTS.md", names)
            self.assertIn("CLAUDE.md", names)
            self.assertIn("CODEX.md", names)
            self.assertIn(".agent/context.json", names)
            self.assertIn(".agent/checklist.md", names)
            context = json.loads((root / ".agent" / "context.json").read_text())
            self.assertEqual(context["name"], root.name)

    def test_readiness_score_grades_repo_signals(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            readiness = calculate_score(scan(root))
            self.assertGreaterEqual(readiness.score, 75)
            self.assertIn(readiness.grade, {"A", "B"})

    def test_json_score_includes_readiness_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            with patch("sys.argv", ["agent-ready", str(root), "--json", "--score"]):
                with patch("builtins.print") as mocked_print:
                    self.assertEqual(main(), 0)
            payload = json.loads(mocked_print.call_args.args[0])
            self.assertIn("readiness", payload)
            self.assertIn("score", payload["readiness"])

    def test_check_exits_nonzero_when_outputs_are_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            with patch("sys.argv", ["agent-ready", str(root), "--check"]):
                self.assertEqual(main(), 1)

    def test_check_passes_after_forced_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            summary = scan(root)
            write_outputs(root, summary, force=True)
            with patch("sys.argv", ["agent-ready", str(root), "--check"]):
                self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
