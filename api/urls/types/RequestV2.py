from api.urls.BaseRequest import baseRequest

class requestV2(baseRequest):
    def __init__(self):
        super().__init__("v2/")

    def getPlayerStats(self, name):
        return self.extension + "player/" + name + "/stats"