from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTextBrowser, QHBoxLayout
from PySide6.QtCore import Qt

class MainSection(QWidget):
    def __init__(self, sig):
        super().__init__()
        self.signal = sig
        self.toggle = False
        self.title = QLabel("Résultat de la transcription avec whisper")
        self.signal.titre.connect(self.changeTitre)

        self.send = QPushButton("Démarrer")
        self.send.clicked.connect(self.HandleChange)

        self.text = QTextBrowser()
        self.text.setText("Parole transcrite")
        self.signal.text.connect(self.showTranscription)

        self.suggestion1 = QTextBrowser()
        self.suggestion1.setText("Suggestion 1")
        
        self.suggestion2 = QTextBrowser()
        self.suggestion2.setText("Suggestion 2")
        
        self.suggestion3 = QTextBrowser()
        self.suggestion3.setText("Suggestion 3")
        
        self.suggestion4 = QTextBrowser()
        self.suggestion4.setText("Suggestion 4")

        suggestionTitre = QLabel("Suggestions")

        self.mainLayout = QHBoxLayout()
        sec1 = QVBoxLayout()
        sec1.setAlignment(Qt.AlignTop)
        sec2 = QVBoxLayout()
        sec2.setAlignment(Qt.AlignTop)

        sec1.addWidget(self.title)
        sec1.addWidget(self.text)

        sec2.addWidget(suggestionTitre)
        sec2.addWidget(self.suggestion1)
        sec2.addWidget(self.suggestion2)
        sec2.addWidget(self.suggestion3)
        sec2.addWidget(self.suggestion4)

        self.mainLayout.addLayout(sec1, 60)
        self.mainLayout.addLayout(sec2, 40)
        self.setLayout(self.mainLayout)

    def changeTitre(self,value):
        self.title.setText(value)

    def showTranscription(self, value):
        self.text.setText(value)

    def HandleChange(self):
        self.toggle = not self.toggle
        if self.toggle:
            self.send.setText("Stopper")
        else :
            self.send.setText("Démarrer")
        self.sig.state.emit(self.toggle)