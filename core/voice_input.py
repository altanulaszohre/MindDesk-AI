import speech_recognition as sr


class VoiceInput:
    def __init__(self, language="en-US"):
        self.recognizer = sr.Recognizer()
        self.language = language

    def listen(self, timeout=5):
        with sr.Microphone() as source:
            print("🔊 Listening... Please speak.")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio, language=self.language)
                print(f"🗣️ Recognized: {text}")
                return text
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand you."
            except sr.RequestError:
                return "Speech recognition service is not available."
            except sr.WaitTimeoutError:
                return "No speech detected. Try again."
