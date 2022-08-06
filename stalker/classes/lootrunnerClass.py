class lootrunner:
    '''
        Predict:
        -1 : Low
        0 : Cork
        1 : Cotl/Rodo/Sky/Se
        2: Unlvl or cotl+rodo+sky+se
        3: cotl+rodo+sky+se
    '''
    def __init__(self, name, server, blocksNow, blocksTotal, mins, predict, timeStamp, nameClass, low):
        self.name = name
        self.server = server
        self.blocksNow = blocksNow
        self.blocksTotal = blocksTotal
        self.mins = mins
        self.predict = predict
        self.timeStamp = timeStamp
        self.nameClass = nameClass
        self.low = low

    def getPredictionName(self):
        if self.predict == 0:
            return "Cork"
        elif self.predict == 1:
            return "Cotl/Rodo/Sky/Se"
        elif self.predict == 2:
            return "Unlvl (Mage) or cotl+rodo+sky+se"
        else:
            return "Unlvl (No Mage) Cotl+Rodo+Sky+Se"
