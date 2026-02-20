import pyaudiowpatch as paudio
import queue
import numpy as np
from scipy.signal import resample_poly
import threading

class InputSound:
    def __init__(self):
        self.pa = paudio.PyAudio()
        self.loopback = self.pa.get_default_wasapi_loopback()
        self.chunk = 2048
        self.samplerate = int(self.loopback["defaultSampleRate"])
        self.index = int(self.loopback["index"])
        self.channels = int(self.loopback["maxInputChannels"])
        self.voice_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        self.buffer_16k = np.array([], dtype=np.float32)

    def callback(self, indata, frame, time, status):
        audio_48k = np.frombuffer(indata, dtype=np.float32)
        self.voice_queue.put(audio_48k.copy())
        return None, paudio.paContinue
    
    def start(self, model):
        self.stream = self.pa.open(
            format=paudio.paFloat32,
            channels=1,
            rate=self.samplerate,
            input=True,
            input_device_index=self.index,
            frames_per_buffer=self.chunk,
            stream_callback=self.callback
        )
        self.stream.start_stream()
        if model == "Vosk":
            self.processing_thread = threading.Thread(target=self.process_chunk2, daemon=True)
        else : 
            self.processing_thread = threading.Thread(target=self.process_chunk, daemon=True)
        self.processing_thread.start()

    def process_chunk(self):
        while True:
            audio_48k = self.voice_queue.get()
            audio_16k = resample_poly(audio_48k, up=1, down=3).astype(np.float32)
            self.buffer_16k = np.concatenate((self.buffer_16k, audio_16k))

            while len(self.buffer_16k) >= 512:
                chunk = self.buffer_16k[:512]
                self.buffer_16k = self.buffer_16k[512:]
                self.audio_queue.put(chunk)

            self.voice_queue.task_done()
    
    def process_chunk2(self):
        while True:
            audio_48k = self.voice_queue.get()

            # 1️⃣ Downsample simple (48000 → 16000)
            audio_16k = audio_48k[::3]

            # 2️⃣ float32 → int16 PCM
            audio_int16 = (audio_16k * 32767).astype(np.int16)

            # 3️⃣ Accumulation buffer
            self.buffer_16k = np.concatenate((self.buffer_16k, audio_int16))

            # 4️⃣ Chunk optimal pour Vosk (2048 recommandé)
            while len(self.buffer_16k) >= 2048:
                chunk = self.buffer_16k[:2048]
                self.buffer_16k = self.buffer_16k[2048:]

                # 5️⃣ envoyer bytes prêts pour Vosk
                self.audio_queue.put(chunk.tobytes())

            self.voice_queue.task_done()

    def stop(self):
        if self.stream.is_active():
            self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

        if self.processing_thread is not None:
            self.processing_thread.join()
