import pyttsx3


class VoiceOutput:
    def __init__(self, voice_gender="female", language="en"):
        self.engine = pyttsx3.init()
        self.voice_gender = voice_gender
        self.language = language
        self.set_voice()

    def set_voice(self):
        voices = self.engine.getProperty("voices")
        selected_voice = None

        for voice in voices:
            # Bazı sistemlerde languages listesi boş olabilir
            lang_match = False
            if hasattr(voice, "languages") and voice.languages:
                try:
                    lang_match = self.language in voice.languages[0].decode("utf-8").lower()
                except Exception:
                    lang_match = False

            # Eğer dil eşleşmiyorsa yine de gender'e bak
            if lang_match or self.language in voice.name.lower():
                if self.voice_gender == "female" and "female" in voice.name.lower():
                    selected_voice = voice
                    break
                elif self.voice_gender == "male" and "male" in voice.name.lower():
                    selected_voice = voice
                    break

        if selected_voice:
            self.engine.setProperty("voice", selected_voice.id)
        else:
            print("⚠️ Using default system voice.")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
