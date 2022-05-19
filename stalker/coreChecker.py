import threading
import time

import api.WynnPy
from stalker.OptPlayerStats import optPlayerStats
from stalker.utils import fileUtils
from stalker.utils.askUtils import generalIntAsk
from stalker.utils.wynnUtils import getPlayerClasses, getLobbyPlayer
from stalker.utils.discordUtils import sendMessageWebhook


class checkerCore:
    def __init__(self, mainThread):
        # Init api
        self.wynnApi = api.WynnPy.wynnPy()
        # Mainthread
        self.mainThread = mainThread
        # If the stalker is running
        self.on = self.running = False
        # Ask informations
        self.askInformations()
        self.loadPingList()

    def loadPingList(self):
        self.pingList = []
        fileUtils.createDirectoryIfNotExists("data")
        fileUtils.createFileIfNotExists("data/ping.txt")
        with open("data/ping.txt") as fp:
            Lines = fp.readlines()
            for line in Lines:
                if len(line := line.strip()) > 0:
                    self.pingList.append(line)

    # noinspection PyAttributeOutsideInit
    def askInformations(self):
        self.player = input("Player: ")
        self.webhook = input("Webhook: ")
        # Get player classes
        playerClasses = getPlayerClasses(self.wynnApi, self.player.strip())
        # Print classes avaible
        askString = ""
        for idx, wynnClass in enumerate(playerClasses.classes):
            askString += "{}) {}, {}\n".format(idx + 1, wynnClass.name, wynnClass.combatLevel.level)
        askString += "Choose: "
        output = generalIntAsk(askString, len(playerClasses.classes)) - 1

        self.level = playerClasses.classes[output].combatLevel.level
        self.name = playerClasses.classes[output].name

    def updatePlayerInformations(self):
        # Get player classes
        playerClasses = getPlayerClasses(self.wynnApi, self.player.strip())
        # Update level
        for wynnClass in playerClasses:
            if wynnClass.name == self.name:
                self.level = wynnClass.combatLevel.level

    def startCheckerThread(self):
        threading.Thread(target=self.startChecking).start()

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
                        sendMessageWebhook("Possible hunter joined: " + player, self.webhook,
                                           ping=self.pingList.__contains__(player) or sureHunter)
                playersChecked.append(player)
            time.sleep(60)

    def isHunter(self, player):
        statsPlayer = getPlayerClasses(self.wynnApi, player)

        if statsPlayer == None:
            return False

        found = False

        for classWynn in statsPlayer.classes:
            toAdd = optPlayerStats(classWynn, statsPlayer.timeStamp)
            if toAdd.combatLevel.level - 10 <= self.level <= toAdd.combatLevel.level + 10 \
                    and (toAdd.combatLevel.level >= 103 or toAdd.gamemode.hunted):
                if toAdd.gamemode.hunted:
                    return True, True
                else:
                    found = True
        return found
