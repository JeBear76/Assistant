import os
from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions, FileSource
import logging
logger = logging.getLogger(__name__)

preRecordedOptions = PrerecordedOptions(
    model='nova-2',            
    smart_format=True
    )

speakOptions = SpeakOptions(
    model='aura-asteria-en', 
    encoding='linear16', 
    container='wav'
    )

class DeepgramAssistant:
    """
    A class that represents a Deepgram Assistant.

    Attributes:
        client (DeepgramClient): The Deepgram client used for communication.
        Debug (bool): A flag indicating whether debug mode is enabled.

    Methods:
        __init__(self, DEBUG=False, voice="aura-asteria-en"): Initializes a new instance of the DeepgramAssistant class.
        changeVoice(self, voice): Changes the voice model used for speech synthesis.
        speak(self, message, filename='./talk.wav'): Generates speech from the given message and saves it to a file.
        listen(self, filename): Transcribes the audio from the given file.

    """

    def __init__(self, DEBUG=False, voice="aura-asteria-en"):
        """
        Initializes a new instance of the DeepgramAssistant class.

        Args:
            DEBUG (bool, optional): A flag indicating whether debug mode is enabled. Defaults to False.
            voice (str, optional): The voice model to use for speech synthesis. Defaults to "aura-asteria-en".
        """
        self.client = DeepgramClient(api_key=os.getenv('DEEPGRAM_API_KEY'))
        speakOptions.model = voice
        self.Debug=DEBUG

    def changeVoice(self, voice):
        """
        Changes the voice model used for speech synthesis.

        Args:
            voice (str): The voice model to use.
        """
        logger.info(f"Changing voice to {voice}")
        speakOptions.model = voice
        
    def speak(self, message, filename='./talk.wav'):
        """
        Generates speech from the given message and saves it to a file.

        Args:
            message (str): The message to convert to speech.
            filename (str, optional): The filename to save the speech to. Defaults to './talk.wav'.

        Returns:
            response: The response object from the Deepgram API.
        """
        logger.info(f"Speaking: {message}")
        speakSource = {
            "text": message
        }
        response = self.client.speak.v('1').save(filename, speakSource, speakOptions)
        logger.info(f"Speech saved response:\n{response.to_json(indent=2)}")
        if self.Debug:
            print(response.to_json(indent=2))

        return response

    def listen(self, filename):        
        """
        Transcribes the audio from the given file.

        Args:
            filename (str): The filename of the audio file to transcribe.

        Returns:
            response: The response object from the Deepgram API.
        """
        logger.info(f"Listening to {filename}")
        with open(filename, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        response = self.client.listen.prerecorded.v("1").transcribe_file(payload, preRecordedOptions)
        logger.info(f"Transcription response:\n{response.to_json(indent=2)}")
        if self.Debug:
            print(response.to_json(indent=2))

        return response