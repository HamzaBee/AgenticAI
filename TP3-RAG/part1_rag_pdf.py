import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

# Charger les variables d'environnement
load_dotenv()

# Configuration des chemins absolus
base_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(base_dir, "acmecorp-employee-handbook.pdf")

# Configuration du modèle
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

# 1. Chargement et extraction de contenu d'un fichier PDF
print(f"--- Chargement du PDF : {pdf_path} ---")
if not os.path.exists(pdf_path):
    print(f"Erreur : Le fichier {pdf_path} est introuvable.")
    exit(1)

loader = PyPDFLoader(pdf_path)
data = loader.load()

# 2. Segmentation de texte (Chunking)
print("--- Segmentation du texte ---")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200, 
    add_start_index=True
)
all_splits = text_splitter.split_documents(data)
print(f"Nombre de chunks créés : {len(all_splits)}")

# 3. Génération d'embeddings textuels (HuggingFace)
print("--- Génération des embeddings (all-MiniLM-L6-v2) ---")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Création et indexation de la base vectorielle en mémoire
print("--- Indexation dans la base vectorielle ---")
vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents(documents=all_splits)

# 5. Définition de l'outil de recherche (Tool)
@tool
def search_handbook(query: str) -> str:
    """Recherche des informations pertinentes dans le manuel de l'employé."""
    print(f"\n[Tool] Recherche sémantique pour : {query}")
    results = vector_store.similarity_search(query, k=2)
    return "\n\n".join([res.page_content for res in results])

# 6. Initialisation de l'agent RAG
print(f"--- Initialisation de l'agent RAG avec {OLLAMA_MODEL} ---")
model = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0
)

agent = create_agent(
    model=model,
    tools=[search_handbook],
    system_prompt="You are a helpful agent that can search the employee handbook for information. Use the search_handbook tool to find answers."
)

# 7. Interrogation
question = "How many days of vacation does an employee get in their first year?"
print(f"\nQuestion : {question}")

response = agent.invoke(
    {"messages": [HumanMessage(content=question)]}
)

print("\nRéponse de l'agent :")
print(response['messages'][-1].content)
