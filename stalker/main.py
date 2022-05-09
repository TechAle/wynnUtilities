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
            return choose


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
                playerStats["k"] = classAdded
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
                classAdded.append(optPlayerStats(classWynn))
    return classAdded

def isTarget(stats, hunterCalling):
    return stats.gamemode.hunted or (hunterCalling and stats.quests.__contains__("A Hunter"))

def askPlayerToStalk():
    while True:
        inp = input("Players (name, name): ")
        if len(inp := inp.strip().split(",")) > 0:
            return inp

def stalkPlayers(players, wynnApi, apiToUse, hunterCalling):
    app.info("Waiting for refresh")
    time.sleep(60*5)


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
        app.info("Api: "+str(apiToUse + 1)+". Server: "+str(servetToTarget)+". Hunter: " + hunterCalling)
        # Get players
        players = wynnApi.getPlayersOnline() if servetToTarget == "all" else wynnApi.getPlayersOnlineInWorld(servetToTarget)
        # Get targets with stats
        targetStats = getTargetStats(players, apiToUse, wynnApi, hunterCalling)
    elif mode == "s":
        toStalk = askPlayerToStalk()
        targetStats = getTargetStats(toStalk, apiToUse, wynnApi, hunterCalling)
        stalkPlayers(targetStats, wynnApi, apiToUse, hunterCalling)


if __name__ == "__main__":
    main()
