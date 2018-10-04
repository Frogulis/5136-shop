import Batch
import datetime

class Product:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.unit = "ea"
        self.originalPrice = 0.00
        self.source = ""
        self.shelfLife = 0
        self.batches = []
        self.batchIdCounter = 0

    def addBatch(self, quantity):
        batch = Batch.Batch()
        batch.batchID = self.generateBatchId()
        batch.actualPrice = self.originalPrice
        batch.quantity = quantity
        batch.shelfLife = self.shelfLife
        batch.shelfDate = datetime.datetime.now()
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
                    del self.batches[currentBatch]
                elif currentBatch.quantity > remainingQuantity:
                    currentBatch.setQuantity(currentBatch.quantity - remainingQuantity)
                    remainingQuantity = 0
                elif currentBatch.quantity < remainingQuantity:
                    del self.batches[currentBatch]
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

    def discount(self):
        pass
