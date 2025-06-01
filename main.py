#building yourself? use "python -m PyInstaller main.spec"

import os
import keyboard
import random
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import threading
import sys
import pywinstyles
import sounddevice as sd
import soundfile as sf

from modules.screenManager import MainScreen, SoundErrorScreen
from modules.config import settings, globals

settings = settings()

globals.path = os.getenv('APPDATA') + "\\ranboard\\sounds\\"
if not os.path.exists(globals.path):
    os.makedirs(globals.path)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

globals.dir_list = os.listdir(globals.path)
loop = True

globals.options = {}
for device in sd.query_devices():
    if int(device["max_output_channels"]) > 0 and sd.query_hostapis()[device["hostapi"]]["name"] == settings.soundApi:
        globals.options.update({str(device["name"]): int(device["index"])})

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
            print(counter,"/",settings.maxclicks)
            if counter == settings.maxclicks:
                counter = 0
                data, samplerate = sf.read(globals.path+globals.dir_list[random.randint(0,len(globals.dir_list)-1)], dtype='float32')
                sd.play(data, samplerate, device=globals.options[MainScreen.selectOutput.get()])
            

#window settings
root = tk.Tk()
root.title('Ranboard')
root.minsize(width=512,height=512)
root.resizable(False,False)
root.iconbitmap(resource_path("Ranboard.ico"))

if __name__ == '__main__':
    try:
        import pyi_splash # type: ignore
        pyi_splash.close()
    except:
        pass
    ##choosing layout
    if len(globals.dir_list) == 0:
        SoundErrorScreen(root)
    else:
        MainScreen(root)
        t1 = threading.Thread(target=run) #start sounds
        t1.start()
    
    root.mainloop()