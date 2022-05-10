from stalker.OptPlayerStats import optPlayerStats
import time

from stalker.utils import logUtils
from stalker.utils.operatorsUtils import *

# Logger
app = logUtils.setup_logger('logger', './logs/app.log')
app.info("Started new session")

def isTarget(stats, hunterCalling):
    return stats.gamemode.hunted or (hunterCalling and stats.quests.__contains__('A Hunter\'s Calling'))


def getTargetStats(players, apiToUse, wynnApi, hunterCalling):
    playerStats = {}
    # V2 api
    if apiToUse == 1:
        ## For every players, get their stats
        for player in players:

            classAdded, info = analysisPlayerClasses(player, wynnApi, hunterCalling)

            ## Add to the dict optimized stats
            if len(classAdded) > 0:
                app.warning("Found possible target: {}. info: {}".format(player, info))
                playerStats[player] = classAdded
            else:
                app.info("Removed " + player)

    # V3 api
    elif apiToUse == 2:
        pass

    return playerStats


def analysisPlayerClasses(player, wynnApi, hunterCalling):
    ## Get every stats
    statsPlayer = wynnApi.getPlayerStats(player)
    ## Classes that are going to be added
    classAdded = []
    info = ""
    if statsPlayer.meta.online:
        ## Check every class
        for classWynn in statsPlayer.classes:
            if isTarget(classWynn, hunterCalling):
                classAdded.append((toAdd := optPlayerStats(classWynn, statsPlayer.timeStamp)))
                info += ("y " if toAdd.gamemode.hunted else "n ") + toAdd.className + "|"
    info = '[' + info + ']'
    return classAdded, info

