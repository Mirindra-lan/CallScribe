import sounddevice as sd
import numpy as np

DEVICE_INDEX = 13  # Haut-parleurs (Jabra LINK 230)

# Récupérer infos du device
device_info = sd.query_devices(DEVICE_INDEX)
samplerate = int(device_info['default_samplerate'])
channels = int(device_info['max_input_channels'])

print("Device :", device_info['name'])
print("Sample rate :", samplerate)
print("Channels: ", channels)

# def callback(indata, frames, time, status):
#     if status:
#         print(status)

#     volume = np.linalg.norm(indata)
#     print("🔊 Niveau audio :", volume)

# with sd.InputStream(
#     device=DEVICE_INDEX,
#     samplerate=samplerate,
#     channels=channels,  # sortie = souvent stéréo
#     dtype='float32',
#     blocksize=1024,
#     callback=callback
# ):
#     print("🎧 Loopback actif sur Jabra...")
#     while True:
#         pass
