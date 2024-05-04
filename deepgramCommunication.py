import os
from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions, FileSource

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
    def __init__(self, DEBUG=False, voice="aura-asteria-en"):
        self.client = DeepgramClient(api_key=os.getenv('DEEPGRAM_API_KEY'))
        speakOptions.model = voice
        self.Debug=DEBUG

    def changeVoice(self, voice):
        speakOptions.model = voice
        
    def speak(self, message, filename='./talk.wav'):
        speakSource = {
            "text": message
        }
        response = self.client.speak.v('1').save(filename, speakSource, speakOptions)
        if self.Debug:
            print(response.to_json(indent=2))

        return response

    def listen(self, filename):        
        with open(filename, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        response = self.client.listen.prerecorded.v("1").transcribe_file(payload, preRecordedOptions)
        if self.Debug:
            print(response.to_json(indent=2))

        return response