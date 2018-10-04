import unittest
import datetime
from Product import Product
from Batch import Batch

class ProductTest(unittest.TestCase):
    def setUp(self):

        self.p1 = Product("1", "Apple", "ea", 5.00, "SA", 14)
        self.p1.addBatch(10)
        self.p1.addBatch(5)
        self.p1.batches.append(Batch("3", 5.00, 10, datetime.date.today() - datetime.timedelta(days = 12), 14))
        self.p1.updateDiscount()
        self.p2 = Product("2", "Banana", "ea", 2.00, "QLD", 8)

    def test1(self):
        assert self.p1.calculateTotalQuantity() == 25, str(self.p1.calculateTotalQuantity())
        assert self.p2.calculateTotalQuantity() == 0, str(self.p2.calculateTotalQuantity())       

    def test2(self):
        assert self.p1.calculateNonDiscountQuantity() == 15, str(self.p1.calculateNonDiscountQuantity())
        assert self.p2.calculateNonDiscountQuantity() == 0, str(self.p2.calculateNonDiscountQuantity())

    def test3(self):
        assert self.p1.calculateDiscountQuantity() == 10, str(self.p1.calculateDiscountQuantity())
        assert self.p2.calculateDiscountQuantity() == 0, str(self.p2.calculateDiscountQuantity())

    def test4(self):
        self.p1.deductStock(self.p1.getOriginalPrice(), 7)
        assert self.p1.calculateTotalQuantity() == 18, str(self.p1.calculateTotalQuantity())
        assert self.p1.calculateNonDiscountQuantity() == 8, str(self.p1.calculateNonDiscountQuantity())
        assert self.p1.calculateDiscountQuantity() == 10, str(self.p1.calculateDiscountQuantity())

if __name__ == '__main__':
    test = ProductTest()
    suite = unittest.TestLoader().loadTestsFromModule(test)
    unittest.TextTestRunner().run(suite)
