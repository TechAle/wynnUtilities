import threading
import time

import api.WynnPy
from api.classes.OptPlayerStats import optPlayerStats
from utils import fileUtils
from utils.askUtils import generalIntAsk
from utils.wynnUtils import getPlayerClasses, getLobbyPlayer
from utils.discordUtils import sendMessageWebhook


class checkerCore:
    def __init__(self, mainThread):
        # Init api
        self.wynnApi = api.WynnPy.wynnPy()
        # Mainthread
        self.mainThread = mainThread
        # If the stalker is running
        self.on = self.running = False
        # Ask informations
        self.loadPingList()
        self.loadInformations()

    def loadPingList(self):
        self.pingList = []
        fileUtils.createDirectoryIfNotExists("./checker/data")
        fileUtils.createFileIfNotExists("./checker/data/ping.txt")
        with open("./checker/data/ping.txt") as fp:
            Lines = fp.readlines()
            for line in Lines:
                if len(line := line.strip()) > 0:
                    self.pingList.append(line)

    # noinspection PyAttributeOutsideInit
    def loadInformations(self):
        data = fileUtils.readConfigFile()
        self.player = data["checker"]["player"]
        self.webhook = data["checker"]["webhook"]
        # Get player classes
        self.playerClasses = getPlayerClasses(self.wynnApi, self.player.strip())
        if self.playerClasses is None:
            return None
        # Print classes avaible
        askString = ""
        for idx, wynnClass in enumerate(self.playerClasses.characters):
            askString += "{}) {}, {}\n".format(idx + 1,
                                               wynnClass.name, wynnClass.combatLevel.level)
        askString += "Choose: "
        output = generalIntAsk(askString, len(self.playerClasses.characters)) - 1

        self.level = self.playerClasses.characters[output].combatLevel.level
        self.name = self.playerClasses.characters[output].name

    def updatePlayerInformations(self):
        # Get player classes
        playerClasses = getPlayerClasses(self.wynnApi, self.player.strip())
        # Update level
        for wynnClass in playerClasses:
            if wynnClass.name == self.name:
                self.level = wynnClass.combatLevel.level

    def startCheckerThread(self):
        if self.playerClasses is not None:
            threading.Thread(target=self.startChecking).start()
        else:
            print("You havent specified the player to be checked in the configuration file")

    def startChecking(self):
        lastLobby = ""
        playersChecked = []

        self.on = self.running = True
        while self.on and self.mainThread.is_alive():
            everyLobby = self.wynnApi.getServerList()
            lobbyPlayers, nowLobby = getLobbyPlayer(everyLobby, self.player)
            if lastLobby != nowLobby:
                playersChecked.clear()
            lastLobby = nowLobby
            for player in lobbyPlayers:
                if player != self.player and not playersChecked.__contains__(player):
                    possibleHunter, sureHunter = self.isHunter(player)
                    if possibleHunter:
                        sendMessageWebhook(
                            "Warning", "Possible hunter joined: " + player, self.webhook)
                playersChecked.append(player)
            time.sleep(60)

    def isHunter(self, player):
        statsPlayer = getPlayerClasses(self.wynnApi, player)

        if statsPlayer is None:
            return False

        found = False

        for classWynn in statsPlayer.characters:
            toAdd = optPlayerStats(classWynn, statsPlayer.timeStamp)
            if toAdd.combatLevel.level - 10 <= self.level <= toAdd.combatLevel.level + 10 \
                    and (toAdd.combatLevel.level >= 103 or toAdd.gamemode.hunted):
                if toAdd.gamemode.hunted:
                    return True, True
                else:
                    found = True
        return found
