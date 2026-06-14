import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

# Charger les variables d'environnement
load_dotenv()

# Configuration des chemins absolus
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "Chinook.db")

# Configuration du modèle
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

# 1. Connexion à la base de données SQLite
print(f"--- Connexion à la base SQL : {db_path} ---")
if not os.path.exists(db_path):
    print(f"Erreur : La base de données {db_path} est introuvable.")
    exit(1)

db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

# 2. Création d'un outil personnalisé pour interroger la base SQL
@tool
def sql_query(query: str) -> str:
    """Obtain information from the database using SQL queries. The input should be a valid SQL query."""
    try:
        print(f"\n[Tool] Exécution de la requête SQL : {query}")
        result = db.run(query)
        print(f"[Tool] Résultat brut : {result}")
        if not result or result == "[]":
            return "No results found for this query."
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# 3. Création de l'agent SQL
system_prompt = """You are a SQL expert.
Rules:
- You MUST use the sql_query tool to answer questions about the database.
- Always generate valid SQL queries based on the schema below.
- Report the results from the tool to the user in a friendly way.

Database schema (Key tables):
Table Artist: ArtistId, Name
Table Album: AlbumId, Title, ArtistId
Table Track: TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice
"""

print(f"--- Initialisation de l'agent SQL avec {OLLAMA_MODEL} ---")
model = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0
)

agent = create_agent(
    model=model,
    tools=[sql_query],
    system_prompt=system_prompt
)

# 4. Interrogation
question = "Give me the first 5 artists in the database"
print(f"\nQuestion : {question}")

response = agent.invoke(
    {"messages": [HumanMessage(content=question)]}
)

print("\nRéponse de l'agent :")
print(response['messages'][-1].content)
