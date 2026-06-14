from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
    temperature=0
)

# Configuration de l'outil de recherche
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    print("Erreur : TAVILY_API_KEY non trouvée dans le fichier .env")
    exit(1)

os.environ["TAVILY_API_KEY"] = tavily_api_key
search_tool = TavilySearchResults(max_results=3)

agent = create_agent(
    model=model,
    tools=[search_tool]
)

question = HumanMessage(content="Qui est le Président de commune actuel de Marrakech ?")
print(f"Recherche en cours pour : {question.content}...")

response = agent.invoke(
    {"messages": [question]}
)

print("\nRéponse :")
print(response['messages'][-1].content)
