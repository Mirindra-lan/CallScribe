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


def asr_worker(speech_queue, asr):
    while True:
        speech = speech_queue.get()

        # if len(speech) > 4800:  # éviter segments trop courts
        #     asr.transcribe(speech)
        asr.transcribe(speech)
        # llm = LlmApi()
        # res1, res2, res3, res4 = llm.getSuggestions(res)
        # sig.sug1.emit(res1)
        # sig.sug2.emit(res2)
        # sig.sug3.emit(res3)
        # sig.sug4.emit(res4)
        speech_queue.task_done()


def main():
    app = QApplication(sys.argv)

    # 🔹 Signals Qt
    signals = UiSignal()

    # 🔹 Queues
    speech_queue = queue.Queue()

    # 🔹 Instances
    #utilisation de input from app
    mic = InputSound()
    vad = VAD(sig=signals, audio_queue=mic.audio_queue, speech_queue=speech_queue)

    #utilisation de input from microphone
    # mic = Microphone(samplerate=16000, channels=1, blocksize=512)
    # vad = VAD(sig=signals, audio_queue=mic.audio_queue, speech_queue=speech_queue)
    asr = WhisperAsr(sig=signals)

    window = Window(signals)
    window.showMaximized()

    # 🔹 Thread VAD
    vad_thread = threading.Thread(target=vad.start, daemon=True)
    vad_thread.start()

    # 🔹 Thread ASR
    asr_thread = threading.Thread(
        target=asr_worker,
        args=(speech_queue, asr),
        daemon=True
    )
    asr_thread.start()

    # 🔹 Start Micro
    mic.start()

    # 🔹 Bouton Start / Stop via signal
    # def handle_state(state):
    #     if state:
    #         print("🎤 Micro activé")
    #         mic.start()
    #     else:
    #         print("🛑 Micro stoppé")
    #         mic.stop()

    # signals.state.connect(handle_state)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
