import argparse
import logging
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
from audio import Audio
from record import Recorder, selectMicrophone
from deepgramCommunication import DeepgramAssistant
from groqCommunication import GroqAssistant

DEFAULT_GREETING = 'What do you want? I\'m busy!'
DEFAULT_VOICE = 'aura-helios-en'

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-s', '--select_device', action='store_const', const=1,
    help='select a device from a list of audio devices'
)
parser.add_argument(
    '-v', '--voice', action='store', default=DEFAULT_VOICE,
    help='change the voice to the assistant'
)
parser.add_argument(
    '-g', '--greet', action='store', default=DEFAULT_GREETING,
    help='change the assistant\'s greeting message'
)
args, remaining = parser.parse_known_args()


load_dotenv()


def main():
    """
    The main function of the Jarvis program.
    
    This function performs the following steps:
    1. Initializes the DeepgramAssistant with a default voice.
    2. Changes the voice if specified by the user.
    3. Plays a greeting message.
    4. Prompts the user to select a microphone device.
    5. Records audio from the selected microphone.
    6. Uses DeepgramAssistant to transcribe the recorded audio.
    7. Passes the transcribed message to GroqAssistant for processing.
    8. Uses DeepgramAssistant to speak the response from GroqAssistant.
    9. Plays the response audio.
    
    Note: This function assumes the existence of the following classes:
    - DeepgramAssistant: A class for interacting with the Deepgram speech recognition API.
    - Audio: A class for playing audio files.
    - Recorder: A class for recording audio from a microphone.
    - GroqAssistant: A class for processing user queries and generating responses.
    """
    try:
        logging.basicConfig(filename='./assistant.log',level=logging.INFO)
        DEBUG = False
        deepgramAssistant = DeepgramAssistant(voice=DEFAULT_VOICE)
        
        if args.voice != DEFAULT_VOICE or args.greet != DEFAULT_GREETING:
            greeting = args.greet
            deepgramAssistant.changeVoice(args.voice)           
            deepgramAssistant.speak(greeting, './greet.wav')

        audio = Audio()
        audio.play('./greet.wav')
        device = 1
        if args.select_device == 1:
            device = selectMicrophone()

        rec = Recorder(device)
        groqAssistant = GroqAssistant(DEBUG)

        # Record the audio
        filename = './output.wav'
        rec.record(filename=filename)
        
        # For Testing - Play the 'output.wav' file
        if DEBUG:
            print('Playing')
            audio.play(filename)

        response = deepgramAssistant.listen(filename=filename)

        chatMessage = response.results.channels[0].alternatives[0].transcript
        if DEBUG:
            print(chatMessage)
        
        assistantMessage = groqAssistant.chat(chatMessage)
        if DEBUG:
            print(assistantMessage)

        deepgramAssistant.speak(assistantMessage)
        audio.play('./talk.wav')
    except Exception as e:
        logger.exception(e)
        print(e)

if __name__ == "__main__":
    main()
    parser.exit(0)