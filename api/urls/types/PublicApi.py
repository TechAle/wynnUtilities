from api.urls.BaseRequest import baseRequest


class publicApi(baseRequest):
    def __init__(self):
        super().__init__("public_api.php?action=")

    def getGuildList(self):
        return self.extension + "guildList"

    def getGuildStats(self, name):
        return self.extension + "guildStats&command=" + name

    def categorySearch(self, category="all"):
        return self.extension + "itemDB&category=" + category

    def nameSearch(self, name=""):
        return self.extension + "itemDB&search=" + name

    def guildLeaderboard(self):
        return self.extension + "statsLeaderboard&type=guild&timeframe=alltime"

    def playerLeaderboard(self):
        return self.extension + "statsLeaderboard&type=player&timeframe=alltime"

    def pvpLeaderboard(self):
        return self.extension + "statsLeaderboard&type=pvp&timeframe=alltime"

    def getServerList(self):
        return self.extension + "onlinePlayers"

    def searchInfo(self, name):
        return self.extension + "statsSearch&search=" + name

    def getTerritory(self):
        return self.extension + "territoryList"

    def getPlayersOnline(self):
        return self.getServerList()
