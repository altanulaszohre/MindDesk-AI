import sys
from PyQt6.QtWidgets import QApplication
from ui.app_window import AppWindow

from core.chat_engine import ChatEngine
from core.summarizer import Summarizer
from core.voice_input import VoiceInput
from core.voice_output import VoiceOutput


def main():
    app = QApplication(sys.argv)

    chat_engine = ChatEngine()
    summarizer = Summarizer()
    voice_input = VoiceInput(language="en-US")
    voice_output = VoiceOutput(voice_gender="female", language="en")

    window = AppWindow(
        chat_engine=chat_engine,
        voice_input=voice_input,
        voice_output=voice_output
    )

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
