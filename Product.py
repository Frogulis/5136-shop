from Batch import Batch
import datetime

class Product:
    def __init__(self, pid="", name="", unit="ea",
            originalPrice=0.00, source="", shelfLife=0, batches=None):
        self.id = pid
        self.name = name
        self.unit = unit
        self.originalPrice = originalPrice
        self.source = source
        self.shelfLife = shelfLife
        if batches is None:
            self.batches = []
        else:
            self.batches = batches

    # for reading files to build batches
    def buildBatch(self, id, actualPrice, quantity, shelfDate, shelfLife):
        newBatch = Batch(id, actualPrice, quantity, shelfDate, shelfLife)
        self.batches.append(newBatch)

    # programming running, owner wants to addBatch
    def addBatch(self, quantity):
        batch = Batch(self.generateBatchId(), self.originalPrice, quantity, datetime.date.today(), self.shelfLife)
        self.batches.append(batch)

    # Please check if there is enough stock before using this method,
    # there is no validation in this method.
    # def deductStock(self,actualPrice,quantity):
    #     remainingQuantity = quantity
    #     for batchIndex in range(0, len(self.batches)):
    #         currentBatch = self.batches[batchIndex]
    #         if currentBatch.actualPrice == actualPrice:
    #             if currentBatch.quantity == remainingQuantity:
    #                 remainingQuantity = 0
    #                 del self.batches[batchIndex]
    #                 break
    #             elif currentBatch.quantity > remainingQuantity:
    #                 currentBatch.setQuantity(currentBatch.quantity - remainingQuantity)
    #                 remainingQuantity = 0
    #                 break
    #             elif currentBatch.quantity < remainingQuantity:
    #                 remainingQuantity -= currentBatch.quantity
    #                 del self.batches[batchIndex]
    #         else:
    #             batchIndex += 1

    def deductStock(self,actualPrice, quantity):
        remQuantity = quantity
        batchIndexToBeDel = []
        for batchIndex in range(len(self.batches)):
            curBatch = self.batches[batchIndex]
            if curBatch.getActualPrice() == actualPrice:
                if curBatch.getQuantity() == remQuantity:
                    batchIndexToBeDel.append(curBatch)
                    break
                elif curBatch.getQuantity() < remQuantity:
                    batchIndexToBeDel.append(curBatch)
                    remQuantity -= curBatch.getQuantity()
                elif curBatch.getQuantity() > remQuantity:
                    curBatch.setQuantity(curBatch.getQuantity()-remQuantity)
                    break
        for batch in batchIndexToBeDel:
            self.batches.remove(batch)

    def setId(self, my_id):
        self.id = my_id

    def setName(self, name):
        self.name = name

    def setUnit(self, unit):
        self.unit = unit

    def setOriginalPrice(self, price):
        self.originalPrice = price

    def setSource(self, source):
        self.source = source

    def setShelfLife(self, life):
        self.shelfLife = life

    def generateBatchId(self):
        if len(self.batches) == 0:
            newBatchId = str(1)
        else:
            newBatchId = str(int(self.batches[-1].getBatchID())+1)
        return newBatchId

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getUnit(self):
        return self.unit

    def getOriginalPrice(self):
        return self.originalPrice

    def getSource(self):
        return self.source

    def getShelfLife(self):
        return self.shelfLife

    def getBatch(self,batchID):
        for batch in self.batches:
            if batchID == batch.getBatchID():
                return batch
        raise Exception("Batch does not exist.")

    def getBatches(self):
        return self.batches

    def getExpiringBatches(self):
        return [batch for batch in self.batches if batch.nearExpiry()]

    def getPriceGroups(self):
        groups = {} #price: quantity
        for batch in self.batches:
            if batch.getActualPrice() not in groups:
                groups[batch.getActualPrice()] = self.calculateStock(batch.getActualPrice())
        return groups

    def calculateTotalQuantity(self):
        total = 0.00
        for batch in self.batches:
            total += batch.getQuantity()
        return total

    def calculateNonDiscountQuantity(self):
        total = 0.00
        for batch in self.batches:
            if batch.getActualPrice() == self.getOriginalPrice():
                total += batch.getQuantity()
        return total

    def calculateDiscountQuantity(self):
        total = 0.00
        for batch in self.batches:
            if batch.getActualPrice() != self.getOriginalPrice():
                total += batch.getQuantity()
        return total

    def updateDiscount(self):
        for batch in self.batches:
            batch.setActualPrice(round(batch.getDiscount() * self.originalPrice),2)

    # return total quantity of that particular price
    def calculateStock(self, price):
        totalQuantity = 0.0
        for batch in self.batches:
            if batch.actualPrice == price:
                totalQuantity += batch.getQuantity()
        return totalQuantity
