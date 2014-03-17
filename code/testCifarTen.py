import unittest
import sys

sys.path.append('tests')

import testExample
import testGeneticAlgorithm
import testDirectories

class TestCifarTen(unittest.TestCase, 
    testExample.TestSequenceFunctions,
    testGeneticAlgorithm.TestGeneticAlgorithm,
    testDirectories.TestDirectories):

    def setUp(self):
        testExample.TestSequenceFunctions.setUp(self)
        testGeneticAlgorithm.TestGeneticAlgorithm.setUp(self)
        testDirectories.TestDirectories.setUp(self)

    def testTest(self):
        self.assertEqual(2 + 2, 4)
            
if __name__ == '__main__':
    unittest.main()

