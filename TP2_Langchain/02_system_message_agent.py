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

system_prompt = "Vous êtes un auteur de science-fiction ; créez une capitale à la demande des utilisateurs."

# Agent avec System Message
scifi_agent = create_agent(
    model=model,
    system_prompt=system_prompt
)

question = HumanMessage(content="Quelle est la capitale de la lune ?")
response = scifi_agent.invoke(
    {"messages": [question]}
)

print(response['messages'][-1].content)
