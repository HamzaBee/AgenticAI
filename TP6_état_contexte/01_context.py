

# ─────────────────────────────────────────────────────────────
# Partie 1 : Définir une classe de contexte structurée
# ─────────────────────────────────────────────────────────────
from dataclasses import dataclass

@dataclass
class ColourContext:
    """Contexte utilisateur : contient les couleurs préférées."""
    favourite_colour: str = "blue"
    least_favourite_colour: str = "yellow"


from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent

model = ChatOllama(model="llama3.2:3b", temperature=0)

# ─────────────────────────────────────────────────────────────
# Partie 2 : Agent sans outils de contexte
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("Partie 2 : Agent sans outils de contexte")
print("=" * 60)

agent_no_tools = create_agent(
    model=model,
    context_schema=ColourContext   # le contexte est défini mais sans outils
)

response = agent_no_tools.invoke(
    {"messages": [HumanMessage(content="What is my favourite colour?")]},
    context=ColourContext()        # contexte par défaut : blue / yellow
)
print("Reponse :", response["messages"][-1].content)


# ─────────────────────────────────────────────────────────────
# Partie 3 : Agent avec outils lisant le contexte (ToolRuntime)
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Partie 3 : Agent avec outils de contexte")
print("=" * 60)

@tool
def get_favourite_colour(runtime: ToolRuntime) -> str:
    """Get the favourite colour of the user from the context."""
    return runtime.context.favourite_colour

@tool
def get_least_favourite_colour(runtime: ToolRuntime) -> str:
    """Get the least favourite colour of the user from the context."""
    return runtime.context.least_favourite_colour

agent_ctx = create_agent(
    model=model,
    tools=[get_favourite_colour, get_least_favourite_colour],
    context_schema=ColourContext
)

response = agent_ctx.invoke(
    {"messages": [HumanMessage(content="What is my favourite colour?")]},
    context=ColourContext()        # favourite_colour="blue" (défaut)
)
print("Reponse (contexte defaut) :", response["messages"][-1].content)


# ─────────────────────────────────────────────────────────────
# Partie 4 : Changement dynamique de contexte
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Partie 4 : Changement de contexte")
print("=" * 60)

response = agent_ctx.invoke(
    {"messages": [HumanMessage(content="What is my favourite colour?")]},
    context=ColourContext(favourite_colour="green")  # contexte modifié
)
print("Reponse (favourite_colour=green) :", response["messages"][-1].content)
