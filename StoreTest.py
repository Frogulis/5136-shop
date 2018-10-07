import unittest
import datetime

from Store import Store
from Product import Product
from Batch import Batch

class StoreTest(unittest.TestCase):
    def setUp(self):
        self.s1 = Store()
        self.p1 = Product("1", "Apple", "ea", 5.00, "SA", 14)
        self.p1.addBatch(10)
        self.p1.addBatch(5)
        self.p1.batches.append(Batch("3", 5.00, 10, datetime.date.today() - datetime.timedelta(days = 12), 14))
        self.p1.updateDiscount()

    def test1(self):
        self.s1.addProduct("Cheese", "kg", 10.00, "France", 50)
        self.assertEqual(len(self.s1.products), 1)
        self.assertEqual(self.s1.products[-1].id, "1")

    def test2(self):
        self.s1.products = [self.p1]
        self.s1.addProduct("Cheese", "kg", 10.00, "France", 50)
        self.assertEqual(len(self.s1.products), 2)
        self.assertEqual(self.s1.products[-1].id, "2")

    def test3(self):
        pass

if __name__ == '__main__':
    test = StoreTest()
    suite = unittest.TestLoader().loadTestsFromModule(test)
    unittest.TextTestRunner().run(suite)