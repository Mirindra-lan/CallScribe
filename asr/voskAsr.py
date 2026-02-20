from vosk import Model, KaldiRecognizer
import json
import queue
import numpy as np

class VoskAsr:
    def __init__(self, modelPath, samplerate, sig):
        self.sig = sig
        self.model = Model(modelPath)
        self.samplerate = samplerate
        self.recognizer = KaldiRecognizer(self.model, self.samplerate)
        self.recognizer.SetWords(True)
        self.running = True

    def transcribe(self, audio, isUser):
        while self.running:
            try:
                data = audio
                data = np.clip(data, -1.0, 1.0)
                speech_bytes = (data * 32767).astype(np.int16).tobytes()
            except queue.Empty:
                continue

            if self.recognizer.AcceptWaveform(speech_bytes):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "")
                if text:
                    self.sig.text.emit(text, isUser)
            else:
                partial = json.loads(self.recognizer.PartialResult())
                p = partial.get("partial", "")
                if p:
                    print(p)

        print("⛔ Arrêté")
