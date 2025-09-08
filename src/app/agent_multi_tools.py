# src/app/agent_multi_tools.py

from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent import AgentExecutor
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from app.tools.tools_temperature import celsius_to_fahrenheit
from app.tools.tools_calculator import multiply
import os
from dotenv import load_dotenv

load_dotenv()

def run():
    print("🔧 Agent multi-outils (calcul, température, etc.)")

    llm = ChatOpenAI(model="gpt-4", temperature=0)

    tools = [
        Tool.from_function(multiply, name="Multiplication", description="Multiplie deux nombres"),
        Tool.from_function(celsius_to_fahrenheit, name="ConvertisseurTempérature", description="Convertit les Celsius en Fahrenheit"),
    ]

    agent: AgentExecutor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    while True:
        question = input("\n💬 Pose une question (ou 'q' pour quitter): ")
        if question.lower() == "q":
            break

        try:
            response = agent.invoke({"input": question})
            print("🧠 Réponse :", response["output"])
        except Exception as e:
            print("⚠️ Erreur :", e)

if __name__ == "__main__":
    run()