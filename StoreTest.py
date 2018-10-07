import unittest
import datetime

from Store import Store
from Product import Product
from Batch import Batch
from CustomerAccount import CustomerAccount

class StoreTest(unittest.TestCase):
    def setUp(self):
        self.s1 = Store()
        self.p1 = Product("1", "Apple", "ea", 5.00, "SA", 14)
        self.p1.addBatch(10)
        self.p1.addBatch(5)
        self.p1.batches.append(Batch("3", 5.00, 10, datetime.date.today() - datetime.timedelta(days = 12), 14))
        self.p1.updateDiscount()

    def test1(self): #addProduct
        self.s1.addProduct("Cheese", "kg", 10.00, "France", 50)
        self.assertEqual(len(self.s1.products), 1)
        self.assertEqual(self.s1.products[-1].id, "1")

    def test2(self):
        self.s1.setProducts([self.p1])
        self.s1.addProduct("Cheese", "kg", 10.00, "France", 50)
        self.assertEqual(len(self.s1.products), 2)
        self.assertEqual(self.s1.products[-1].id, "2")

    def test3(self): #addCustomer
        self.s1.addCustomer('doggo1', 'Jerj Clooners', '0312345678', '123 Hollywoo Bvd')
        self.assertEqual(len(self.s1.customers), 1)
        self.assertEqual(self.s1.getCustomer("1").getName(), 'Jerj Clooners')

    def test4(self): #getOrderHistoryAsList
        each_l = 5
        no_c = 10
        orderHistory = {str(i): [None] * each_l for i in range(1,no_c + 1)}
        self.s1.setOrderHistory(orderHistory)
        self.assertEqual(len(self.s1.getOrderHistoryAsList()), each_l * no_c)

    def test5(self):
        self.assertEqual(len(self.s1.getOrderHistoryAsList()), 0)

    def test6(self):
        self.s1.addOrder("C0001")
        self.s1.addOrder("C0002")
        self.s1.addOrder("C0001")
        self.s1.addOrder("C0002")
        self.assertEqual(len(self.s1.getOrderHistory()), 2)
        for os in self.s1.getOrderHistory().values():
            self.assertEqual(len(os), 2)

    def test7(self):
        pass



if __name__ == '__main__':
    test = StoreTest()
    suite = unittest.TestLoader().loadTestsFromModule(test)
    unittest.TextTestRunner().run(suite)