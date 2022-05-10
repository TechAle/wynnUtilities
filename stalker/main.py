import api.WynnPy


from stalker.ask import *
from stalker.playerStalker import stalkPlayers

# Setup logger
# Directory of every chats
from stalker.utils import directoryUtils, logUtils

directoryUtils.createIfNotExists("./logs")

# Logger
app = logUtils.setup_logger('logger', './logs/app.log')
app.info("Started new session")

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
        focus = askFocus()
        app.info("Api: " + str(apiToUse + 1) + ". Server: " + str(
            servetToTarget) + ". Hunter: " + "y" if hunterCalling else "n")
        # Start stalking
        stalkPlayers(wynnApi, servetToTarget, apiToUse, hunterCalling, focus)
    elif mode == "s":
        toStalk = askPlayerToStalk()
        stalkPlayers(wynnApi, toStalk, apiToUse, hunterCalling, False)


if __name__ == "__main__":
    main()
