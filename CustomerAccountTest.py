import unittest
from UserAccountTest import UserAccountTest
from UserAccount import UserAccount
from CustomerAccount import CustomerAccount


class CustomerAccountTest(unittest.TestCase):
    def setUp(self):
        #        ID, password, name, phoneNumber, address, shoppingCart, balance = 0, loggedIn = False
        self.user1 = CustomerAccount('C12345', 'somepwd', 'Amy', '0428912576', '11 Foster Road, Mount Waverley', None, 15, True)
        self.user2 = CustomerAccount('C12340', 'nopwd', 'Sarah', '0441209418', '42 West Crescent, Mount Waverley', None, 0, True)

    def test1(self):
        self.user1.logIn('somepwd')
        self.assertTrue(self.user1.getLoggedIn())

    def test2(self):
        self.assertRaises(Exception, self.user2.logIn, 'skdfjh')
        self.assertFalse(self.user2.getLoggedIn())

    def test3(self):
        self.user1.topUp(3)
        # self.assertTrue(self.user1.getBalance())
        self.assertEqual(self.user1.getBalance(), 18.00)

    def test4(self):
        self.user2.topUp(17.25)
        # self.assertTrue(self.user2.getBalance())
        self.assertEqual(self.user2.getBalance(), 17.25)

    def test5(self):
        self.user1.subtractBalance(5.50)
        self.assertEqual(self.user1.getBalance(), 9.50)

    def test6(self):
        # self.user2.subtractBalance(5.50)
        self.assertRaises(Exception, self.user2.subtractBalance, 5.50)
        self.assertEqual(self.user2.getBalance(), 0)


if __name__ == '__main__':

    test = CustomerAccountTest()
    suite = unittest.TestLoader().loadTestsFromModule(test)
    unittest.TextTestRunner().run(suite)