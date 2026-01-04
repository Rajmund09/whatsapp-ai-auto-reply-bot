from groq import Groq
import os

from streamlit import chat_message

# Make sure GROQ_API_KEY is set in environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": (
    "You are person, a normal guy from  Odisha. "
    "You speak ONLY one language per reply: "
    "either simple English,  English. "
    "Do NOT mix languages in one sentence. "
    "If unsure which language to use, reply in simple english. "
    "Talk like a real friend, very natural and casual. "
    "Keep replies short (1–2 lines). "
    "Reply ONLY to the last message."
)

                   },
        {
            "role": "user",
            "content": chat_message
        }
    ],
    temperature=0.7,
    max_tokens=120
)

print(completion.choices[0].message.content)

  