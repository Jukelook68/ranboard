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

path = os.getenv('APPDATA') + "\\ranboard\\sounds\\"
if not os.path.exists(path):
    os.makedirs(path)

dir_list = os.listdir(path)
maxclicks = 100
triggerKey = "w"

#soundboard processes
def run():
    global maxclicks
    counter = 0
    while True:
        try:
            root.winfo_exists()
        except:
            print("Window closed, exiting")
            break
        keyboard.wait(triggerKey)
        counter += 1
        print(counter,"/",maxclicks)
        if counter == maxclicks:
            counter = 0
            playsound.playsound(path+dir_list[random.randint(0,len(dir_list)-1)])
#p1 = Process(target=run)

#button funtions
def kill():
    root.destroy()

def openSoundFolder():
    os.startfile(path)

def changeTriggerAmt():
    global maxclicks
    runTxt.focus() #removes focus from entry
    try:
        maxclicks = int(triggerEntry.get())
        print(maxclicks)
    except:
        triggerEntry.delete(0,tk.END)
        triggerEntry.insert(0,maxclicks)

#window settings
root = tk.Tk()
root.title('Ranboard')
root.minsize(width=256,height=184)

#layout
runTxt = ttk.Label(root, text="Ranboard is running, "+ str(len(dir_list))+ " sounds detected")
stopBtn = ttk.Button(root, text='Stop', width=25, command=kill)

folderTxt = ttk.Label(root, text="Add sounds as mp3 files here:")
folderBtn = ttk.Button(root, text='Open Folder', width=25, command=openSoundFolder)

triggerTxt = ttk.Label(root, text="Number of clicks per sound:")
triggerEntry = ttk.Entry(root)
triggerEntry.insert(0,maxclicks)
triggerSetBtn = ttk.Button(root, text='Set', width=10, command=changeTriggerAmt)


runTxt.pack()
stopBtn.pack()
folderTxt.pack()
folderBtn.pack()
triggerTxt.pack()
triggerEntry.pack(side=tk.LEFT)
triggerSetBtn.pack(side=tk.LEFT)

#theming
sv_ttk.use_dark_theme()
def apply_theme_to_titlebar(root): #from theme docs
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

# Example usage (replace `root` with the reference to your main/Toplevel window)
apply_theme_to_titlebar(root)

if __name__ == '__main__':
    t1 = threading.Thread(target=run)
    t1.start()
    root.mainloop()