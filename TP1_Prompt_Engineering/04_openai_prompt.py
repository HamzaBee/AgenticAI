from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "your_openai_key_here":
    print("Error: Please set a valid OPENAI_API_KEY in the .env file.")
else:
    llm = ChatOpenAI(model="gpt-4o", api_key=api_key)

    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "C'est quoi un Agent AI"}
    ])

    print("\nResponse from OpenAI:")
    print(response.content)
