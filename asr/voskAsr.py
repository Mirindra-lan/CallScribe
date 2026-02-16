from vosk import Model, KaldiRecognizer
import json
import queue

class VoskAsr:
    def __init__(self, modelPath, samplerate, block_size, channels):
        self.model = Model(modelPath)
        self.samplerate = samplerate
        self.blockSize = block_size
        self.channels = channels
        self.recognizer = KaldiRecognizer(self.model, self.samplerate)
        self.recognizer.SetWords(True)

    def transcribe(self, audio_queue):
        while self.running:
            try:
                data = audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "")
                if text:
                    print(text)
            else:
                partial = json.loads(self.recognizer.PartialResult())
                p = partial.get("partial", "")
                if p:
                    print(p)

        print("⛔ Arrêté")
