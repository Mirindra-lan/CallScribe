from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QTextBrowser,
QScrollArea, QHBoxLayout)
from PySide6.QtCore import Qt
from gui.chatBubble import ChatBubble
from gui.bullMessage import BullMessage

class MainSection(QWidget):
    def __init__(self, sig):
        super().__init__()
        print(self.width(), self.height())

        self.signal = sig
        self.toggle = False
        self.title = QLabel("Résultat de la transcription avec whisper")
        self.signal.titre.connect(self.changeTitre)
        self.signal.newMessage.connect(self.addNewLine)

        self.send = QPushButton("Démarrer")
        self.send.clicked.connect(self.HandleChange)

        self.text = QTextBrowser()
        self.text.setText("Parole transcrite")
        self.signal.text.connect(self.showTranscription)

        self.suggestion1 = QTextBrowser()
        self.suggestion1.setText("Suggestion 1")
        self.suggestion1.setObjectName("suggestion")
        self.signal.sug1.connect(self.setSuggestion1)
        
        self.suggestion2 = QTextBrowser()
        self.suggestion2.setText("Suggestion 2")
        self.signal.sug2.connect(self.setSuggestion2)
        
        self.suggestion3 = QTextBrowser()
        self.suggestion3.setText("Suggestion 3")
        self.signal.sug3.connect(self.setSuggestion3)
        
        self.suggestion4 = QTextBrowser()
        self.suggestion4.setText("Suggestion 4")
        self.signal.sug4.connect(self.setSuggestion4)

        suggestionTitre = QLabel("Suggestions")


        self.mainLayout = QHBoxLayout()
        sec1 = QVBoxLayout()
        sec1.setAlignment(Qt.AlignTop)
        sec2 = QVBoxLayout()
        sec2.setAlignment(Qt.AlignTop)

        la1 = QVBoxLayout()
        la2 = QVBoxLayout()
        
        la1.addWidget(self.title)
        # la1.addWidget(self.text)


        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.scroll_layout = QVBoxLayout(container)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(container)

        la2.addWidget(scroll)
        sec1.addLayout(la1)
        sec1.addLayout(la2)

        sec2.addWidget(suggestionTitre)
        sec2.addWidget(self.suggestion1)
        sec2.addWidget(self.suggestion2)
        sec2.addWidget(self.suggestion3)
        sec2.addWidget(self.suggestion4)

        self.mainLayout.addLayout(sec1, 60)
        self.mainLayout.addLayout(sec2, 40)
        self.setLayout(self.mainLayout)

        self.suggestion3.setStyleSheet("""
            QTextBrowser#suggestion {
                background-color: #2d2d2d;
                border-radius: 12px;
                padding: 12px;
                color: white;
            }
        """)

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

    def setSuggestion1(self,value):
        self.suggestion1.setText(value)
        
    def setSuggestion2(self,value):
        self.suggestion2.setText(value)
    
    def setSuggestion3(self,value):
        self.suggestion3.setText(value)
    
    def setSuggestion4(self,value):
        self.suggestion4.setText(value)


    def addNewLine(self, text):
        self.toggle = not self.toggle
        self.addMessage(text, self.toggle)

    def addMessage(self, text, isUser: bool):
        container = QWidget()
        layout = QHBoxLayout(container)
        if isUser:
            message = BullMessage(container, text,"#0A0A55")
            layout.addStretch(3)
            layout.addWidget(message, 7)
        else:
            message = BullMessage(container, text)
            layout.addWidget(message, 7)
            layout.addStretch(3)
        self.scroll_layout.addWidget(container)