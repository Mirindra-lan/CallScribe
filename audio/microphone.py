import sounddevice as sd
import queue

class Microphone:
    def __init__(self, samplerate=16000, channels=1, blocksize=512, dType='float32'):
        self.audio_queue = queue.Queue()
        self.samplerate = samplerate
        self.channels = channels
        self.blocksize = blocksize
        self.dtype = dType
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
            dtype= self.dtype,
            callback=self.callback
        )
        self.stream.start()
    
    def start2(self):
        self.stream = sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=8000,
            dtype="int16",
            channels=self.channels,
            callback=self.callback
        )
        self.stream.start()

    def stop(self):
        if self.isRuning and self.stream:
            self.stream.stop()
            self.stream.close()
            self.isRuning = False
            self.stream = None