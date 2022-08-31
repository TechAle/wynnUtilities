from api.urls.types import PublicApi, RequestV2, RequestV3, RequestAthena, RequestLegacy


class urlList:
    def __init__(self):
        self.pApi = PublicApi.publicApi()
        self.v2 = RequestV2.requestV2()
        self.v3 = RequestV3.requestV3()
        self.athena = RequestAthena.requestAthena()
        self.legacy = RequestLegacy.requestLegacy()

    def getLocations(self):
        return self.legacy.getLocations()

    def getServerUptime(self):
        return self.athena.getServerUptime()

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

    def getPlayerStats(self, name):
        return self.v2.getPlayerStats(name)

    def getPlayersOnline(self):
        return self.pApi.getPlayersOnline()

    def getClasses(self, name):
        return self.v3.getClasses(name)

    def getWynnClass(self, name, classWynn):
        return self.v3.getWynnClass(name, classWynn)

    def getIngridients(self):
        return self.athena.getIngridients()