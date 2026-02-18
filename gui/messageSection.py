from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout
from PySide6.QtCore import Qt
from gui.bullMessage import BullMessage

class MessageSection(QWidget):
    def __init__(self):
        super().__init__()
        self.toggle = False
        self.main_layout = QVBoxLayout(self)

        self.main_scroll = QScrollArea()
        self.main_scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.scroll_layout = QVBoxLayout(self.container)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.main_scroll.setWidget(self.container)

        self.main_layout.addWidget(self.main_scroll)

    def newMessage(self, text, isUser: bool):
        layout = QHBoxLayout()
        if isUser:
            message = BullMessage(self.container, text,"#0A0A55")
            layout.addStretch(3)
            layout.addWidget(message, 7)
        else:
            message = BullMessage(self.container, text)
            layout.addWidget(message, 7)
            layout.addStretch(3)
        self.scroll

    def addMessage(self, value):
        self.toggle = not self.toggle
        self.newMessage(value, self.toggle)