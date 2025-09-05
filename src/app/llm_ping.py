# src/app/llm_ping.py

from openai import OpenAI
from dotenv import load_dotenv
import os

def run():
    # Charger la clé depuis .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Clé API manquante. Ajoute OPENAI_API_KEY dans ton .env.")

    # Client OpenAI (clé lue automatiquement via variable d'environnement)
    client = OpenAI()

    # Appel simple (Responses API)
    response = client.responses.create(
        model="gpt-4.1-mini",  # rapide et peu coûteux
        input="Dis juste OK.",
    )

    print("Réponse du modèle :", response.output_text)

if __name__ == "__main__":
    run()