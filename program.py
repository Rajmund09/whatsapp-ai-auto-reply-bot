import pyautogui
import time
import pyperclip
import os
import re
import hashlib
import pygetwindow as gw
import base64
import io
from groq import Groq
from dotenv import load_dotenv
from PIL import Image, ImageChops
import mss

# =========================
# CONFIGURATION
# =========================
load_dotenv(override=True)

CHECK_INTERVAL = 5  # Vision-based check
BOT_NAME = os.getenv("BOT_NAME", "Aryan")
WHATSAPP_TITLE = "WhatsApp" 
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# Relative Offsets (Chat area)
CHAT_AREA_LEFT = 0.35
CHAT_AREA_TOP = 0.1
CHAT_AREA_RIGHT = 0.98
CHAT_AREA_BOTTOM = 0.85

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# STATE MANAGEMENT
# =========================
last_screenshot_hash = ""
last_replied_msg = ""

def get_image_hash(img):
    """Generates a simple hash for an image to detect changes."""
    return hashlib.md5(img.tobytes()).hexdigest()

def focus_whatsapp():
    """Finds and brings the WhatsApp window to the front."""
    try:
        windows = gw.getWindowsWithTitle(WHATSAPP_TITLE)
        if not windows:
            return None
        
        win = windows[0]
        if win.isMinimized:
            win.restore()
        
        try:
            win.activate()
        except Exception:
            pass
            
        return win
    except Exception as e:
        print(f"Focusing Error: {e}")
        return None

def capture_chat_visual(win):
    """Captures the chat area visual."""
    if not win: return None
    
    try:
        # Calculate coordinates
        left = win.left + int(win.width * CHAT_AREA_LEFT)
        top = win.top + int(win.height * CHAT_AREA_TOP)
        width = int(win.width * (CHAT_AREA_RIGHT - CHAT_AREA_LEFT))
        height = int(win.height * (CHAT_AREA_BOTTOM - CHAT_AREA_TOP))
        
        # Capture screenshot
        with mss.mss() as sct:
            monitor = {"top": top, "left": left, "width": width, "height": height}
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
        # Downscale for efficiency
        img.thumbnail((600, 600))
        return img
    except Exception as e:
        print(f"Error in capture_chat_visual: {e}")
        return None

def encode_image(img):
    """Encodes a PIL image to base64."""
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=70) # Lower quality for faster upload
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_visual_update(img):
    """Uses Vision API to read the last message."""
    global last_replied_msg
    
    base64_image = encode_image(img)
    
    try:
        completion = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": f"Identify the very last message received in this WhatsApp chat. If the last message is from '{BOT_NAME}' or 'You', return 'NONE'. Otherwise, return ONLY the text of the message. Do not include timestamps or names."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            max_tokens=100
        )
        msg = completion.choices[0].message.content.strip()
        if msg.upper() == "NONE" or msg == last_replied_msg:
            return None
        return msg
    except Exception as e:
        print(f"Vision API Error: {e}")
        return None

def get_ai_reply(last_msg, bot_previous_reply=""):
    system_prompt = (
        f"You are {BOT_NAME}, a real human friend chatting on WhatsApp. "
        "Talk in a casual, relaxed, and relatable way. Use conversational English, and you can mix in a little bit of casual Hindi (Hinglish). "
        "Do NOT sound like a robot or customer service. "
        "Keep replies very short, typically just 1 sentence or a few words. "
        "NEVER mention you are an AI, a bot, or an assistant."
    )
    
    # Provide conversation context if available
    context = ""
    if bot_previous_reply:
        context = f"You recently said: '{bot_previous_reply}'\n"
        
    user_prompt = f"{context}Friend says: '{last_msg}'\n\nReply naturally to your friend:"

    try:
        completion = client.chat.completions.create(
            # Using a smarter model for much better conversational quality
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=50
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Chat API Error: {e}")
        return ""

def main():
    global last_screenshot_hash, last_replied_msg
    print(f"--- {BOT_NAME} Visual WhatsApp Bot Started ---")
    
    while True:
        try:
            win = focus_whatsapp()
            if not win:
                print("Waiting for WhatsApp...")
                time.sleep(5)
                continue
                
            img = capture_chat_visual(win)
            if not img:
                time.sleep(2)
                continue
            
            # Check for visual changes to avoid redundant API calls
            current_hash = get_image_hash(img)
            if current_hash == last_screenshot_hash:
                time.sleep(CHECK_INTERVAL)
                continue
            
            print("Visual change detected! Analyzing...")
            last_screenshot_hash = current_hash
            
            new_msg = get_visual_update(img)
            if new_msg:
                print(f"New message seen: {new_msg}")
                reply = get_ai_reply(new_msg, bot_previous_reply=last_replied_msg)
                
                if reply:
                    # Click message box to ensure focus
                    pyautogui.click(win.left + int(win.width * 0.6), win.top + int(win.height * 0.95))
                    
                    pyperclip.copy(reply)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.2)
                    pyautogui.press('enter')
                    print(f"Reply sent: {reply}")
                    
                    last_replied_msg = new_msg
                    # Wait for message to appear and update hash
                    time.sleep(2)
                    img_after = capture_chat_visual(win)
                    if img_after:
                        last_screenshot_hash = get_image_hash(img_after)
            
        except KeyboardInterrupt:
            print("Bot stopped.")
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(2)
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
