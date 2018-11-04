import unittest
import sys
sys.path.append('../src')
from testthis import multiply,add

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_numbers_3_4(self):
        self.assertEqual( multiply(3,4), 12)

    def test_strings_a_3(self):
        self.assertEqual( multiply('a',3), 'aaa')

    def test_add_3_4(self):
        self.assertEqual(add(3,4), 7)

    def test_add_a_b(self):
        self.assertEqual(add("a","b"), "ab")

if __name__ == '__main__':
    unittest.main()
