from langchain_ollama import ChatOllama
from IPython.display import Markdown
import os
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
print(f"Running local model {model_name}...")
llm = ChatOllama(model=model_name)

response = llm.invoke([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "C'est quoi un Agent AI"}
])

print("\nResponse:")
print(response.content)
