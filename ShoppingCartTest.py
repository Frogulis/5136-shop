import unittest
from ShoppingCart import ShoppingCart


class ShoppingCartTest(unittest.TestCase):
    def setUp(self):
        self.sc1 = ShoppingCart()
        self.sc1.addToShoppingCart('1', 5.12, 1)
        self.sc1.addToShoppingCart('2', 1.23, 100)


    def test1(self):
        self.assertEqual(self.sc1.getTotalPrice(), 128.12)
        self.sc1.adjustQuantity('2', 1.23, 200)
        self.assertRaises(Exception, self.sc1.adjustQuantity, '1', 1.23, 200) #invalid combo of id and price
        self.assertEqual(self.sc1.getTotalPrice(), 251.12)

    def test2(self):
        self.assertRaises(Exception, self.sc1.deleteFromShoppingCart, '1', 1.23)
        self.sc1.deleteFromShoppingCart('1', 5.12)
        self.assertEqual(self.sc1.getTotalPrice(), 123.00)


if __name__ == '__main__':

    test = ShoppingCartTest()
    suite = unittest.TestLoader().loadTestsFromModule(test)
    unittest.TextTestRunner().run(suite)