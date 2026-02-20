from queue import Queue
import torch
import numpy as np
from gui.signal import UiSignal
from asr.voskApi import VoskApi

class VoiceActivity:
    def __init__(self, sig: UiSignal, sender: VoskApi, audio_queue: Queue, speech_queue: Queue
                 ,samplerate=16000, threshold=0.5):
    # def __init__(self, sig: UiSignal, audio_queue: Queue, speech_queue: Queue
    #              ,samplerate=16000, threshold=0.5):
        
        self.audio_queue = audio_queue
        self.speech_queue = speech_queue
        self.samplerate = samplerate
        self.threshold = threshold
        self.isRecording = False
        self.sig = sig
        self.sender = sender

        self.model, utils = torch.hub.load('snakers4/silero-vad', 'silero_vad', trust_repo=True)
        self.vad = utils[3](
            self.model,
            threshold=self.threshold,
            sampling_rate=self.samplerate,
            min_silence_duration_ms=800,
            speech_pad_ms=200
        )
        
    def processChunk(self, chunk):
        audio_np = np.frombuffer(chunk, dtype=np.int16)
        audio_float = audio_np.astype(np.float32) / 32768.0
        return torch.from_numpy(audio_float)

    def start(self):
        while True:
            data = self.audio_queue.get()
            audio = self.processChunk(data)
            vadRes = self.vad(audio)

            if vadRes is not None:
                if vadRes.get("start"):
                    self.sig.voskTitre.emit("L'utilisateur parle")
                    self.isRecording = True
                    self.isSpeak = True
                    self.sender.start()
                
                if vadRes.get("end"):
                    self.sig.voskTitre.emit("Parole terminé")
                    self.isRecording = False
                    self.isSpeak = self.isRecording
                    self.sender.stop()

            if self.isRecording:
                self.speech_queue.put(data)

            self.audio_queue.task_done()