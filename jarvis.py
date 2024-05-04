import json
import os
from dotenv import load_dotenv

with open('config.json') as config_file:
    config = json.load(config_file)

config_file.close()

deepGramApiKey = config["deepGramApiKey"]

print(f'key: {deepGramApiKey}')

load_dotenv()

print(os.getenv('DEEPGRAM_API_KEY'))