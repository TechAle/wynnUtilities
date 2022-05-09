from threading import Thread, Lock
import time
# import the library
import urllib.request
import json
from urllib.error import HTTPError
import requests


class requestManger:
    MAX_REQUESTS = 2E4
    TIME_REQUESTS = 1200

    requestsDone = []

    def sendRequest(self, request):
        self.updateRequests()
        while len(self.requestsDone) >= self.MAX_REQUESTS:
            print("Max requests, please wait")
            time.sleep(10)
            self.updateRequests()
        output = self.makeRequest(request)
        self.requestsDone.append(time.time())
        return output


    def updateRequests(self):
        pass

    def makeRequest(self, url):
        # make the request
        r = requests.get(url)
        # get the data
        json = r.json()

        return json
