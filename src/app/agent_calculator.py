# src/app/agent_calculator.py

# Importe ChatOpenAI : permet d'utiliser un modèle GPT via LangChain
from langchain_openai import ChatOpenAI

# Importe ce qu’il faut pour créer un agent avec des outils
from langchain.agents import tool, initialize_agent, AgentType

# Pour charger les variables d’environnement (comme ta clé API)
from dotenv import load_dotenv
import os


# --------------------------
# 1. Déclaration d’un outil
# --------------------------

# Le décorateur @tool indique que cette fonction peut être utilisée par un agent LangChain
@tool
def multiply(a: float, b: float) -> float:
    """Multiplie deux nombres."""
    return a * b

# ⚠️ Important : le nom, la docstring et les types aident le LLM à comprendre comment utiliser la fonction.
# Ex : ici, il comprend : "multiply prend deux nombres en entrée, renvoie leur produit."


# --------------------------
# 2. Fonction principale
# --------------------------

def run():
    # Charge les variables d’environnement depuis le fichier .env (ex: ta clé OpenAI)
    load_dotenv()

    # ----------------------
    # 3. Instancie le modèle LLM
    # ----------------------

    # Crée une instance d’un modèle GPT (ici gpt-4.1-mini)
    llm = ChatOpenAI(
        model="gpt-4.1-mini",  # rapide, économique, suffisant pour des tests d’agents
        temperature=0,         # 0 = réponses fiables, non créatives (idéal pour des calculs)
    )

    # ----------------------
    # 4. Initialise l’agent
    # ----------------------

    agent = initialize_agent(
        tools=[multiply],               # liste des outils accessibles à l’agent
        llm=llm,                        # le LLM à utiliser
        agent=AgentType.OPENAI_FUNCTIONS,  # Type d’agent = supporte le "tool calling" natif
        verbose=True                    # Affiche toutes les étapes dans le terminal (très utile pour apprendre)
    )

    # ----------------------
    # 5. Question posée à l’agent
    # ----------------------

    question = "Combien font 17 fois 24 ?"

    # ----------------------
    # 6. Lancement de l’agent
    # ----------------------

    response = agent.invoke({"input": question})

    # ----------------------
    # 7. Affiche la réponse finale
    # ----------------------

    print("\nRéponse finale :", response["output"])

# Ce bloc garantit que le script ne s’exécute que si lancé directement (et pas importé dans un autre fichier)
if __name__ == "__main__":
    run()