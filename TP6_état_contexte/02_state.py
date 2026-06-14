from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

model = ChatOllama(model="llama3.2:3b", temperature=0)

# ─────────────────────────────────────────────────────────────
# Partie 5 
# ─────────────────────────────────────────────────────────────
class CustomState(AgentState):
    """État enrichi : ajoute favourite_colour à l'état de l'agent."""
    favourite_colour: str


# ─────────────────────────────────────────────────────────────
# Partie 6a : Agent qui MODIFIE l'état
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("Partie 6a : Agent qui modifie l'etat")
print("=" * 60)

@tool
def update_favourite_colour(favourite_colour: str, runtime: ToolRuntime) -> Command:
    """Update the favourite colour of the user in the state once they've revealed it."""
    return Command(update={
        "favourite_colour": favourite_colour,
        "messages": [ToolMessage(
            "Successfully updated favourite colour",
            tool_call_id=runtime.tool_call_id
        )]
    })

agent_update = create_agent(
    model=model,
    tools=[update_favourite_colour],
    checkpointer=InMemorySaver(),
    state_schema=CustomState
)

config_1 = {"configurable": {"thread_id": "session_update"}}

response = agent_update.invoke(
    {"messages": [HumanMessage(content="My favourite colour is green")]},
    config_1
)
print("Reponse :", response["messages"][-1].content)
print("Etat favourite_colour :", response.get("favourite_colour", "non defini"))


# ─────────────────────────────────────────────────────────────
# Partie 6b : Agent qui LIT l'état (et le met à jour)
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Partie 6b : Agent qui lit l'etat")
print("=" * 60)

@tool
def read_favourite_colour(runtime: ToolRuntime) -> str:
    """Read the favourite colour of the user from the agent state."""
    try:
        return runtime.state["favourite_colour"]
    except KeyError:
        return "No favourite colour found in state"

agent_read = create_agent(
    model=model,
    tools=[update_favourite_colour, read_favourite_colour],
    checkpointer=InMemorySaver(),
    state_schema=CustomState
)

config_2 = {"configurable": {"thread_id": "session_read"}}

# Etape 1 : L'utilisateur révèle sa couleur préférée → mise à jour de l'état
print("\n[Etape 1] Mise a jour de l'etat...")
response = agent_read.invoke(
    {"messages": [HumanMessage(content="My favourite colour is green")]},
    config_2
)
print("Reponse :", response["messages"][-1].content)

# Etape 2 : L'utilisateur demande sa couleur → l'agent lit l'état
print("\n[Etape 2] Lecture de l'etat...")
response = agent_read.invoke(
    {"messages": [HumanMessage(content="What's my favourite colour?")]},
    config_2
)
print("Reponse :", response["messages"][-1].content)
