import os
import json
import tkinter as tk
from pathlib import Path
import sounddevice as sd

#determined by app
soundPath = os.getenv('APPDATA') + "\\ranboard\\sounds\\"
settingsPath = Path(os.getenv('APPDATA') + "\\ranboard\\settings.json")
soundList = os.listdir(soundPath)
deviceList = {}
root = tk.Tk()

#variable
defaults = {
        "soundAPI": "MME", #not customisable in app, never needs to change for most users
        "maxClicks": 100,
        "currentDevice": sd.query_devices()[sd.default.device[1]]["name"]
        }

settings = defaults #changes once loaded

#creates default settings if non existant
if not settingsPath.is_file():
    with open(settingsPath, "x+") as file:
        json.dump(defaults, file)
        file.close()

#loads saved settings
with open(settingsPath, mode="r", encoding="utf-8") as file:
    settings = json.load(file)    
    file.close()

for device in sd.query_devices():
    if int(device["max_output_channels"]) > 0 and sd.query_hostapis()[device["hostapi"]]["name"] == settings["soundAPI"]:
        deviceList.update({str(device["name"]): int(device["index"])})

def save(): #should be called whenever any settings change, so most callbacks
    with open(settingsPath, "w+") as file:
        json.dump(settings, file)
        file.close()

def setDevice(varname, *args):
    #varname is an identifier used to find the var
    settings["currentDevice"] = root.getvar(varname)
    save()