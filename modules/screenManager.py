import os
import sys
import random
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sounddevice as sd
import soundfile as sf
import pywinstyles

from .config import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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

class MainScreen:
    #build screen layout
    def __init__(self, root):
        self.root = root
        self.soundPath = soundPath
        self.soundList = soundList
        self.deviceList = deviceList
        self.selectedDeviceTK = tk.StringVar()

        self.frame1 = ttk.LabelFrame(self.root,text="Ranboard")
        self.root.img = ImageTk.PhotoImage(Image.open(resource_path("ranboard-short.png")).resize((200,100)))
        self.logo= tk.Label(self.frame1, image = self.root.img)
        self.inFrame1 = ttk.Frame(self.frame1)
        self.testButton = ttk.Button(self.inFrame1, text='Test', style='Accent.TButton', width=15, command=self.test)
        self.stopBtn = ttk.Button(self.inFrame1, text='Stop', style='Accent.TButton', width=15, command=self.kill)
        self.frame1.grid(column=0,row=0,columnspan=2,rowspan=1,padx=(20, 10), pady=(20, 10),sticky="nesw")

        #sounds and file button
        self.frame2 = ttk.LabelFrame(self.root,text="Sounds")
        self.soundAmt = ttk.Label(self.frame2, text=str(len(self.soundList))+ " sounds detected")
        self.folderTxt = ttk.Label(self.frame2, text="Add sounds as mp3 files here:")
        self.folderBtn = ttk.Button(self.frame2, text='Open Folder', style='Accent.TButton', width=25, command=self.openSoundFolder)
        self.frame2.grid(column=0,row=1,columnspan=2,rowspan=1,padx=(20, 10), pady=(20, 10),sticky="nesw")

        #trigger settings
        self.frame3 = ttk.LabelFrame(self.root,text="Trigger Settings")
        self.triggerTxt = ttk.Label(self.frame3, text="Number of keyboard clicks per sound:")
        self.inFrame3 = ttk.Frame(self.frame3)
        self.triggerEntry = ttk.Entry(self.inFrame3)
        self.triggerEntry.insert(0,settings["maxClicks"])
        self.triggerSetBtn = ttk.Button(self.inFrame3, text='Set', style='Accent.TButton', width=10, command=self.changeTriggerAmt)
        self.frame3.grid(column=0,row=2,columnspan=2,rowspan=1,padx=(20, 10), pady=(20, 10),sticky="nesw")

        #device settings
        self.frame4 = ttk.LabelFrame(self.root,text="Sound Device")
        self.soundOutput = ttk.OptionMenu(self.frame4, self.selectedDeviceTK, *self.deviceList.keys())
        self.selectedDeviceTK.set(settings["currentDevice"])
        self.selectedDeviceTK.trace_add("write", setDevice) #changes settings["currentDevice"]
        self.frame4.grid(column=0,row=3,columnspan=2,rowspan=1,padx=(20, 10), pady=(20, 10),sticky="nesw")

        self.logo.pack()
        self.inFrame1.pack()
        self.testButton.pack(side="left",padx=5)
        self.stopBtn.pack(side="left",padx=5)
        self.soundAmt.pack()
        self.folderTxt.pack(pady=10)
        self.folderBtn.pack()
        self.triggerTxt.pack()
        self.inFrame3.pack()
        self.triggerEntry.pack(side="left")
        self.triggerSetBtn.pack(side="left")
        self.soundOutput.pack()

        self.root.grid_columnconfigure(0,weight=1,)
        self.root.grid_rowconfigure(list(range(4)),weight=1)

        #theming
        self.root.tk.call('source', resource_path('theme/forest-dark.tcl'))
        ttk.Style().theme_use('forest-dark')
        apply_theme_to_titlebar(self.root)
    #button callbacks
    def kill(self):
        save() #saves current settings
        global loop
        self.root.destroy()
        loop = False
    def openSoundFolder(self):
        os.startfile(self.soundPath)
    def changeTriggerAmt(self):
        self.frame1.focus() #removes focus from entry
        try:
            settings["maxClicks"] = int(self.triggerEntry.get())
            print(settings["maxClicks"])
        except:
            self.triggerEntry.delete(0,tk.END)
            self.triggerEntry.insert(0,settings["maxClicks"])
        save()
    def test(self):
        data, samplerate = sf.read(self.soundPath+self.soundList[random.randint(0,len(self.soundList)-1)], dtype='float32')
        sd.play(data, samplerate, device=self.deviceList[settings["currentDevice"]])

class SoundErrorScreen:
    def __init__(self, root):
        self.root = root
        self.path = soundPath
        self.frame2 = ttk.LabelFrame(self.root,text="Sounds")
        self.folderTxt = ttk.Label(self.frame2, text="No sound files detected, add sounds as\nmp3 files here and restart:",justify="center")
        self.folderBtn = ttk.Button(self.frame2, text='Open Folder', style='Accent.TButton', width=25, command=self.openSoundFolder)
        self.frame2.grid(column=0,row=0,columnspan=2,rowspan=1,padx=(20, 10), pady=(20, 10),sticky="nesw")

        self.folderTxt.pack(pady=(50, 1))
        self.folderBtn.pack()

        self.root.grid_columnconfigure(0,weight=1,)
        self.root.grid_rowconfigure(list(range(4)),weight=1)

        #theming
        self.root.tk.call('source', resource_path('theme/forest-dark.tcl'))
        ttk.Style().theme_use('forest-dark')
        apply_theme_to_titlebar(self.root)
    
    def openSoundFolder(self):
            os.startfile(soundPath)