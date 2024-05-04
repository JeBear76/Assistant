import pyaudio  
import wave  
from time import sleep

class Audio:
    """
    A class for playing audio files using PyAudio and wave module.

    Attributes:
        chunk (int): The number of frames to read at a time.
        p (pyaudio.PyAudio): The PyAudio object for audio stream management.
        stream (pyaudio.Stream): The audio stream object.
        f (wave.Wave_read): The wave file object.

    Methods:
        play(path): Plays the audio file located at the given path.
        stop(): Stops the audio playback and closes the audio stream.
    """

    def __init__(self):
        self.chunk = 1024
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.f = None

    def play(self, path):
        """
        Plays the audio file located at the given path.

        Args:
            path (str): The path to the audio file.

        Raises:
            FileNotFoundError: If the audio file is not found.
        """
        self.f = wave.open(path, "rb")
        self.stream = self.p.open(format=self.p.get_format_from_width(self.f.getsampwidth()),
                                  channels=self.f.getnchannels(),
                                  rate=self.f.getframerate(),
                                  output=True)
        data = self.f.readframes(self.chunk)
        while data:
            self.stream.write(data)
            data = self.f.readframes(self.chunk)

        sleep(0.5)

        self.stream.stop_stream()
        self.stream.close()
        self.f.close()

    def stop(self):
        """
        Stops the audio playback and closes the audio stream.
        """
        if not self.stream.is_stopped:
            self.stream.stop_stream()
        if self.stream.is_active:
            self.stream.close()
        if self.f is not None:
            self.f.close()
        self.p.terminate()  # close PyAudio
