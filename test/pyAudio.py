import pyaudiowpatch as pyaudio
import torch
import numpy as np
import queue
import librosa

# ======================
# CONFIG
# ======================

CHUNK = 2048  # plus stable
TARGET_SR = 16000
MIN_SAMPLES = 512

audio_queue = queue.Queue()

# ======================
# SILERO
# ======================

model, utils = torch.hub.load('snakers4/silero-vad', 'silero_vad', force_reload=False)

(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

vad_iterator = VADIterator(model)

# ======================
# PYAUDIO LOOPBACK
# ======================

p = pyaudio.PyAudio()
loopback = p.get_default_wasapi_loopback()
SAMPLE_RATE = int(loopback["defaultSampleRate"])

channels = loopback["maxInputChannels"]  # change à 2 si nécessaire

def callback(in_data, frame_count, time_info, status):
    audio_queue.put(in_data)
    return (None, pyaudio.paContinue)

stream = p.open(
    format=pyaudio.paFloat32,
    channels=channels,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK,
    input_device_index=loopback["index"],
    stream_callback=callback,
)

stream.start_stream()
print("🎧 Loopback actif")

# ======================
# TRAITEMENT VAD
# ======================

import numpy as np
import torch
import librosa

CHUNK_SIZE = 512          # obligatoire pour 16kHz
TARGET_SR = 16000

vad_buffer = np.array([], dtype=np.float32)

while True:
    data = audio_queue.get()

    # int16 → float32
    audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32)

    # Si stéréo → mono
    if channels == 2:
        audio_np = audio_np.reshape(-1, 2).mean(axis=1)

    # Normalisation
    audio_np /= 32768.0

    # Resample vers 16k
    if SAMPLE_RATE != TARGET_SR:
        audio_np = librosa.resample(audio_np, orig_sr=SAMPLE_RATE, target_sr=TARGET_SR)

    # Accumulation
    vad_buffer = np.concatenate([vad_buffer, audio_np])

    # 🔥 Traitement par blocs fixes
    while len(vad_buffer) >= CHUNK_SIZE:

        chunk = vad_buffer[:CHUNK_SIZE]
        vad_buffer = vad_buffer[CHUNK_SIZE:]

        # convertir en tensor [1, 512]
        tensor = torch.from_numpy(chunk).unsqueeze(0)

        # inference
        speech_prob = model(tensor, TARGET_SR).item()

        if speech_prob < 0.5:
            print("🗣️ Speech", speech_prob)
        else:
            print("🔇 Silence", speech_prob)
