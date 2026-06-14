from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "your_openai_key_here":
    print("Error: Please set a valid OPENAI_API_KEY in the .env file.")
else:
    client = OpenAI(api_key=api_key)

    print("Generating image...")
    response = client.images.generate(
        model="dall-e-3",
        prompt="Je veux une photo d'un chat qui code du java",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    print(f"Image generated! URL: {image_url}")
    print("Note: In a local script, you can open this URL in your browser.")
