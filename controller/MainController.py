class MainController:
    def __init__(self, sig):
        self.sig = sig
        self.sig.state.connect(self.handleToggle)
        self.state = False

    def handleToggle(self, value):
        self.state = value
        if self.state:
            self.sig.titre.emit("Demarrer")
        else:
            self.sig.titre.emit("Stopper")
