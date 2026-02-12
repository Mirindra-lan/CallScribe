import sounddevice as sd
import queue

class Microphone:
    def __init__(self, samplerate=16000, channels=1, blocksize=512):
        self.audio_queue = queue.Queue()
        self.samplerate = samplerate
        self.channels = channels
        self.blocksize = blocksize
        self.isRuning = False

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata.copy())

    def start(self):
        if not self.isRuning:
            self.isRuning = True

        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            blocksize=self.blocksize,
            callback=self.callback
        )
        self.stream.start()
    
    def stop(self):
        if self.isRuning and self.stream:
            self.stream.stop()
            self.stream.close()
            self.isRuning = False
            self.stream = None