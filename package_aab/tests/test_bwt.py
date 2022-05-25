import unittest
from src.bwt import BWT


class test_BWT(unittest.TestCase):
    def setUp(self):
        self.btw = BWT("TAGACAGAGA$")


class test_BwtMethods(test_BWT):
    def test_runTest(self):
        x = self.btw.bwt()
        y = "AGGGTCAAAA$"
        self.assertEqual(str(x), y)

    def test_lastToFirst(self):
        x = self.btw.last_to_first()
        y = ["1", "7", "8", "9", "10", "6", "2", "3", "4", "5", "0"]
        self.assertEqual(str(x), y)


if __name__ == '__main__':
    unittest.main()