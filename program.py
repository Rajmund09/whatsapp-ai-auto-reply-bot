import pyautogui
import time
import pyperclip
import os
from groq import Groq

# =========================
# CONFIGURATION
# =========================
CHECK_INTERVAL = 5

WHATSAPP_ICON = (910, 1168)
CHAT_DRAG_START = (694, 212)
CHAT_DRAG_END = (1161, 1114)
CLICK_OUTSIDE = (1013, 1093)
MESSAGE_BOX = (1013, 1093)
SEND_BUTTON = (1873, 1089)

# =========================
# GROQ CLIENT SETUP
# =========================
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# CHAT CHANGE DETECTION
# =========================
last_chat_snapshot = ""
last_bot_reply = ""   # ✅ ADDED

def has_new_message(current_chat):
    global last_chat_snapshot
    if current_chat != last_chat_snapshot:
        last_chat_snapshot = current_chat
        return True
    return False

# =========================
# UTIL FUNCTIONS
# =========================
def copy_chat_history():
    pyautogui.moveTo(*CHAT_DRAG_START)
    pyautogui.dragTo(*CHAT_DRAG_END, duration=1.5, button='left')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    pyautogui.click(*CLICK_OUTSIDE)
    return pyperclip.paste()

def send_message(text):
    pyperclip.copy(text)
    pyautogui.click(*MESSAGE_BOX)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    pyautogui.click(*SEND_BUTTON)

def get_ai_reply(chat_history):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
               "content": (
    "You are person, a normal guy from , Odisha. "
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
                "content": chat_history
            }
        ],
        temperature=0.7,
        max_tokens=120
    )
    return completion.choices[0].message.content.strip()

# =========================
# BOT SELF-MESSAGE CHECK
# =========================
def is_own_last_message(chat_text):
    global last_bot_reply
    if not last_bot_reply:
        return False
    return chat_text.strip().endswith(last_bot_reply.strip())

# =========================
# OPEN WHATSAPP
# =========================
pyautogui.click(*WHATSAPP_ICON)
time.sleep(2)

# =========================
# MAIN LOOP
# =========================
while True:
    time.sleep(CHECK_INTERVAL)

    chat_history = copy_chat_history()
    print(chat_history)

    if not has_new_message(chat_history):
        continue

    # 🚫 Ignore if last message is bot's own reply
    if is_own_last_message(chat_history):
        continue

    reply = get_ai_reply(chat_history)
    last_bot_reply = reply   # ✅ STORE BOT REPLY
    send_message(reply)
