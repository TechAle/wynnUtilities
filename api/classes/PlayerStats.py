class playerStats:
    def __init__(self, json):
        self.username = json["username"]
        self.uuid = json["uuid"]
        self.rank = json["rank"]
        self.guild = json["guild"]
        self.ranking = json["ranking"]
        self.meta = meta(json["meta"])
        self.globals = globals(json["global"])
        self.classes = []
        for classCheck in json["classes"]:
            self.classes.append(wynnClass(classCheck))

class wynnClass:
    def __init__(self, dict):
        self.name = dict["name"]
        self.totalLevel = dict["level"]
        self.combatLevel = profClass(dict["professions"]["combat"])
        self.alchemismLevel = profClass(dict["professions"]["alchemism"])
        self.armouringLevel = profClass(dict["professions"]["armouring"])
        self.cookingLevel = profClass(dict["professions"]["cooking"])
        self.farmingLevel = profClass(dict["professions"]["farming"])
        self.fishingLevel = profClass(dict["professions"]["fishing"])
        self.jewelingLevel = profClass(dict["professions"]["jeweling"])
        self.miningLevel = profClass(dict["professions"]["mining"])
        self.tailoringLevel = profClass(dict["professions"]["tailoring"])
        self.weaponsmithingLevel = profClass(dict["professions"]["weaponsmithing"])
        self.woodcuttingLevel = profClass(dict["professions"]["woodcutting"])
        self.woodworkingLevel = profClass(dict["professions"]["woodworking"])
        self.skills = dict["skills"]
        self.dungeons = dict["dungeons"]["list"]
        self.quests = dict["quests"]["list"]
        self.raids = dict["raids"]["list"]
        self.itemsIdentified = dict["itemsIdentified"]
        self.mobsKilled = dict["mobsKilled"]
        self.pvpKills = dict["pvp"]["kills"]
        self.pvpDeaths = dict["pvp"]["deaths"]
        self.logins = dict["logins"]
        self.deaths = dict["deaths"]
        self.playtime = dict["playtime"]
        self.gamemode = gamemode(dict["gamemode"])
        self.chestsFound = dict["chestsFound"]

class gamemode:
    def __init__(self, dict):
        self.craftsman = dict["craftsman"]
        self.hardcore = dict["hardcore"]
        self.ironman = dict["ironman"]
        self.hunted = dict["hunted"]

class profClass:
    def __init__(self, dict):
        self.level = dict["level"]
        self.xp = dict["xp"]

class globals:
    def __init__(self, dict):
        self.chestsFound = dict["chestsFound"]
        self.blocksWalked = dict["blocksWalked"]
        self.itemsIdentified = dict["itemsIdentified"]
        self.mobsKilled = dict["mobsKilled"]
        self.totalLevel = dict["totalLevel"]
        self.pvp = dict["pvp"]
        self.logins = dict["logins"]
        self.deaths = dict["deaths"]
        self.discoveries = dict["discoveries"]
        self.eventsWon = dict["eventsWon"]


class meta:
    def __init__(self, dict):
        self.firstJoin = dict["firstJoin"]
        self.lastJoin = dict["lastJoin"]
        self.playtime = dict["playtime"]
        self.veteran = dict["veteran"]
        self.online = dict["location"]["online"]
        self.server = dict["location"]["server"]