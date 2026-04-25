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

# Bot Persona
BOT_NAME = "Aryan" # You can change this to your preferred name

# =========================
# GROQ CLIENT SETUP
# =========================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
    system_prompt = (
        f"You are {BOT_NAME}, a friendly and helpful guy from Odisha. "
        "You are responding to messages on WhatsApp. "
        "Talk like a real friend—natural, casual, and relatable. "
        "Use a mix of simple English and Odia if it feels natural, or just English if the user is using it. "
        "Keep replies short and concise (1-2 lines), like a real chat. "
        "The chat history provided includes names and timestamps in various formats. "
        "Ignore the formatting and focus on the latest message and the overall context. "
        "IMPORTANT: Do NOT include your name or timestamps in your reply. "
        "Just give the direct message text."
    )
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the recent chat history:\n\n{chat_history}\n\nPlease provide a natural reply to the last message."}
            ],
            temperature=0.8,
            max_tokens=150
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting AI reply: {e}")
        return ""

# =========================
# BOT SELF-MESSAGE CHECK
# =========================
def is_own_last_message(chat_text):
    global last_bot_reply
    if not last_bot_reply:
        return False
    
    # Clean up both for comparison
    clean_chat = chat_text.strip().lower()
    clean_reply = last_bot_reply.strip().lower()
    
    # Check if the chat ends with our reply (ignoring minor variations)
    return clean_reply in clean_chat[-len(clean_reply)-10:]

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
    if reply:
        last_bot_reply = reply   # ✅ STORE BOT REPLY
        
        # Simulate typing time
        typing_delay = len(reply) * 0.05 + 1 # 0.05s per char + 1s base
        typing_time = min(max(typing_delay, 1), 4) # between 1 and 4 seconds
        print(f"Simulating typing for {typing_time:.1f}s...")
        time.sleep(typing_time)
        
        send_message(reply)
