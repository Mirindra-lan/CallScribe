from pycaw.pycaw import AudioUtilities
from proctap import ProcessAudioCapture
from queue import Queue

class ProcessSound:
    def __init__(self, processName:str):
        self.pid = self.findPidByName(processName)
        self.voice_queue = Queue()
        self.stream = None

    def findPidByName(self, name: str) -> int:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process:
                if session.Process.name().lower() == name.lower():
                    return session.Process.pid
                if session.Process.name().lower() == f"{name.lower()}.exe":
                    return session.Process.pid
                
        return None
    
    def callback(self, data:bytes, frame:int):
        self.voice_queue.put(data)

    def start(self):
        if self.pid is not None:
            self.stream = ProcessAudioCapture(pid=self.pid, on_data=self.callback)

        if self.stream is not None:
            self.stream.start()

    def stop(self):
        if self.stream is not None:
            self.stream.stop()
