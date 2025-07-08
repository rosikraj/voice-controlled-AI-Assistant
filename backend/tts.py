import pyttsx3

_engine = pyttsx3.init()
_engine.setProperty("rate", 150)  # speech speed


def speak_response(text: str) -> None:
    """Non‑blocking TTS helper."""
    _engine.say(text)
    _engine.runAndWait()
