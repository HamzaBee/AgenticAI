from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
    temperature=0
)

class CapitalInfo(BaseModel):
    nom: str
    localisation: str
    ambiance: str
    economie: str

system_prompt = """
Vous êtes un auteur de science-fiction et vous devez créer une capitale spatiale à la demande d'un utilisateur.
Veuillez respecter la structure ci-dessous.
Nom : Nom de la capitale
Localisation : Lieu où elle est située
Ambiance : Description en 2 ou 3 mots
Économie : Principaux secteurs d'activité
"""

# Utilisation de create_agent avec response_format (Pydantic BaseModel)
agent = create_agent(
    model=model,
    system_prompt=system_prompt,
    response_format=CapitalInfo
)

question = HumanMessage(content="Quelle est la capitale de la lune ?")
print("Génération d'une réponse structurée via BaseModel...")

response = agent.invoke(
    {"messages": [question]}
)

# La réponse structurée est accessible via la clé 'structured_response'
print(response["structured_response"])
