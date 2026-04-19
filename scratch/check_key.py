import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GROQ_API_KEY")
if key:
    print(f"Key found. Length: {len(key)}")
    print(f"Starts with: {key[:4]}")
    print(f"Ends with: {key[-4:]}")
else:
    print("GROQ_API_KEY not found in environment.")
