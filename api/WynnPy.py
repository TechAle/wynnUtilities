from api.RequestManager import requestManger
from api.classes.Guild import guild
from api.classes.Item import item
from api.classes.Player import player
from api.classes.PlayerStats import playerStats, wynnClass
from api.classes.Territory import territory
from api.urls.UrlList import urlList


class wynnPy:
    BASEURL = "http://api.wynncraft.com/"
    WEBURL = "https://web-api.wynncraft.com/"

    def __init__(self):
        self.requestManager = requestManger()
        self.uList = urlList()

    def getGuildList(self):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getGuildList())
        return response["guilds"]

    def getTerritory(self):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getTerritory())
        territories = []
        for territoryCheck in response["territories"]:
            territories.append({
                territoryCheck: territory(response["territories"][territoryCheck])
            })
        return response["territories"]

    def getGuildStats(self, name):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getGuildStats(name))
        return guild(response)

    def getCategory(self, category):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getCategory(category))
        items = []
        for itemCheck in response["items"]:
            items.append(item(itemCheck))
        return items

    def getNames(self, name):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getNames(name))
        items = []
        for itemCheck in response["items"]:
            items.append(item(itemCheck))
        return items

    def getLeaderboardGuild(self):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getLeaderboardGuild())
        guilds = []
        for guildCheck in response["data"]:
            guilds.append(guild(guildCheck))
        return guilds

    def getLeaderboardPlayer(self):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getLeaderboardPlayer())
        players = []
        for playerCheck in response["data"]:
            players.append(player(playerCheck))
        return players

    def getLeaderboardPvp(self):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getLeaderboardPvp())
        players = []
        for playerCheck in response["data"]:
            players.append(player(playerCheck))
        return players

    def getServerList(self):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getServerList())
        del response["request"]
        return response

    def searchInfo(self, name):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.searchInfo(name))
        del response["request"]
        del response["search"]
        return response

    def getPlayerStats(self, name):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getPlayerStats(name))
        return playerStats(response["data"][0])

    def getPlayersOnline(self):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getServerList())
        players = []
        del response["request"]
        for server in response:
            players.extend(response[server])
        return players

    def getPlayersOnlineInWorld(self, world):
        response = self.requestManager.sendRequest(self.BASEURL + self.uList.getServerList())
        return response[world]

    def getClasses(self, name):
        response = self.requestManager.sendRequest(self.WEBURL + self.uList.getClasses(name))
        return response

    def getWynnClass(self, name, classWynn):
        response = self.requestManager.sendRequest(self.WEBURL + self.uList.getWynnClass(name, classWynn))
        return wynnClass(response)

