from api.urls.BaseRequest import baseRequest

class requestLegacy(baseRequest):
    def __init__(self):
        super().__init__("")

    def getLocations(self):
        return self.extension + "map/getMyLocation"

