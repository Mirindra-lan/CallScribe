from PySide6.QtWidgets import (QTextBrowser, QLabel)
from PySide6.QtCore import Qt
import sys


class ChatBubble(QLabel):
    def __init__(self, text, is_user=False):
        super().__init__()

        self.setText("""
            <p style="
                font-size:18px;
                padding:12px;
                background-color:#e3f2fd;
                border-radius:10px;
            ">
            ceci est un texte long
            </p>
        """)
        # self.setReadOnly(True)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # largeur max 70% écran
        self.setMaximumWidth(800)

        if is_user:
            bg_color = "#0078ff"
            align = Qt.AlignRight
        else:
            bg_color = "#2d2d2d"
            align = Qt.AlignLeft

        self.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {bg_color};
                color: white;
                border-radius: 15px;
                padding: 12px;
                border: none;
                font-size: 14px;
            }}
        """)

        self.setAlignment(align)
