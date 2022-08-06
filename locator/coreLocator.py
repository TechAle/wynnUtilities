import json
import threading
import time

import api
from utils import fileUtils


class locatorCore:
    def __init__(self, mainThread):
        # Init api
        self.wynnApi = api.WynnPy.wynnPy()
        # Mainthread
        self.mainThread = mainThread
        # If the stalker is running
        self.on = self.running = False
        # Load
        self.loadInformations()

    def loadInformations(self):
        data = fileUtils.readConfigFile()
        self.target = data["locator"]["player"]

    def startLocatorThread(self):
        threading.Thread(target=self.startLocating).start()

    def startLocating(self):
        self.on = self.running = True
        oldCoords = {
            "x" : 0,
            "y" : 0,
            "z" : 0
        }
        listPoints = []
        while self.on and self.mainThread.is_alive():
            playersFound = self.wynnApi.getLocations()
            foundPlayer = None
            for player in playersFound:
                if player["name"] == self.target:
                    foundPlayer = player
                    break
            if foundPlayer is not None:
                if oldCoords["x"] != foundPlayer["x"] or oldCoords["y"] != foundPlayer["y"] or oldCoords["z"] != foundPlayer["z"]:
                    oldCoords = {
                        "x" : foundPlayer["x"],
                        "y": foundPlayer["y"],
                        "z": foundPlayer["z"]
                    }
                    listPoints.append(oldCoords)
            time.sleep(5)
        output = {
            "points": listPoints,
            "chests": [],
            "notes": [],
            "date": "Aug 6, 2022 3:24:01 AM"
        }
        fileUtils.createDirectoryIfNotExists("locator/results")
        with open('./locator/results/'+self.target+'.json', 'w') as fp:
            json.dump(output, fp)

