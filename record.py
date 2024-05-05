import queue
import sys
import time

import sounddevice as sd
import soundfile as sf
import numpy # Make sure NumPy is loaded before it is used in the callback
assert numpy # avoid "imported but unused" message (W0611)
import logging
logger = logging.getLogger(__name__)

from utils import prettyDict

def selectMicrophone():
    """
    Prompts the user to select a microphone device by displaying a list of available devices and asking for the device number.

    Returns:
        int: The selected microphone device number.
    """
    devices = sd.query_devices()

    for device in devices:
        print(prettyDict(device))

    microphone = input('Enter the microphone device number: ')

    return int(microphone)

class Recorder:
    """
    A class for recording audio from a microphone.

    Args:
        device (int): The index of the audio device to use. Default is 1.
        channels (int): The number of audio channels. Default is 2.
        samplerate (int): The sample rate of the audio. Default is 44100.

    Attributes:
        q (Queue): A queue to store the recorded audio data.
        device (int): The index of the audio device being used.
        channels (int): The number of audio channels being recorded.
        samplerate (int): The sample rate of the audio being recorded.
    """

    def __init__(self, device=1, channels=2, samplerate=44100, DEBUG=False):
        sd.default.device = device
        logger.info(f'default microphone:{sd.default.device}')
        if DEBUG:
            print(f'default microphone:{sd.default.device}')
        self.q = queue.Queue()
        self.device = device
        self.channels = channels
        self.samplerate = samplerate

    def __del__(self):
        del self.q

    def callback(self, indata, frames, time, status):
        """
        This is called (from a separate thread) for each audio block.

        Args:
            indata (ndarray): The input audio data.
            frames (int): The number of frames in the audio block.
            time (CData): The time stamp of the audio block.
            status (int): The status of the audio block.

        Returns:
            None
        """
        if status:
            print(status, file=sys.stderr)

        self.q.put(indata.copy())

    def record(self, filename='./output.wav'):
        """
        Records audio from the microphone and saves it to a file.

        Args:
            filename (str): The path to the output file. Default is './output.wav'.

        Returns:
            None
        """
        logger.info(f'Recording audio to {filename}')
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
        logger.info('Recording finished')
        print('\nRecording finished')
                       