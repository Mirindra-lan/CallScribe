from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser
from PySide6.QtCore import Signal
from gui.signal import UiSignal

class VoskGui(QWidget):
    def __init__(self, signal: UiSignal):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.signals = signal
        self.resize(600,400)
        self.setWindowTitle("Transciption avec vosk")

        self.titre = QLabel("Titre")
        self.signals.voskTitre.connect(self.setTitre)

        self.partial = QTextBrowser()
        self.signals.voskPart.connect(self.setPart)
        self.finalRes = QTextBrowser()
        self.signals.voskRes.connect(self.setRes)

        self.main_layout.addWidget(self.titre)
        self.main_layout.addWidget(self.partial)
        self.main_layout.addWidget(self.finalRes)


        self.setLayout(self.main_layout)

    def setTitre(self, text):
        if text:
            self.titre.setText(text)

    def setPart(self, text):
        if text:
            self.partial.setText(text)
    
    def setRes(self, text):
        if text:
            self.finalRes.setText(text)