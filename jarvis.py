import os
import argparse
import sounddevice as sd

from dotenv import load_dotenv
from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions, FileSource
from audio import Audio
from record import Recorder, selectMicrophone

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-s', '--select_device', action='store_const', const=1,
    help='select a device from a list of audio devices')
args, remaining = parser.parse_known_args()

load_dotenv()

freq = 44100    # Sample frequency

key = os.getenv('DEEPGRAM_API_KEY')

speak_prompt = {"text": "Hello, how are you doing today?"}

def main():
    try:
        audio = Audio()
        device = 1
        
        # # Play the 'talk.wav' file
        # audio.play('./talk.wav')
        if args.select_device == 1:
            device = selectMicrophone()

        print(f'key:{key}')

        while True:
                
        # Record the audio
        rec = Recorder(device)
        rec.record()
        # Play the 'output.wav' file
        print('Playing')
        audio.play('./output.wav')

        client = DeepgramClient(api_key=key)
        
        preRecordedOptions = PrerecordedOptions(
            model='nova-2',            
            smart_format=True
            )

        speakOptions = SpeakOptions(
            model='aura-asteria-en', 
            encoding='linear16', 
            container='wav'
            )

        with open("./output.wav", "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        response = client.listen.prerecorded.v("1").transcribe_file(payload, preRecordedOptions)
        # response = client.speak.v('1').save('./talk.wav', speak_prompt, speakOptions)

        print(response.to_json(indent=2))

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
    parser.exit(0)