import time

import api.WynnPy
from stalker.OptPlayerStats import optPlayerStats

from stalker.ask import *
from stalker.utils.operatorsUtils import *


class stalkerCore:
    def __init__(self, logger):
        # Init api
        self.wynnApi = api.WynnPy.wynnPy()
        self.logger = logger

    def askInformations(self):
        self.mode = askSingleOrWorld()

        # Ask for the api
        self.apiToUse = askApi()

        # Ask for checking hunter's calling
        self.hunterCalling = askHunterCalling()

        if self.mode == "w":
            # Ask for the server
            self.toStalk = askServer()
            self.focus = askFocus()
        else:
            self.toStalk= askPlayerToStalk()
            self.focus = False

        self.logger("Set up new stalker: Mode: {} Api: {} Hunter's Calling: {} Target: {} Focus: {}"
                    .format(self.mode, self.apiToUse, self.hunterCalling, self.toStalk, self.focus))

    def startStalking(self):
        prevTargets = None
        while True:
            # Get players
            players = self.wynnApi.getPlayersOnline() if self.toStalk == "all" else \
                self.wynnApi.getPlayersOnlineInWorld(self.toStalk) if type(self.toStalk) != list else \
                    self.wynnApi.getPlayersOnlineInWorlds(self.toStalk) if self.toStalk[0].isnumeric() else self.toStalk
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
                                        # @formatter:off
                                        outputStr = "{} Lobby: {} Hunted: {}\n".format(nowPlayer, self.wynnApi.getLobbyPlayer(nowPlayer), "y" if nowClass.gamemode.hunted else "n")
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
                                            outputStr += "Combat: {}LvL {}xp".format(combatLvl, combatXp) + "\n"

                                        if  lazyOr((alchemismLvl := nowClass.alchemismLevel.level - beforeClass.alchemismLevel.level) > 0,
                                                   (alchemismXp := (0 if alchemismLvl > 0 else nowClass.alchemismLevel.xp - beforeClass.alchemismLevel.xp)) > 0):
                                            outputStr += "Alchemism: {}LvL {}xp".format(alchemismLvl, alchemismXp) + "\n"

                                        if  lazyOr((armouringLvl := nowClass.armouringLevel.level - beforeClass.armouringLevel.level) > 0,
                                                   (armouringXp := (0 if armouringLvl > 0 else nowClass.armouringLevel.xp - beforeClass.armouringLevel.xp)) > 0):
                                            outputStr += "Armouring: {}LvL {}xp".format(armouringLvl, armouringXp) + "\n"

                                        if  lazyOr((farmingLvl := nowClass.farmingLevel.level - beforeClass.farmingLevel.level) > 0,
                                                   (farmingXp := (0 if farmingLvl > 0 else nowClass.farmingLevel.xp - beforeClass.farmingLevel.xp)) > 0):
                                            outputStr += "Farming: {}LvL {}xp".format(farmingLvl, farmingXp) + "\n"

                                        if  lazyOr((fishingLvl := nowClass.fishingLevel.level - beforeClass.fishingLevel.level) > 0,
                                                   (fishingXp := (0 if fishingLvl > 0 else nowClass.fishingLevel.xp - beforeClass.fishingLevel.xp)) > 0):
                                            outputStr += "Fishing: {}LvL {}xp".format(fishingLvl, fishingXp) + "\n"

                                        if  lazyOr((miningLvl := nowClass.miningLevel.level - beforeClass.miningLevel.level) > 0,
                                                   (miningXp := (0 if miningLvl > 0 else nowClass.miningLevel.xp - beforeClass.miningLevel.xp)) > 0):
                                            outputStr += "Mining: {}LvL {}xp".format(miningLvl, miningXp) + "\n"

                                        if  lazyOr((tailoringLvl := nowClass.tailoringLevel.level - beforeClass.tailoringLevel.level) > 0,
                                                   (tailoringXp := (0 if tailoringLvl > 0 else nowClass.tailoringLevel.xp - beforeClass.tailoringLevel.xp)) > 0):
                                            outputStr += "Taioloring: {}LvL {}xp".format(tailoringLvl, tailoringXp) + "\n"

                                        if  lazyOr((weaponsmithingLvl := nowClass.weaponsmithingLevel.level - beforeClass.weaponsmithingLevel.level) > 0,
                                                   (weaponsmithingXp := (0 if weaponsmithingLvl > 0 else nowClass.weaponsmithingLevel.xp - beforeClass.weaponsmithingLevel.xp)) > 0):
                                            outputStr += "Weaponsmithing: {}LvL {}xp".format(weaponsmithingLvl, weaponsmithingXp) + "\n"

                                        if  lazyOr((woodworkingLvl := nowClass.woodworkingLevel.level - beforeClass.woodworkingLevel.level) > 0,
                                                   (woodworkingXp := (0 if woodworkingLvl > 0 else nowClass.woodworkingLevel.xp - beforeClass.woodworkingLevel.xp)) > 0):
                                            outputStr += "Woodworking: {}LvL {}xp".format(woodworkingLvl, woodworkingXp) + "\n"

                                        if  lazyOr((woodcuttingLvl := nowClass.woodcuttingLevel.level - beforeClass.woodcuttingLevel.level) > 0,
                                                   (woodcuttingXp := (0 if woodcuttingLvl > 0 else nowClass.woodcuttingLevel.xp - beforeClass.woodcuttingLevel.xp)) > 0):
                                            outputStr += "Woodcutting: {}LvL {}xp".format(woodcuttingLvl, woodcuttingXp) + "\n"


                                        self.logger.warning(outputStr)
                                        # @formatter:on

            prevTargets = targetStats

            if self.focus:
                self.toStalk = [x for x in prevTargets]

            self.logger("Waiting for refresh")
            time.sleep(10 * 60)

    def getTargetStats(self, players):
        playerStats = {}
        # V2 api
        if self.apiToUse == 1:
            ## For every players, get their stats
            for player in players:

                classAdded, info = self.analysisPlayerClasses(player)

                ## Add to the dict optimized stats
                if len(classAdded) > 0:
                    self.logger.warning("Found possible target: {}. info: {}".format(player, info))
                    playerStats[player] = classAdded
                else:
                    self.logger.info("Removed " + player)

        # V3 api
        elif self.apiToUse == 2:
            pass

        return playerStats

    def analysisPlayerClasses(self, player):
        ## Get every stats
        statsPlayer = self.wynnApi.getPlayerStats(player)
        ## Classes that are going to be added
        classAdded = []
        info = ""
        if statsPlayer.meta.online:
            ## Check every class
            for classWynn in statsPlayer.classes:
                if self.isTarget(classWynn):
                    classAdded.append((toAdd := optPlayerStats(classWynn, statsPlayer.timeStamp)))
                    info += ("y " if toAdd.gamemode.hunted else "n ") + toAdd.className + "|"
        info = '[' + info + ']'
        return classAdded, info

    def isTarget(self, stats):
        return stats.gamemode.hunted or (self.hunterCalling and stats.quests.__contains__('A Hunter\'s Calling'))