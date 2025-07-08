import threading
import time
import tkinter as tk
from tkinter import scrolledtext

from automation import TurbifyAutomation
from nlp_handler import extract_intent
from speech_handler import listen_for_speech
from tts import speak_response


class VoiceAssistantUI:
    """Tkinter‑based GUI wrapper around TurbifyAutomation with voice I/O."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Turbify Voice Assistant")
        self.root.geometry("520x420")

        # --- Widgets -------------------------------------------------------
        self.history = scrolledtext.ScrolledText(
            self.root, width=62, height=18, state=tk.DISABLED
        )
        self.history.pack(pady=10)

        self.mic_btn = tk.Button(
            self.root, text="🎤 Start Listening", width=20, command=self.toggle_listening
        )
        self.mic_btn.pack()

        self.exit_btn = tk.Button(self.root, text="Quit", width=10, command=self.on_close)
        self.exit_btn.pack(pady=6)

        # --- Runtime state --------------------------------------------------
        self.listening: bool = False
        self.automation = TurbifyAutomation(headless=False)
        self.listener_thread: threading.Thread | None = None

        # Introduce assistant on launch
        self.introduce_assistant()

        # Close‑button handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------------------------------------------------------------
    # Utility helpers
    # ---------------------------------------------------------------------

    def introduce_assistant(self) -> None:
        """Display and speak a short intro explaining the assistant."""
        intro_text = (
            "👋 Welcome to the Turbify Voice Assistant!\n"
            "Here’s what I can do for you:\n"
            " • Search a domain – say something like 'search example.com'\n"
            " • Spell out a domain – say 'spell e x a m p l e dot com'\n"
            " • Go to the hosting or domains section – just say 'hosting' or 'domains'\n"
            " • Exit the application – say 'exit'\n\n"
            "🟢 Click 'Start Listening' below to begin."
        )
        self.log(intro_text)
        speak_response(
            "Welcome to the Turbify Voice Assistant. "
            "You can ask me to search for domain names, spell them out, or navigate to the hosting page. "
            "Click the Start Listening button whenever you're ready to begin."
        )

    def log(self, text: str) -> None:
        """Append a line to the scroll‑back history."""
        self.history.configure(state=tk.NORMAL)
        self.history.insert(tk.END, text + "\n")
        self.history.see(tk.END)
        self.history.configure(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # Voice listening lifecycle
    # ------------------------------------------------------------------

    def toggle_listening(self) -> None:
        """Start/stop the background speech‑recognition thread."""
        if not self.listening:
            self.listening = True
            self.mic_btn.config(text="⏸️ Stop Listening")
            self.listener_thread = threading.Thread(target=self.listen_loop, daemon=True)
            self.listener_thread.start()
        else:
            self.listening = False
            self.mic_btn.config(text="🎤 Start Listening")

    def listen_loop(self) -> None:
        """Background loop: wait for speech and dispatch on the Tk event loop."""
        while self.listening and self.root.winfo_exists():
            cmd = listen_for_speech()
            if not cmd:
                continue
            self.root.after(0, self.handle_command, cmd)
            time.sleep(0.5)

    # ------------------------------------------------------------------
    # Command parsing helpers
    # ------------------------------------------------------------------

    @staticmethod
    def extract_domain(cmd: str) -> str:
        spoken = cmd.lower().replace("dot", ".").replace(" ", "")
        domain = spoken.split("search")[-1].strip()
        if "." not in domain:
            domain += ".com"
        return domain

    @staticmethod
    def extract_spelled_domain(cmd: str) -> str:
        letters = cmd.lower().replace("spell", "").replace("dot", ".").split()
        return "".join(letters)

    # ------------------------------------------------------------------
    # Intent handling
    # ------------------------------------------------------------------

    def handle_command(self, cmd: str) -> None:
        self.log(f"🗨️ You: {cmd}")
        intent = extract_intent(cmd)
        self.log(f"🤖 Intent: {intent}")

        try:
            domain: str | None = None
            if cmd.lower().startswith("spell"):
                domain = self.extract_spelled_domain(cmd)
                self.log(f"🔡 Spelled domain: {domain}")
                speak_response(f"You spelled: {domain}. Searching now.")
            elif intent == "search":
                domain = self.extract_domain(cmd)
                speak_response(f"Searching {domain}")

            if domain:
                result = self.automation.search_domain(domain)
                speak_response(result)
                self.log(f"✅ {result}")
            elif intent == "navigate":
                target = "web hosting" if "hosting" in cmd.lower() else "domains"
                speak_response(f"Navigating to {target}")
                result = self.automation.navigate_to(target)
                self.log(f"➡️ {result}")
                speak_response(result)
            elif intent == "greet":
                speak_response("Hello there! How can I assist you?")
                self.log("👋 Hello!")
            elif intent == "exit":
                speak_response("Goodbye!")
                self.on_close()
            else:
                speak_response("Sorry, I didn't understand that.")
                self.log("❓ Unknown intent.")
        except Exception as e:
            self.log(f"❌ Error: {e}")
            speak_response("Something went wrong.")

    # ------------------------------------------------------------------
    # Shutdown and cleanup
    # ------------------------------------------------------------------

    def on_close(self) -> None:
        self.listening = False
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=2)
        self.automation.close()
        self.root.destroy()


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = VoiceAssistantUI(tk_root)
    tk_root.mainloop()
