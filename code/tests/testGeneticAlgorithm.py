import geneticAlgorithm

class TestGeneticAlgorithm():

    def setUp(self):
        self.ga = geneticAlgorithm.GeneticAlgorithm(0)

    def testCrossover(self):
        chrome0 = [0, 1, 2]
        chrome1 = [3, 4, 5]
        self.ga.crossover(chrome0, chrome1)
        
        # Chromosomes together should still contain all of the original genes.
        allgenes = chrome0 + chrome1
        allgenes.sort()
        self.assertEqual(range(6), allgenes)

        # There is only 1 in 2^32 chance that two chromosomes of length 32 will 
        # remain changed after crossover. Consider that probability zero.
        zeros = [0] * 32
        ones = [1] * 32
        self.ga.crossover(zeros, ones)
        self.assertNotEqual(zeros, [0] * 32)
    
    def testCrossoverProbability(self):
        self.assertEqual(1.0, self.ga.crossoverProbability(4.0, 7.0, 2.0, 3.0))
        self.assertEqual(1.0, self.ga.crossoverProbability(4.0, 7.0, 2.0, 4.0))
        self.assertEqual(2.0 / 3.0, self.ga.crossoverProbability(4.0, 7.0, 2.0, 5.0))
        
