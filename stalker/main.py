import api.WynnPy
from stalker.OptPlayerStats import optPlayerStats
import time

# Setup logger
# Directory of every chats
from stalker.utils import directoryUtils, logUtils

directoryUtils.createIfNotExists("./logs")

# Logger
app = logUtils.setup_logger('logger', './logs/app.log')
app.info("Started new session")


def askApi():
    while True:
        if (choose := input("Api:\n1) v2\n2) v3\nChoose: ")).isnumeric() \
                and (choose := int(choose)) > 0 and choose <= 2:
            return choose


def askServer():
    while True:

        if (choose := input("Server (all-number):")).isnumeric() and ((choose := int(choose)) > 0 and choose <= 50) \
                or type(choose) == str and choose.lower() == "all":
            return choose


def askSingleOrWorld():
    while True:
        if type(choose := input("Single or World? (s-w):")) == str and (
                choose := choose.lower()) == "s" or choose == "w":
            return choose


def askHunterCalling():
    while True:
        if type(choose := input("Hunter's calling? (y-n):")) == str and (
                choose := choose.lower()) == "y" or choose == "n":
            return choose == "y"


def getTargetStats(players, apiToUse, wynnApi, hunterCalling):
    playerStats = {}
    # V2 api
    if apiToUse == 1:
        ## For every players, get their stats
        for player in players:

            classAdded = analysisPlayerClasses(player, wynnApi, hunterCalling)

            ## Add to the dict optimized stats
            if len(classAdded) > 0:
                app.warning("Found possible target: " + player)
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
    if statsPlayer.meta.online:
        ## Check every class
        for classWynn in statsPlayer.classes:
            if isTarget(classWynn, hunterCalling):
                classAdded.append(optPlayerStats(classWynn, statsPlayer.timeStamp))
    return classAdded


def isTarget(stats, hunterCalling):
    return stats.gamemode.hunted or (hunterCalling and stats.quests.__contains__('A Hunter\'s Calling'))


def askPlayerToStalk():
    while True:
        inp = input("Players (name, name): ")
        if len(inp := inp.strip().split(",")) > 0:
            return inp


def stalkPlayers(wynnApi, toStalk, apiToUse, hunterCalling):
    prevTargets = None
    while True:
        # Get players
        players = wynnApi.getPlayersOnline() if toStalk == "all" else \
            wynnApi.getPlayersOnlineInWorld(toStalk) if type(toStalk) != list else \
                toStalk
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
                                    # Everything that changed
                                    mobsKilled = nowClass.mobsKilled - beforeClass.mobsKilled
                                    chestsFound = nowClass.chestsFound - beforeClass.chestsFound
                                    blocksWalked = nowClass.blocksWalked - beforeClass.blocksWalked
                                    questsDone = list(set(nowClass.quests) - set(beforeClass.quests))
                                    playTime = nowClass.playtime - beforeClass.playtime
                                    alchemism = "alchemism " + str(
                                        nowClass.alchemismLevel.level - beforeClass.alchemismLevel.level) + "L " + str(
                                        nowClass.alchemismLevel.xp - beforeClass.alchemismLevel.xp) + "xp"
                                    armouring = "armouring " + str(
                                        nowClass.armouringLevel.level - beforeClass.armouringLevel.level) + "L " + str(
                                        nowClass.armouringLevel.xp - beforeClass.armouringLevel.xp) + "xp"
                                    combat = "combat " + str(
                                        nowClass.combatLevel.level - beforeClass.combatLevel.level) + "L " + str(
                                        nowClass.combatLevel.xp - beforeClass.combatLevel.xp) + "xp"
                                    cooking = "cooking " + str(
                                        nowClass.cookingLevel.level - beforeClass.cookingLevel.level) + "L " + str(
                                        nowClass.cookingLevel.xp - beforeClass.cookingLevel.xp) + "xp"
                                    farming = "farming " + str(
                                        nowClass.farmingLevel.level - beforeClass.farmingLevel.level) + "L " + str(
                                        nowClass.farmingLevel.xp - beforeClass.farmingLevel.xp) + "xp"
                                    fishing = "fishing " + str(
                                        nowClass.fishingLevel.level - beforeClass.fishingLevel.level) + "L " + str(
                                        nowClass.fishingLevel.xp - beforeClass.fishingLevel.xp) + "xp"
                                    mining = "mining " + str(
                                        nowClass.miningLevel.level - beforeClass.miningLevel.level) + "L " + str(
                                        nowClass.miningLevel.xp - beforeClass.miningLevel.xp) + "xp"
                                    tailoring = "tailoring " + str(
                                        nowClass.tailoringLevel.level - beforeClass.tailoringLevel.level) + "L " + str(
                                        nowClass.tailoringLevel.xp - beforeClass.tailoringLevel.xp) + "xp"
                                    weaponsmithing = "weaponsmithing " + str(
                                        nowClass.weaponsmithingLevel.level - beforeClass.weaponsmithingLevel.level) + "L " + str(
                                        nowClass.weaponsmithingLevel.xp - beforeClass.weaponsmithingLevel.xp) + "xp"
                                    woodworking = "woodworking " + str(
                                        nowClass.woodworkingLevel.level - beforeClass.woodworkingLevel.level) + "L " + str(
                                        nowClass.woodworkingLevel.xp - beforeClass.woodworkingLevel.xp) + "xp"
                                    woodcutting = "woodcutting " + str(
                                        nowClass.woodcuttingLevel.level - beforeClass.woodcuttingLevel.level) + "L " + str(
                                        nowClass.woodcuttingLevel.xp - beforeClass.woodcuttingLevel.xp) + "xp"
                                    # Get where he is (This get updated every minute)
                                    lobby = wynnApi.getLobbyPlayer(nowPlayer)
                                    # Output
                                    message = "Player: {}. Hunted: {}. Hunter's calling: {}. Lobby: {}\n" \
                                              "Mobs: {}. Chests: {}. Walked: {}. Quests: {}. Time: {}\n" \
                                              "{} {} {}\n{} {} {}\n{} {} {}\n{} {}".format(
                                        nowPlayer, "y" if nowClass.gamemode.hunted else "n",
                                        "y" if nowClass.quests.__contains__('A Hunter\'s Calling') else "n", lobby,
                                        mobsKilled, chestsFound, blocksWalked, questsDone.__str__(), playTime,
                                        alchemism, armouring, combat, cooking, farming, fishing, mining, tailoring,
                                        weaponsmithing,
                                        woodcutting, woodworking
                                    )
                                    app.warning(message)

        prevTargets = targetStats
        time.sleep(10 * 60)


def main():
    # Init api
    wynnApi = api.WynnPy.wynnPy()

    mode = askSingleOrWorld()

    # Ask for the api
    apiToUse = askApi()

    # Ask for checking hunter's calling
    hunterCalling = askHunterCalling()

    if mode == "w":
        # Ask for the server
        servetToTarget = askServer()
        app.info("Api: " + str(apiToUse + 1) + ". Server: " + str(
            servetToTarget) + ". Hunter: " + "y" if hunterCalling else "n")
        # Start stalking
        stalkPlayers(wynnApi, servetToTarget, apiToUse, hunterCalling)
    elif mode == "s":
        toStalk = askPlayerToStalk()
        stalkPlayers(wynnApi, toStalk, apiToUse, hunterCalling)


if __name__ == "__main__":
    main()
