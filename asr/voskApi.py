import requests
import threading
import numpy as np
from scipy.signal import resample_poly
from gui.signal import UiSignal

class VoskApi:
    def __init__(self, speech_queue, signal: UiSignal):
        self.speech_queue = speech_queue
        self.running = False
        self.signal = signal
        self.thread = None
        self.url = "http://192.168.0.246:6066/speech-to-text-stream"

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._send)
        self.thread.start()

    def stop(self):
        self.running = False

    def _generator(self):
        while self.running:
            try:
                data = self.speech_queue.get(timeout=0.5)
                # data_8k = self.downsample(data)
                yield data
            except:
                continue
    
    def downsample(self, chunk):
        audio_np = np.frombuffer(chunk, dtype=np.int16)
        if len(audio_np) == 0:
            return b""
        audio_foat = audio_np.astype(np.float32) / 32768.0

        sample8k = resample_poly(audio_foat, up=1, down=2)
        sample_8k_int16 = (sample8k * 32768).astype(np.int16)
        return sample_8k_int16.tobytes()
    
    def _send(self):
        headers = {"Content-Type": "application/octet-stream"}

        response = requests.post(
            self.url,
            data=self._generator(),
            headers=headers,
            stream=True
        )

        for line in response.iter_lines():
            if line:
                self.signal.voskRes.emit(line.decode())