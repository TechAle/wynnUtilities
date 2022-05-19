import time

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
                time.sleep(60 - int(time.strftime("%S")))
            else:
                return None
    return statsPlayer

def getLobbyPlayer(lobby, player):
    for server in lobby:
        if lobby[server].__contains__(player):
            return lobby[server], server
    return [], ""