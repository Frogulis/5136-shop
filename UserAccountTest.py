import unittest
from UserAccount import UserAccount

class UserAccountTest(unittest.TestCase):
    def setUp(self):
        #                       userId, name, password, loggedIn=False
        self.user1 = UserAccount('C12345', 'Amy', 'somepwd', True)
        self.user2 = UserAccount('C12340', 'Sarah', 'nopwd', False)

    def test1(self):
        self.user1.logIn('somepwd')
        self.assertTrue(self.user1.getLoggedIn())

    def test2(self):
        self.assertRaises(Exception, self.user1.logIn, 'skdfjh')

if __name__ == '__main__':

    test = UserAccountTest()
    suite = unittest.TestLoader().loadTestsFromModule(test)
    unittest.TextTestRunner().run(suite)