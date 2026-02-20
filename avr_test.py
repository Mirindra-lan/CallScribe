import pyaudiowpatch as pyaudio
import requests
import threading

URL = "http://192.168.0.246:6066/speech-to-text-stream"

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000          # IMPORTANT: ton serveur upsample 8kHz → 16kHz
CHUNK = 1024

audio = pyaudio.PyAudio()

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

def audio_generator():
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            yield data
    except KeyboardInterrupt:
        print("Stopping audio...")
        stream.stop_stream()
        stream.close()
        audio.terminate()

def send_audio():
    headers = {
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(
        URL,
        data=audio_generator(),
        headers=headers,
        stream=True
    )

    print("Connected to server...")

    for line in response.iter_lines():
        if line:
            print("Transcript:", line.decode())

if __name__ == "__main__":
    send_audio()