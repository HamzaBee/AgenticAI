"""
================================================================
 Chef Personnel Agent -- Agent IA Culinaire
================================================================
Combining:
  1. System Message   -- chef personality & instructions
  2. Web Search Tool  -- Tavily for recipes/techniques
  3. Memory           -- remembers user preferences (InMemorySaver)
  4. RAG              -- local culinary knowledge base (vector store)
================================================================
Run modes:
  python chef_personnel_agent.py            # interactive chat
  APP_MODE=demo python chef_personnel_agent.py  # automated demo
"""

import os
import textwrap
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_tavily import TavilySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# ----------------------------------------------------------------
# 0. Configuration
# ----------------------------------------------------------------
load_dotenv()

OLLAMA_MODEL       = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0"))
TAVILY_API_KEY     = os.getenv("TAVILY_API_KEY")
APP_MODE           = os.getenv("APP_MODE", "interactive")

# ----------------------------------------------------------------
# 1. RAG -- Base de connaissances culinaires locale
# ----------------------------------------------------------------
CULINARY_KNOWLEDGE = [
    Document(
        page_content=textwrap.dedent("""\
            Associations classiques d'ingredients :
            - Tomate + basilic + mozzarella -> Caprese, pizza margherita
            - Poulet + citron + ail -> roti mediterraneen
            - Lait de coco + curry + gingembre -> curry thai, soupe laksa
            - Oeuf + farine + lait -> pate a crepes, omelette, quiche
            - Riz + legumes + sauce soja -> riz saute asiatique
            - Lentilles + epices (cumin, coriandre) -> dal indien
            - Pomme de terre + fromage + creme -> gratin dauphinois
            - Courgette + ail + huile d'olive -> ratatouille provencale
        """),
        metadata={"source": "associations"},
    ),
    Document(
        page_content=textwrap.dedent("""\
            Techniques de cuisson essentielles :
            - Saute : cuisson rapide a feu vif avec peu de matiere grasse
            - Braise : longue cuisson dans un liquide (viandes dures, legumineuses)
            - Poche : cuisson dans un liquide fremissant (oeuf poche, poisson delicat)
            - Roti : cuisson au four a chaleur seche (poulet entier, legumes racines)
            - Vapeur : preserve vitamines et textures (legumes verts, filets de poisson)
            - Confit : cuisson lente dans la graisse ou le sucre
            - Wok : cuisson tres rapide a tres haute temperature
        """),
        metadata={"source": "techniques"},
    ),
    Document(
        page_content=textwrap.dedent("""\
            Substitutions courantes en cuisine :
            - Beurre -> huile de coco ou compote de pommes (patisserie allegee)
            - Creme fraiche -> yaourt grec ou lait de coco (version legere)
            - Farine de ble -> farine de riz ou d'amande (sans gluten)
            - Sucre blanc -> miel, sirop d'erable ou dattes (naturel)
            - Oeuf -> graine de lin + eau, ou aquafaba (vegan)
            - Viande -> tofu, tempeh, seitan, lentilles (vegetarien/vegan)
        """),
        metadata={"source": "substitutions"},
    ),
    Document(
        page_content=textwrap.dedent("""\
            Adaptation aux regimes alimentaires :
            - Sans gluten : eviter ble, seigle, orge -- utiliser riz, quinoa, sarrasin
            - Sans lactose : remplacer lait/creme par laits vegetaux (avoine, amande, coco)
            - Vegan : aucun produit animal -- legumineuses, tofu, noix, graines
            - Halal : pas de porc ni alcool -- viandes halal certifiees
            - Cetogene (keto) : peu de glucides, riche en graisses -- eviter sucre, pain, riz
            - Allergie aux noix : eviter arachides, amandes, noisettes, noix de cajou
        """),
        metadata={"source": "regimes"},
    ),
    Document(
        page_content=textwrap.dedent("""\
            Recettes rapides (moins de 20 minutes) :
            - Pates a l'ail et huile (aglio e olio) : pates + ail + huile d'olive + persil
            - Omelette aux legumes : oeufs + legumes du frigo + fromage
            - Riz saute aux oeufs : riz cuit + oeuf + sauce soja + legumes
            - Wrap poulet-crudites : tortilla + poulet + salade + tomate + sauce yaourt
            - Soupe express tomate-basilic : tomates concassees + bouillon + basilic mixe
            - Bruschetta : pain toaste + tomates + ail + basilic + huile d'olive
        """),
        metadata={"source": "recettes_rapides"},
    ),
    Document(
        page_content=textwrap.dedent("""\
            Conseils de conservation des aliments :
            - Herbes fraiches : dans un verre d'eau au refrigerateur
            - Avocats coupes : avec du jus de citron pour eviter l'oxydation
            - Fromage : enveloppe dans du papier cire (pas de film plastique)
            - Viande crue : au bas du refrigerateur, separee des aliments cuits
            - Pommes de terre : endroit sombre et frais, separees des oignons
            - Restes cuits : refrigerateur max 3 jours, congelateur max 3 mois
        """),
        metadata={"source": "conservation"},
    ),
]

