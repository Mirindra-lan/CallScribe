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
from asr.voskAsr import VoskAsr


def asr_worker(speech_queue, asr, source):
    while True:
        speech = speech_queue.get()
        isUser = isinstance(source, Microphone)

        # if len(speech) > 4800:  # éviter segments trop courts
        #     asr.transcribe(speech)
        asr.transcribe(speech, isUser)

        speech_queue.task_done()


def main():
    app = QApplication(sys.argv)

    signals = UiSignal()
    speech_queue = queue.Queue()

    mic = Microphone(16000, 1, 512, 'float32')
    vad = VAD(sig=signals, audio_queue=mic.audio_queue, speech_queue=speech_queue,samplerate=16000)
    asr = VoskAsr("C:/Users/MRD/CallScrib/models/vosk-model-fr-0.22", 16000, signals)

    vad_thread = threading.Thread(target=vad.start, daemon=True)
    worker_thread = threading.Thread(target=asr_worker, args=(speech_queue, asr, mic,), daemon=True)

    vad_thread.start()
    worker_thread.start()

    fen = Window(sig=signals)
    fen.show()

    mic.start()
    
    sys.exit(app.exec())



if __name__ == "__main__":
    main()
