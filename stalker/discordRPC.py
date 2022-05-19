import time

import pypresence
from pypresence import Presence
import threading

class RPC:
    def __init__(self, mainThread):
        self.on = True
        self.mainThread = mainThread
        self.start = int(time.time())
        self.client_id = "973942027563712632"
        self.state = 0
        self.hunted = 0
        try:
            self.RPC = Presence(self.client_id)
            self.RPC.connect()
            threading.Thread(target=self.run).start()
        except pypresence.exceptions.DiscordNotFound:
            pass

    def stop(self):
        self.on = False

    def increasePlayer(self, num):
        self.state += num

    def increaseHunted(self):
        self.hunted += 1

    def run(self):
        while self.on and self.mainThread.is_alive():
            self.RPC.update(
                large_image= "pic",
                large_text= "Created by TechAle",
                details= "Tracking people",
                state= str(self.state) + " people analyzed. " + str(self.hunted) + " hunted found",
                start= self.start,
                buttons=[{"label": "Github", "url": "https://github.com/TechAle/wynnStalker"},
                         {"label": "Youtube", "url": "https://www.youtube.com/channel/UCTN8g2pb7WSBq_zDdFF_aVQ"}]
            )
            time.sleep(30)