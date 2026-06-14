from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
    temperature=0
)

# Utilisation de InMemorySaver pour la mémoire
memory = InMemorySaver()

agent = create_agent(
    model=model,
    checkpointer=memory
)

# Configuration de la session (thread_id)
config = {"configurable": {"thread_id": "session_sami"}}

# Premier message
q1 = HumanMessage(content="Bonjour, mon nom est Sami et je suis un développeur.")
print(f"Utilisateur : {q1.content}")
r1 = agent.invoke({"messages": [q1]}, config)
print(f"Agent : {r1['messages'][-1].content}")

# Deuxième message (nécessite la mémoire)
q2 = HumanMessage(content="Quel est mon métier ?")
print(f"\nUtilisateur : {q2.content}")
r2 = agent.invoke({"messages": [q2]}, config)
print(f"Agent : {r2['messages'][-1].content}")
