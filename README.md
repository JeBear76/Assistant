# Assistant

Ask it questions and it'll answer.


## APIs
- [deepgram](https://deepgram.com/)
- [groq](https://groq.com/)

## Getting Started
In your working directory, create a **.env** file and add the following lines to it
```
DEEPGRAM_API_KEY=<your deepgram api key>
GROQ_API_KEY=<your groq api key>
```
  
Run 
```
    source ./venv/bin/activate
    python ./assistant-gui.py
```

## Python dependencies
- `sudo apt install python3-dotenv`
- `sudo apt-get install python3-pyaudio`
- `pip install python-dotenv`
- `sudo apt install python3-tk`
- `pip install customtkinter`
- `pip install pillow`
- `pip install python-dotenv`
- `pip install deepgram-sdk`
- `pip install pygobject`
- `pip install wavio`
- `pip install soundfile`
- `pip install sounddevice`
- `pip install groq`
- `pip install pynput`

## Pulse Audio Setup for WLS2

### Install PulseAudio on Windows
Don't start the service at the end of these instructions before completing the pulseAudio configuration in the next step.
[follow these instructions](https://gist.github.com/Stormwind99/e5ffc026a44ec2374f92864652d94854)  

### Configure pulseAudio on Windows
- Change **etc\pulse\default.pa**
    - _load-module module-waveout sink_name=output source_name=input record=0_
    - _load-module module-native-protocol-tcp auth-ip-acl=172.0.0.0/12_ 
    or  
    - _load-module module-native-protocol-tcp auth-anonymous=true_
The second option is un-secure but if you're playing in your house, that shouldn't be an issue.

- Change **etc\pulse\deamon.conf**
    - _exit-idle-time = -1_

### Configure sound on the WSL2 instance
- On WSL2 Ubuntu 22.04/24.04 (Those are the only 2 I've played with)
    - `sudo apt update`
    - `sudo apt install libpulse0 pulseaudio`
    - `export PULSE_SERVER=tcp:$(grep nameserver /etc/resolv.conf | awk '{print $2}');`


## Microphone Setup for WLS2
Summary of [Microsoft Learn Article](https://learn.microsoft.com/en-us/windows/wsl/connect-usb)
- In PowerShell, `winget install --interactive --exact dorssel.usbipd-win`
- In an elevated Powershell `usbopd bind --busid <busid of the mic/camera>`
    - _--force_ may be needed
- In PowerShell, 
    - `usbipd list` to confirm sharing
    - `usbipd attach --wsl --busid <busid of the mic/camera>`
- On WSL2 Ubuntu 22.04 `lsusb` to confirm that the device is here