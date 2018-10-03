import Batch

class Product:
	def __init__(self):
		self.id = ""
		self.name = ""
		self.unit = "ea"
		self.originalPrice = 0.00
		self.source = ""
		self.shelfLife = 0
		self.batches = []

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

	def calculateDiscountQuality(self):
		total = 0.00
		for batch in self.batches:
			if batch.getActualPrice() != self.getOriginalPrice():
				total += batch.getQuantity()
		return total

	
