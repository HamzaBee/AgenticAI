from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

# Initialiser le modèle Ollama
model = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
    temperature=0
)

# Création d'un agent simple (sans tools pour l'instant)
# On utilise create_agent comme indiqué dans le PDF (disponible dans langchain-agents/langchain>=0.3)
agent = create_agent(model=model)

question = HumanMessage(content="Quelle est la capitale de la lune ?")

response = agent.invoke(
    {"messages": [question]}
)

print(response['messages'][-1].content)
