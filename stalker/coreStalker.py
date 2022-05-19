import api.WynnPy
from api.classes.OptPlayerStats import optPlayerStats

from utils.askUtils import *
from utils.operatorsUtils import *

from utils import fileUtils
import threading

from utils.logUtils import createLogger

from utils.wynnUtils import *


# https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

class stalkerCore:
    def __init__(self, logger, mainThread, RPC):
        # Init api
        self.wynnApi = api.WynnPy.wynnPy()
        # Mainthread
        self.mainThread = mainThread
        # RPC
        self.RPC = RPC
        # Logger
        self.logger = logger

        # Logger for hunted people
        self.loggerHunded = createLogger("./stalker/logs/hunted")
        self.loggerHunters = createLogger("./stalker/logs/hunters")
        # If the stalker is running
        self.on = self.running = False
        # Locker for multithreading
        self.lock = threading.Lock()
        # Players that are not in hunted mode
        self.listPlayers = []
        # Load people that are not in hunted mode
        self.loadNoHuntedPeople()
        # Ask informations
        self.askInformations()

    def loadNoHuntedPeople(self):
        fileUtils.createDirectoryIfNotExists("./stalker/data")
        fileUtils.createFileIfNotExists("./stalker/data/players.txt")
        with open("./stalker/data/players.txt") as fp:
            Lines = fp.readlines()
            for line in Lines:
                if len(line := line.strip()) > 0:
                    self.listPlayers.append(line)

    # noinspection PyAttributeOutsideInit
    def askInformations(self):

        self.mode = generalStringAsk("s) Single\nw) Worlds", ["s", "w"])

        # Ask for the api
        self.apiToUse = generalIntAsk("Api:\n1) v2\n2) v3\nChoose:", 2)

        # Ask for checking hunter's calling
        self.hunterCalling = generalStringAsk("Hunter's calling (y/n)?", ["y", "n"], "y")

        # noinspection PyAttributeOutsideInit
        self.multiThreading = generalIntAsk("Multithreading? (N^ threads) ", 50)

        if self.mode == "w":
            # Ask for the server
            self.toStalk = askServer()
            self.focus = generalStringAsk("Focus (y/n)?", ["y", "n"], "y")
        else:
            self.toStalk = askPlayerToStalk()
            self.focus = False

        self.logger.info("Set up new stalker: Mode: {} Api: {} Hunter's Calling: {} Target: {} Focus: {}"
                         .format(self.mode, self.apiToUse, self.hunterCalling, self.toStalk, self.focus))

    def startStalkingThread(self):
        threading.Thread(target=self.startStalking).start()

    def startStalking(self):
        prevTargets = None
        self.on = self.running = True
        while self.on and self.mainThread.is_alive():
            # Get players
            players = self.wynnApi.getPlayersOnline() if self.toStalk == "all" else \
                self.wynnApi.getPlayersOnlineInWorld(self.toStalk) if type(self.toStalk) != list else \
                    self.wynnApi.getPlayersOnlineInWorlds(self.toStalk) if self.toStalk[0].isnumeric() else self.toStalk
            self.logger.info("Total players: {}".format(len(players)))
            # Remove already known non-hunted players
            i = 0
            while i < len(players):
                if self.listPlayers.__contains__(players[i]):
                    players.pop(i)
                    i -= 1
                i += 1
            self.logger.info("Total players after non-hunted: {}".format(len(players)))
            self.RPC.increasePlayer(len(players))
            # Get targets with stats
            ## Split array for multithreading
            everyArrays = list(split(players, self.multiThreading))

            # This is a really cool way. I would use another way for this but i mean, you always learn new things
            ## https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
            threads = []
            results = [0] * self.multiThreading
            for i in range(self.multiThreading):
                threads.append(threading.Thread(target=self.getTargetStats, args=(everyArrays[i], results, i)))
                threads[i].start()

            for i in range(self.multiThreading):
                threads[i].join()

            targetStats = {}

            for i in range(len(results)):
                for player in results[i]:
                    targetStats[player] = results[i][player]

            if prevTargets is not None:
                # Search for the name of the player we are checking
                for nowPlayer in targetStats:
                    if prevTargets.__contains__(nowPlayer):
                        # Now we have to search for the same class
                        for nowClass in targetStats[nowPlayer]:
                            for beforeClass in prevTargets[nowPlayer]:
                                if nowClass.className == beforeClass.className:
                                    # Found it, lets check if he was active
                                    if nowClass.blocksWalked != beforeClass.blocksWalked:

                                        if nowClass.gamemode.hunted:
                                            self.RPC.increaseHunted()

                                        # @formatter:off
                                        outputStr = "{} Lobby: {} Hunted: {} Class: {} Level: {}\n".format(nowPlayer, self.wynnApi.getLobbyPlayer(nowPlayer), "y" if nowClass.gamemode.hunted else "n", nowClass.className, nowClass.combatLevel.level)
                                        # Everything that changed
                                        if (mobsKilled := nowClass.mobsKilled - beforeClass.mobsKilled) > 0:
                                            outputStr += "Mobs Killed: " + str(mobsKilled) + "\n"
                                        if (chestsFound := nowClass.chestsFound - beforeClass.chestsFound) > 0:
                                            outputStr += "Chests Opened: " + str(chestsFound) + "\n"
                                        if (blocksWalked := nowClass.blocksWalked - beforeClass.blocksWalked) > 0:
                                            outputStr += "Blocks Walked: " + str(blocksWalked) + "\n"
                                        if len(questsDone := list(set(nowClass.quests) - set(beforeClass.quests))) > 0:
                                            outputStr += "Quests Done: " + questsDone.__str__() + "\n"
                                        if (playtime := nowClass.playtime - beforeClass.playtime) > 0:
                                            outputStr += "Playtime: " + str(playtime) + "\n"

                                        if  lazyOr((combatLvl := nowClass.combatLevel.level - beforeClass.combatLevel.level) > 0,
                                                   (combatXp := (0 if combatLvl > 0 else nowClass.combatLevel.xp - beforeClass.combatLevel.xp)) > 0):
                                            outputStr += "Combat: {}LvL {}xp Real: {}".format(combatLvl, combatXp, nowClass.combatLevel.level) + "\n"

                                        if  lazyOr((alchemismLvl := nowClass.alchemismLevel.level - beforeClass.alchemismLevel.level) > 0,
                                                   (alchemismXp := (0 if alchemismLvl > 0 else nowClass.alchemismLevel.xp - beforeClass.alchemismLevel.xp)) > 0):
                                            outputStr += "Alchemism: {}LvL {}xp Real: {}".format(alchemismLvl, alchemismXp, nowClass.alchemismLevel.level) + "\n"

                                        if  lazyOr((armouringLvl := nowClass.armouringLevel.level - beforeClass.armouringLevel.level) > 0,
                                                   (armouringXp := (0 if armouringLvl > 0 else nowClass.armouringLevel.xp - beforeClass.armouringLevel.xp)) > 0):
                                            outputStr += "Armouring: {}LvL {}xp Real: {}".format(armouringLvl, armouringXp, nowClass.armouringLevel.level) + "\n"

                                        if  lazyOr((farmingLvl := nowClass.farmingLevel.level - beforeClass.farmingLevel.level) > 0,
                                                   (farmingXp := (0 if farmingLvl > 0 else nowClass.farmingLevel.xp - beforeClass.farmingLevel.xp)) > 0):
                                            outputStr += "Farming: {}LvL {}xp Real: {}".format(farmingLvl, farmingXp, nowClass.farmingLevel.level) + "\n"

                                        if  lazyOr((fishingLvl := nowClass.fishingLevel.level - beforeClass.fishingLevel.level) > 0,
                                                   (fishingXp := (0 if fishingLvl > 0 else nowClass.fishingLevel.xp - beforeClass.fishingLevel.xp)) > 0):
                                            outputStr += "Fishing: {}LvL {}xp Real: {}".format(fishingLvl, fishingXp, nowClass.fishingLevel.level) + "\n"

                                        if  lazyOr((miningLvl := nowClass.miningLevel.level - beforeClass.miningLevel.level) > 0,
                                                   (miningXp := (0 if miningLvl > 0 else nowClass.miningLevel.xp - beforeClass.miningLevel.xp)) > 0):
                                            outputStr += "Mining: {}LvL {}xp Level: {}".format(miningLvl, miningXp, nowClass.miningLevel.level) + "\n"

                                        if  lazyOr((tailoringLvl := nowClass.tailoringLevel.level - beforeClass.tailoringLevel.level) > 0,
                                                   (tailoringXp := (0 if tailoringLvl > 0 else nowClass.tailoringLevel.xp - beforeClass.tailoringLevel.xp)) > 0):
                                            outputStr += "Taioloring: {}LvL {}xp Real: {}".format(tailoringLvl, tailoringXp, nowClass.tailoringLevel.level) + "\n"

                                        if  lazyOr((weaponsmithingLvl := nowClass.weaponsmithingLevel.level - beforeClass.weaponsmithingLevel.level) > 0,
                                                   (weaponsmithingXp := (0 if weaponsmithingLvl > 0 else nowClass.weaponsmithingLevel.xp - beforeClass.weaponsmithingLevel.xp)) > 0):
                                            outputStr += "Weaponsmithing: {}LvL {}xp Real: {}".format(weaponsmithingLvl, weaponsmithingXp, nowClass.weaponsmithingLevel.level) + "\n"

                                        if  lazyOr((woodworkingLvl := nowClass.woodworkingLevel.level - beforeClass.woodworkingLevel.level) > 0,
                                                   (woodworkingXp := (0 if woodworkingLvl > 0 else nowClass.woodworkingLevel.xp - beforeClass.woodworkingLevel.xp)) > 0):
                                            outputStr += "Woodworking: {}LvL {}xp Real: {}".format(woodworkingLvl, woodworkingXp, nowClass.woodworkingLevel.level) + "\n"

                                        if  lazyOr((woodcuttingLvl := nowClass.woodcuttingLevel.level - beforeClass.woodcuttingLevel.level) > 0,
                                                   (woodcuttingXp := (0 if woodcuttingLvl > 0 else nowClass.woodcuttingLevel.xp - beforeClass.woodcuttingLevel.xp)) > 0):
                                            outputStr += "Woodcutting: {}LvL {}xp Real: {}".format(woodcuttingLvl, woodcuttingXp, nowClass.woodcuttingLevel.level) + "\n"

                                        if nowClass.gamemode.hunted:
                                            self.logger.log(36, outputStr)
                                            self.loggerHunded.log(36, outputStr)
                                        else:
                                            self.logger.log(35, outputStr)
                                            self.loggerHunters.log(35, outputStr)
                                        # @formatter:on

            prevTargets = targetStats

            if self.focus:
                self.toStalk = [x for x in prevTargets]

            self.logger.info("Waiting for refresh. Total target: {}".format(len(prevTargets)))
            time.sleep(60 - int(time.strftime("%S")))

    def getTargetStats(self, players, results, i):
        playerStats = {}
        # V2 api
        if self.apiToUse == 1:
            ## For every players, get their stats
            for player in players:

                classAdded, info, oneHunted = self.analysisPlayerClasses(player)

                ## Add to the dict optimized stats
                if len(classAdded) > 0:
                    threading.Thread(target=lambda: self.logger.warning("Found possible target: {}. info: {}".format(player, info))).start()
                    playerStats[player] = classAdded
                else:
                    threading.Thread(target=lambda: self.logger.info("Removed " + player)).start()

                    # We add him to this list only if he doesnt have hunter's calling or hunted.
                    if not oneHunted:
                        self.lock.acquire()
                        try:
                            self.listPlayers.append(player)
                        finally:
                            self.lock.release()
                        with open("./stalker/data/players.txt", "a") as rf:
                            rf.write(player + "\n")
                            rf.close()


        # V3 api
        elif self.apiToUse == 2:
            pass

        results[i] = playerStats

    # TODO: It works but it could coded be better
    def analysisPlayerClasses(self, player):

        statsPlayer = getPlayerClasses(self.wynnApi, player, self.logger)

        if statsPlayer == None:
            return [], "", False

        ## Classes that are going to be added
        classAdded = []
        oneHunted = False
        info = ""
        ## Check every class
        for classWynn in statsPlayer.classes:
            toAdd = optPlayerStats(classWynn, statsPlayer.timeStamp)
            if isTarget(classWynn, self.hunterCalling):
                classAdded.append(toAdd)
                info += ("y " if toAdd.gamemode.hunted else "n ") + toAdd.className + "|"
                oneHunted = True
            elif isTarget(classWynn, True):
                oneHunted = True
        # So, if this guy now is offline, we set classAdded to none
        if not statsPlayer.meta.online:
            classAdded = []
        info = '[' + info + ']'
        return classAdded, info, oneHunted
