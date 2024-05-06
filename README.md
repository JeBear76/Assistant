# Assistant
## APIs
- [deepgram](https://deepgram.com/)
- [groq](https://groq.com/)

## Getting Started
In your working directory, create a **.env** file and add the following lines to it
```
DEEPGRAM_API_KEY=<your deepgram api key>
GROQ_API_KEY=<your groq api key>
```

## Python dependencies
- `sudo apt install python3-dotenv`
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
- Download [PulseAudio](http://bosmans.ch/pulseaudio/pulseaudio-1.1.zip)
- Change **etc\pulse\default.pa**
    - _load-module module-waveout sink_name=output source_name=input record=0_
    - _load-module module-native-protocol-tcp auth-ip-acl=172.0.0.0/12_
- Change **etc\pulse\deamon.conf**
    - _exit-idle-time = -1_
- In PowerShell, `.\pulseAudio.exe`
- On WSL2 Ubuntu 22.04
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