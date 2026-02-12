from asr.whisperAsr import WhisperAsr
from audio.microphone import Microphone
from audio.vad import VAD

import threading
import queue
import time
def main():
    speech_queue = queue.Queue()

    mic = Microphone(samplerate=16000, channels=1, blocksize=512)
    vad = VAD(audio_queue=mic.audio_queue, speech_queue=speech_queue)
    asr = WhisperAsr()

    vad_thread = threading.Thread(target=vad.start, daemon=True)
    vad_thread.start()

    mic.start()

    print("Parlez.... Ctrl+C pour arrêter")

    try:
        while True:
            speech = speech_queue.get()
            if len(speech) < 4800:
                continue

            asr.transcribe(speech)
            speech_queue.task_done()
    
    except KeyboardInterrupt:
        print("Terminé....")

    finally:
        mic.stop()
        vad.stop()

if __name__ == "__main__":
    main()