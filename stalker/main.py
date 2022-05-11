from stalker.core import stalkerCore, getPlayerClasses
from stalker.utils import logUtils
from stalker.utils.askUtils import generalIntAsk
import api.WynnPy
import sys

stalker = None

app = logUtils.createLogger()


def startBot():
    global stalker
    if stalker is None:
        stalker = stalkerCore(app)
    if not stalker.running:
        stalker.startStalkingThread()


def stopBot():
    # noinspection PyUnresolvedReferences
    if stalker is not None and stalker.on:
        stalker.on = False


def checkInfoPlayer():
    playerName = input("Name player: ")
    apiWynn = api.WynnPy.wynnPy()
    player = getPlayerClasses(apiWynn, playerName.strip())
    print("Name: {} Lobby: {} Online: {} Guild: {}, {} Total level: {}\nClasses:"
          .format(player.username, apiWynn.getLobbyPlayer(player.username), player.meta.online,
                  player.guild["name"], player.guild["rank"], player.globals.totalLevel["combined"]))

    for wynnClass in player.classes:
        print(
            "Name: {} Level: {} Blocks walked: {} chests: {} Playtime: {}\nMobs Killed: {} Deaths: {} PvpKills: {} PvpDeaths: {}\n"
            "Craftsman: {} Hardcore: {} Hunted: {} Ironman: {}\n"
            "Strenght: {} Dexterity: {} Intelligence: {} Defence: {} Agility: {}\n"
            "Alchemism: {} Armouring: {} Cooking: {} Farming: {} Fishing: {} Jeweling: {} Mining: {}\n"
            "Tailoring: {} Weaponsmithing: {} Woodcutting: {} Woodworking: {}\n"
            .format(wynnClass.name, wynnClass.combatLevel.level, wynnClass.blocksWalked, wynnClass.chestsFound,
                    wynnClass.playtime,
                    wynnClass.mobsKilled, wynnClass.deaths, wynnClass.pvpKills, wynnClass.pvpDeaths,
                    wynnClass.gamemode.craftsman, wynnClass.gamemode.hardcore, wynnClass.gamemode.hunted,
                    wynnClass.gamemode.ironman,
                    wynnClass.skills["strength"], wynnClass.skills["dexterity"], wynnClass.skills["intelligence"],
                    wynnClass.skills["defence"], wynnClass.skills["agility"],
                    wynnClass.alchemismLevel.level, wynnClass.armouringLevel.level, wynnClass.cookingLevel.level,
                    wynnClass.farmingLevel.level, wynnClass.fishingLevel.level, wynnClass.jewelingLevel.level,
                    wynnClass.miningLevel.level,
                    wynnClass.tailoringLevel.level, wynnClass.weaponsmithingLevel.level,
                    wynnClass.woodcuttingLevel.level, wynnClass.woodworkingLevel.level))

def getPlayers():
    players = []

    with open("data/players.txt", "r") as fp:
        Lines = fp.readlines()
        for line in Lines:
            if len(line := line.strip()) > 0:
                players.append(line)
    players = list(dict.fromkeys(players))

    return players

def writePlayers(players):
    with open("data/players.txt", "w") as fp:
        for player in players:
            fp.write(player + "\n")
        fp.close()

def fixDuplicatedPlayers():
    writePlayers(getPlayers())

def updateNonHunted():
    players = getPlayers()

    writePlayers(players)

def stop():
    sys.exit(0)


if __name__ == "__main__":
    while True:
        {
            1: startBot,
            2: stopBot,
            3: checkInfoPlayer,
            4: fixDuplicatedPlayers,
            5: updateNonHunted,
            6: stop
        }[generalIntAsk("1) Start bot\n2) Stop bot\n3) Check info\n4) Fix duplicates\n5) Update non hunted\n6) Stop\nChoose: ", 6)]()
