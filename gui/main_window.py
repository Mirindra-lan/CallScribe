from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QHBoxLayout
from PySide6.QtCore import Qt
from gui.drawer import Drawer
from gui.mainSection import MainSection

class Window(QWidget):
    def __init__(self, sig):
        super().__init__()
        self.sig = sig

        self.side = Drawer()
        self.main = MainSection(self.sig)
        # self.main = 
        self.resize(600,400)
        self.setWindowTitle("Learn OOP with python")

        parentLayout = QVBoxLayout()
        div = QHBoxLayout()
        draw = QVBoxLayout()
        draw.addWidget(self.side)
        section = QVBoxLayout()
        section.addWidget(self.main)

        div.addLayout(draw, 18)
        div.addLayout(section, 82)

        parentLayout.addLayout(div)
        self.setLayout(parentLayout)
    
    

    

    