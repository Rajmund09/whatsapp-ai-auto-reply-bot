import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(override=True)

# Get key from .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BOT_NAME = "Aryan"

system_prompt = (
    f"You are {BOT_NAME}, a real human friend. "
    "Talk like a normal person on WhatsApp—casual, relaxed, and relatable. "
    "Use simple English, and if you know any Hindi or Odia, mix it in naturally like friends do. "
    "Keep replies very short and punchy (max 1-2 lines). "
    "NEVER mention you are an AI, an assistant, or a language model. "
    "Do not be overly helpful or formal. Just be a guy chatting with his friends."
)

def test_reply(message):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Recent chat:\n{message}"}
            ],
            temperature=0.85,
            max_tokens=150
        )
        print(f"Reply: {completion.choices[0].message.content}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_reply("Hello, how are you?")