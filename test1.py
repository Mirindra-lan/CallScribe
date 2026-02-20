import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import os
app = QApplication(sys.argv)

window = QMainWindow()

webview = QWebEngineView()
path = os.path.abspath("frontend/dist/index.html")
webview.setUrl(QUrl.fromLocalFile(path))

window.setCentralWidget(webview)
window.resize(800, 600)
window.show()

sys.exit(app.exec())
