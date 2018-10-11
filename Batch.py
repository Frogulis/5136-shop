import datetime


class Batch:
    def __init__(self,batchID = "",actualPrice = 0.00,quantity=0.00,shelfDate=None, shelfLife=0):
        self.batchID = batchID
        if shelfDate is None:
            self.shelfDate = datetime.date.today()
        else:
            self.shelfDate = shelfDate
        self.actualPrice = float(actualPrice)
        self.quantity = float(quantity)
        self.setExpiryDate(shelfLife)
        self.shelfLife = shelfLife


    def generateActualPrice(self, originalPrice):
        self.setActualPrice(originalPrice * self.getDiscount())

    def getActualPrice(self):
        return self.actualPrice

    def getBatchID(self):
        return self.batchID

    def getDiscount(self):
        if not self.nearExpiry():
            return 1.0
        else:
            return 0.3 + 0.7 * ((self.expiryDate - datetime.date.today()).days / self.shelfLife)

    def getExpiryDate(self):
        return self.expiryDate

    def getShelfDate(self):
        return self.shelfDate

    def getQuantity(self):
        return self.quantity

    def nearExpiry(self):
        return not ((self.expiryDate - datetime.date.today())/datetime.timedelta(days = self.shelfLife) > 0.7)

    def setActualPrice(self, actualPrice):
        self.actualPrice = float(actualPrice)

    def setBatchId(self,batchID):
        self.batchID = batchID

    def setExpiryDate(self, daysTilExpiry):
        self.expiryDate = self.shelfDate + datetime.timedelta(days= daysTilExpiry)

    def setShelfDate(self, shelfDate):
        self.shelfDate = shelfDate

    def setQuantity(self, quantity):
        self.quantity = quantity

if __name__ == '__main__':
    bs = [Batch(23, 1.00, 20, datetime.date.today(), i) for i in range(0, 10)]
    for b in bs:
        print(b.getDiscount())
