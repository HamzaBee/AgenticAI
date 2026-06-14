# 👨‍🍳 TP Agents avec LangGraph — SDIA

Ce projet implémente un **Agent Chef Personnel** capable de proposer des recettes basées sur les ingrédients disponibles, tout en mémorisant les préférences de l'utilisateur et en effectuant des recherches web si nécessaire.

---

### 📂 Structure du Labo

- **`01_simple_agent.py`** : Création d'un agent de base.
- **`02_system_message_agent.py`** : Utilisation d'un System Message pour définir le comportement.
- **`03_few_shot_agent.py`** : Apprentissage par l'exemple (Few-shot).
- **`04_structured_response_agent.py`** : Formatage de la sortie via le prompt.
- **`05_basemodel_response_agent.py`** : Sortie structurée avec Pydantic.
- **`06_tools_agent.py`** : Utilisation d'outils personnalisés (Tools).
- **`07_web_search_agent.py`** : Intégration de la recherche web avec Tavily.
- **`08_memory_agent.py`** : Gestion de la mémoire de conversation.
- **`chef_personnel_agent.py`** : Script principal combinant tous les concepts pour le TP.
- **`requirements.txt`** : Liste des dépendances nécessaires.
- **`.env.example`** : Modèle de configuration pour les variables d'environnement.

---

### ⚙️ Installation

1.  **Installation des dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

---

### 🔑 Configuration

Créez un fichier `.env` à partir de `.env.example` :
```bash
OLLAMA_MODEL=llama3.2:3b
TAVILY_API_KEY=your_api_key
APP_MODE=interactive
OLLAMA_TEMPERATURE=0
```

---

### 🚀 Exécution

- **Mode interactif (par défaut) :**
  ```bash
  python chef_personnel_agent.py
  ```

- **Mode démo :**
  ```bash
  APP_MODE=demo python chef_personnel_agent.py
  ```
