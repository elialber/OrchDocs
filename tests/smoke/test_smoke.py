import json
import os
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT = os.path.join(REPO, ".claude", "hooks", "orch.py")
FIXTURE = os.path.join(REPO, "tests", "smoke", "fixtures", "repo")

DIRS = ["docs/orchdocs", "docs/adr", "reference/chatgpt-prompts", "pipeline/stages",
        "pipeline/checklists", "projects", ".claude/commands", ".claude/skills", "tests"]


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return f.read()


def hook(cmd, root, payload):
    return subprocess.run(
        [sys.executable, SCRIPT, cmd], input=json.dumps(payload), capture_output=True,
        text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=root))


class StructureTest(unittest.TestCase):
    def test_directories_exist(self):
        for d in DIRS:
            self.assertTrue(os.path.isdir(os.path.join(REPO, d)), d)

    def test_root_documents_exist(self):
        for f in ["CLAUDE.md", "CONTEXT.md", "reference/chatgpt-prompts/README.md",
                  ".claude/commands/orch-status.md", "docs/agents/issue-tracker.md",
                  "docs/agents/domain.md", "docs/agents/triage-labels.md"]:
            self.assertTrue(os.path.isfile(os.path.join(REPO, f)), f)

    def test_context_terms(self):
        text = read("CONTEXT.md")
        for term in ["Project", "Brief", "Stage", "Stage Contract", "Gate", "Draft", "Review",
                     "Approval", "Freeze", "Change Request", "Open Decision"]:
            self.assertIn(f"**{term}** _(provisório)_", text)


class ClaudeMdTest(unittest.TestCase):
    def setUp(self):
        self.text = read("CLAUDE.md")

    def test_short(self):
        self.assertLessEqual(len(self.text.splitlines()), 60)

    def test_rules_and_sources(self):
        for needle in ["Um documento por vez", "documentos anteriores", "FROZEN", "Change Request",
                       "OPEN DECISION", "MUST / SHOULD / COULD", "contexto fresco", "fase 6",
                       "Constitution > PRD > TRD > Pipeline Spec > Implementation Plan",
                       "## Agent skills"]:
            self.assertIn(needle, self.text)


class HookWiringTest(unittest.TestCase):
    def test_settings_register_hooks(self):
        hooks = json.loads(read(".claude/settings.json"))["hooks"]
        pre = hooks["PreToolUse"][0]
        self.assertIn("Edit", pre["matcher"])
        self.assertIn("Write", pre["matcher"])
        self.assertIn("orch.py\" pre-tool-use", pre["hooks"][0]["command"])
        self.assertIn("orch.py\" stop", hooks["Stop"][0]["hooks"][0]["command"])

    def test_blocks_frozen_fixture(self):
        target = os.path.join(FIXTURE, "projects", "demo", "docs", "constitution.md")
        result = hook("pre-tool-use", FIXTURE,
                      {"tool_name": "Edit", "tool_input": {"file_path": target}})
        self.assertEqual(result.returncode, 2)
        self.assertIn("FROZEN", result.stderr)

    def test_status_on_this_repo_has_no_projects(self):
        result = subprocess.run([sys.executable, SCRIPT, "status"], capture_output=True,
                                text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=REPO))
        self.assertEqual(result.stdout.strip(), "nenhum projeto")


if __name__ == "__main__":
    unittest.main()
