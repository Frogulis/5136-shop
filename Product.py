import Batch
import datetime

class Product:
    def __init__(self, pid="", name="", unit="ea",
            originalPrice=0.00, source="", shelfLife=0, batches=None, batchIdCounter=0):
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
        self.batchIdCounter = batchIdCounter

    def addBatch(self, quantity):
        batch = Batch.Batch(self.generateBatchId(), self.originalPrice, quantity, datetime.date.today(), self.shelfLife)
        self.batches.append(batch)

    # Please check if there is enough stock before using this method,
    # there is no validation in this method.
    def deductStock(self,actualPrice,quantity):
        remainingQuantity = quantity
        batchIndex = 0
        while remainingQuantity > 0 and batchIndex < len(self.batches):
            currentBatch = self.batches[batchIndex]
            if currentBatch.actualPrice == actualPrice:
                if currentBatch.quantity == remainingQuantity:
                    remainingQuantity = 0
                    del self.batches[batchIndex]
                elif currentBatch.quantity > remainingQuantity:
                    currentBatch.setQuantity(currentBatch.quantity - remainingQuantity)
                    remainingQuantity = 0
                elif currentBatch.quantity < remainingQuantity:
                    del self.batches[batchIndex]
                    remainingQuantity -= currentBatch.quantity
                    batchIndex += 1
            else:
                batchIndex += 1

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
        newBatchId = str(self.batchIdCounter + 1)
        self.batchIdCounter += 1
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
            batch.setActualPrice(batch.getDiscount() * self.originalPrice)
