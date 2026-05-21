# WhatsApp AI Auto-Reply Bot 🤖💬

A vision-powered, context-aware desktop automation bot that automatically reads and replies to WhatsApp messages. Built using **Python**, **Groq Cloud APIs (Vision & Text LLMs)**, and **PyAutoGUI** desktop automation.

The bot acts as a real human friend, utilizing computer vision to read incoming messages directly from your screen and typing natural replies.

---

## 🚀 Key Features

- **👁️ Vision-Based Message Reading**: Uses Groq's Vision LLM (`meta-llama/llama-4-scout-17b-16e-instruct`) to analyze screenshots of the WhatsApp chat window, dynamically detecting and parsing the last incoming message. No WhatsApp API or browser automation library (like Selenium/Puppeteer) is required!
- **⚡ Visual Hashing (API Optimization)**: Computes MD5 hashes of the chat window capture. It only contacts the Vision API when a visual change is detected, saving API tokens and reducing network overhead.
- **🗣️ Natural & Context-Aware Conversational AI**: Powered by Groq's `llama-3.3-70b-versatile` model. It maintains a short chat context (remembers its own previous reply), talks in casual Hinglish/English/Odia, and adopts a customizable human persona (defaults to **"Aryan"**). It is designed to match authentic texting behaviors (lowercase, no ending periods, slang).
- **🗔 Automated Window Focus**: Automatically searches for, restores, and activates the official WhatsApp desktop window before executing actions.
- **⌨️ Instant Clipboard Injection**: Copies generated replies directly to the clipboard (`pyperclip`) and pastes them (`ctrl + v`), ensuring fast, reliable delivery and avoiding slow keystroke simulation.

---

## 🛠️ Tech Stack

- **Core**: Python 3.x
- **LLM Provider**: Groq API
  - **Vision Model**: `meta-llama/llama-4-scout-17b-16e-instruct` (extracts text from screenshot)
  - **Chat Model**: `llama-3.3-70b-versatile` (generates the response)
- **GUI & Screen Capture**:
  - `mss` (Ultra-fast screenshotting library)
  - `PyGetWindow` (Window focus and size control)
  - `pyautogui` (Clicking and pasting keyboard shortcuts)
  - `pyperclip` (System clipboard management)
  - `Pillow` (Image preprocessing and scaling)

---

## ⚙️ Configuration & Environment Variables

Create a `.env` file in the root directory of the project. Here are the variables you can configure:

| Variable | Description | Default Value |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | **(Required)** Your Groq API Key | *None* |
| `BOT_NAME` | The persona/name the bot will adopt | `Aryan` |

> [!TIP]
> You can also adjust advanced configuration options directly in the top section of `program.py`, such as:
> - `CHECK_INTERVAL`: How often the bot scans for changes (default: `5` seconds).
> - `VISION_MODEL`: The multimodal model used to read messages.
> - Chat area offsets (`CHAT_AREA_LEFT`, `CHAT_AREA_TOP`, etc.) to match your layout.

---

## 💬 Prompt Design & Texting Behavior

The bot features a highly optimized system prompt that instructs the LLM to behave like a real human friend rather than an AI assistant. Key rules include:
- **Texting Style**: Writes in mostly lowercase and avoids ending periods (`.`) which typically make replies look robotic or passive-aggressive.
- **Tone**: A relaxed, lazy, and sometimes dry college-student vibe.
- **Multilingual (Hinglish/Odia)**: Automatically responds in natural Hinglish (conversational Hindi mixed with English) or simple English. It also handles local language inputs like Odia (e.g., matching Odia queries like *"kan chalichi"* with natural Odia responses).
- **Anti-Helper Behavior**: Refuses technical utility tasks (like writing code or essays) lazily (e.g., *"bhai google krle na 😂"*).
- **Active AI Denial**: Will humorously deny being an AI or robot if asked.

---

## 📥 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/whatsapp-ai-auto-reply-bot.git
cd whatsapp-ai-auto-reply-bot
```

### 2️⃣ Install Dependencies
Make sure you have Python installed, then install the required packages:
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Create a file named `.env` in the root folder and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
BOT_NAME=Aryan
```

### 4️⃣ Start the Bot
Run the program. The bot will automatically search for your WhatsApp window and start listening for messages:
```bash
python program.py
```

---

## ⚠️ Important Considerations & Limitations

> [!WARNING]
> **Windows Scaling & Coordinates**:
> The bot relies on relative offsets of the WhatsApp window to crop the chat area and click the input field. If your OS has display scaling enabled (e.g., 125% or 150%), or if you use a customized layout, you may need to adjust the relative coordinate factors (`CHAT_AREA_LEFT`, etc.) or the click offsets in `program.py`.

> [!IMPORTANT]
> - Keep the WhatsApp window visible and not obscured by other windows when the bot is running.
> - To avoid loop issues, the bot automatically ignores messages if the last sender is identified as the bot itself (`BOT_NAME` or `You`).
> - Use this bot responsibly. Automated messaging may violate WhatsApp's terms of service if misused.

---

## 👤 Author

**Raj**
- BCA Student | Python & Automation Enthusiast
- From Kalahandi, Odisha 🇮🇳
