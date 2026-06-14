import base64
import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

path = "rag.png"
model_name = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

if os.path.exists(path):
    print(f"Analyzing image '{path}' with model {model_name}...")
    img_base64 = encode_image(path)
    
    # Note: Ensure you have a vision-capable model pulled in Ollama (e.g., llama3.2-vision)
    llm_vision = ChatOllama(model=model_name)
    
    resp_vision = llm_vision.invoke([
        HumanMessage(content=[
            {"type": "text", "text": "Qu'est ce que tu vois dans cette image?"},
            {"type": "image_url", "image_url": f"data:image/png;base64,{img_base64}"}
        ])
    ])
    
    print("\nDescription:")
    print(resp_vision.content)
else:
    print(f"File '{path}' not found. Please place an image named 'rag.png' in the current directory.")
