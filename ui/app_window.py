
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QHBoxLayout, QSizePolicy, QScrollArea, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import datetime


class AppWindow(QWidget):
    def __init__(self, chat_engine, voice_input=None, voice_output=None):
        super().__init__()
        self.setWindowTitle("🧠 MindDesk AI")
        self.setMinimumSize(900, 620)
        self.setStyleSheet(self._load_styles())

        self.chat_engine = chat_engine
        self.voice_input = voice_input
        self.voice_output = voice_output

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        header = QLabel("🧠 MindDesk AI")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #7B61FF, stop:1 #00AEEF);
            color: white; padding: 16px; border-radius: 12px;
        """)
        layout.addWidget(header)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: #F4F6FC;")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.chat_container)
        layout.addWidget(self.scroll_area)

        # Input + send row
        input_row = QHBoxLayout()
        self.chat_box = QTextEdit()
        self.chat_box.setPlaceholderText("💬 Type your message...")
        self.chat_box.setFixedHeight(60)
        self.chat_box.setStyleSheet("""
            background-color: white;
            border: 1px solid #CCCCCC;
            border-radius: 12px;
            padding: 10px;
            color: #333333;
            font-size: 14px;
            font-family: 'Segoe UI';
        """)
        input_row.addWidget(self.chat_box)

        self.btn_send = self._create_button("💬 Send", "#7B61FF", self.respond)
        self.btn_send.setFixedHeight(60)
        self.btn_send.setFixedWidth(110)
        input_row.addWidget(self.btn_send)

        layout.addLayout(input_row)

        # Bottom button row
        bottom_row = QHBoxLayout()
        bottom_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_speak = self._create_button("🎙 Speak", "#4CAF50", self.listen_and_respond)
        self.btn_listen = self._create_button("🗣 Listen", "#FF9800", self.speak_last_reply)
        self.btn_file = self._create_button("📂 Load Text", "#00AEEF", self.load_file)
        self.btn_summarize = self._create_button("📝 Summarize", "#9C27B0", self.summarize_text)

        for btn in [self.btn_speak, self.btn_listen, self.btn_file, self.btn_summarize]:
            bottom_row.addWidget(btn)

        layout.addLayout(bottom_row)
        self.setLayout(layout)

    def _create_button(self, text, color, action):
        btn = QPushButton(text)
        btn.setFixedHeight(38)
        btn.setStyleSheet(f""" 
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #5555FF;
            }}
        """)
        btn.clicked.connect(action)
        return btn

    def _add_message(self, text, is_user=True):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(f""" 
            background-color: {'#E1F5FE' if is_user else '#EDE7F6'};
            border: 1px solid #CCCCCC;
            border-radius: 14px;
            padding: 10px;
            margin: 6px;
            color: #333;
        """)

        wrapper = QHBoxLayout()
        wrapper.setContentsMargins(8, 2, 8, 2)
        if is_user:
            wrapper.addStretch()
            wrapper.addWidget(label)
        else:
            wrapper.addWidget(label)
            wrapper.addStretch()

        container = QWidget()
        container.setLayout(wrapper)
        self.chat_layout.addWidget(container)

        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def respond(self):
        text = self.chat_box.toPlainText().strip()
        if text:
            self._add_message(text, is_user=True)
            reply = self.chat_engine.generate_reply(text)
            self._add_message(reply, is_user=False)
            self.chat_box.clear()
            self.last_reply = reply

    def summarize_text(self):
        text = self.chat_box.toPlainText().strip()
        if text:
            summary = f"Summary: {text[:120]}..."  # dummy
            self._add_message(summary, is_user=False)

    def listen_and_respond(self):
        if self.voice_input:
            heard = self.voice_input.listen()
            self.chat_box.setText(heard)
            self.respond()

    def speak_last_reply(self):
        if hasattr(self, 'last_reply') and self.voice_output:
            self.voice_output.speak(self.last_reply)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.chat_box.setText(f.read())

    def _load_styles(self):
        return """
        QWidget {
            background-color: #F4F6FC;
            font-family: 'Segoe UI';
            font-size: 14px;
        }

        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 10px;
            margin: 8px 0 8px 0;
        }
        QScrollBar::handle:vertical {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #9B59B6, stop:1 #8E44AD
            );
            border-radius: 6px;
            min-height: 30px;
        }
        QScrollBar::handle:vertical:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #B084D6, stop:1 #A066C9
            );
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            background: none;
            border: none;
            height: 0px;
        }
        """

