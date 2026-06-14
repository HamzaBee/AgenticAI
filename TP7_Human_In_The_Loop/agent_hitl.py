"""
================================================================
 TP7 - Human In The Loop (HITL)
================================================================
"""

# ─────────────────────────────────────────────────────────────
# Partie 1 : Definition des outils
# ─────────────────────────────────────────────────────────────
from langchain.tools import tool, ToolRuntime


@tool
def read_email(runtime: ToolRuntime) -> str:
    """Read an email from the agent state."""
    # Lit l'email depuis l'etat de l'agent (injecte via EmailState)
    return runtime.state["email"]


@tool
def send_email(body: str) -> str:
    """Send an email with the given body."""
    # Simulation d'envoi (pas de vrai envoi ici)
    print(f"  [send_email] Corps du message : {body}")
    return "Email sent"


# ─────────────────────────────────────────────────────────────
# Partie 2 : Creation de l'agent HITL
# ─────────────────────────────────────────────────────────────
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


class EmailState(AgentState):
    """Etat enrichi : contient l'email a traiter."""
    email: str


model = ChatOllama(model="llama3.2:3b", temperature=0)

agent = create_agent(
    model=model,
    tools=[read_email, send_email],
    state_schema=EmailState,
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "read_email": False,   # pas d'interruption pour la lecture
                "send_email": True,    # INTERRUPTION avant envoi (action sensible)
            },
            description_prefix="Tool execution requires approval",
        ),
    ],
)

config = {"configurable": {"thread_id": "email_thread_1"}}

# Premier appel : l'agent lit l'email et PREPARE l'envoi
# => L'execution est SUSPENDUE avant send_email (interrupt_on=True)
print("=" * 60)
print("Partie 2 : Premier appel — l'agent se suspend avant send_email")
print("=" * 60)

response = agent.invoke(
    {
        "messages": [HumanMessage(
            content=(
                "Veuillez lire mon e-mail et envoyer une reponse immediatement. "
                "Envoyez la reponse maintenant dans le meme fil de discussion."
            )
        )],
        "email": (
            "Bonjour Sara, je vais etre en retard pour notre reunion de demain. "
            "Pouvons-nous la reprogrammer ? Cordialement, Sofia"
        ),
    },
    config=config,
)

print("Reponse brute :", response)

# Afficher les details de l'interruption
if "__interrupt__" in response:
    interrupt_data = response["__interrupt__"]
    print("\n[Interruption detectee]")
    print("  Metadata completes :", interrupt_data)

    # Extraire le corps de l'email que l'agent voulait envoyer
    try:
        proposed_body = interrupt_data[0].value["action_requests"][0]["args"]["body"]
        print("  Corps propose par l'agent :", proposed_body)
    except (KeyError, IndexError, TypeError) as e:
        print("  (Impossible d'extraire le corps :", e, ")")
else:
    print("Pas d'interruption — l'agent a termine directement.")


# ─────────────────────────────────────────────────────────────
# Partie 3 : Approuver le resultat
# ─────────────────────────────────────────────────────────────
from langgraph.types import Command

print("\n" + "=" * 60)
print("Partie 3 : Approbation — l'email est envoye tel quel")
print("=" * 60)

# Meme thread_id => reprend la ou l'execution s'est arretee
response_approve = agent.invoke(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config=config,
)
print("Reponse apres approbation :", response_approve["messages"][-1].content)


# ─────────────────────────────────────────────────────────────
# Partie 4 : Refuser le resultat
# (Relancer une nouvelle session pour tester le rejet)
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Partie 4 : Rejet — l'agent ne peut pas envoyer l'email")
print("=" * 60)

config_reject = {"configurable": {"thread_id": "email_thread_reject"}}

# Relancer l'agent pour creer une nouvelle interruption
agent.invoke(
    {
        "messages": [HumanMessage(
            content=(
                "Veuillez lire mon e-mail et envoyer une reponse immediatement."
            )
        )],
        "email": (
            "Bonjour Sara, je vais etre en retard pour notre reunion de demain. "
            "Pouvons-nous la reprogrammer ? Cordialement, Sofia"
        ),
    },
    config=config_reject,
)

# Refuser l'action avec un message d'explication
response_reject = agent.invoke(
    Command(
        resume={
            "decisions": [
                {
                    "type": "reject",
                    "message": "J'annule notre rendez-vous.",
                }
            ]
        }
    ),
    config=config_reject,
)
print("Reponse apres rejet :", response_reject["messages"][-1].content)


# ─────────────────────────────────────────────────────────────
# Partie 5 : Modifier le resultat avant execution
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Partie 5 : Modification — l'humain corrige le corps de l'email")
print("=" * 60)

config_edit = {"configurable": {"thread_id": "email_thread_edit"}}

# Relancer l'agent pour creer une nouvelle interruption
agent.invoke(
    {
        "messages": [HumanMessage(
            content=(
                "Veuillez lire mon e-mail et envoyer une reponse immediatement."
            )
        )],
        "email": (
            "Bonjour Sara, je vais etre en retard pour notre reunion de demain. "
            "Pouvons-nous la reprogrammer ? Cordialement, Sofia"
        ),
    },
    config=config_edit,
)

# Modifier l'action : l'humain remplace le corps de l'email
response_edit = agent.invoke(
    Command(
        resume={
            "decisions": [
                {
                    "type": "edit",
                    "edited_action": {
                        "name": "send_email",   # nom de l'outil a modifier
                        "args": {               # nouveaux arguments
                            "body": (
                                "Je suis desol(e)e mais je dois annuler notre "
                                "rendez-vous, je ne serai pas libre. Sara"
                            )
                        },
                    },
                }
            ]
        }
    ),
    config=config_edit,
)
print("Reponse apres modification :", response_edit["messages"][-1].content)
