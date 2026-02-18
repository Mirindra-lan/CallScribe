from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
import sys
import os


class Backend(QObject):
    dataChanged = Signal(str)

    @Slot(str)
    def receiveMessage(self, msg):
        print("Message from React:", msg)

    def sendData(self, text):
        self.dataChanged.emit(text)


app = QApplication(sys.argv)

view = QWebEngineView()

backend = Backend()
channel = QWebChannel()
channel.registerObject("backend", backend)

view.page().setWebChannel(channel)
file_path = os.path.abspath("frontend/dist/index.html")
view.load(QUrl.fromLocalFile(file_path))

view.show()

# Test : envoyer une donnée après 2 sec
from PySide6.QtCore import QTimer
QTimer.singleShot(2000, lambda: backend.sendData("Hello from Python 🚀"))

sys.exit(app.exec())
