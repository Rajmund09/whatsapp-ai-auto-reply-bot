import os
from groq import Groq
from dotenv import load_dotenv

# Try with existing env var first
key_env = os.environ.get("GROQ_API_KEY")
print(f"Testing key from shell environment: {key_env[:10]}...{key_env[-4:] if key_env else ''}")
client_env = Groq(api_key=key_env)
try:
    client_env.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=5
    )
    print("Success with shell key!")
except Exception as e:
    print(f"Failed with shell key: {e}")

# Try loading from .env and forcing override
load_dotenv(override=True)
key_file = os.getenv("GROQ_API_KEY")
print(f"\nTesting key from .env file: {key_file[:10]}...{key_file[-4:] if key_file else ''}")
client_file = Groq(api_key=key_file)
try:
    client_file.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=5
    )
    print("Success with .env key!")
except Exception as e:
    print(f"Failed with .env key: {e}")
