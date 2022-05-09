from abc import abstractmethod


class baseRequest:
    extension = ""

    def __init__(self, extension):
        self.extension = extension

    def doRequest(self, params):
        return self.extension + '/' + params
