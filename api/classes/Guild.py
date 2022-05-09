from api.classes.PlayerGuild import playerGuild

class guild:

    def __init__(self, json):
        if json.__contains__("error"):
            self.error = True
        else:
            self.error = False
            self.name = json["name"]
            self.prefix = json["prefix"]
            self.xp = json["xp"]
            self.level = json["level"]
            self.created = json["created"]
            self.territories = json["territories"]

            if json.__contains__("territories"):
                self.warCount = json["warCount"] if json.__contains__("warCount") else None
                self.banner = json["banner"]
                self.memberCount = json["membersCount"]
                self.num = json["num"]
            else:
                self.createdFriendly = json["createdFriendly"]
                self.members = []
                for member in json["members"]:
                    self.members.append(playerGuild(member))