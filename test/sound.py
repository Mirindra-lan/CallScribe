import pyaudiowpatch as pa

p = pa.PyAudio()

inputdevice = p.get_default_wasapi_loopback()
print(inputdevice)
deviceIndex = int(inputdevice["index"])
p.is_format_supported(
    rate=inputdevice["defaultSampleRate"],
    input_format=pa.paFloat32,
    input_channels=inputdevice["maxInputChannels"],
    input_device=deviceIndex,
)
print(inputdevice["defaultSampleRate"]) #48000.0