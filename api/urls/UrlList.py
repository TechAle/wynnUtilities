from api.urls.types import PublicApi, RequestV2


class urlList:
    def __init__(self):
        self.pApi = PublicApi.publicApi()
        self.v2 = RequestV2.requestV2()

    def getGuildList(self):
        return self.pApi.getGuildList()

    def getGuildStats(self, name):
        return self.pApi.getGuildStats(name)

    def getCategory(self, category):
        return self.pApi.categorySearch(category)

    def getNames(self, name):
        return self.pApi.nameSearch(name)

    def getLeaderboardGuild(self):
        return self.pApi.guildLeaderboard()

    def getLeaderboardPlayer(self):
        return self.pApi.playerLeaderboard()

    def getLeaderboardPvp(self):
        return self.pApi.pvpLeaderboard()

    def getServerList(self):
        return self.pApi.getServerList()

    def getTerritory(self):
        return self.pApi.getTerritory()

    def searchInfo(self, name):
        return self.pApi.searchInfo(name)