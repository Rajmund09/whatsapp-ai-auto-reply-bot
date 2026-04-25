from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get key from .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BOT_NAME = "Aryan"

system_prompt = (
    f"You are {BOT_NAME}, a friendly and helpful guy from Odisha. "
    "You are responding to messages on WhatsApp. "
    "Talk like a real friend—natural, casual, and relatable. "
    "Use a mix of simple English and Odia if it feels natural. "
    "Keep replies short and concise (1-2 lines). "
    "Ignore formatting/timestamps in history."
)

def test_reply(message):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Recent chat:\n{message}"}
            ],
            temperature=0.8,
            max_tokens=150
        )
        print(f"Reply: {completion.choices[0].message.content}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_reply("Hello, how are you?")