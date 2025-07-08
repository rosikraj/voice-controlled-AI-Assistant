import speech_recognition as sr


def listen_for_speech(timeout: int = 5, phrase_time_limit: int = 8) -> str:
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8
    recognizer.energy_threshold = 300
    with sr.Microphone() as source:
        print("🎙️  Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"📝  Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("🤔  Could not understand the audio.")
    except sr.RequestError as e:
        print(f"🚫  Speech service error: {e}")
    return ""
