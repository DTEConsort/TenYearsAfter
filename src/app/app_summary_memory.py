import os
from dotenv import load_dotenv

# Charger la clé API depuis .env
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory


def main():
    # 1) Modèle
    llm = ChatOpenAI(model="gpt-4.1-mini")

    # 2) Mémoire par résumé
    memory = ConversationSummaryMemory(llm=llm)

    # 3) Chaîne conversationnelle avec mémoire résumé
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )

    # 4) Plusieurs échanges pour tester
    print(">> Échange 1")
    print(conversation.predict(input="Bonjour, je m’appelle David et j’aime le football."))

    print("\n>> Échange 2")
    print(conversation.predict(input="J’habite à Paris depuis 5 ans."))

    print("\n>> Échange 3")
    print(conversation.predict(input="Quel est mon prénom et où j’habite ?"))

    # 5) Vérifier le résumé stocké
    print("\n--- Résumé interne de la mémoire ---")
    print(memory.buffer)


if __name__ == "__main__":
    main()