def stalkPlayers(wynnApi, toStalk, apiToUse, hunterCalling, focus):
    prevTargets = None
    while True:
        # Get players
        players = wynnApi.getPlayersOnline() if toStalk == "all" else \
            wynnApi.getPlayersOnlineInWorld(toStalk) if type(toStalk) != list else \
                wynnApi.getPlayersOnlineInWorlds(toStalk) if toStalk[0].isnumeric() else toStalk
        # Get targets with stats
        targetStats = getTargetStats(players, apiToUse, wynnApi, hunterCalling)
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
                                    outputStr = ""
                                    # Everything that changed
                                    if (mobsKilled := nowClass.mobsKilled - beforeClass.mobsKilled) > 0:
                                        outputStr += "Mobs Killed: " + mobsKilled
                                    if (chestsFound := nowClass.chestsFound - beforeClass.chestsFound) > 0:
                                        outputStr += "Chests Opened: " + chestsFound
                                    if (blocksWalked := nowClass.blocksWalked - beforeClass.blocksWalked) > 0:
                                        outputStr += "Blocks Walked: " + blocksWalked
                                    if len(questsDone := list(set(nowClass.quests) - set(beforeClass.quests))) > 0:
                                        outputStr += "Quests Done: " + questsDone.__str__()
                                    if (playtime := nowClass.playtime - beforeClass.playtime) > 0:
                                        outputStr += "Playtime: " + playtime
                                    outputStr += "Lobby: " + wynnApi.getLobbyPlayer(nowPlayer)

                                    if  lazyOr((alchemismLvl := nowClass.alchemismLevel.level - beforeClass.alchemismLevel.level) > 0,
                                               (alchemismXp := (0 if alchemismLvl > 0 else nowClass.alchemismLevel.xp - beforeClass.alchemismLevel.xp)) > 0):
                                        outputStr += "Alchemism: {}LvL {}xp".format(alchemismLvl, alchemismXp)

                                    if  lazyOr((armouringLvl := nowClass.armouringLevel.level - beforeClass.armouringLevel.level) > 0,
                                               (armouringXp := (0 if armouringLvl > 0 else nowClass.armouringLevel.xp - beforeClass.armouringLevel.xp)) > 0):
                                        outputStr += "Armouring: {}LvL {}xp".format(armouringLvl, armouringXp)

                                    if  lazyOr((combatLvl := nowClass.combatLevel.level - beforeClass.combatLevel.level) > 0,
                                               (combatXp := (0 if combatLvl > 0 else nowClass.combatLevel.xp - beforeClass.combatLevel.xp)) > 0):
                                        outputStr += "Combat: {}LvL {}xp".format(combatLvl, combatXp)

                                    if  lazyOr((combatLvl := nowClass.combatLevel.level - beforeClass.combatLevel.level) > 0,
                                               (combatXp := (0 if combatLvl > 0 else nowClass.combatLevel.xp - beforeClass.combatLevel.xp)) > 0):
                                        outputStr += "Combat: {}LvL {}xp".format(combatLvl, combatXp)

                                    if  lazyOr((combatLvl := nowClass.combatLevel.level - beforeClass.combatLevel.level) > 0,
                                               (combatXp := (0 if combatLvl > 0 else nowClass.combatLevel.xp - beforeClass.combatLevel.xp)) > 0):
                                        outputStr += "Combat: {}LvL {}xp".format(combatLvl, combatXp)

                                    if  lazyOr((fishingLvl := nowClass.fishingLevel.level - beforeClass.fishingLevel.level) > 0,
                                               (fishingXp := (0 if fishingLvl > 0 else nowClass.fishingLevel.xp - beforeClass.fishingLevel.xp)) > 0):
                                        outputStr += "Fishing: {}LvL {}xp".format(fishingLvl, fishingXp)

                                    if  lazyOr((miningLvl := nowClass.miningLevel.level - beforeClass.miningLevel.level) > 0,
                                               (miningXp := (0 if miningLvl > 0 else nowClass.miningLevel.xp - beforeClass.miningLevel.xp)) > 0):
                                        outputStr += "Mining: {}LvL {}xp".format(miningLvl, miningXp)

                                    if  lazyOr((tailoringLvl := nowClass.tailoringLevel.level - beforeClass.tailoringLevel.level) > 0,
                                               (tailoringXp := (0 if tailoringLvl > 0 else nowClass.tailoringLevel.xp - beforeClass.tailoringLevel.xp)) > 0):
                                        outputStr += "Taioloring: {}LvL {}xp".format(tailoringLvl, tailoringXp)

                                    if  lazyOr((weaponsmithingLvl := nowClass.weaponsmithingLevel.level - beforeClass.weaponsmithingLevel.level) > 0,
                                               (weaponsmithingXp := (0 if weaponsmithingLvl > 0 else nowClass.weaponsmithingLevel.xp - beforeClass.weaponsmithingLevel.xp)) > 0):
                                        outputStr += "Weaponsmithing: {}LvL {}xp".format(weaponsmithingLvl, weaponsmithingXp)

                                    if  lazyOr((woodworkingLvl := nowClass.woodworkingLevel.level - beforeClass.woodworkingLevel.level) > 0,
                                               (woodworkingXp := (0 if woodworkingLvl > 0 else nowClass.woodworkingLevel.xp - beforeClass.woodworkingLevel.xp)) > 0):
                                        outputStr += "Woodworking: {}LvL {}xp".format(woodworkingLvl, woodworkingXp)

                                    if  lazyOr((woodcuttingLvl := nowClass.woodcuttingLevel.level - beforeClass.woodcuttingLevel.level) > 0,
                                               (woodcuttingXp := (0 if woodcuttingLvl > 0 else nowClass.woodcuttingLevel.xp - beforeClass.woodcuttingLevel.xp)) > 0):
                                        outputStr += "Woodcutting: {}LvL {}xp".format(woodcuttingLvl, woodcuttingXp)


                                    app.warning(outputStr)
                                    # @formatter:on

        prevTargets = targetStats

        if focus:
            toStalk = [x for x in prevTargets]

        time.sleep(10 * 60)