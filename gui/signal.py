from PySide6.QtCore import QObject, Signal

class UiSignal(QObject):
    titre = Signal(str)
    text = Signal(str, bool)
    state = Signal(bool)
    sug1 = Signal(str)
    sug2 = Signal(str)
    sug3 = Signal(str)
    sug4 = Signal(str)