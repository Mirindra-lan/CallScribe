import pyaudiowpatch as paudio
import queue

class MicroPyAudio:
    def __init__(self, rate= 16000, frames=1024, channels=1, input=True, type=paudio.paInt16,
                 voice_queue: queue.Queue = queue.Queue()):
        self.rate = rate
        self.frames = frames
        self.channels = channels
        self.input = input
        self.type = type
        self.pa = paudio.PyAudio()
        self.stream = None
        self.voice_queue = voice_queue

    def start(self):
        self.stream = self.pa.open(
            rate=self.rate,
            frames_per_buffer=self.frames,
            input=self.input,
            channels=self.channels,
            format=self.type,
            stream_callback=self.callback
        )

        self.stream.start_stream()

    def callback(self, indata, frame, time, status):
        self.voice_queue.put(indata)
        return (None, paudio.paContinue)
    
    def stop(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.pa.terminate()
