import json
import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT = os.path.join(REPO, ".claude", "hooks", "orch.py")


def run(cmd, root, payload=None):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=root)
    return subprocess.run(
        [sys.executable, SCRIPT, cmd], input=json.dumps(payload or {}),
        capture_output=True, text=True, env=env)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content if isinstance(content, str) else json.dumps(content))


def edit(path, tool="Edit"):
    return {"tool_name": tool, "tool_input": {"file_path": path}}


class PreToolUseTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        write(os.path.join(self.root, "projects", "demo", ".orch", "state.json"), {
            "stage": "constitution",
            "documents": {"docs/constitution.md": {"status": "FROZEN"},
                          "docs/prd.md": {"status": "DRAFT"}}})
        write(os.path.join(self.root, "docs", "orchdocs", ".status.json"),
              {"documents": {"prd.md": "FROZEN"}})

    def test_blocks_frozen_project_document(self):
        target = os.path.join(self.root, "projects", "demo", "docs", "constitution.md")
        for tool in ("Edit", "Write", "MultiEdit"):
            result = run("pre-tool-use", self.root, edit(target, tool))
            self.assertEqual(result.returncode, 2, tool)
            self.assertIn("Change Request", result.stderr)

    def test_blocks_frozen_orchdocs_document_by_relative_path(self):
        result = run("pre-tool-use", self.root, edit("docs/orchdocs/prd.md"))
        self.assertEqual(result.returncode, 2)

    def test_allows_draft_and_untracked(self):
        for rel in ("projects/demo/docs/prd.md", "README.md"):
            self.assertEqual(run("pre-tool-use", self.root, edit(rel)).returncode, 0, rel)

    def test_ignores_other_tools(self):
        target = os.path.join(self.root, "projects", "demo", "docs", "constitution.md")
        self.assertEqual(run("pre-tool-use", self.root, edit(target, "Read")).returncode, 0)


class StopTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.transcript = os.path.join(self.root, "t.jsonl")
        write(self.transcript, "\n".join(json.dumps(e) for e in [
            {"type": "user", "message": {"role": "user", "content": "escreva a constitution"}},
            {"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": "Write", "input": {"file_path": "projects/demo/docs/c.md"}}]}},
        ]))
        self.payload = {"session_id": "abc123456789", "transcript_path": self.transcript}
        self.log = os.path.join(self.root, "projects", "demo", ".orch", "sessions.md")

    def test_noop_without_active_project(self):
        self.assertEqual(run("stop", self.root, self.payload).returncode, 0)
        self.assertFalse(os.path.exists(self.log))

    def test_writes_one_block_per_session(self):
        os.makedirs(os.path.join(self.root, "projects", "demo"))
        write(os.path.join(self.root, "projects", ".active"), "demo\n")
        run("stop", self.root, self.payload)
        run("stop", self.root, self.payload)
        run("stop", self.root, dict(self.payload, session_id="other"))
        with open(self.log, encoding="utf-8") as f:
            text = f.read()
        self.assertEqual(text.count("<!-- session:abc123456789 -->"), 1)
        self.assertEqual(text.count("<!-- session:other -->"), 1)
        self.assertIn("escreva a constitution", text)
        self.assertIn("projects/demo/docs/c.md", text)


class StatusTest(unittest.TestCase):
    def test_no_projects(self):
        root = tempfile.mkdtemp()
        os.makedirs(os.path.join(root, "projects"))
        self.assertEqual(run("status", root).stdout.strip(), "nenhum projeto")

    def test_lists_projects_with_stage(self):
        root = tempfile.mkdtemp()
        write(os.path.join(root, "projects", "demo", ".orch", "state.json"), {"stage": "prd"})
        write(os.path.join(root, "projects", ".active"), "demo")
        self.assertEqual(run("status", root).stdout.strip(), "- demo (ativo): prd")


if __name__ == "__main__":
    unittest.main()
