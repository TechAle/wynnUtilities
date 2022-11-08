from datetime import datetime

from discord import Webhook, RequestsWebhookAdapter

import api.WynnPy
from api.classes.OptPlayerStats import optPlayerStats
from api.classes.PlayerStats import playerStats
from stalker.classes.lootrunnerClass import lootrunner
from stalker.classes.serverClass import serverManager

from utils.operatorsUtils import *

from utils import fileUtils, discordUtils
import threading

from utils.logUtils import createLogger

from utils.wynnUtils import *

import time


# https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)


# https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


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
        self.debugger = ""

        # Logger for hunted people
        self.loggerHunded = createLogger("./stalker/logs/hunted")
        self.loggerHunters = createLogger("./stalker/logs/hunters")
        # If the stalker is running
        self.on = self.running = False
        # Locker for multithreading
        self.lock = threading.Lock()
        # Players that are not in hunted mode
        self.listPlayers = []
        # Known lootrunners
        self.knownLootrunners = []
        # Timestamps
        self.timeStamps = {}
        # Server class
        self.serverManager = serverManager()
        # Load people that are not in hunted mode
        self.loadNoHuntedPeople()
        # Load known lootrunners
        self.loadKnownLootrunners()
        # Ask informations
        self.loadInformations()
        self.minuteStage = int(datetime.now().minute / 15)

    def lrGuild(self):
        self.serverManager.updateServers(self.wynnApi)
        try:
            lines = open('lrGuildResults.txt', 'r').readlines()
            while lines.__len__() > 0:
                if lines[0][:2] == "WC":
                    break
                else:
                    lines.pop(0)

            for lrers in lines:
                # noinspection PyBroadException
                try:
                    newLrers = lrers.split()
                    wc = newLrers[0]
                    # noinspection PyRedeclaration
                    if newLrers[2] == 'h':
                        timeLr = newLrers[1:5]
                        timeLr = time.time() - int(timeLr[0]) * 60 * 60 - int(timeLr[2]) * 60
                        name = newLrers[5]
                        zone = newLrers[6:]
                    else:
                        timeLr = newLrers[1:3]
                        timeLr = time.time() - int(timeLr[0])*60
                        name = newLrers[3]
                        zone = newLrers[4:]
                    timeLr *= 1000
                    zone = "Claimed: " + " ".join(zone)
                    self.serverManager.addLootrunner(lootrunner("*" + name, wc, "", "", "?", zone, timeLr, "?", False, True))
                except Exception:
                    pass
        except FileNotFoundError:
            open("lrGuildResults.txt", 'a').close()
    def threadTime(self):
        self.playersTime = {}

        while True:
            serversOnline = ""
            while serversOnline.__len__() == 0:
                serversOnline = self.wynnApi.getServerList()
                if serversOnline.__len__() == 0:
                    time.sleep(60 - int(time.strftime("%S")))
            playersOnline = []
            for server in serversOnline:
                for player in serversOnline[server]:
                    playersOnline.append(player)
                    # Check if we have alr have it
                    if self.playersTime.__contains__(player):
                        # Get server
                        # noinspection PyUnresolvedReferences
                        serverBefore = self.playersTime[player]["server"]
                        # If it's not the same server, change time
                        if serverBefore != server:
                            self.playersTime[player]["time"] = time.time()
                            self.playersTime[player]["server"] = server
                            self.playersTime[player]["retry"] = 0
                    # If not, add it
                    else:
                        self.playersTime[player] = {
                            "time": time.time(),
                            "server": server,
                            "retry": 0
                        }

            # Check if someone logout
            keys = list(self.playersTime.keys())
            for i in range(len(keys)):
                if not playersOnline.__contains__(keys[i]):
                    if self.playersTime[keys[i]]["retry"] != 15:
                        self.playersTime[keys[i]]["retry"] += 1
                        continue
                    else:
                        self.playersTime.pop(keys[i])
                        i -= 1
                        self.lock.acquire()
                        try:
                            if self.timeStamps.__contains__(keys[i]):
                                self.timeStamps.pop(keys[i])
                        finally:
                            self.lock.release()

            time.sleep(60 - int(time.strftime("%S")))

    def loadNoHuntedPeople(self):
        fileUtils.createDirectoryIfNotExists("./stalker/data")
        fileUtils.createFileIfNotExists("./stalker/data/players.txt")
        with open("./stalker/data/players.txt") as fp:
            Lines = fp.readlines()
            for line in Lines:
                if len(line := line.strip()) > 0:
                    self.listPlayers.append(line)

    def loadKnownLootrunners(self):
        fileUtils.createDirectoryIfNotExists("./stalker/data")
        fileUtils.createFileIfNotExists("./stalker/data/lootrunners.txt")
        with open("./stalker/data/lootrunners.txt") as fp:
            Lines = fp.readlines()
            for line in Lines:
                if len(line := line.strip()) > 0:
                    self.knownLootrunners.append(line)

    # noinspection PyAttributeOutsideInit
    def loadInformations(self):
        data = fileUtils.readConfigFile()
        self.mode = data["stalker"]["mode"]

        # Ask for the api
        self.apiToUse = data["stalker"]["api"]

        # Ask for checking hunter's calling
        self.hunterCalling = "y" if data["stalker"]["hunterCalling"] == True else "n"

        # noinspection PyAttributeOutsideInit
        self.multiThreading = data["stalker"]["requestsPerTime"]

        self.toStalk = data["stalker"]["toStalk"]

        self.webhookHunter = data["stalker"]["webhookHunted"]
        self.webhookLr = data["stalker"]["webhookLootrunners"]

        self.filters = data["stalker"]["filters"]

        self.logger.info("Set up new stalker: Mode: {} Api: {} Hunter's Calling: {} Target: {}"
                         .format(self.mode, self.apiToUse, self.hunterCalling, self.toStalk))
        threading.Thread(target=self.threadTime).start()

    def startStalkingThread(self):
        threading.Thread(target=self.startStalking).start()

    def startStalking(self):
        prevTargets = {}
        prevPrevTargets = {}
        self.on = self.running = True
        if self.webhookHunter != "":
            discordUtils.sendMessageWebhook("Started hunted stalker", "", self.webhookHunter)
        if self.webhookLr != "":
            discordUtils.sendMessageWebhook("Started lootrunner tracker", "", self.webhookLr)
        while self.on and self.mainThread.is_alive():
            # Get players
            players = self.wynnApi.getPlayersOnline() if self.toStalk == "all" else \
                self.wynnApi.getPlayersOnlineInWorld(self.toStalk) if type(self.toStalk) != list else \
                    self.wynnApi.getPlayersOnlineInWorlds(self.toStalk) if self.toStalk[0].isnumeric() else self.toStalk
            self.logger.info("Total players: {} Players: {}".format(len(players), players.__len__()))
            # Remove already known non-hunted players and players in timeStamp without 30mins
            i = 0
            while i < len(players):
                if self.listPlayers.__contains__(players[i]):
                    players.pop(i)
                    i -= 1
                i += 1

            i = 0
            while i < len(players):
                if (self.timeStamps.__contains__(players[i]) and
                        current_milli_time() - self.timeStamps[players[i]] < 1000 * 60 * 30):
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
                try:
                    # noinspection PyTypeChecker
                    for player in results[i]:
                        # noinspection PyUnresolvedReferences
                        targetStats[player] = results[i][player]
                except TypeError:
                    pass

            for player in targetStats:
                self.lock.acquire()
                try:
                    if not self.timeStamps.__contains__(player):
                        self.timeStamps[player] = targetStats[player][0].timeStamp
                finally:
                    self.lock.release()

            self.serverManager.updateServers(self.wynnApi)

            # Search for the name of the player we are checking [49797763]
            for nowPlayer in targetStats:
                if nowPlayer == self.debugger:
                    a = 0
                if not prevTargets.__contains__(nowPlayer):
                    prevTargets[nowPlayer] = targetStats[nowPlayer]
                    self.logger.info("Checked " + nowPlayer + " new")
                else:
                    self.logger.info("Checking " + nowPlayer)
                    found = True
                    # Now we have to search for the same class
                    for nowClass in targetStats[nowPlayer]:
                        for beforeClass in prevTargets[nowPlayer]:
                            if nowClass.uuid == beforeClass.uuid:
                                self.lock.acquire()
                                try:
                                    if self.timeStamps.__contains__(nowPlayer):
                                        self.timeStamps[nowPlayer] = current_milli_time()
                                finally:
                                    self.lock.release()

                                hunterActive = False
                                notLr = False
                                # @formatter:off
                                outputStr = "{} Lobby: {} Class: {}. Hunted: {} Level: {} Craftman: {} Ironman: {} Hardcore: {}\n".format(nowPlayer, self.wynnApi.getLobbyPlayer(nowPlayer), nowClass.type, "y" if nowClass.gamemode.hunted else "n", nowClass.combatLevel.level,
                                                                                                                                         "y" if nowClass.gamemode.craftsman else "n", "y" if nowClass.gamemode.ironman else "n", "y" if nowClass.gamemode.hardcore else "n")
                                # Everything that changed
                                if (mobsKilled := nowClass.mobsKilled - beforeClass.mobsKilled) > 0:
                                    outputStr += "Mobs Killed: " + str(mobsKilled) + "\n"
                                if (chestsFound := nowClass.chestsFound - beforeClass.chestsFound) > 0:
                                    outputStr += "Chests Opened: " + str(chestsFound) + "\n"

                                if len(questsDone := list(set(nowClass.quests) - set(beforeClass.quests))) > 0:
                                    outputStr += "Quests Done: " + questsDone.__str__() + "\n"
                                    notLr = True

                                if  lazyOr((combatLvl := nowClass.combatLevel.level - beforeClass.combatLevel.level) > 0,
                                           (combatXp := (0 if combatLvl > 0 else nowClass.combatLevel.xp - beforeClass.combatLevel.xp)) > 0):
                                    outputStr += "Combat: {}LvL {}xp Real: {}".format(combatLvl, combatXp, nowClass.combatLevel.level) + "\n"
                                    if (combatLvl > 0 or combatXp > 0.1) and nowClass.combatLevel.level != 106:
                                        notLr = True

                                if  lazyOr((farmingLvl := nowClass.farmingLevel.level - beforeClass.farmingLevel.level) > 0,
                                           (farmingXp := (0 if farmingLvl > 0 else nowClass.farmingLevel.xp - beforeClass.farmingLevel.xp)) > 0):
                                    outputStr += "Farming: {}LvL {}xp Real: {}".format(farmingLvl, farmingXp, nowClass.farmingLevel.level) + "\n"
                                    hunterActive = True

                                if  lazyOr((fishingLvl := nowClass.fishingLevel.level - beforeClass.fishingLevel.level) > 0,
                                           (fishingXp := (0 if fishingLvl > 0 else nowClass.fishingLevel.xp - beforeClass.fishingLevel.xp)) > 0):
                                    outputStr += "Fishing: {}LvL {}xp Real: {}".format(fishingLvl, fishingXp, nowClass.fishingLevel.level) + "\n"
                                    hunterActive = True

                                if  lazyOr((miningLvl := nowClass.miningLevel.level - beforeClass.miningLevel.level) > 0,
                                           (miningXp := (0 if miningLvl > 0 else nowClass.miningLevel.xp - beforeClass.miningLevel.xp)) > 0):
                                    outputStr += "Mining: {}LvL {}xp Level: {}".format(miningLvl, miningXp, nowClass.miningLevel.level) + "\n"
                                    hunterActive = True

                                if  lazyOr((woodcuttingLvl := nowClass.woodcuttingLevel.level - beforeClass.woodcuttingLevel.level) > 0,
                                           (woodcuttingXp := (0 if woodcuttingLvl > 0 else nowClass.woodcuttingLevel.xp - beforeClass.woodcuttingLevel.xp)) > 0):
                                    outputStr += "Woodcutting: {}LvL {}xp Real: {}".format(woodcuttingLvl, woodcuttingXp, nowClass.woodcuttingLevel.level) + "\n"
                                    hunterActive = True


                                if  lazyOr((woodworkingLvl := nowClass.woodworkingLevel.level - beforeClass.woodworkingLevel.level) > 0,
                                           (woodworkingXp := (0 if woodworkingLvl > 0 else nowClass.woodworkingLevel.xp - beforeClass.woodworkingLevel.xp)) > 0):
                                    outputStr += "Woodworking: {}LvL {}xp Real: {}".format(woodworkingLvl, woodworkingXp, nowClass.woodcuttingLevel.level) + "\n"
                                    notLr = True

                                if  lazyOr((weaponsmithingLvl := nowClass.weaponsmithingLevel.level - beforeClass.weaponsmithingLevel.level) > 0,
                                           (weaponsmithingXp := (0 if weaponsmithingLvl > 0 else nowClass.weaponsmithingLevel.xp - beforeClass.weaponsmithingLevel.xp)) > 0):
                                    outputStr += "Weaponsmith: {}LvL {}xp Real: {}".format(weaponsmithingLvl, weaponsmithingXp, nowClass.woodcuttingLevel.level) + "\n"
                                    notLr = True

                                if  lazyOr((tailoringLvl := nowClass.tailoringLevel.level - beforeClass.tailoringLevel.level) > 0,
                                           (tailoringXp := (0 if tailoringLvl > 0 else nowClass.tailoringLevel.xp - beforeClass.tailoringLevel.xp)) > 0):
                                    outputStr += "Tailoring: {}LvL {}xp Real: {}".format(tailoringLvl, tailoringXp, nowClass.woodcuttingLevel.level) + "\n"
                                    notLr = True

                                if  lazyOr((alchemismLvl := nowClass.alchemismLevel.level - beforeClass.alchemismLevel.level) > 0,
                                           (alchemismXp := (0 if alchemismLvl > 0 else nowClass.alchemismLevel.xp - beforeClass.alchemismLevel.xp)) > 0):
                                    outputStr += "Alchemism: {}LvL {}xp Real: {}".format(alchemismLvl, alchemismXp, nowClass.woodcuttingLevel.level) + "\n"
                                    notLr = True

                                if  lazyOr((armouringLvl := nowClass.armouringLevel.level - beforeClass.armouringLevel.level) > 0,
                                           (armouringXp := (0 if armouringLvl > 0 else nowClass.armouringLevel.xp - beforeClass.armouringLevel.xp)) > 0):
                                    outputStr += "Armouring: {}LvL {}xp Real: {}".format(armouringLvl, armouringXp, nowClass.woodcuttingLevel.level) + "\n"
                                    notLr = True

                                blocksWalkedTotal = abs(nowClass.blocksWalked - beforeClass.blocksWalked)
                                blocksWalkedNow = blocksWalkedTotal
                                if blocksWalkedTotal > 0:
                                    if prevPrevTargets is not None and prevPrevTargets.__contains__(nowPlayer):
                                        for beforeBeforeClass in prevPrevTargets[nowPlayer]:
                                            if beforeBeforeClass.type == beforeClass.type and beforeBeforeClass.server == beforeClass.server:
                                                blocksWalkedTotal += abs(beforeClass.blocksWalked - beforeBeforeClass.blocksWalked)
                                    outputStr += "Blocks Walked now: " + str(blocksWalkedNow) + " Total: " + str(blocksWalkedTotal) + "\n"
                                elif blocksWalkedTotal < 0:
                                    outputStr += "Tf blocks walked is negative? How? " + str(blocksWalkedNow)

                                if (dungeonsDone := self.getDifferenceDungeons(nowClass.dungeons, beforeClass.dungeons)) != "":
                                    notLr = True
                                    outputStr += "Dungeons: \n" + dungeonsDone

                                if (raidsDone := self.getDifferenceDungeons(nowClass.raids, beforeClass.raids)) != "":
                                    notLr = True
                                    outputStr += "Raids: \n" + raidsDone

                                timePlaying = 0
                                if self.playersTime.__contains__(nowPlayer):
                                    timePlaying = int((time.time() - self.playersTime[nowPlayer]["time"])/60)
                                outputStr += " Time: " + str(timePlaying) + "mins\n"


                                # Hunted
                                if isTarget(nowClass, self.hunterCalling) and blocksWalkedNow > 0:
                                    if nowClass.gamemode.hunted:
                                        self.RPC.increaseHunted()
                                        self.logger.log(36, outputStr)
                                        if self.webhookHunter != "":
                                            discordUtils.sendMessageWebhook("Hunted found: " + nowPlayer, outputStr, self.webhookHunter)
                                            webhook = Webhook.from_url(self.webhookHunter, adapter=RequestsWebhookAdapter())
                                            webhook.send("<@&1005921707002966057>", username="wynnStalker", avatar_url="https://cdn.discordapp.com/app-icons/973942027563712632/3043f3b6d99b2b737ef7216e8c14c106.png?size=256")
                                        else:
                                            self.loggerHunded.log(36, outputStr)
                                    else:
                                        if hunterActive:
                                            self.logger.log(35, outputStr)
                                            if self.webhookHunter != "":
                                                discordUtils.sendMessageWebhook("Hunter found: " + nowPlayer, outputStr, self.webhookHunter, "00faff")
                                            else:
                                                self.loggerHunters.log(35, outputStr)

                                if not notLr and not hunterActive and mobsKilled < 500 and self.filters["max"] > blocksWalkedNow:
                                    predictZone = ""
                                    predictZoneNumber = -1
                                    low = False

                                    if nowClass.type.__contains__("MAGE") or nowClass.type.__contains__("WIZARD"):
                                        low, predictZone, predictZoneNumber = self.checkBlocks(nowPlayer, blocksWalkedNow, blocksWalkedTotal, self.filters["mage"])
                                    elif nowClass.type.__contains__("SHAMAN") or nowClass.type.__contains__("SKYSEER"):
                                        low, predictZone, predictZoneNumber = self.checkBlocks(nowPlayer, blocksWalkedNow, blocksWalkedTotal, self.filters["shaman"])
                                    elif nowClass.type.__contains__("ASSASSIN") or nowClass.type.__contains__("NINJA"):
                                        low, predictZone, predictZoneNumber = self.checkBlocks(nowPlayer, blocksWalkedNow, blocksWalkedTotal, self.filters["assassin"])
                                    elif nowClass.type.__contains__("WARRIOR") or nowClass.type.__contains__("KNIGHT"):
                                        low, predictZone, predictZoneNumber = self.checkBlocks(nowPlayer, blocksWalkedNow, blocksWalkedTotal, self.filters["warrior"])
                                    elif nowClass.type.__contains__("ARCHER") or nowClass.type.__contains__("HUNTER"):
                                        low, predictZone, predictZoneNumber = self.checkBlocks(nowPlayer, blocksWalkedNow, blocksWalkedTotal, self.filters["archer"])

                                    if predictZone != "":
                                        if self.knownLootrunners.__contains__(nowPlayer):
                                            nowPlayer = "!" + nowPlayer
                                        self.logger.log(36, "Lootrunner: " + nowPlayer + "\n" + predictZone)
                                        self.RPC.increaseLootrunners()

                                        if self.webhookLr != "":
                                            server = nowClass.server
                                            if prevTargets.__contains__(nowPlayer) and timePlaying < 15:
                                                server = prevTargets[nowPlayer][0].server
                                            #discordUtils.sendMessageWebhook("Lootrunner found: " + nowPlayer + " " + nowClass.type, predictZone + "\n" + outputStr, self.webhookLr, "ffffff" if low else "000000")
                                            self.serverManager.addLootrunner(lootrunner(nowPlayer, server, blocksWalkedNow, blocksWalkedTotal, timePlaying, predictZoneNumber, nowClass.timeStamp, nowClass.type, low))
                                    else:
                                        threading.Thread(target=lambda: self.logger.warning(
                                            "Not accepted: {} {}".format(nowPlayer, outputStr))).start()
                                else:
                                    if outputStr.__len__() > 0:
                                        threading.Thread(target=lambda: self.logger.warning(
                                            "Not accepted: {} {}".format(nowPlayer, outputStr))).start()

                    changedServer = False
                    if prevTargets.__contains__(nowPlayer):
                        if prevTargets[nowPlayer][0].server != targetStats[nowPlayer][0].server:
                            changedServer = True

                    if changedServer:
                        if prevPrevTargets.__contains__(nowPlayer):
                            prevPrevTargets.pop(nowPlayer)
                        prevTargets[nowPlayer] = targetStats[nowPlayer]
                    else:
                        prevPrevTargets[nowPlayer] = prevTargets[nowPlayer]
                        prevTargets[nowPlayer] = targetStats[nowPlayer]

                                    # @formatter:on

            minute = datetime.now().minute
            report = False
            if self.minuteStage == 0:
                report = minute >= 15
            elif self.minuteStage == 1:
                report = minute >= 30
            elif self.minuteStage == 2:
                report = minute >= 45
            elif self.minuteStage == 3:
                report = minute < 45
            if report:
                self.minuteStage += 1
                self.minuteStage %= 4
                idReport = str(time.time())
                self.logger.info("Printing report with id " + idReport)
                self.serverManager.exportServers(self.webhookLr, idReport)
            self.logger.info("Waiting for refresh. Total target: {}".format(len(prevTargets)))
            time.sleep(60 - int(time.strftime("%S")))

    def checkBlocks(self, nowPlayer, blocksWalkedNow, blocksWalkedTotal, limits):
        predictZone = ""
        predictZoneNumber = -1
        low = False
        if blocksWalkedNow > limits["lowStart"] and limits["toCheck"]:

            if blocksWalkedTotal < limits["cork"]:
                low = True
            elif blocksWalkedTotal < limits["cotl or rodo or sky"]:
                predictZone = "Cork"
                predictZoneNumber = 1
                low = False
            elif blocksWalkedTotal < limits["cotl and rodo and sky or unlvl"]:
                predictZone = "Between rodo, sky and see"
                predictZoneNumber = 2
                low = False
            else:
                predictZone = "Unlvl or cork+rodo+sky+se"
                predictZoneNumber = 3
                low = False
            predictZone += "\nLow: " + str(low) + " Lobby: " + str(
                self.wynnApi.getLobbyPlayer(nowPlayer)) + " Blocks: " + str(blocksWalkedTotal)
        return low, predictZone, predictZoneNumber

    def getTargetStats(self, players, results, i):
        playerStats = {}
        # V2 api
        if self.apiToUse == 1:
            ## For every players, get their stats
            for player in players:

                if player == self.debugger:
                    a = 0

                classAdded, info, oneHunted, isHigh = self.analysisPlayerClasses(player)

                ## Add to the dict optimized stats
                if len(classAdded) > 0:
                    threading.Thread(target=lambda: self.logger.warning(
                        "Found possible target: {}. info: {}".format(player, info))).start()
                    playerStats[player] = classAdded
                else:
                    if not isHigh:
                        threading.Thread(target=lambda: self.logger.info("Removed " + player)).start()

                        # We add him to this list only if he doesnt have hunter's calling or hunted.
                        self.listPlayers.append(player)
                        with open("./stalker/data/players.txt", "a") as rf:
                            rf.write(player + "\n")
                            rf.close()


        # V3 api
        elif self.apiToUse == 2:
            pass

        results[i] = playerStats

    def getDifferenceDungeons(self, nowDungeons, beforeDungeons):
        output = ""
        for dungeon in nowDungeons:
            if beforeDungeons.__contains__(dungeon):
                if nowDungeons[dungeon] != beforeDungeons[dungeon]:
                    output += dungeon + " " + str(nowDungeons[dungeon] - beforeDungeons[dungeon]) + "\n"
            else:
                output += dungeon + " " + str(nowDungeons[dungeon]) + "\n"
        return ""

    def analysisPlayerClasses(self, player):

        statsPlayer = getPlayerClasses(self.wynnApi, player, self.logger)

        if statsPlayer is None or statsPlayer == "" or not type(statsPlayer) == playerStats \
                or len(statsPlayer.characters) == 0:
            return [], "", False, True

        ## Classes that are going to be added
        classAdded = []
        oneHunted = False
        isHigh = False
        info = ""
        ## Check every class
        for classWynn in statsPlayer.characters:
            toAdd = optPlayerStats(classWynn, statsPlayer.meta.server, statsPlayer.timeStamp)
            added = False
            if isHighLevel(classWynn):
                classAdded.append(toAdd)
                isHigh = True
                added = True
                info += "l " + toAdd.type + "|"
            if isTarget(classWynn, self.hunterCalling):
                if not added:
                    classAdded.append(toAdd)
                info += ("y " if toAdd.gamemode.hunted else "n ") + toAdd.type + "|"
                oneHunted = True
            elif isTarget(classWynn, True):
                if not added:
                    classAdded.append(toAdd)
                oneHunted = True
        # So, if this guy now is offline, we set classAdded to none
        if not statsPlayer.meta.online:
            classAdded = []
        info = '[' + info + ']'
        return classAdded, info, oneHunted, isHigh
