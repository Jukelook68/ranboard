#building yourself? use "PyInstaller main.spec"

import os
import random
import keyboard
import tkinter as tk
import threading
import sounddevice as sd
import soundfile as sf

from modules.screenManager import MainScreen, SoundErrorScreen, resource_path
from modules.config import settings, globals

settings = settings()

globals.path = os.getenv('APPDATA') + "\\ranboard\\sounds\\"
if not os.path.exists(globals.path):
    os.makedirs(globals.path)

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
                sd.play(data, samplerate, device=globals.options[globals.selectOutput.get()])
            

#global window settings
root = tk.Tk()
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
    if len(globals.dir_list) == 0:
        SoundErrorScreen(root)
    else:
        MainScreen(root)
        t1 = threading.Thread(target=run) #start sounds
        t1.start()
    
    root.mainloop()