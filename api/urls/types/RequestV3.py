from api.urls.BaseRequest import baseRequest


class requestV3(baseRequest):
    def __init__(self):
        super().__init__("api/v3/")

    def getClasses(self, name):
        return self.extension + "player/" + name + "/characters"

    def getWynnClass(self, name, classWynn):
        return self.extension + "player/" + name + "/characters/" + classWynn
