from pycaw.pycaw import AudioUtilities
from proctap import ProcessAudioCapture
import time
from queue import Queue

audio_queue = Queue()

def on_audio(pcm_data: bytes, frame_count: int):
    print(frame_count)
    audio_queue.put(pcm_data)
        
def findPidByName(name: str) -> int:
    sessions = AudioUtilities.GetAllSessions()
    for s in sessions:
        if s.Process:
            if s.Process.name().lower() == name.lower():
                return s.Process.pid
            
            if s.Process.name().lower() == f"{name.lower()}.exe":
                return s.Process.pid
    return None

            # print(s.Process.name(), s.Process.pid, s.SimpleAudioVolume.GetMasterVolume())
            
pid = findPidByName("spotify")

if pid is not None:
    with ProcessAudioCapture(pid=pid, on_data=on_audio):
        print("Capture commence")
        time.sleep(60)
