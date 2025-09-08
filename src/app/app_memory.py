# import os
# from dotenv import load_dotenv

# # Charger automatiquement la clé API OpenAI depuis le fichier .env
# load_dotenv()

# from langchain_openai import ChatOpenAI
# from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory


# def main():
#     # ------------------------------
#     # 1. Initialisation du modèle
#     # ------------------------------
#     # On utilise le modèle de chat GPT-4.1-mini via LangChain
#     llm = ChatOpenAI(model="gpt-4.1-mini")

#     # ------------------------------
#     # 2. Ajout de la mémoire
#     # ------------------------------
#     # La mémoire stocke l’historique complet de la conversation
#     # Ici : ConversationBufferMemory garde tous les échanges en clair
#     memory = ConversationBufferMemory()

#     # ------------------------------
#     # 3. Création de la chaîne conversationnelle
#     # ------------------------------
#     # On relie le modèle + la mémoire → une chaîne de dialogue
#     conversation = ConversationChain(
#         llm=llm,
#         memory=memory,
#         verbose=True  # affiche le prompt généré en arrière-plan (debug)
#     )

#     # ------------------------------
#     # 4. Exemple d’utilisation
#     # ------------------------------
#     print(">> Question 1")
#     response1 = conversation.predict(input="Bonjour, je m’appelle David.")
#     print("Réponse :", response1)

#     print("\n>> Question 2")
#     response2 = conversation.predict(input="Quel est mon prénom ?")
#     print("Réponse :", response2)


# if __name__ == "__main__":
#     main()

import os
from dotenv import load_dotenv

# Charger la clé API depuis .env
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


def main():
    # 1) Modèle
    llm = ChatOpenAI(model="gpt-4.1-mini")

    # 2) Mémoire
    memory = ConversationBufferMemory()

    # 3) Chaîne conversationnelle
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )

    # 4) On te demande ton prénom
    prenom = input("👋 Bonjour ! Quel est ton prénom ? ").strip()

    # 5) On enregistre ton prénom dans la mémoire
    ack = conversation.predict(input=f"Bonjour, je m’appelle {prenom}.")
    print("🤖", ack)

    # 6) À la fin du programme → tu poses toi-même la question
    question = input("\n👉 Pose-moi une question (ex: 'Comment je m'appelle ?') : ")
    reponse = conversation.predict(input=question)
    print("🤖", reponse)


if __name__ == "__main__":
    main()