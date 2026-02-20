import pyaudiowpatch as paudio
import threading
import queue
from audio.microPyAudio import MicroPyAudio
from asr.voskUse import VoskUse
from audio.voiceActivity import VoiceActivity
from PySide6.QtWidgets import QApplication
import sys
from gui.voskGui import VoskGui
from gui.signal import UiSignal
from asr.voskApi import VoskApi

RATE = 16000
FRAME = 512


audio_queue = queue.Queue()
speech_queue = queue.Queue()
signals = UiSignal()
isSpeak = False


mic = MicroPyAudio(rate=RATE, frames=FRAME, channels=1, input=True, type=paudio.paInt16, voice_queue=audio_queue)
# asr = VoskUse(sig=signals, langue="fr", rate=RATE)
sender = VoskApi(speech_queue=speech_queue, signal=signals)
vad = VoiceActivity(sig=signals, sender=sender,audio_queue=audio_queue, samplerate=RATE, speech_queue=speech_queue)

vad_thread = threading.Thread(target=vad.start, daemon=True)
# worker_thread = threading.Thread(target=asr.transcribe, args=(speech_queue,), daemon=True)
mic.start()
vad_thread.start()
# worker_thread.start()

app = QApplication(sys.argv)
fen = VoskGui(signal=signals)
fen.show()

signals.voskTitre.emit("tu peux parler maintenant")

sys.exit(app.exec())