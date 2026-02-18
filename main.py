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


def asr_worker(speech_queue, asr, source):
    while True:
        speech = speech_queue.get()
        isUser = isinstance(source, Microphone)

        # if len(speech) > 4800:  # éviter segments trop courts
        #     asr.transcribe(speech)
        asr.transcribe(speech, isUser)
        # llm = LlmApi()
        # res1, res2, res3, res4 = llm.getSuggestions(res)
        # sig.sug1.emit(res1)
        # sig.sug2.emit(res2)
        # sig.sug3.emit(res3)
        # sig.sug4.emit(res4)
        speech_queue.task_done()


# def main():
#     app = QApplication(sys.argv)

#     # 🔹 Signals Qt
#     signals = UiSignal()

#     # 🔹 Queues
#     speech_queue = queue.Queue()
#     # speech_queue2 = queue.Queue()

#     # 🔹 Instances
#     #utilisation de input from app

#     mic = InputSound()
#     vad = VAD(sig=signals,audio_queue=mic.audio_queue, speech_queue=speech_queue)

#     #utilisation de input from microphone
#     # mic2 = Microphone(samplerate=16000, channels=1, blocksize=512)
#     # vad2 = VAD(sig=signals, audio_queue=mic.audio_queue, speech_queue=speech_queue2)

#     asr = WhisperAsr(sig=signals)

#     window = Window(signals)
#     window.showMaximized()

#     # 🔹 Thread VAD
#     vad_thread = threading.Thread(target=vad.start, daemon=True)
#     vad_thread.start()
    
#     # vad2_thread = threading.Thread(target=vad2.start, daemon=True)
#     # vad2_thread.start()
#     # 🔹 Thread ASR
#     asr_thread = threading.Thread(
#         target=asr_worker,
#         args=(speech_queue, asr, mic),
#         daemon=True
#     )
#     asr_thread.start()

#     # asr_thread2 = threading.Thread(
#     #     target=asr_worker,
#     #     args=(speech_queue2, asr),
#     #     daemon=True
#     # )
#     # asr_thread.start()

#     # 🔹 Start Micro
#     mic.start()

#     # 🔹 Bouton Start / Stop via signal
#     # def handle_state(state):
#     #     if state:
#     #         print("🎤 Micro activé")
#     #         mic.start()
#     #     else:
#     #         print("🛑 Micro stoppé")
#     #         mic.stop()

#     # signals.state.connect(handle_state)

#     sys.exit(app.exec())

def main():
    app = QApplication(sys.argv)

    signals = UiSignal()

    # 🔹 Queues séparées
    speech_queue1 = queue.Queue()
    speech_queue2 = queue.Queue()

    # 🔹 Sources audio
    input_sound = InputSound()
    microphone = Microphone(samplerate=16000, channels=1, blocksize=512)

    # 🔹 VAD séparés
    vad1 = VAD(sig=signals, audio_queue=input_sound.audio_queue, speech_queue=speech_queue1)
    vad2 = VAD(sig=signals, audio_queue=microphone.audio_queue, speech_queue=speech_queue2)

    # 🔹 ASR (⚠️ voir remarque plus bas)
    asr1 = WhisperAsr(sig=signals)
    asr2 = WhisperAsr(sig=signals)

    window = Window(signals)
    window.showMaximized()

    # 🔹 Threads VAD
    threading.Thread(target=vad1.start, daemon=True).start()
    threading.Thread(target=vad2.start, daemon=True).start()

    # 🔹 Threads ASR
    threading.Thread(
        target=asr_worker,
        args=(speech_queue1, asr1, input_sound),
        daemon=True
    ).start()

    threading.Thread(
        target=asr_worker,
        args=(speech_queue2, asr2, microphone),
        daemon=True
    ).start()

    # 🔹 Démarrer les deux captures
    input_sound.start()
    microphone.start()

    sys.exit(app.exec())



if __name__ == "__main__":
    main()
