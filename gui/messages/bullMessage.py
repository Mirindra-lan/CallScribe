from PySide6.QtWidgets import QTextBrowser, QSizePolicy
from PySide6.QtCore import Qt, QEvent

class BullMessage(QTextBrowser):
    def __init__(self, parent=None, text="", color="#0A0A0A"):
        super().__init__(parent)

        self.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {color};
                border-radius: 12px;
                padding: 12px;
                border: none;
            }}
        """)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.setHtml(text)

        self.textChanged.connect(self.adjustHeight)

        self.adjustHeight()
        self.adjustWidth()
        if parent:
            parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() == QEvent.Resize:
            self.adjustHeight()
            self.adjustWidth()
        return super().eventFilter(obj, event)

    def adjustWidth(self):
        if self.parent():
            parent_width = self.parent().width()
            self.setMaximumWidth(int(parent_width * 0.7))

    def adjustHeight(self):
        doc_height = self.document().size().height()
        self.setMaximumHeight(int(doc_height))