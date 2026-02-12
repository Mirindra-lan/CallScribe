import torch
import queue

class VAD:
    def __init__(self, sig,audio_queue: queue.Queue, speech_queue: queue.Queue
                 ,samplerate=16000, threshold=0.5):
        self.audio_queue = audio_queue
        self.speech_queue = speech_queue
        self.samplerate = samplerate
        self.threshold = threshold
        self.sig = sig

        self.model, utils = torch.hub.load('snakers4/silero-vad', 'silero_vad', trust_repo=True)
        self.vad = utils[3](self.model, threshold=self.threshold,
                            sampling_rate=self.samplerate, min_silence_duration_ms=800, speech_pad_ms=200)
        self.buf = []
        self.isRunning = False
        self.recording =False
    
    def start(self):
        self.isRunning = True
        while self.isRunning:
            chunk = self.audio_queue.get()
            self.processChunk(chunk)
            self.audio_queue.task_done()
    
    def processChunk(self, chunk):
        audio = torch.from_numpy(chunk.squeeze()).float()

        vadRes = self.vad(audio)

        if vadRes is not None:
            if vadRes.get("start"):
                # print("L'utilisateur parle")
                self.sig.titre.emit("L'utilisateur parle")
                self.buf = []
                self.recording = True
            
            if vadRes.get("end"):
                # print("Parole termine")
                self.sig.titre.emit("Parole terminé")
                speech = torch.cat(self.buf).numpy()
                self.speech_queue.put(speech)
                self.buf = []
                self.recording = False
                return
        
        if self.recording:
            self.buf.append(audio)
    
    def stop(self):
        self.isRunning = False