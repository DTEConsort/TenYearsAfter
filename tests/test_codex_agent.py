"""Regression tests that never contact the OpenAI API."""

import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock


MODULE_PATH = Path(__file__).resolve().parents[1] / "src/app/codex_agent.py"


class CodexAgentSafetyTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("codex_agent_test", MODULE_PATH)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_import_does_not_call_api_or_modify_files(self):
        self.assertTrue(callable(self.module.modifier_code))

    def test_draft_is_separate_and_existing_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.py"
            draft = Path(directory) / "draft.py"
            source.write_text("print('original')\n", encoding="utf-8")
            client = MagicMock()
            client.chat.completions.create.return_value.choices[0].message.content = "print('draft')\n"
            with unittest.mock.patch.dict(sys.modules, {
                "openai": types.SimpleNamespace(OpenAI=lambda: client),
                "dotenv": types.SimpleNamespace(load_dotenv=lambda: None),
            }):
                with self.assertRaises(ValueError):
                    self.module.modifier_code(source, "edit", source)
                self.assertEqual(client.chat.completions.create.call_count, 0)
                self.module.modifier_code(source, "edit", draft)
                self.assertEqual(source.read_text(encoding="utf-8"), "print('original')\n")
                self.assertEqual(draft.read_text(encoding="utf-8"), "print('draft')\n")
                with self.assertRaises(FileExistsError):
                    self.module.modifier_code(source, "edit", draft)


if __name__ == "__main__":
    unittest.main()
