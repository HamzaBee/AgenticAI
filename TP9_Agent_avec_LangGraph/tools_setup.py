import os
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

model = None

try:
    from langchain_ollama import ChatOllama
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    model = ChatOllama(model=ollama_model, temperature=0)
except Exception as e:
    print(f"[Warning] ChatOllama failed to initialize: {e}")

if model is None and os.getenv("GROQ_API_KEY"):
    try:
        from langchain_groq import ChatGroq
        model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        print("[Info] Fallback to ChatGroq successful.")
    except Exception as e:
        print(f"[Warning] ChatGroq failed to initialize: {e}")

if model is None and os.getenv("OPENAI_API_KEY"):
    try:
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        print("[Info] Fallback to ChatOpenAI successful.")
    except Exception as e:
        print(f"[Warning] ChatOpenAI failed to initialize: {e}")

if model is None:
    raise RuntimeError("No LLM model could be initialized. Please run Ollama or set API keys in .env.")

@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """Divide two integers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

tools = [add, multiply, divide]
tools_by_name = {t.name: t for t in tools}
model_with_tools = model.bind_tools(tools)

if __name__ == "__main__":
    print(f"LLM initialized: {model.__class__.__name__}")
    print(f"Tools available: {list(tools_by_name.keys())}")
    test_res = model_with_tools.invoke("What is 3 times 4?")
    print("Test Invoke Tool Calls:", getattr(test_res, "tool_calls", None))
