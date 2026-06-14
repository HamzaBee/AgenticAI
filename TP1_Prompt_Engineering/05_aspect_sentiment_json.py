from langchain_ollama import ChatOllama
import json
import os
from dotenv import load_dotenv

load_dotenv()

system_message = """
Effectuez une analyse de sentiments basée sur les aspects des avis concernant
les ordinateurs portables présentés en entrée.
Chaque avis peut comporter un ou plusieurs des aspects suivants : screen, keyboard et pad.
Pour chaque avis présenté en entrée :
- Identifiez la présence d'au moins un des trois aspects (screen, keyboard, pad).
- Attribuez une polarité de sentiment (positive, negative ou neutral) à chaque
aspect. Organisez votre réponse dans un objet JSON avec les en-têtes suivants :
- category:[liste des aspects]
- polarity:[liste des polarités correspondantes pour chaque aspect] Si
l'un des aspects n'est pas présent dans l'avis de l'utilisateur, tu supposes que la polarité est neutre
"""

model_name = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
llm = ChatOllama(
    model=model_name,
    format="json",
    temperature=0
)

user_review = "L'écran est très bon, mais je n'ai pas aimé la souris. le clavier Ma fih Maytchaf"

resp = llm.invoke([
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_review}
])

print("Response Content (JSON):")
print(resp.content)

try:
    result = json.loads(resp.content)
    print(f"\nDetected Categories: {result.get('category')}")
    print(f"Detected Polarity: {result.get('polarity')}")
except Exception as e:
    print(f"JSON Parsing Error: {e}")
