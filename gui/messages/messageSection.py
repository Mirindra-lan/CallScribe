from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from gui.messages.bullMessage import BullMessage
from PySide6.QtCore import Qt

class MessageSec(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        self.scrollBox = QScrollArea()
        self.scrollBox.setWidgetResizable(True)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)
        # self.container.setMinimumHeight(int(self.height()))
        # self.container.setMinimumWidth(int(self.width()))
        self.scrollBox.setWidget(self.container)

        self.main_layout.addWidget(self.scrollBox)

        self.addMessage("""
            Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.
        """, True)
        self.addMessage("""
            Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.
        """, False)
        self.addMessage("""
            Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.
        """, True)
        self.addMessageScroll("""
            Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.
        """, True)
        self.addMessageScroll("""
            Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.
        """, False)
        self.addMessageScroll("""
            Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.Ceci est un texte long qui doit créer
            une bulle avec une largeur de 70%
            et une hauteur adaptée automatiquement.
        """, True)

        self.main_layout.addStretch()

    def addMessage(self, text, isUser: bool):
        layout = QHBoxLayout()
        if isUser:
            message = BullMessage(self, text,"#0A0A55")
            layout.addStretch(3)
            layout.addWidget(message, 7)
        else:
            message = BullMessage(self, text)
            layout.addWidget(message, 7)
            layout.addStretch(3)
        self.main_layout.addLayout(layout)


    def addMessageScroll(self, text, isUser: bool):
        container = QWidget()
        layout = QHBoxLayout(container)

        if isUser:
            message = BullMessage(self.container, text,"#0A0A55")
            layout.addStretch(3)
            layout.addWidget(message, 7)
        else:
            message = BullMessage(self.container, text)
            layout.addWidget(message, 7)
            layout.addStretch(3)

        self.container_layout.addLayout(layout)
        # self.container_layout.addWidget(container)

        self.scrollBox.verticalScrollBar().setValue(
            self.scrollBox.verticalScrollBar().maximum()
        )