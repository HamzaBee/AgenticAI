import os
from dotenv import load_dotenv
from typing import Dict, Any, List
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# Charger les variables d'environnement
load_dotenv()

# Configuration
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0"))
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
APP_MODE = os.getenv("APP_MODE", "interactive")

# Initialisation du modèle
model = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=OLLAMA_TEMPERATURE
)

# Configuration de l'outil de recherche (Tavily)
tools = []
if TAVILY_API_KEY:
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
    tools.append(TavilySearchResults(max_results=3))
else:
    print("Warning: TAVILY_API_KEY non configurée dans .env. La recherche web sera désactivée.")

# Prompt système pour le Chef Personnel
system_prompt = (
    "Vous êtes un Chef Cuisinier Personnel expert et amical. "
    "Votre rôle est d'aider l'utilisateur à préparer des repas délicieux avec les ingrédients qu'il a sous la main. "
    "Vous devez : \n"
    "1. Mémoriser les préférences (allergies, goûts, régimes) de l'utilisateur pour personnaliser vos futures suggestions.\n"
    "2. Proposer des recettes créatives basées sur les ingrédients fournis.\n"
    "3. Utiliser l'outil de recherche web si vous avez besoin de précisions sur une recette ou une technique culinaire.\n"
    "4. Expliquer les étapes de manière claire et simple.\n"
    "Répondez toujours en français, avec un ton enthousiaste et professionnel."
)

# Initialisation de l'agent avec mémoire
memory = InMemorySaver()

# Création de l'agent en utilisant create_agent (standard de la plateforme)
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=memory
)

def run_interactive():
    """Lance l'agent en mode conversationnel interactif."""
    config = {"configurable": {"thread_id": "user_session_1"}}
    
    print(f"\n--- 👨‍🍳 Bienvenue chez votre Chef Personnel ({OLLAMA_MODEL}) ---")
    print("Dites-moi ce que vous avez dans votre frigo ou vos préférences !")
    print("(Tapez 'exit' pour quitter)\n")
    
    while True:
        try:
            user_input = input("Vous : ")
            if user_input.lower() in ["exit", "quit", "quitter"]:
                print("Bon appétit et à bientôt !")
                break
            
            if not user_input.strip():
                continue
                
            result = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=config
            )
            
            final_response = result["messages"][-1].content
            print(f"\nChef : {final_response}\n")
            
        except KeyboardInterrupt:
            print("\nInterruption... Au revoir !")
            break
        except Exception as e:
            print(f"\nOups, une erreur est survenue : {e}")

def run_demo():
    """Exécute une séquence de démonstration pour montrer la mémoire et l'utilisation des outils."""
    config = {"configurable": {"thread_id": "demo_session"}}
    print("\n--- 🚀 Lancement de la démo du Chef Personnel ---")
    
    demo_steps = [
        "Bonjour ! Je m'appelle Sami. Je suis allergique aux noix et j'adore la cuisine épicée.",
        "J'ai du poulet, du lait de coco et du riz. Que me conseilles-tu ?",
        "Peux-tu me rappeler mon nom et mes restrictions alimentaires pour vérifier que tu as bien suivi ?"
    ]
    
    for i, step in enumerate(demo_steps, 1):
        print(f"\n[Étape {i}] Utilisateur : {step}")
        result = agent.invoke(
            {"messages": [HumanMessage(content=step)]},
            config=config
        )
        print(f"Chef : {result['messages'][-1].content}")

if __name__ == "__main__":
    if APP_MODE == "demo":
        run_demo()
    else:
        run_interactive()
