"""
Voice input via the microphone.

Fix vs. the original: the original called `voice_to_text()` at module
import time (`user_answer = voice_to_text()` at the bottom of the file).
That means just importing this module triggered the microphone -- a nasty
surprise for any other code that imports the package. Now it only runs
when you explicitly call `voice_to_text()`.
"""

import speech_recognition as sr


def voice_to_text() -> str:
    """Listen on the default microphone and return the recognized text.

    Returns "" if nothing could be understood or the service failed,
    instead of raising, so callers can handle a no-answer case cleanly.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Speech recognition service error:", e)
        return ""


if __name__ == "__main__":
    # Manual test: `python -m ai_model.voice.input_voice`
    print("Answer:", voice_to_text())
