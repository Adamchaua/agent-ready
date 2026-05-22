import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent_ready.cli import main
from agent_ready.generator import write_outputs
from agent_ready.scanner import scan


class AgentReadyTest(unittest.TestCase):
    def make_repo(self, root: Path) -> Path:
        (root / "package.json").write_text(json.dumps({"scripts": {"test": "vitest", "build": "vite build", "lint": "eslint ."}, "dependencies": {"react": "latest", "vite": "latest"}}))
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
