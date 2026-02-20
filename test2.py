import sys
import json
import queue
import sounddevice as sd

from vosk import Model, KaldiRecognizer
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QTextEdit, QLabel, QVBoxLayout, QScrollArea, QTextBrowser
)
from PySide6.QtCore import QThread, Signal, Qt

# =========================
# CONFIG
# =========================
MODEL_PATH = "C:/Users/MRD/Downloads/vosk-model-fr-0.22/vosk-model-fr-0.22"
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 8000

# =========================
# WORKER THREAD (VOSK ONLY)
# =========================
class VoskWorker(QThread):
    partial = Signal(str)
    final = Signal(str)
    status = Signal(str)

    def __init__(self, recognizer, audio_queue):
        super().__init__()
        self.recognizer = recognizer
        self.audio_queue = audio_queue
        self.running = True

    def run(self):
        self.status.emit("🎙️ Reconnaissance vocale active")

        while self.running:
            try:
                data = self.audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "")
                if text:
                    self.final.emit(text)
            else:
                partial = json.loads(self.recognizer.PartialResult())
                p = partial.get("partial", "")
                if p:
                    self.partial.emit(p)

        self.status.emit("⛔ Arrêté")

    def stop(self):
        self.running = False
        self.wait()

# =========================
# MAIN WINDOW
# =========================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-time transcription")
        self.resize(600, 450)

        # UI
        self.start_btn = QPushButton("▶ Alefa")
        self.status_label = QLabel("⏸️ Inactif")

        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)

        container = QWidget()
        self.scroll_layout = QVBoxLayout(container)
        scroll_are = QScrollArea()
        scroll_are.setWidgetResizable(True)
        scroll_are.setWidget(container)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status_label)
        layout.addWidget(QLabel("📝 Transcription en temps réel"))
        layout.addWidget(self.text_box)
        layout.addWidget(container)
        layout.addWidget(self.start_btn)

        # Audio queue
        self.audio_queue = queue.Queue()

        # Vosk
        model = Model(MODEL_PATH)
        recognizer = KaldiRecognizer(model, SAMPLE_RATE)
        recognizer.SetWords(True)

        # Worker
        self.worker = VoskWorker(recognizer, self.audio_queue)
        self.worker.partial.connect(self.show_partial)
        self.worker.final.connect(self.show_final)
        self.worker.status.connect(self.status_label.setText)

        # Sounddevice stream (MAIN THREAD)
        self.stream = sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            dtype="int16",
            channels=CHANNELS,
            callback=self.audio_callback
        )

        self.start_btn.clicked.connect(self.toggle)

    # =========================
    # AUDIO CALLBACK (SAFE)
    # =========================
    def audio_callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)
        self.audio_queue.put(bytes(indata))

    # =========================
    # UI ACTIONS
    # =========================
    def toggle(self):
        if not self.worker.isRunning():
            self.text_box.clear()
            self.stream.start()
            self.worker.start()
            self.start_btn.setText("⛔ Arrêter")
            self.status_label.setText("🎙️ Écoute...")
        else:
            self.stream.stop()
            self.worker.stop()
            self.start_btn.setText("▶ Démarrer")
            self.status_label.setText("⏸️ Inactif")

    def show_partial(self, text):
        self.text_box.setPlainText(text)

    def show_final(self, text):
        textR = QTextBrowser()
        textR.setText(text)
        self.scroll_layout.addWidget(textR)


# =========================
# APP ENTRY
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
