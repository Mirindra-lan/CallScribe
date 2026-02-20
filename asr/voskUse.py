import os
from dotenv import load_dotenv
from vosk import Model, KaldiRecognizer
import queue
import json
from gui.signal import  UiSignal

class VoskUse:
    def __init__(self,sig:UiSignal ,langue="fr", rate=16000):
        load_dotenv()
        if langue.upper() == "FR":
            self.model_path = os.getenv("MODEL_FR")
        else: self.model_path = os.getenv("MODEL_EN")
        self.rate = rate
        self.sig = sig
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, self.rate)

    def transcribe(self, audio_queue: queue.Queue):
        while True:
            data = audio_queue.get()

            if self.recognizer.AcceptWaveform(data):
                res = json.loads(self.recognizer.Result())
                if res.get("text"):
                    self.sig.voskRes.emit(res.get("text"))
            else:
                partial = json.loads(self.recognizer.PartialResult())
                if partial.get("partial"):
                    self.sig.voskPart.emit(partial.get("partial"))
            
