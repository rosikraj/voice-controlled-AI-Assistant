# 🗣️ Voice-Controlled AI Assistant for Turbify

This project is a **voice-controlled desktop assistant** that helps users navigate and interact with the **Turbify website** using just voice commands.

We used only **free, open-source tools** to build this:

- 🗣️ `SpeechRecognition` – Captures and converts your voice to text  
- 🧠 Rule-based NLP – Understands your intent from speech  
- 🌐 `Playwright` – Automates interactions with the Turbify website  
- 🔊 `pyttsx3` – Speaks back responses using offline text-to-speech  
- 🖥️ `Tkinter` – GUI for the desktop app  

> ✅ Everything runs **locally and offline**  
> 💸 **No API keys**, **no costs**, and **no usage limits**

---

## ⚙️ Getting Started

### 🔹 1. Install Python 3.10

Make sure you're using **Python 3.10.x** (not 3.11+ due to compatibility with some dependencies).-python-3.10.0-amd64.exe

---

### 🔹 2. Install Dependencies

After cloning the repo:

**bash**
cd backend
pip install -r requirements.txt

**To start the voice assistant:**
cd backend
python ui.py
