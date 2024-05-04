import argparse
from dotenv import load_dotenv
from audio import Audio
from record import Recorder, selectMicrophone
from deepgramCommunication import DeepgramAssistant
from groqCommunication import GroqAssistant

# from pynput import keyboard

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-s', '--select_device', action='store_const', const=1,
    help='select a device from a list of audio devices')
args, remaining = parser.parse_known_args()

load_dotenv()

# def on_activate_h():
#     print('<ctrl>+<alt>+h pressed')

# def on_activate_i():
#     print('<ctrl>+<alt>+i pressed')
        
# with keyboard.GlobalHotKeys({
        #         '<ctrl>+<alt>+h': on_activate_h,
        #         '<ctrl>+<alt>+i': on_activate_i}) as h:
        #     h.join()

def main():
    try:
        DEBUG = False
        greeting = 'What do you want? I\'m busy!'
        deepgramAssistant = DeepgramAssistant(voice="aura-helios-en")
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
        
        groqResponse = groqAssistant.chat(chatMessage)
        if DEBUG:
            print(groqResponse)

        deepgramAssistant.speak(groqResponse)
        audio.play('./talk.wav')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
    parser.exit(0)