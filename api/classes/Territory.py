class territory:
    def __init__(self, json):
        self.territory = json["territory"]
        self.guild = json["guild"]
        self.acquired = json["acquired"]
        self.attacker = json["attacker"]
        self.location = json["location"]