# src/app/agent_faq.py

#from langchain.embeddings import OpenAIEmbeddings
#from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
#from langchain.document_loaders import TextLoader
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
#from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Charger le document
loader = TextLoader("../data/faq.txt")
documents = loader.load()

# 2. Découper le texte en chunks
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents)

# 3. Créer l'index FAISS
embeddings = OpenAIEmbeddings()
vectordb = FAISS.from_documents(docs, embeddings)

# 4. Créer la mémoire de conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 5. Créer la chaîne RAG conversationnelle
llm = ChatOpenAI(model="gpt-4", temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectordb.as_retriever(), memory=memory)

# 6. Boucle de conversation
print("🤖 Assistant FAQ basé sur vos documents\n")

while True:
    question = input("💬 Vous : ")
    if question.lower() in ["q", "quit", "exit"]:
        break
    result = qa.run(question)
    print(f"🤖 Assistant : {result}")