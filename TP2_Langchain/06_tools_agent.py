from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
    temperature=0
)

@tool
def meteo_capitale(ville: str) -> str:
    """
    Donne la météo d'une capitale (valeurs fixes pour test).
    Args:
        ville: nom de la capitale
    """
    print(f"\n[Tool] Appel de meteo_capitale pour : {ville}")
    temperature = 25
    humidite = 60
    pression = 1013
    return (
        f"Météo à {ville} : "
        f"Température = {temperature}°C, "
        f"Humidité = {humidite}%, "
        f"Pression = {pression} hPa"
    )

system_prompt = "Utilisez les outils fournis pour répondre aux questions."

agent = create_agent(
    model=model,
    tools=[meteo_capitale],
    system_prompt=system_prompt
)

question = HumanMessage(content="Quelle est la météo à Capitole lunaire ?")
response = agent.invoke(
    {"messages": [question]}
)

print("\nRéponse finale :")
print(response['messages'][-1].content)
