import time
from datetime import datetime

import discord
from discord import Webhook, RequestsWebhookAdapter
from discord_webhook import DiscordWebhook, DiscordEmbed


class serverManager:
    def __init__(self):
        self.serversBefore = {}
        self.updates = 0
        self.avar = "https://cdn.discordapp.com/app-icons/973942027563712632/3043f3b6d99b2b737ef7216e8c14c106.png?size=256"

    def addLootrunner(self, lootrunner):
        if self.serversBefore.__contains__(lootrunner.server):
            if lootrunner.disc:
                for player in self.serversBefore[lootrunner.server]["players"]:
                    if player.disc:
                        if player.name == lootrunner.name and player.predict == lootrunner.predict:
                            return
            self.serversBefore[lootrunner.server]["players"].append(lootrunner)
            self.serversBefore[lootrunner.server]["lastLooted"] = lootrunner.timeStamp

    def updateServers(self, wynnApi):
        serversOnline = wynnApi.getServerUptime()
        if len(serversOnline) > 0:
            for serverToCheck in serversOnline:
                if not self.serversBefore.__contains__(serverToCheck):
                    self.serversBefore[serverToCheck] = {
                        "uptime": serversOnline[serverToCheck],
                        "players": [],
                        "lastLooted": serversOnline[serverToCheck]
                    }
                elif serversOnline[serverToCheck] != self.serversBefore[serverToCheck]["uptime"]:
                    self.serversBefore[serverToCheck]["uptime"] = self.serversBefore[serverToCheck]["lastLooted"] = serversOnline[serverToCheck]

            servers = self.serversBefore.copy().keys()
            for serverToCheck in servers:
                if not serversOnline.__contains__(serverToCheck):
                    del self.serversBefore[serverToCheck]

            for servers in self.serversBefore:
                i = 0
                while i < len(self.serversBefore[servers]["players"]):
                    if (round(time.time() * 1000) - self.serversBefore[servers]["players"][i].timeStamp) / 1000 / 60 > 60*4+15:
                        self.serversBefore[servers]["players"].pop(i)
                        i -= 1
                    i += 1

    def exportServers(self, webhook, idReport):
        if webhook == "":
            return
        serversSorted = self.getSortedServers()
        self.updates += 1
        webhook = Webhook.from_url(webhook, adapter=RequestsWebhookAdapter())  # Initializing webhook
        embed = discord.Embed(
            title=f"Starting the report n^" + str(self.updates),
            color=0x40a0c6)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text="Id: " + idReport)
        webhook.send(username="wynnStalker", avatar_url=self.avar, embed=embed)
        time.sleep(1)

        for servers in serversSorted:
            embed = discord.Embed(
                title=f"World: `"+servers['server']+"`",
                description=f"uptime: <t:{int(servers['uptime']/1000)}:R> last looted: <t:{int(servers['lastLooted']/1000)}:R> Lootrunners: {len(servers['players'])}\n",
                color=0x40a0c6)
            listPlayers = ""
            listPrediction = ""
            for player in servers["players"]:
                if not player.disc:
                    listPlayers += f"{player.name} ({player.blocksNow}-{player.blocksTotal}) {player.mins}mins {player.nameClass} <t:{int(player.timeStamp/1000)}:R> Low: {str(player.low)}\n"
                else:
                    listPlayers += f"{player.name} low: False"
                if player.predict != -1:
                    listPrediction += f"{player.getPredictionName()} <t:{int(player.timeStamp/1000)}:R>\n"
            if listPlayers != "":
                embed.add_field(name="Players: ",
                                value=listPlayers)
            if listPrediction != "":
                embed.add_field(name="Prediction spots",
                                value=listPrediction,
                                inline=False)
            try:
                webhook.send(username="wynnStalker", avatar_url=self.avar, embed=embed)
                time.sleep(1)
            except discord.errors.HTTPException:
                pass

        nowTime = datetime.now()
        stageMinute = int(nowTime.minute / 15)
        nextReportTimeStamp = datetime.timestamp(
            datetime(nowTime.year, nowTime.month,
                     nowTime.day + (1 if nowTime.hour == 23 and stageMinute == 3 else 0),
                     nowTime.hour + (
                         -23 if stageMinute == 3 and nowTime.hour == 23 else 1 if stageMinute == 3 else 0),
                     0 if stageMinute == 3 else 30 if stageMinute == 2 else 30 if stageMinute == 1 else 15)
        )

        embed = discord.Embed(
            title=f"Ended the report n^" + str(self.updates),
            description=f"Next report: <t:{int(nextReportTimeStamp)}:R>",
            color=0x40a0c6)
        embed.timestamp = datetime.utcnow()
        webhook.send(username="wynnStalker", avatar_url=self.avar, embed=embed)
        webhook.send("<@&1000312359224623155>", username="wynnStalker", avatar_url=self.avar)

    '''
        - Bottom servers with less then 1.2 hours
        - Middle servers sorted by lootrunners found
        - Top with no lootrunners
    '''
    def getSortedServers(self):
        # Output and temp variable to mess with
        serverTemp = {}
        noLootrunners = []
        withLootunners = []
        less1Hours = []
        # Set lastLooted in every servers
        for server in self.serversBefore:
            serverTemp[server] = {}
            serverTemp[server]["lastLooted"] = self.serversBefore[server]["lastLooted"]
            serverTemp[server]["players"] = self.serversBefore[server]["players"]
            serverTemp[server]["uptime"] = self.serversBefore[server]["uptime"]
            serverTemp[server]["server"] = server
            if (time.time() - serverTemp[server]["uptime"]/1000) / 60 > 60:
                if len(self.serversBefore[server]["players"]) > 0:
                    withLootunners.append(serverTemp[server])
                else:
                    noLootrunners.append(serverTemp[server])
            else:
                less1Hours.append(serverTemp[server])
        # Now sort
        withLootunners = sorted(withLootunners, key=lambda d: d['lastLooted'])
        noLootrunners = sorted(noLootrunners, key=lambda d: d['players'])
        output = noLootrunners
        output.extend(withLootunners)
        output.extend(less1Hours)

        return output
