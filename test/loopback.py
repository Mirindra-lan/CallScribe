import pyaudiowpatch as pyaudio
from vosk import Model, KaldiRecognizer
import json
from dotenv import load_dotenv
import os
import queue

load_dotenv()

MODEL_PATH = os.getenv("MODEL_EN")
CHUNK = 1024

audio_queue = queue.Queue()
p = pyaudio.PyAudio()

# 🎧 Loopback automatique
loopback = p.get_default_wasapi_loopback()
SAMPLE_RATE = int(loopback["defaultSampleRate"])

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

# 🎧 Callback AUDIO uniquement (pas de Vosk ici)
def audio_callback(in_data, frame_count, time_info, status):
    if status:
        print(status)
    audio_queue.put(in_data)
    return (None, pyaudio.paContinue)

# 🎧 Ouverture stream
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK,
    input_device_index=loopback["index"],
    stream_callback=audio_callback,
)

stream.start_stream()

print("🎙️ Transcription en cours... Ctrl+C pour arrêter.")

try:
    while True:
        data = audio_queue.get()

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print("📝", result.get("text", ""))
        # else:
        #     partial = json.loads(recognizer.PartialResult())
        #     print("⏳", partial.get("partial", ""), end="\r")

except KeyboardInterrupt:
    print("\n⛔ Arrêt demandé")

stream.stop_stream()
stream.close()
p.terminate()
