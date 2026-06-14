# TP9 : Agent avec LangGraph — SDIA

Ce TP montre comment utiliser **LangGraph** pour concevoir des agents capables d'utiliser des outils (tools), de gérer des workflows avec intervention humaine (Human-in-the-Loop ou HITL), d'effectuer des sauvegardes automatiques d'état (checkpoints) et de manipuler l'historique d'exécution (time-travel / state-forking).

---

## Structure du TP

Les scripts sont divisés en 4 modules indépendants qui structurent la progression :

1. **`tools_setup.py`** (Partie 1) :
   - Initialise le modèle de langage local via **Ollama** (modèle `llama3.2:3b`).
   - Intègre un système de fallback robuste vers **Groq** ou **OpenAI** si Ollama n'est pas actif.
   - Définit les outils arithmétiques annotés `@tool` (`add`, `multiply`, `divide`).

2. **`agent_node.py`** (Partie 2) :
   - Graphe d'agent utilisant un état personnalisé `AgentState` gérant l'historique complet des messages (réducteur `add`) et le nombre d'appels LLM (`llm_calls`).
   - Contient la logique décisionnelle du LLM pour l'appel d'outils et l'exécution en boucle.
   - Présente les 3 modes d'exécution : invoke standard, streaming de mise à jour d'état (`updates`), et streaming de tokens (`messages`).

3. **`hitl_workflow.py`** (Partie 3) :
   - Utilise l'API fonctionnelle moderne de LangGraph (`@task` et `@entrypoint`).
   - Introduit une interruption de workflow à l'aide d'un `interrupt()` pour approbation humaine de brouillon de texte.
   - Reprend l'exécution à l'aide de l'objet `Command(resume=True)`.

4. **`tp_agent.py`** (Partie 4 - TP complet) :
   - Agent avec outils incorporant un nœud d'approbation (`approve_node`) et une sauvegarde en mémoire (`InMemorySaver`).
   - Gère deux scénarios d'interaction humaine (Approbation et Rejet).
   - Démontre la fonctionnalité de voyage dans le temps (Time Travel/Forking) en récupérant un ancien état depuis l'historique, en modifiant la transition d'état et en relançant l'exécution avec d'autres décisions.

---

## Dépendances & Prérequis

- L'environnement virtuel du projet géré par `uv` contient déjà toutes les dépendances requises (`langchain-ollama`, `langgraph`, etc.).
- Assurez-vous que le service local **Ollama** est démarré et que le modèle `llama3.2:3b` est téléchargé (`ollama run llama3.2:3b`). Si Ollama n'est pas démarré, le code utilisera automatiquement vos clés API Groq ou OpenAI définies dans `.env`.

---

## Exécution des scripts

Vous pouvez lancer chaque script directement depuis le dossier racine en utilisant `uv` :

```bash
# Partie 1 : Vérifier la configuration des outils
uv run python TP9_Agent_avec_LangGraph/tools_setup.py

# Partie 2 : Lancer l'agent simple et tester le streaming
uv run python TP9_Agent_avec_LangGraph/agent_node.py

# Partie 3 : Lancer le workflow fonctionnel HITL (Human-in-the-Loop)
uv run python TP9_Agent_avec_LangGraph/hitl_workflow.py

# Partie 4 : Lancer le TP complet (Interrupts, Approve, Reject, State Forking)
uv run python TP9_Agent_avec_LangGraph/tp_agent.py
```

---

## Concepts clés étudiés

> [!NOTE]
> **Dynamic Interrupt (`interrupt()`)**  
> Permet d'arrêter le flux d'exécution au milieu d'un nœud ou d'un entrypoint pour attendre une action externe (humaine), sauvegardant l'état courant.

> [!TIP]
> **Command object (`Command`)**  
> Utilisé dans les graphes récents de LangGraph pour envoyer des valeurs de reprise (`Command(resume=...)`) ou forcer une transition vers un nœud spécifique (`Command(goto=...)`).

> [!IMPORTANT]
> **Time Travel & Forking**  
> Grâce au Checkpointer (`InMemorySaver`), chaque transition du graphe génère un point de sauvegarde identifiable. On peut explorer l'historique via `get_state_history`, sélectionner une version passée de l'état, la modifier via `update_state` et relancer l'exécution depuis ce point pour explorer une branche alternative.
