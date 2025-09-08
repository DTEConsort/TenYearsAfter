# src/app/agent_calculator2.py

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from app.tools.tools_calculator import multiply
from app.tools.tools_temperature import celsius_to_fahrenheit

from dotenv import load_dotenv
load_dotenv()

# Définir les outils à disposition
tools = [
    Tool(
        name="Multiplication",
        func=multiply,
        description="Utilisé pour multiplier deux nombres. Entrée: dictionnaire avec 'a' et 'b'."
    ),
    Tool(
        name="ConvertisseurTempérature",
        func=celsius_to_fahrenheit,
        description="Utilisé pour convertir des degrés Celsius en Fahrenheit. Entrée: un float représentant les degrés Celsius."
    )
]

# Initialiser le modèle
# llm = ChatOpenAI(model="gpt-4.0", temperature=0)
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Créer l'agent avec tous les outils
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run():
    print("Agent outils personnalisés (calcul et température)")
    while True:
        question = input("\n💬 Pose une question (ou 'q' pour quitter): ")
        if question.lower() in ["q", "quit", "exit"]:
            break
        response = agent.run(question)
        print("🧠 Réponse:", response)

if __name__ == "__main__":
    run()



# from langchain.agents import initialize_agent, Tool
# from langchain.agents.agent_types import AgentType
# # from langchain.tools.python.tool import PythonREPLTool
# from langchain.chat_models import ChatOpenAI
# from dotenv import load_dotenv
# import os

# # Charger les variables d'environnement (.env)
# load_dotenv()

# # Initialiser le modèle LLM
# llm = ChatOpenAI(
#     temperature=0,
#     model="gpt-4.1-mini"
# )

# # Définir un outil personnalisé (simple calculateur)
# def multiplication(a: int, b: int) -> str:
#     """Multiplie deux nombres entiers et retourne le résultat."""
#     return f"{a} fois {b} font {a * b}."

# # Emballer cette fonction comme un outil utilisable par un agent
# tool_multiplication = Tool(
#     name="multiply",
#     func=lambda x: multiplication(*map(int, x.split())),
#     description="Multiplie deux nombres. Entrée : deux entiers séparés par un espace."
# )

# # Initialiser l'agent avec l'outil
# agent = initialize_agent(
#     tools=[tool_multiplication],
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# def run():
#     # Phrase posée à l’agent
#     question = "Quelle est le résultat de 5 fois 10 ?"
#     response = agent.run(question)
#     print("\n🤖 Réponse finale :", response)

# if __name__ == "__main__":
#     run()