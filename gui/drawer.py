from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Signal
import qtawesome as faIcon

class Drawer(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)

        self.mainLayout.addWidget(self.topIcon(), alignment=Qt.AlignTop | Qt.AlignLeft)
        self.mainLayout.addWidget(MenuItem("Nouvelle discussion",'mdi.chat-plus-outline'))
        self.mainLayout.addWidget(MenuItem("Recherche dans le converstion",'mdi.magnify-plus-outline'))
        self.mainLayout.addWidget(MenuItem("Paramètres",'mdi.cog-outline'))
        self.mainLayout.addWidget(self.historyTitle())

        self.setStyleSheet("""
            QLabel#his {
                color: gray;
                margin-top: 20px;
            }
        """)
        self.setLayout(self.mainLayout)

    def historyTitle(self):
        history = QLabel("Historique")
        history.setObjectName("his")
        return history

    def topIcon(self):
        label = QLabel()
        label.setPixmap(faIcon.icon('mdi.headset', color='white').pixmap(40,40))
        return label
    
class MenuItem(QWidget):
    clicked = Signal()

    def __init__(self, texte, iconMap, color="gray", x=20, y=20):
        super().__init__()
        self.layoutt = QHBoxLayout()
        self.layoutt.setAlignment(Qt.AlignLeft)
        self.icon = QLabel()
        self.icon.setPixmap(faIcon.icon(iconMap, color=color).pixmap(x,y))
        self.text = QLabel(texte)
        self.layoutt.addWidget(self.icon)
        self.layoutt.addWidget(self.text)
        self.setLayout(self.layoutt)


    def mousePressEvent(self, event):
        self.clicked.emit()