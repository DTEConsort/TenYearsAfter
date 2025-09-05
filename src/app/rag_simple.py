# src/app/rag_simple.py

# Chargement de fichiers texte
from langchain_community.document_loaders import TextLoader

# Indexation des documents sous forme vectorielle
from langchain_community.vectorstores import FAISS

# Conversion du texte en vecteurs numériques (embeddings)
from langchain_community.embeddings import OpenAIEmbeddings

# Création de la chaîne RAG (retrieval + génération)
from langchain.chains import RetrievalQA

# Appel au modèle GPT via OpenAI
from langchain_openai import ChatOpenAI

# Chargement des variables d’environnement (.env)
from dotenv import load_dotenv
import os


def run():
    # -------------------------------------------
    # 1. Charger la clé API depuis .env
    # -------------------------------------------
    load_dotenv()

    # -------------------------------------------
    # 2. Liste des fichiers texte à indexer
    # -------------------------------------------
    doc_paths = [
        "docs/offre_ia.txt",
        "docs/offre_rh.txt"
    ]

    # -------------------------------------------
    # 3. Charger et concaténer tous les documents
    # -------------------------------------------
    all_documents = []
    for path in doc_paths:
        loader = TextLoader(path, encoding="utf-8")
        docs = loader.load()
        all_documents.extend(docs)

    # -------------------------------------------
    # 4. Créer les embeddings (vecteurs)
    # -------------------------------------------
    embeddings = OpenAIEmbeddings()

    # -------------------------------------------
    # 5. Indexer tous les documents dans FAISS
    # -------------------------------------------
    vectorstore = FAISS.from_documents(all_documents, embeddings)

    # -------------------------------------------
    # 6. Construire le moteur de recherche augmentée
    # -------------------------------------------
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4.1-mini"),
        retriever=retriever,
        return_source_documents=True
    )

    # -------------------------------------------
    # 7. Poser une question (sur IA ou RH)
    # -------------------------------------------
    question = "Quels sont les objectifs de l’offre IA ? Existe t-il une formation associée ?"

    # -------------------------------------------
    # 8. Interroger la base et récupérer la réponse
    # -------------------------------------------
    result = qa_chain.invoke({"query": question})

    # -------------------------------------------
    # 9. Afficher la réponse et la source utilisée
    # -------------------------------------------
    print("\n🤖 Réponse :\n", result["result"])
    # sprint("\n📄 Source utilisée :\n", result["source_documents"][0].page_content)


# Lancer si le fichier est exécuté directement
if __name__ == "__main__":
    run()
# -------------------------------------------