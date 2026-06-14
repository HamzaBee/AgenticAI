from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
    temperature=0
)

# Pour une réponse structurée sans BaseModel, on utilise le prompt
system_prompt = """
Vous êtes un auteur de science-fiction et vous devez créer une capitale spatiale à la demande d'un utilisateur.
Veuillez respecter la structure ci-dessous.
Nom : Nom de la capitale
Localisation : Lieu où elle est située
Ambiance : Description en 2 ou 3 mots
Économie : Principaux secteurs d'activité
"""

scifi_agent = create_agent(
    model=model,
    system_prompt=system_prompt
)

question = HumanMessage(content="Quelle est la capitale de la lune ?")
response = scifi_agent.invoke(
    {"messages": [question]}
)

print(response['messages'][-1].content)
