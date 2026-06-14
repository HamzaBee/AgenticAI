# TP8 : Workflows avec LangGraph — SDIA

Ce projet présente l'utilisation de **LangGraph** pour concevoir, structurer et exécuter différents types de workflows d'agents et d'états d'exécution.

---

## Structure du TP

Le TP est divisé en 6 scripts Python indépendants correspondant à chaque partie du cours :

- **`hello_graph.py`** (Partie 1) : Initialisation d'un graphe minimal avec un unique nœud, utilisant `MessagesState` pré-défini de LangGraph.
- **`two_step_workflow.py`** (Partie 2) : Workflow séquentiel simple reliant deux étapes consécutives (`refine_topic` -> `write_joke`) à l'aide d'un état (`State`) personnalisé.
- **`reducers_demo.py`** (Partie 3) : Illustration du mécanisme des **Reducers** (avec `operator.add`), montrant comment les modifications apportées à une clé d'état par plusieurs nœuds successifs s'accumulent au lieu d'être écrasées.
- **`message_state.py`** (Partie 4) : Définition d'un état personnalisé `ChatState` gérant un historique de messages avec un réducteur de liste (`add`) et un compteur d'étapes (`steps`).
- **`conditional_workflow.py`** (Partie 5) : Implémentation de routes et transitions décisionnelles (conditionnelles) via `add_conditional_edges` et un routeur (`check_joke`) pour déterminer dynamiquement l'étape suivante.
- **`workflow_loop.py`** (Partie 6) : Création d'une boucle cyclique où le graphe ré-exécute un nœud tant qu'un compteur n'a pas atteint la valeur limite ($n < 5$). Ce script génère et exporte également la structure du graphe au format PNG sous le nom de `graph2.png`.

---

## Dépendances

Les dépendances requises sont déjà configurées dans le projet. Pour exécuter ces scripts avec `uv`, utilisez l'environnement virtuel du projet.

---

## Exécution

Vous pouvez exécuter chaque partie directement avec la commande correspondante depuis le terminal :

```bash
# Partie 1 : Hello Graph
uv run python hello_graph.py

# Partie 2 : Workflow séquentiel à deux étapes
uv run python two_step_workflow.py

# Partie 3 : Démonstration des Reducers
uv run python reducers_demo.py

# Partie 4 : Gestion de l'état des messages personnalisés
uv run python message_state.py

# Partie 5 : Workflow conditionnel
uv run python conditional_workflow.py

# Partie 6 : Boucle dans un Workflow (Génère graph2.png)
uv run python workflow_loop.py
```

---

## Concepts clés étudiés

| Concept                 | Description                                                                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Node (Nœud)**         | Fonction Python représentant une unité de calcul recevant l'état actuel et retournant des mises à jour d'état.                                |
| **Edge (Arête)**        | Liaison définissant le flux de contrôle séquentiel direct entre deux nœuds (`START`, `END`, ou nœud à nœud).                                  |
| **Reducer (Réducteur)** | Fonction spéciale (comme `operator.add`) associée à une clé de l'état pour définir comment fusionner de nouvelles valeurs avec les anciennes. |
| **Conditional Edge**    | Branchement dynamique basé sur la valeur retournée par une fonction de routage pour diriger le flux vers différents nœuds.                    |
| **Graph Visualisation** | Utilisation de l'API de représentation de graphe                                                                                              |
