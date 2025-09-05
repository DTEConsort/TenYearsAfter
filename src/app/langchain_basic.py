# src/app/langchain_basic.py

# Importe la classe ChatOpenAI depuis l’intégration LangChain ↔ OpenAI
# Cette classe permet d’interagir avec les modèles "chat" comme GPT-3.5 ou GPT-4
from langchain_openai import ChatOpenAI

# Permet de charger les variables d’environnement depuis un fichier .env
from dotenv import load_dotenv

# Sert à accéder aux variables d’environnement (comme la clé API)
import os


# Fonction principale du script
def run():
    # Charge les variables d’environnement (ex : OPENAI_API_KEY)
    load_dotenv()

    # Crée une instance du modèle de conversation GPT via LangChain
    # Cette classe encapsule la logique d'appel à OpenAI
    llm = ChatOpenAI(
        model="gpt-4.1-mini",  # nom du modèle utilisé (léger, rapide, peu coûteux)
        temperature=0.7,       # contrôle la "créativité" du modèle (0 = déterministe, 1 = plus aléatoire)
    )

    # Texte (prompt) à envoyer au modèle
    prompt = "Explique-moi simplement ce qu'est LangChain."

    # Appel du modèle avec le prompt → retourne une réponse sous forme d’objet "AIMessage"
    response = llm.invoke(prompt)

    # Affiche uniquement le contenu textuel généré par le modèle
    print("Réponse :\n", response.content)


# Ce bloc garantit que le script s’exécute uniquement s’il est lancé directement
# et non pas importé ailleurs comme un module
if __name__ == "__main__":
    run()
