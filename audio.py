import pyaudio  
import wave  
from time import sleep

class Audio:
    def __init__(self):
        self.chunk = 1024
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.f = None

    def play(self, path):
        self.f = wave.open(path, "rb")
        self.stream = self.p.open(format = self.p.get_format_from_width(self.f.getsampwidth()),  
                    channels = self.f.getnchannels(),  
                    rate = self.f.getframerate(),  
                    output = True)  
        data = self.f.readframes(self.chunk)  
        while data:  
            self.stream.write(data)  
            data = self.f.readframes(self.chunk) 

        sleep(0.5)

        self.stream.stop_stream()  
        self.stream.close()  
        self.f.close()

    def stop(self):
        if not self.stream.is_stopped:
            self.stream.stop_stream()
        if self.stream.is_active :
            self.stream.close()
        if self.f is not None:
            self.f.close()
        self.p.terminate()            # close PyAudio