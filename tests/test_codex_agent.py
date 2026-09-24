import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.app import codex_agent


class CodexAgentTests(unittest.TestCase):
    def test_rejects_path_outside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outside_file = Path(directory) / "outside.py"
            outside_file.write_text("print('outside')\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "dans le dépôt"):
                codex_agent.lire_fichier(outside_file)

    def test_extracts_fenced_python(self) -> None:
        content = "```python\nprint('ok')\n```"
        self.assertEqual(codex_agent._extraire_code_python(content), "print('ok')")

    def test_rejects_invalid_generated_python(self) -> None:
        with self.assertRaises(SyntaxError):
            codex_agent._valider_code_python("texte non Python", "generated.py")

    def test_default_writes_preview_without_changing_source(self) -> None:
        with tempfile.TemporaryDirectory(dir=codex_agent.PROJECT_ROOT) as directory:
            source = Path(directory) / "sample.py"
            source.write_text("print('original')\n", encoding="utf-8")

            with patch.object(
                codex_agent, "_generer_code", return_value="print('generated')"
            ):
                destination = codex_agent.modifier_code(
                    source, "change le message"
                )

            self.assertEqual(source.read_text(encoding="utf-8"), "print('original')\n")
            self.assertEqual(
                destination.read_text(encoding="utf-8"), "print('generated')\n"
            )


if __name__ == "__main__":
    unittest.main()
