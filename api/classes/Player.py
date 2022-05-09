class player:
    def __init__(self, json):
        a = 0
        self.name = json["name"]
        self.uuid = json["uuid"]
        self.kills = json["kills"]
        self.level = json["level"]
        self.xp = json["xp"]
        self.minPlayed = json["minPlayed"]
        self.rank = json["rank"]
        self.displayTag = json["displayTag"]
        self.veteran = json["veteran"]
        self.num = json["num"]
        if json.__contains__("guild"):
            self.guild = json["guild"]
            self.guildTag = json["guildTag"]