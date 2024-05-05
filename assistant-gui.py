from dotenv import load_dotenv
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from pynput import keyboard
import argparse
import logging

from assistant import Assistant
import json

logger = logging.getLogger(__name__)

load_dotenv()

def on_activate_h():
     print('<ctrl>+<alt>+h pressed')

def on_activate_i():
     print('<ctrl>+<alt>+i pressed')
        
hk = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+h': on_activate_h,
        '<ctrl>+<alt>+i': on_activate_i})
hk.start()

def Resize_Image(image, maxsize):
    r1 = image.size[0]/maxsize[0] # width ratio
    r2 = image.size[1]/maxsize[1] # height ratio
    ratio = max(r1, r2)
    newsize = (int(image.size[0]/ratio), int(image.size[1]/ratio))
    image = image.resize(newsize)
    return image

class CustomUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        # Add your customizations here
        self.title("Jebear's Assistant")
        self.geometry("400x300")
        
        micIconImg = Image.open('./assets/mic-icon.png')
        micIconImg = Resize_Image(micIconImg, (240, 240))
        self.micIcon = ImageTk.PhotoImage(micIconImg)
        ctk.CTkButton(self, image=self.micIcon, text='').grid(row=1, column=1, sticky="nsew")
        # Create and add your custom widgets here
        label = tk.Label(self, text="Hello, Custom UI!").grid(row=0, column=0, columnspan=3, sticky="nsew")

if __name__ == "__main__":
    logging.basicConfig(filename='./assistant.log',level=logging.INFO)
    with open('config.json') as config_file:
        config = json.load(config_file)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-s', '--select_device', action='store_const', const=1,
        help='select a device from a list of audio devices'
    )
    parser.add_argument(
        '-v', '--voice', action='store', default=config.voice,
        help='change the voice to the assistant'
    )
    parser.add_argument(
        '-g', '--greet', action='store', default=config.greeting,
        help='change the assistant\'s greeting message'
    )
    args, remaining = parser.parse_known_args()

    regenerateGreeting=False
    if(args.greet != config['greeting']):
        config['greeting'] = args.greet
        regenerateGreeting=True
    if(args.voice != config['voice']):
        config['voice'] = args.voice
        regenerateGreeting=True

    if regenerateGreeting:
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)

    assistant = Assistant(config, regenerateGreeting, DEBUG=False)

    app = CustomUI()
    app.mainloop()