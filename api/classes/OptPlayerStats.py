class optPlayerStats:
    def __init__(self, wynnClass, timestamp):
        self.className = wynnClass.name
        self.mobsKilled = wynnClass.mobsKilled
        self.gamemode = wynnClass.gamemode
        self.deaths = wynnClass.deaths
        self.dungeons = wynnClass.dungeons
        self.quests = wynnClass.quests
        self.raids = wynnClass.raids
        self.chestsFound = wynnClass.chestsFound
        self.blocksWalked = wynnClass.blocksWalked
        self.playtime = wynnClass.playtime
        self.alchemismLevel = wynnClass.alchemismLevel
        self.armouringLevel = wynnClass.armouringLevel
        self.combatLevel = wynnClass.combatLevel
        self.cookingLevel = wynnClass.cookingLevel
        self.farmingLevel = wynnClass.farmingLevel
        self.fishingLevel = wynnClass.fishingLevel
        self.miningLevel = wynnClass.miningLevel
        self.tailoringLevel = wynnClass.tailoringLevel
        self.weaponsmithingLevel = wynnClass.weaponsmithingLevel
        self.woodcuttingLevel = wynnClass.woodcuttingLevel
        self.woodworkingLevel = wynnClass.woodworkingLevel
        self.timeStamp = timestamp

