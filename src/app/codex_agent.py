"""Propose a Python edit for review without changing the source file."""

import argparse
from pathlib import Path


def modifier_code(chemin: Path, prompt: str, sortie: Path) -> Path:
    """Send source to OpenAI with explicit consent, then save a separate draft."""
    from dotenv import load_dotenv
    from openai import OpenAI

    source = chemin.resolve(strict=True)
    if not source.is_file() or source.suffix != ".py":
        raise ValueError("Le fichier source doit être un fichier Python existant.")
    if sortie.resolve() == source:
        raise ValueError("La sortie doit être distincte du fichier source.")

    code = source.read_text(encoding="utf-8")
    load_dotenv()
    response = OpenAI().chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un expert Python qui améliore le code."},
            {"role": "user", "content": f"Voici le code :\n\n{code}\n\nModifie-le selon : {prompt}"},
        ],
        temperature=0.3,
    )
    draft = response.choices[0].message.content
    if not draft:
        raise ValueError("Le modèle n'a renvoyé aucun contenu.")
    # 'x' refuses to overwrite an existing draft. The original is never opened for writing.
    with sortie.open("x", encoding="utf-8") as file:
        file.write(draft)
    return sortie


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Fichier Python à soumettre")
    parser.add_argument("instruction", help="Modification demandée")
    parser.add_argument("--output", type=Path, required=True, help="Nouveau fichier pour la proposition")
    parser.add_argument(
        "--send-to-openai", action="store_true", required=True,
        help="Confirme que le contenu du fichier sera transmis à OpenAI",
    )
    args = parser.parse_args()
    print(f"Proposition enregistrée dans : {modifier_code(args.source, args.instruction, args.output)}")


if __name__ == "__main__":
    main()
