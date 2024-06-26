import os
from groq import Groq
import logging
logger = logging.getLogger(__name__)

from utils import prettyDict

class GroqAssistant:
    """
    A class representing a Groq Assistant.

    Attributes:
        Debug (bool): A flag indicating whether debug mode is enabled.
        client (Groq): An instance of the Groq client.

    Methods:
        chat(message): Sends a chat message to the Groq Assistant and returns the response.

    """

    def __init__(self, DEBUG=False):
        """
        Initializes a new instance of the GroqAssistant class.

        Args:
            DEBUG (bool, optional): A flag indicating whether debug mode is enabled. Defaults to False.

        """
        self.Debug = DEBUG
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )
        self.conversationMessages = [
                {
                    "role": "system",
                    "content": "you are a helpful assistant. you will limit your answer to the necessary information and not provide any unnecessary information."
                }
            ]

    def chat(self, message):
        """
        Sends a chat message to the Groq Assistant and returns the response.

        Args:
            message (str): The message to send to the Groq Assistant.

        Returns:
            str: The response from the Groq Assistant.

        """
        logger.info(f"Sending chat message: {message}")
        
        self.conversationMessages.append(
            {
                "role": "user",
                "content": message
            }
        )
        
        chat_completion = self.client.chat.completions.create(
            messages=self.conversationMessages,
            model="mixtral-8x7b-32768",
            max_tokens=256,
            temperature=1.0,
            top_p=1.0,
        )
        
        logger.info(f"Received chat response:\n{chat_completion}")
        
        if self.Debug:
            print(chat_completion)
        
        self.conversationMessages.append(
            {
                "role": "assistant",
                "content": chat_completion.choices[0].message.content
            }
        )
        return chat_completion.choices[0].message.content