print("--- [RAG] Initialisation de la base de connaissances culinaires ---")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(CULINARY_KNOWLEDGE)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents(splits)
print(f"[OK] {len(splits)} chunks indexes dans la base culinaire.")


@tool
def recherche_culinaire(query: str) -> str:
    """
    Effectue une recherche semantique dans la base de connaissances culinaires locale.
    Utile pour : associations d'ingredients, techniques de cuisson, substitutions,
    regimes alimentaires, recettes rapides, conseils de conservation.
    Toujours utiliser cet outil en premier avant la recherche web.
    """
    print(f"\n  [RAG Tool] Recherche locale : {query}")
    results = vector_store.similarity_search(query, k=3)
    if not results:
        return "Aucun resultat trouve dans la base culinaire."
    return "\n\n---\n\n".join(doc.page_content for doc in results)


# ----------------------------------------------------------------
# 2. Outil de recherche web -- Tavily
# ----------------------------------------------------------------
tools: list = [recherche_culinaire]

if TAVILY_API_KEY:
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
    tools.append(TavilySearch(max_results=3))
    print("[OK] Outil de recherche web (Tavily) active.")
else:
    print("[!] TAVILY_API_KEY manquante -- recherche web desactivee.")

# ----------------------------------------------------------------
# 3. System Message -- Personnalite et instructions du chef
# ----------------------------------------------------------------
SYSTEM_PROMPT = (
    "Vous etes ChefBot, un Chef Cuisinier Personnel expert, chaleureux et tres creatif.\n\n"
    "Votre mission :\n"
    "1. Recevoir la liste des ingredients disponibles dans le refrigerateur de l'utilisateur.\n"
    "2. Memoriser ses preferences personnelles : allergies, gouts, regimes alimentaires "
    "(vegetarien, sans gluten, halal, etc.) et les appliquer systematiquement.\n"
    "3. Proposer un ou plusieurs plats creatifs et adaptes aux ingredients disponibles.\n"
    "4. Utiliser l'outil `recherche_culinaire` pour consulter la base de connaissances "
    "culinaires locale (associations, techniques, substitutions, regimes alimentaires).\n"
    "5. Utiliser l'outil `recherche_web` pour trouver des recettes ou techniques "
    "specifiques si la base locale ne suffit pas.\n\n"
    "Format recommande pour une recette :\n"
    "- Nom du plat\n"
    "- Ingredients necessaires\n"
    "- Etapes de preparation numerotees\n"
    "- Temps de preparation estime\n"
    "- Conseil du chef\n\n"
    "Repondez toujours en francais, avec un ton enthousiaste et professionnel. "
    "Si l'utilisateur mentionne une allergie ou une preference, confirmez-le "
    "et tenez-en compte dans toutes les reponses suivantes."
)

