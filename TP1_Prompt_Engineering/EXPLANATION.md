# 🧠 TP Ingénierie des Prompts — SDIA

Ce projet regroupe l'ensemble des travaux pratiques réalisés pour le module **Ingénierie des Prompts**. L'objectif est d'explorer la manipulation des LLMs (locaux et cloud) à travers différentes techniques de prompting et de traitement de données.

---

### 📂 Structure du Labo

Le projet est découpé en scripts indépendants pour faciliter les tests :

- **`01_tokenisation.py`** : Analyse du découpage en tokens avec la bibliothèque `tiktoken`.
- **`02_ollama_prompt.py`** : Première interaction avec des modèles locaux via Ollama.
- **`03_groq_prompt.py`** : Utilisation de l'API Groq pour des réponses ultra-rapides.
- **`04_openai_prompt.py`** : Intégration standard avec les modèles GPT d'OpenAI.
- **`05_aspect_sentiment_json.py`** : Extraction structurée de sentiments (JSON) basée sur des aspects spécifiques.
- **`06_image_generation.py`** : Création d'images assistée par IA (DALL-E 3).
- **`07_image_description.py`** : Analyse et description d'images (Multi-modal) avec Ollama.

---

### ⚙️ Installation & Setup

Le projet utilise **`uv`** pour une gestion rapide et efficace de l'environnement virtuel.

1.  **Initialisation :**

    ```powershell
    uv venv
    uv sync
    ```

2.  **Activation :**
    - _Windows :_ `.venv\Scripts\Activate.ps1`
    - _Linux/macOS :_ `source .venv/bin/activate`

---

### 🔑 Configuration

Les clés API et paramètres du modèle sont gérés via un fichier `.env`.  
Copiez le template et remplissez vos accès :

```bash
cp .env.example .env
```

**Variables requises :**

- `OPENAI_API_KEY` : Clé secrète OpenAI.
- `GROQ_API_KEY` : Clé secrète Groq.
- `OLLAMA_MODEL` : Modèle local utilisé (défaut: `llama3.2:3b`).

---

### 🚀 Exécution

Chaque script peut être lancé individuellement depuis la racine :

```bash
python 01_tokenisation.py
python 05_aspect_sentiment_json.py
```

---

\*Réalisé dans le cadre du Master
