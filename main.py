#building yourself? use "PyInstaller main.spec"

import os
import random
import keyboard
import tkinter as tk
import threading
import sounddevice as sd
import soundfile as sf

from modules.screenManager import MainScreen, SoundErrorScreen, resource_path
from modules.config import *

if not os.path.exists(soundPath):
    os.makedirs(soundPath)

loop = True

#soundboard processes
def run():
    global loop
    loop = True
    counter = 0
    while loop:
        try: #fallback for loop, check that the program is still running
            root.winfo_exists()
        except:
            print("Window closed, exiting")
            break
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            counter += 1
            print(counter,"/",settings["maxClicks"])
            if counter == settings["maxClicks"]:
                counter = 0
                data, samplerate = sf.read(soundPath+soundList[random.randint(0,len(soundList)-1)], dtype='float32')
                sd.play(data, samplerate, device=deviceList[settings["currentDevice"]])
            

#global window settings
root.title('Ranboard')
root.minsize(width=512,height=512)
root.resizable(False,False)
root.iconbitmap(resource_path("Ranboard.ico"))

if __name__ == '__main__':
    #attempt to close splash screen (import only exists in packaged form)
    try:
        import pyi_splash # type: ignore
        pyi_splash.close()
    except:
        pass

    #choosing screen
    if len(soundList) == 0:
        SoundErrorScreen(root)
    else:
        MainScreen(root)
        t1 = threading.Thread(target=run) #start sounds
        t1.start()
    
    root.mainloop()