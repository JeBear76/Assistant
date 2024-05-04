import queue
import sys
import time

import sounddevice as sd
import soundfile as sf
import numpy # Make sure NumPy is loaded before it is used in the callback
assert numpy # avoid "imported but unused" message (W0611)

from utils import prettyDict

def selectMicrophone():
    # Query available audio devices
    devices = sd.query_devices()

    # Print the available devices
    for device in devices:
        print(prettyDict(device))

    # Prompt the user to enter the microphone device number
    microphone = input('Enter the microphone device number: ')

    # Set the default audio device to the selected microphone
    return int(microphone)

class Recorder:
    def __init__(self, device=1, channels = 2, samplerate = 44100):
        sd.default.device = device
        print(f'default microphone:{sd.default.device}')
        self.q = queue.Queue()
        self.device = device
        self.channels = channels
        self.samplerate = samplerate

    def __del__(self):         
        del self.q        

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        
        self.q.put(indata.copy())

    def record(self, filename='./output.wav'):
        try:
            with sf.SoundFile(filename, mode='w', samplerate=44100,
                            channels=self.channels) as file:
                with sd.InputStream(samplerate=self.samplerate, device=self.device,
                                    channels=self.channels, callback=self.callback):
                    t = time.time()
                    while True:
                        file.write(self.q.get())
                        if time.time() - t > 10:
                            break
        except KeyboardInterrupt:
            pass
        print('\nRecording finished')
                       