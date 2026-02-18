from PySide6.QtWidgets import (QWidget, QApplication, QVBoxLayout, QHBoxLayout)
import sys
from gui.messages.messageSection import MessageSec
from gui.menu.drawer import Drawer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.widget = MessageSec()
        self.divH = QHBoxLayout()
        self.sec1 = QVBoxLayout()
        self.sec2 = QHBoxLayout()
        self.div3 = QVBoxLayout()
        self.div1 = QVBoxLayout()
        self.div2 = QVBoxLayout()
        self.drawer = Drawer()

        self.div1.addWidget(self.widget)
        self.div3.addWidget(self.drawer)

        self.sec1.addLayout(self.div3)
        self.sec2.addLayout(self.div1, 65)
        self.sec2.addLayout(self.div2, 35)

        self.divH.addLayout(self.sec1, 18)
        self.divH.addLayout(self.sec2, 82)
        self.setLayout(self.divH)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windows = MainWindow()
    windows.setWindowTitle("Callscribe")
    windows.showMaximized()
    sys.exit(app.exec())
