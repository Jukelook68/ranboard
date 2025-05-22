import os
import keyboard
import mouse
import random
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import threading
import sys
import pywinstyles
import sounddevice as sd
import soundfile as sf

path = os.getenv('APPDATA') + "\\ranboard\\sounds\\"
if not os.path.exists(path):
    os.makedirs(path)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            counter += 1
            print(counter,"/",maxclicks)
            if counter == maxclicks:
                counter = 0
                data, samplerate = sf.read(path+dir_list[random.randint(0,len(dir_list)-1)], dtype='float32')
                sd.play(data, samplerate, device=options[selectOutput.get()])
            

#window settings
root = tk.Tk()
root.title('Ranboard')
root.minsize(width=512,height=512)
root.resizable(False,False)

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
        def test():
            data, samplerate = sf.read(path+dir_list[random.randint(0,len(dir_list)-1)], dtype='float32')
            sd.play(data, samplerate, device=options[selectOutput.get()])
            
        #main frame, stop button
        frame1 = ttk.LabelFrame(root,text="Ranboard")
        root.img = ImageTk.PhotoImage(Image.open(resource_path("ranboard-short.png")).resize((200,100)))
        logo= tk.Label(frame1, image = root.img)
        inFrame1 = ttk.Frame(frame1)
        testButton = ttk.Button(inFrame1, text='Test', style='Accent.TButton', width=15, command=test)
        stopBtn = ttk.Button(inFrame1, text='Stop', style='Accent.TButton', width=15, command=kill)
        frame1.grid(column=0,row=0,columnspan=2,rowspan=1,padx=(20, 10), pady=(20, 10),sticky="nesw")

        #sounds and file button
        frame2 = ttk.LabelFrame(root,text="Sounds")
        soundAmt = ttk.Label(frame2, text=str(len(dir_list))+ " sounds detected")
        folderTxt = ttk.Label(frame2, text="Add sounds as mp3 files here:")
        folderBtn = ttk.Button(frame2, text='Open Folder', style='Accent.TButton', width=25, command=openSoundFolder)
        frame2.grid(column=0,row=1,columnspan=2,rowspan=1,padx=(20, 10), pady=(20, 10),sticky="nesw")

        #trigger settings
        frame3 = ttk.LabelFrame(root,text="Trigger Settings")
        triggerTxt = ttk.Label(frame3, text="Number of keyboard clicks per sound:")
        inFrame3 = ttk.Frame(frame3)
        triggerEntry = ttk.Entry(inFrame3)
        triggerEntry.insert(0,maxclicks)
        triggerSetBtn = ttk.Button(inFrame3, text='Set', style='Accent.TButton', width=10, command=changeTriggerAmt)
        frame3.grid(column=0,row=2,columnspan=2,rowspan=1,padx=(20, 10), pady=(20, 10),sticky="nesw")

        #device settings
        frame4 = ttk.LabelFrame(root,text="Sound Device")
        soundOutput = ttk.OptionMenu(frame4, selectOutput, *options.keys())
        selectOutput.set(sd.query_devices()[sd.default.device[1]]["name"])
        frame4.grid(column=0,row=3,columnspan=2,rowspan=1,padx=(20, 10), pady=(20, 10),sticky="nesw")

        logo.pack()
        inFrame1.pack()
        testButton.pack(side="left",padx=5)
        stopBtn.pack(side="left",padx=5)
        soundAmt.pack()
        folderTxt.pack(pady=10)
        folderBtn.pack()
        triggerTxt.pack()
        inFrame3.pack()
        triggerEntry.pack(side="left")
        triggerSetBtn.pack(side="left")
        soundOutput.pack()

        root.grid_columnconfigure(0,weight=1,)
        root.grid_rowconfigure(list(range(4)),weight=1)

        #theming
        root.tk.call('source', resource_path('forest-dark.tcl'))
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
        root.tk.call('source', resource_path('forest-dark.tcl'))
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
    try:
        import pyi_splash # type: ignore
        pyi_splash.close()
    except:
        pass
    ##choosing layout
    if len(dir_list) == 0:
        layouts.missingSounds()
    else:
        layouts.mainScreen()
        t1 = threading.Thread(target=run) #start sounds
        t1.start()
    
    root.mainloop()