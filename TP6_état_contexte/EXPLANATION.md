# TP6 - Agent avec Etat et Contexte

Deux concepts distincts de LangChain/LangGraph appliques a un agent couleurs.

---

## Structure du projet

| Fichier | Parties | Concept |
| ---------------------- | ------- | ------------------------------------------------ |
| `01_context.py` | 1 - 4 | **Contexte** : injection de donnees par invocation |
| `02_state.py` | 5 - 6 | **Etat** : donnees persistantes entre les tours |

---

## Concepts

### Contexte (01_context.py)

Le **contexte** est une structure de donnees passee a chaque invocation.
Il est **immutable** pendant l'execution et **re-injecte** a chaque appel.

```
Invocation 1 : context=ColourContext()                      → blue
Invocation 2 : context=ColourContext(favourite_colour="green") → green
```

- `ColourContext` : dataclass avec `favourite_colour` et `least_favourite_colour`
- `ToolRuntime` : objet injecte automatiquement dans les outils, donne acces a `runtime.context`
- `context_schema` : parametre de `create_agent` qui declare le type de contexte
- `context=...` : passe le contexte lors de `agent.invoke(...)`

### Etat (02_state.py)

L'**etat** est persistant entre les tours d'une meme session (`thread_id`).
Il peut etre **modifie** par les outils via `Command(update={...})`.

```
Tour 1 : "My favourite colour is green" → update_favourite_colour() → etat["favourite_colour"] = "green"
Tour 2 : "What's my favourite colour?"  → read_favourite_colour()   → "green"
```

- `AgentState` : classe de base LangChain pour les etats d'agents
- `CustomState(AgentState)` : etat enrichi avec le champ `favourite_colour`
- `state_schema` : parametre de `create_agent` qui declare le schema d'etat
- `Command(update={...})` : retourne une mise a jour de l'etat depuis un outil
- `runtime.state["favourite_colour"]` : lit l'etat courant depuis un outil

---

## Execution

```bash
# Parties 1-4 : Contexte
python 01_context.py

# Parties 5-6 : Etat
python 02_state.py
```

---

## Resultats attendus

### 01_context.py
```
Partie 2 : Agent sans outils de contexte
Reponse : I don't have any information about your personal preferences...

Partie 3 : Agent avec outils de contexte
Reponse (contexte defaut) : Your favourite colour is blue.

Partie 4 : Changement de contexte
Reponse (favourite_colour=green) : Your favourite colour is green.
```

### 02_state.py
```
Partie 6a : Agent qui modifie l'etat
Reponse : Successfully updated your favourite colour to green!
Etat favourite_colour : green

Partie 6b : Agent qui lit l'etat
[Etape 1] Mise a jour de l'etat...
Reponse : Successfully updated your favourite colour to green!
[Etape 2] Lecture de l'etat...
Reponse : Your favourite colour is green!
```
