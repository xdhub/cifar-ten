import unittest
import sys

sys.path.append('tests')

import testExample

class TestCifarTen(unittest.TestCase, testExample.TestSequenceFunctions):

    def setUp(self):
        testExample.TestSequenceFunctions.setUp(self)

    def goof(self):
        x = 1
            
if __name__ == '__main__':
    unittest.main()

