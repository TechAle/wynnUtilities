class playerGuild:
    def __init__(self, dict):
        self.name = dict["name"]
        self.uuid = dict["uuid"]
        self.rank = dict["rank"]
        self.contributed = dict["contributed"]
        self.joined = dict["joined"]
        self.joinedFriendly = dict["joinedFriendly"]