# ----------------------------------------------------------------
# 4. Modele + Agent avec Memoire (InMemorySaver)
# ----------------------------------------------------------------
print(f"--- [AGENT] Initialisation avec {OLLAMA_MODEL} ---")
model = ChatOllama(model=OLLAMA_MODEL, temperature=OLLAMA_TEMPERATURE)
memory = InMemorySaver()      # mecanisme de memoire de conversation

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory,      # chaque thread_id garde son historique
)
print("[OK] Agent pret!\n")

# ----------------------------------------------------------------
# 5. Modes d'execution
# ----------------------------------------------------------------

def run_interactive():
    """Mode interactif : conversation libre avec le chef."""
    config = {"configurable": {"thread_id": "chef_session_1"}}

    print("=" * 60)
    print(f"  ChefBot -- Votre Chef Personnel IA ({OLLAMA_MODEL})")
    print("=" * 60)
    print("Donnez-moi la liste de vos ingredients disponibles,")
    print("ou precisez vos preferences / restrictions alimentaires.")
    print("(Tapez 'exit' pour terminer)\n")

    while True:
        try:
            user_input = input("Vous : ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "quitter"):
                print("\nBon appetit et a bientot !")
                break

            result = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
            )
            print(f"\nChef : {result['messages'][-1].content}\n")

        except KeyboardInterrupt:
            print("\nInterruption. Au revoir !")
            break
        except Exception as e:
            print(f"\nErreur : {e}\n")


def run_demo():
    """
    Mode demo : scenario automatique illustrant les 4 fonctionnalites.
    1. Memoire   -- enregistrement des preferences
    2. RAG       -- association d'ingredients (base locale)
    3. RAG       -- technique de cuisson (base locale)
    4. Web       -- recette specifique en ligne
    5. Memoire   -- rappel des preferences memorisees
    """
    config = {"configurable": {"thread_id": "chef_demo"}}

    print("=" * 60)
    print("  Demo -- Chef Personnel IA")
    print("  Fonctionnalites : System Message | Web | Memoire | RAG")
    print("=" * 60)

    steps = [
        (
            "[1/5] Memoire -- preferences utilisateur",
            "Bonjour ! Je m'appelle Yasmine. Je suis allergique aux noix "
            "et je suis vegetarienne. J'adore la cuisine epice.",
        ),
        (
            "[2/5] RAG -- association d'ingredients",
            "J'ai dans mon frigo : des lentilles, du cumin, de la coriandre, "
            "des tomates et du yaourt grec. Que puis-je cuisiner ?",
        ),
        (
            "[3/5] RAG -- technique de cuisson",
            "Quelle est la meilleure technique pour cuire les lentilles ?",
        ),
        (
            "[4/5] Web -- recette specifique en ligne",
            "Peux-tu me trouver une recette de dal indien epice avec "
            "les ingredients que j'ai mentionnes ?",
        ),
        (
            "[5/5] Memoire -- verification des preferences",
            "Pour finir, rappelle-moi mon prenom et mes restrictions "
            "alimentaires pour que je puisse verifier que tu m'as bien suivi.",
        ),
    ]

    for label, step in steps:
        print(f"\n" + "-" * 60)
        print(f"  {label}")
        print("-" * 60)
        print(f"Utilisateur : {step}\n")
        result = agent.invoke(
            {"messages": [HumanMessage(content=step)]},
            config=config,
        )
        print(f"Chef : {result['messages'][-1].content}")

    print("\n" + "=" * 60)
    print("  Fin de la demonstration.")
    print("=" * 60)


# ----------------------------------------------------------------
# Point d'entree
# ----------------------------------------------------------------
if __name__ == "__main__":
    if APP_MODE == "demo":
        run_demo()
    else:
        run_interactive()
