import sys
import threading
import queue
from PySide6.QtWidgets import QApplication

from audio.microphone import Microphone
from audio.inputSound import InputSound
from audio.vad import VAD
from asr.whisperAsr import WhisperAsr
from gui.main_window import Window
from gui.signal import UiSignal
from llm.llmApi import LlmApi


class Main:

    def __init__(self):
        # 🔹 App Qt
        self.app = QApplication(sys.argv)

        # 🔹 Signals Qt
        self.signals = UiSignal()

        # 🔹 Queues
        self.speech_queue = queue.Queue()

        # 🔹 Instances
        # Utilisation input système
        # self.mic = InputSound()

        # Si tu veux micro direct :
        self.mic = Microphone(samplerate=16000, channels=1, blocksize=512)

        self.vad = VAD(
            sig=self.signals,
            audio_queue=self.mic.audio_queue,
            speech_queue=self.speech_queue
        )

        self.asr = WhisperAsr(sig=self.signals)

        # 🔹 UI
        self.window = Window(self.signals)

    # =========================
    # 🔹 ASR Worker Thread
    # =========================
    def asr_worker(self):
        while True:
            speech = self.speech_queue.get()

            res = self.asr.transcribe(speech)
            self.signals.newMessage.emit(res)
            # 🔥 Si tu veux LLM plus tard :
            # llm = LlmApi()
            # res1, res2, res3, res4 = llm.getSuggestions(res)
            # self.signals.sug1.emit(res1)
            # self.signals.sug2.emit(res2)
            # self.signals.sug3.emit(res3)
            # self.signals.sug4.emit(res4)

            self.speech_queue.task_done()

    # =========================
    # 🔹 Start Threads
    # =========================
    def start_threads(self):
        # Thread VAD
        self.vad_thread = threading.Thread(
            target=self.vad.start,
            daemon=True
        )
        self.vad_thread.start()

        # Thread ASR
        self.asr_thread = threading.Thread(
            target=self.asr_worker,
            daemon=True
        )
        self.asr_thread.start()

    # =========================
    # 🔹 Main Entry
    # =========================
    def main(self):
        self.window.showMaximized()

        # Start threads
        self.start_threads()

        # Start Micro
        self.mic.start()

        sys.exit(self.app.exec())


# =========================
# 🔹 Entry Point
# =========================
if __name__ == "__main__":
    main = Main()
    main.main()
