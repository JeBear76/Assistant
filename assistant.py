from audio import Audio
from record import Recorder
from deepgramCommunication import DeepgramAssistant
from groqCommunication import GroqAssistant
import logging

logger = logging.getLogger(__name__)
class Assistant:
    def __init__(self, config, regenerateGreeting, DEBUG=False):
        self.DEBUG = DEBUG
        self.deepgramAssistant = DeepgramAssistant(voice=config.voice)
        if regenerateGreeting:
            self.deepgramAssistant.speak(config.greeting, './greet.wav')        
        self.audio = Audio()
        self.rec = Recorder(config.device)
        self.groqAssistant = GroqAssistant(self.DEBUG)

    def greet(self):
        self.audio.play('./greet.wav')        

    def record_audio(self, filename='./output.wav'):
        self.audio.play('./assets/ready.wav')
        self.rec.record(filename=filename)
        return filename

    def transcribe_audio(self, filename):
        response = self.deepgramAssistant.listen(filename=filename)
        chatMessage = response.results.channels[0].alternatives[0].transcript
        if self.DEBUG:
            print(chatMessage)
        return chatMessage

    def process_message(self, chatMessage):
        assistantMessage = self.groqAssistant.chat(chatMessage)
        if self.DEBUG:
            print(assistantMessage)
        return assistantMessage

    def speak_response(self, assistantMessage):
        self.deepgramAssistant.speak(assistantMessage)
        self.audio.play('./talk.wav')

    def mainLoop(self):
        try:
            self.initialize()
            filename = self.record_audio()
            chatMessage = self.transcribe_audio(filename)
            assistantMessage = self.process_message(chatMessage)
            self.speak_response(assistantMessage)
        except Exception as e:
            logger.exception(e)
            print(e)

