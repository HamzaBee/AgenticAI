from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key or api_key == "your_groq_key_here":
    print("Error: Please set a valid GROQ_API_KEY in the .env file.")
else:
    llm = ChatGroq(model="llama3-8b-8192", groq_api_key=api_key)

    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "C'est quoi un Agent AI"}
    ])

    print("\nResponse from Groq:")
    print(response.content)
