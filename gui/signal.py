from PySide6.QtCore import QObject, Signal

class UiSignal(QObject):
    titre = Signal(str)
    text = Signal(str)
    state = Signal(bool)