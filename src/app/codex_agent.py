from __future__ import annotations

import argparse
import ast
import os
import shutil
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _resolve_python_path(path: str | Path) -> Path:
    """Resolve a Python file while keeping access inside this repository."""
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    candidate = candidate.resolve()

    try:
        candidate.relative_to(PROJECT_ROOT)
    except ValueError as exc:
        raise ValueError("Le fichier doit rester dans le dépôt.") from exc

    if candidate.suffix != ".py":
        raise ValueError("Seuls les fichiers Python peuvent être modifiés.")
    return candidate


def lire_fichier(path: str | Path) -> str:
    return _resolve_python_path(path).read_text(encoding="utf-8")


def _extraire_code_python(content: str) -> str:
    """Remove an optional Markdown fence from a model response."""
    stripped = content.strip()
    if not stripped.startswith("```"):
        return stripped

    first_newline = stripped.find("\n")
    closing_fence = stripped.rfind("```")
    if first_newline == -1 or closing_fence <= first_newline:
        raise ValueError("Réponse balisée incomplète reçue du modèle.")
    return stripped[first_newline + 1 : closing_fence].strip()


def _valider_code_python(content: str, filename: str) -> None:
    """Reject model output that is not syntactically valid Python."""
    ast.parse(content, filename=filename)


def _write_atomic(path: Path, content: str) -> None:
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    os.close(fd)
    temporary_path = Path(temporary_name)
    try:
        temporary_path.write_text(content, encoding="utf-8")
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _generer_code(code: str, prompt: str) -> str:
    """Call OpenAI only after an explicit user invocation."""
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Clé API manquante. Ajoutez OPENAI_API_KEY dans .env.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu améliores du code Python. Retourne uniquement le fichier Python "
                    "complet, sans commentaire Markdown ni bloc de code."
                ),
            },
            {
                "role": "user",
                "content": f"Voici le code :\n\n{code}\n\nModification demandée : {prompt}",
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def modifier_code(path: str | Path, prompt: str, *, apply: bool = False) -> Path:
    """Generate a validated preview, or apply it after explicit opt-in."""
    target = _resolve_python_path(path)
    original = target.read_text(encoding="utf-8")
    generated = _extraire_code_python(_generer_code(original, prompt))
    _valider_code_python(generated, str(target))

    if apply:
        backup = target.with_suffix(f"{target.suffix}.bak")
        shutil.copy2(target, backup)
        destination = target
    else:
        destination = target.with_suffix(".generated.py")

    _write_atomic(destination, f"{generated.rstrip()}\n")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Génère une proposition de modification Python sans écraser la source."
    )
    parser.add_argument("path", help="Fichier Python situé dans le dépôt")
    parser.add_argument("prompt", help="Modification demandée")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Écrase explicitement la source après validation et crée une sauvegarde",
    )
    args = parser.parse_args()

    destination = modifier_code(args.path, args.prompt, apply=args.apply)
    action = "appliqué" if args.apply else "généré pour revue"
    print(f"Changement {action} : {destination}")


if __name__ == "__main__":
    main()
