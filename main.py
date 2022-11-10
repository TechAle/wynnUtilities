import logging

from checker.coreChecker import checkerCore
from locator.coreLocator import locatorCore
from stalker.coreStalker import stalkerCore, getPlayerClasses, isTarget
from utils import logUtils
from utils.askUtils import generalIntAsk
import api.WynnPy
import sys
from stalker.discordRPC import RPC
import threading
import flask
from multiprocessing import Process

from utils.wynnUtils import isHighLevel

stalker = None
checker = None
locator = None
dRPC = None

app = logUtils.createLogger("app")


def startBot():
    global stalker
    if stalker is None:
        stalker = stalkerCore(app, threading.currentThread(), dRPC)
    if not stalker.running:
        stalker.startStalkingThread()


def stopBot():
    # noinspection PyUnresolvedReferences
    if stalker is not None and stalker.on:
        stalker.on = False


def startChecker():
    global checker
    if checker is None:
        checker = checkerCore(threading.current_thread())

    if not checker.running:
        checker.startCheckerThread()


def endChecker():
    # noinspection PyUnresolvedReferences
    if checker is not None and checker.on:
        checker.on = False


def checkInfoPlayer():
    playerName = input("Name player: ")
    apiWynn = api.WynnPy.wynnPy()
    player = getPlayerClasses(apiWynn, playerName.strip())
    print("Name: {} Lobby: {} Online: {} Guild: {}, {} Total level: {}\nClasses:"
          .format(player.username, apiWynn.getLobbyPlayer(player.username), player.meta.online,
                  player.guild["name"], player.guild["rank"], player.globals.totalLevel["combined"]))

    for wynnClass in player.characters:
        print(
            "Name: {} IsHigh: {} Level: {} Blocks walked: {} chests: {} Playtime: {}\nMobs Killed: {} Deaths: {} PvpKills: {} PvpDeaths: {}\n"
            "Craftsman: {} Hardcore: {} Hunted: {} Ironman: {}\n"
            "Strenght: {} Dexterity: {} Intelligence: {} Defence: {} Agility: {}\n"
            "Alchemism: {} Armouring: {} Cooking: {} Farming: {} Fishing: {} Jeweling: {} Mining: {}\n"
            "Tailoring: {} Weaponsmithing: {} Woodcutting: {} Woodworking: {}\n"
                .format(wynnClass.type, isHighLevel(wynnClass), wynnClass.combatLevel.level, wynnClass.blocksWalked, wynnClass.chestsFound,
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

    with open("stalker/data/players.txt", "r") as fp:
        Lines = fp.readlines()
        for line in Lines:
            if len(line := line.strip()) > 0:
                players.append(line)
    players = list(dict.fromkeys(players))

    return players


def writePlayers(players):
    with open("stalker/data/players.txt", "w") as fp:
        for player in players:
            fp.write(player + "\n")
        fp.close()


def fixDuplicatedPlayers():
    writePlayers(getPlayers())


def updateNonHunted():
    apiWynn = api.WynnPy.wynnPy()
    players = getPlayers()
    print("Total players: {}... This is going to take a while".format(len(players)))
    i = 0
    removed = 0
    while i < len(players):
        statsPlayer = getPlayerClasses(apiWynn, players[i])
        i += 1
        if statsPlayer is None:
            continue
        for classWynn in statsPlayer.characters:
            if isHighLevel(classWynn):
                i -= 1
                players.pop(i)
                removed += 1
                break
        if i % 20 == 0:
            print("Removed {} and we are at {}%".format(removed, i / len(players) * 100))
            writePlayers(players)

    print("Removed in total {} players".format(removed))
    writePlayers(players)


def stop():
    global server
    server.terminate()
    sys.exit(0)

def startLocationStalker():
    global locator
    if locator is None:
        locator = locatorCore(threading.current_thread())
    if not locator.running:
        locator.startLocatorThread()

def stopLocationStalker():
    global locator
    if locator is not None and locator.on:
        locator.on = False

def lrGuild():
    if stalker is not None and stalker.on:
        # noinspection PyUnresolvedReferences
        stalker.lrGuild()

def menuThread():
    while True:
        {
            1: startBot,
            2: stopBot,
            3: checkInfoPlayer,
            4: fixDuplicatedPlayers,
            5: updateNonHunted,
            6: startChecker,
            7: endChecker,
            8: startLocationStalker,
            9: stopLocationStalker,
            10: lrGuild,
            11: stop
        }[generalIntAsk(
            "1) Start bot\n2) Stop bot\n3) Check info\n4) Fix duplicates\n5) Update non hunted\n6) Start Checker\n"
            "7) End Checker\n8) Start Location Stalker\n9) Stop Location Stalker\n10) Lr Guild\n11) Stop\nChoose: ",
            11)]()

def apiThread():
    app = flask.Flask(__name__)

    @app.route('/wynnStalker', methods=['POST'])
    def wynnStalker():
        player = flask.request.values.get("player")
        location = flask.request.values.get("location")
        wc = flask.request.values.get("wc")
        if stalker is not None and stalker.on:
            # noinspection PyUnresolvedReferences
            stalker.addLootrunnerApi(player, location, wc)
        return ""

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(port=9090)

if __name__ == "__main__":
    dRPC = RPC(threading.current_thread())
    # Set timer so that we see the menu after api is done
    threading.Timer(2, menuThread).start()
    # Flask get mad if he is not in main thread
    apiThread()
