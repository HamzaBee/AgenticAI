# 🔍 Lab3-RAG — RAG et Agents SQL

Ce projet explore l'utilisation des agents pour interroger des sources de données non structurées (PDF via RAG) et structurées (SQL).

---

### 📂 Structure du Labo

- **`part1_rag_pdf.py`** : Implémentation d'un agent RAG (Retrieval-Augmented Generation). Il découpe le manuel de l'employé en chunks, les transforme en vecteurs sémantiques avec Hugging Face, et permet à l'IA de répondre à des questions basées sur ce document.
- **`part2_sql_agent.py`** : Agent expert en SQL capable de traduire des questions en langage naturel en requêtes SQL pour interroger la base de données `Chinook.db`.
- **`acmecorp-employee-handbook.pdf`** : Le document source pour la partie RAG.
- **`Chinook.db`** : Base de données SQLite d'exemple (musique).

---

### ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

### 🚀 Exécution

1.  **Agent RAG (PDF) :**
    ```bash
    python part1_rag_pdf.py
    ```

2.  **Agent SQL :**
    ```bash
    python part2_sql_agent.py
    ```

---

\*Réalisé dans le cadre du Master SDIA
