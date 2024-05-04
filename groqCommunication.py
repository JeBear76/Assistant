
import os

from groq import Groq

from utils import prettyDict

class GroqAssistant:
    def __init__(self, DEBUG=False):
        self.Debug = DEBUG
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )

    def chat(self, message):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant. you will limit your answer to the necessary information and not provide any unnecessary information."
                },
                {
                    "role": "user",
                    "content": message,                    
                }
            ],
            model="mixtral-8x7b-32768",
            max_tokens=256,
            temperature=1.0,
            top_p=1.0,
        )
        if self.Debug:
            print(chat_completion)

        return chat_completion.choices[0].message.content
