import time

import api.WynnPy
from stalker.OptPlayerStats import optPlayerStats

from stalker.utils.askUtils import *
from stalker.utils.operatorsUtils import *

from stalker.utils import fileUtils
import threading


def isTarget(stats, hunterCallingCheck):
    return stats.gamemode.hunted or (hunterCallingCheck and stats.quests.__contains__('A Hunter\'s Calling'))


def getPlayerClasses(wynnApi, player, logger=None):
    while True:
        ## Get every stats
        statsPlayer = wynnApi.getPlayerStats(player)
        if type(statsPlayer) != bool:
            break
        else:
            if not statsPlayer:
                if logger is not None:
                    logger.error("Rate limit exceed. Please wait")
                time.sleep(0.5 * 60)
            else:
                return None
    return statsPlayer


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
        # If the stalker is running
        self.on = self.running = False
        # Players that are not in hunted mode
        self.listPlayers = []
        # Load people that are not in hunted mode
        self.loadNoHuntedPeople()
        # Ask informations
        self.askInformations()

    def loadNoHuntedPeople(self):
        fileUtils.createDirectoryIfNotExists("data")
        fileUtils.createFileIfNotExists("data/players.txt")
        with open("data/players.txt") as fp:
            Lines = fp.readlines()
            for line in Lines:
                if len(line := line.strip()) > 0:
                    self.listPlayers.append(line)

    def askInformations(self):

        # noinspection PyAttributeOutsideInit
        self.mode = generalStringAsk("s) Single\nw) Worlds", ["s", "w"])

        ## Ask for the api
        # noinspection PyAttributeOutsideInit
        self.apiToUse = generalIntAsk("Api:\n1) v2\n2) v3\nChoose:", 2)

        ## Ask for checking hunter's calling
        # noinspection PyAttributeOutsideInit
        self.hunterCalling = generalStringAsk("Hunter's calling (y/n)?", ["y", "n"], "y")

        if self.mode == "w":
            ## Ask for the server
            # noinspection PyAttributeOutsideInit
            self.toStalk = askServer()
            # noinspection PyAttributeOutsideInit
            self.focus = generalStringAsk("Focus (y/n)?", ["y", "n"], "y")
        else:
            # noinspection PyAttributeOutsideInit
            self.toStalk = askPlayerToStalk()
            # noinspection PyAttributeOutsideInit
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
            targetStats = self.getTargetStats(players)
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

                                        else:
                                            self.logger.log(35, outputStr)
                                        # @formatter:on

            prevTargets = targetStats

            if self.focus:
                self.toStalk = [x for x in prevTargets]

            self.logger.info("Waiting for refresh. Total target: {}".format(len(prevTargets)))
            time.sleep(0.25 * 60)

    def getTargetStats(self, players):
        playerStats = {}
        # V2 api
        if self.apiToUse == 1:
            ## For every players, get their stats
            for player in players:

                classAdded, info, oneHunted = self.analysisPlayerClasses(player)

                ## Add to the dict optimized stats
                if len(classAdded) > 0:
                    self.logger.warning("Found possible target: {}. info: {}".format(player, info))
                    playerStats[player] = classAdded
                else:
                    self.logger.info("Removed " + player)

                    # We add him to this list only if he doesnt have hunter's calling or hunted.
                    if not oneHunted:
                        self.listPlayers.append(player)
                        with open("data/players.txt", "a") as rf:
                            rf.write(player + "\n")
                            rf.close()


        # V3 api
        elif self.apiToUse == 2:
            pass

        return playerStats

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
