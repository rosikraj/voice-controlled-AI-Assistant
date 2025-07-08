from speech_handler import listen_for_speech
from nlp_handler import extract_intent
from automation import TurbifyAutomation
from tts import speak_response
import time


def handle_speech_command(command: str, automation: TurbifyAutomation) -> bool:
    intent = extract_intent(command)
    print(f"🔎 Detected intent: {intent}")

    if intent == "search":
        words = command.split()
        # heuristic: last "wordish" token
        domain = next((w for w in reversed(words) if "." in w or w.isalpha()), words[-1])
        if "." not in domain:
            domain += ".com"
        speak_response(f"Searching domain {domain}")
        result = automation.search_domain(domain)
        speak_response(f"Result: {result}")
        print(result)

    elif intent == "navigate":
        target = "web hosting" if "hosting" in command.lower() else "domains"
        msg = automation.navigate_to(target)
        speak_response(msg)

    elif intent == "greet":
        speak_response("Hello there! How can I assist you?")

    elif intent == "exit":
        speak_response("Good‑bye!")
        return False

    else:
        speak_response("Sorry, I didn't understand that.")
    return True


def main() -> None:
    print("🚀  Turbify Voice Assistant (CLI)")
    automation = TurbifyAutomation()
    try:
        while True:
            cmd = listen_for_speech()
            if cmd and not handle_speech_command(cmd, automation):
                break
            time.sleep(1)
    finally:
        automation.close()


if __name__ == "__main__":
    main()
