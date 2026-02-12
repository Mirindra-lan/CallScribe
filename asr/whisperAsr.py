import whisper
import queue
import numpy as np

class WhisperAsr:
    def __init__(self, sig):
        self.sig = sig
        self.model = whisper.load_model("base")

    def transcribe(self, audio):
        self.sig.titre.emit("Transcription en cours...")
        res = self.model.transcribe(audio)
        # print("transcription en cours....")
        self.sig.text.emit(res["text"])
        self.sig.titre.emit("Fin de transcription")
        # print(res["text"])

    def queueToAudio(self, voice_queue: queue.Queue) -> np.ndarray:
        chunks = []

        while True:
            try:
                chunk = voice_queue.get_nowait()
            except queue.Empty:
                break

            if chunk.ndim == 2:
                if chunk.shape[1] == 1:
                    chunk = chunk[:, 0]
                else:
                    chunk = chunk.mean(axis=1)

            chunks.append(chunk.astype(np.float32, copy=False))

        if not chunks:
            return np.empty((0,), dtype=np.float32)
        
        audio = np.concatenate(chunks)

        return audio