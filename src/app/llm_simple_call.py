# Importe la classe principale du SDK OpenAI (v1 officiel)
from openai import OpenAI

# Permet de charger les variables d'environnement à partir d'un fichier .env
from dotenv import load_dotenv

# Sert à accéder aux variables d'environnement du système
import os


# Fonction principale de ton script
def run():
    # Charge les variables définies dans le fichier .env dans les variables d'environnement système
    load_dotenv()

    # Récupère la clé API depuis les variables d'environnement
    api_key = os.getenv("OPENAI_API_KEY")

    # Si la clé est manquante, on arrête le programme avec une erreur explicite
    if not api_key:
        raise RuntimeError("Clé API manquante.")

    # Initialise un client OpenAI — il utilise automatiquement la clé via la variable d'environnement
    client = OpenAI()

    # Envoie une requête à l'API OpenAI via la méthode "responses"
    # - model : modèle utilisé (ici gpt-4.1-mini, rapide et économique)
    # - input : texte envoyé au modèle
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="Quelle est la capitale du Groenland ?",
    )

    # Affiche la réponse renvoyée par le modèle
    print("Réponse du modèle :", response.output_text)


# Ce bloc garantit que le code s'exécute uniquement si ce fichier est lancé directement (pas si importé)
if __name__ == "__main__":
    run()
    