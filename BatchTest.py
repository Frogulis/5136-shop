import unittest
import datetime
from Batch import Batch

class BatchTest(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        b1 = Batch(1, 1.14, 10, datetime.date.today(), 8)
        assert b1.getExpiryDate() == datetime.date.today() + datetime.timedelta(days = 8)

    def test2(self):
        bs = [Batch(1, 1.14, 10, datetime.date.today(), i) for i in range(9)][::-1]
        prev = bs[0].getDiscount()
        for b in bs[1:]:
            a = b.getDiscount()
            assert a < prev, "{}, {}".format(a, prev)
            prev = a

if __name__ == '__main__':
    test = BatchTest()
    suite = unittest.TestLoader().loadTestsFromModule(test)
    unittest.TextTestRunner().run(suite)
