from api.urls.BaseRequest import baseRequest


class requestAthena(baseRequest):
    def __init__(self):
        super().__init__("cache/get/")

    def getServerUptime(self):
        return self.extension + "serverList"

    def getIngridients(self):
        return self.extension + "ingredientList"

