import os
import playsound
import keyboard
import mouse
import random
import tkinter as tk
from tkinter import ttk
from multiprocessing import Process
import threading
import sv_ttk
import sys
import pywinstyles
import sounddevice as sd
import soundfile as sf

path = os.getenv('APPDATA') + "\\ranboard\\sounds\\"
if not os.path.exists(path):
    os.makedirs(path)

dir_list = os.listdir(path)
loop = True
maxclicks = 100
triggerKey = "w"
soundApi = "MME"

options = {}
for device in sd.query_devices():
    if int(device["max_output_channels"]) > 0 and sd.query_hostapis()[device["hostapi"]]["name"] == soundApi:
        options.update({str(device["name"]): int(device["index"])})

#soundboard processes
def run():
    global maxclicks
    global loop
    loop = True
    counter = 0
    while loop:
        try: #fallback for loop, check that the program is still running
            root.winfo_exists()
        except:
            print("Window closed, exiting")
            break
        keyboard.wait(triggerKey)
        counter += 1
        print(counter,"/",maxclicks)
        if counter == maxclicks:
            counter = 0
            data, samplerate = sf.read(path+dir_list[random.randint(0,len(dir_list)-1)], dtype='float32')
            sd.play(data, samplerate, device=options[selectOutput.get()])

#window settings
root = tk.Tk()
root.title('Ranboard')
root.minsize(width=256,height=256)

selectOutput = tk.StringVar()

class layouts:
    def mainScreen():
        def kill():
            global loop
            root.destroy()
            loop = False

        def openSoundFolder():
            os.startfile(path)

        def changeTriggerAmt():
            global maxclicks
            frame1.focus() #removes focus from entry
            try:
                maxclicks = int(triggerEntry.get())
                print(maxclicks)
            except:
                triggerEntry.delete(0,tk.END)
                triggerEntry.insert(0,maxclicks)
        frame1 = ttk.LabelFrame(root,text="Ranboard")
        stopBtn = ttk.Button(frame1, text='Stop', width=25, command=kill)
        frame1.grid(column=0,row=0,columnspan=1,rowspan=1,padx=(20, 10), pady=(20, 10))

        frame2 = ttk.LabelFrame(root,text="Sounds")
        soundAmt = ttk.Label(frame2, text=str(len(dir_list))+ " sounds detected")
        folderTxt = ttk.Label(frame2, text="Add sounds as mp3 files here:")
        folderBtn = ttk.Button(frame2, text='Open Folder', width=25, command=openSoundFolder)
        frame2.grid(column=0,row=1,columnspan=1,rowspan=1,padx=(20, 10), pady=(20, 10))

        frame3 = ttk.LabelFrame(root,text="Triggering")
        triggerTxt = ttk.Label(frame3, text="Number of clicks per sound:")
        triggerEntry = ttk.Entry(frame3)
        triggerEntry.insert(0,maxclicks)
        triggerSetBtn = ttk.Button(frame3, text='Set', width=10, command=changeTriggerAmt)
        frame3.grid(column=0,row=2,columnspan=1,rowspan=1,padx=(20, 10), pady=(20, 10))

        frame4 = ttk.LabelFrame(root,text="Sound Device")
        soundOutput = ttk.OptionMenu(frame4, selectOutput, *options.keys())
        selectOutput.set(sd.query_devices()[sd.default.device[1]]["name"])
        frame4.grid(column=0,row=3,columnspan=1,rowspan=1,padx=(20, 10), pady=(20, 10))

        stopBtn.pack()
        soundAmt.pack()
        folderTxt.pack()
        folderBtn.pack()
        triggerTxt.pack()
        triggerEntry.pack(side=tk.LEFT)
        triggerSetBtn.pack(side=tk.LEFT)
        soundOutput.pack()

        #theming
        root.tk.call('source', 'forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')
        apply_theme_to_titlebar(root)

    def missingSounds():
        def openSoundFolder():
            os.startfile(path)

        folderTxt = ttk.Label(root, text="No sound files detected, add sounds as\nmp3 files here and restart:",justify="center")
        folderBtn = ttk.Button(root, text='Open Folder', width=25, command=openSoundFolder)

        folderTxt.pack(pady=(50, 1))
        folderBtn.pack()

        #theming
        root.tk.call('source', 'forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')
        apply_theme_to_titlebar(root)
        
def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#313131")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

if __name__ == '__main__':
    ##choosing layout
    if len(dir_list) == 0:
        layouts.missingSounds()
    else:
        layouts.mainScreen()
        t1 = threading.Thread(target=run) #start sounds
        t1.start()
    
    root.mainloop()