import datetime
class Batch:
    def __init__(self,batchID,actualPrice,quantity,shelfLife):
        self.batchID = batchID
        self.expiryDate = datetime.date.today() + datetime.timedelta(days= shelfLife)
        self.actualPrice = actualPrice
        self.quantity = quantity

    def getBatchID(self):
        return self.batchID

    def setBatchId(self,batchID):
        self.batchID = batchID

    def getExpiryDate(self):
        return  self.expiryDate

    #to setExpriryDate() be added or edited
    def setExpiryDate(self,expiryDays):
        self.expiryDate = datetime.date.today() + datetime.timedelta(days= expiryDays)

    def getActualPrice(self):
        return self.actualPrice

    def setActualPrice(self, actualPrice):
        self.actualPrice = actualPrice

    def getQuantity(self):
        return self.quantity

    def setQuantity(self, quantity):
        self.quantity = quantity